import os
from typing import List, Tuple

import boto3
import botocore.client
from boto3.s3.transfer import S3Transfer
from botocore.credentials import Credentials, RefreshableCredentials
from botocore.session import Session as BotocoreSession

from vessl import vessl_api
from vessl.cli._util import sizeof_fmt
from vessl.util.common import remove_prefix
from vessl.util.downloader import Downloader
from vessl.util.exception import (
    InvalidParamsError,
    InvalidVolumeFileError,
    VesslApiException,
)


class FileTransmission:
    def __init__(self, source_path, source_abs_path, dest_abs_path, size):
        self.source_path = source_path
        self.source_abs_path = source_abs_path
        self.dest_abs_path = dest_abs_path
        self.size = size


class VolumeFileTransfer:
    def __init__(self, volume_id: int):
        self.volume = vessl_api.volume_read_api(volume_id=volume_id)
        self.provider = None
        self.region_name = None
        self.bucket_name = None
        self.prefix = None
        self.endpoint = None
        self.s3_client = None
        self._update_federation_credentials()

    def download(self, source_path, dest_path):
        if self.provider == "gs":
            result = vessl_api.volume_file_list_api(
                volume_id=self.volume.id,
                recursive=True,
                path=source_path,
                need_download_url=True,
            ).results
            files = sorted(result, key=lambda x: x.path)
            Downloader.download(source_path, dest_path, *files, quiet=True)
            return

        (
            file_transmissions,
            total_size,
        ) = self._get_download_file_transmissions_and_total_size(source_path, dest_path)
        total_file_count = len(file_transmissions)
        if total_file_count == 0:
            print("No files to download.")
            return

        formatted_total_size = sizeof_fmt(total_size)
        print(f"Downloading {total_file_count} file(s) ({formatted_total_size})...")

        succeeded_count = 0
        succeeded_size = 0
        for file_transmission in file_transmissions:
            dirname = os.path.dirname(file_transmission.dest_abs_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            try:
                self._get_s3_client().download_file(
                    self.bucket_name,
                    file_transmission.source_abs_path,
                    file_transmission.dest_abs_path,
                    Callback=self._create_callback(succeeded_size, total_size),
                )
                succeeded_count += 1
                succeeded_size += file_transmission.size
            except BaseException as e:
                print(f"Failed to download {file_transmission.source_path}.")
                raise e

        print(f"Total {succeeded_count} file(s) downloaded.")

    def upload(self, source_path, dest_path):
        if self.volume.is_read_only:
            print("Cannot upload to read-only volume.")
            return

        s3_client = self._get_s3_client()
        (
            file_transmissions,
            total_size,
        ) = self._get_upload_file_transmissions_and_total_size(source_path, dest_path)
        total_file_count = len(file_transmissions)
        if total_file_count == 0:
            print("No files to upload.")
            return

        formatted_total_size = sizeof_fmt(total_size)
        print(f"Uploading {total_file_count} file(s) ({formatted_total_size})...")

        succeeded_count = 0
        succeeded_size = 0
        succeeded_files = []
        for file_transmission in file_transmissions:
            try:
                s3_client.upload_file(
                    file_transmission.source_abs_path,
                    self.bucket_name,
                    file_transmission.dest_abs_path,
                    Callback=self._create_callback(succeeded_size, total_size),
                )
                succeeded_count += 1
                succeeded_size += file_transmission.size
                succeeded_files.append({"path": os.path.basename(file_transmission.dest_abs_path)})
            except BaseException as e:
                print(f"Failed to upload {file_transmission.source_path}.")
                raise e

        print(f"Total {succeeded_count} file(s) uploaded.")
        return succeeded_files

    def copy(self, source_path, dest_path):
        # TODO
        return

    def remove(self, path):
        # TODO
        return

    def _create_callback(self, current_size, total_size):
        if total_size < 100 * 1024 * 1024:
            return None

        total_transmitted = current_size
        last_percent = int(total_transmitted / total_size * 100)
        formatted_size = sizeof_fmt(total_size)
        interval = max(int(31 * 1024 * 1024 / total_size * 100), 3)

        def callback(transmitted_bytes):
            nonlocal total_transmitted, last_percent
            total_transmitted += transmitted_bytes
            percent = int(total_transmitted / total_size * 100)
            if percent - last_percent >= interval or percent == 100:
                print(f"{sizeof_fmt(total_transmitted)}/{formatted_size} ({percent}%) completed.")
                last_percent = percent

        return callback

    def _update_federation_credentials(self):
        federation_credentials = vessl_api.volume_federate_api(volume_id=self.volume.id)
        self.region_name = federation_credentials.region
        self.bucket_name = federation_credentials.bucket
        self.prefix = federation_credentials.prefix
        self.provider = federation_credentials.token.provider
        self.endpoint = federation_credentials.endpoint

    def __get_s3_api_endpoint_url(self):
        return os.environ.get("VESSL_VOLUME_S3_API_ENDPOINT_URL", self.endpoint)

    def __get_s3_api_verify_ssl(self):
        if os.environ.get("VESSL_VOLUME_S3_API_VERIFY_SSL") == "false":
            return False
        return None

    def _get_s3_client(self) -> S3Transfer:
        if self.s3_client:
            return self.s3_client

        no_refresh = os.environ.get("VESSL_VOLUME_CREDENTIAL_NO_REFRESH") == "true"
        if no_refresh:
            return self._get_s3_client_from_static_credentials()

        refreshable_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.__get_s3_session_credentials(),
            refresh_using=self.__get_s3_session_credentials,
            method="sts-assume-role",
        )

        botocore_session = BotocoreSession()
        botocore_session._credentials = refreshable_credentials
        botocore_session.set_config_variable("region", self.region_name)
        session = boto3.session.Session(botocore_session=botocore_session)
        config = botocore.client.Config(connect_timeout=120, read_timeout=120)
        self.s3_client = session.client(
            "s3",
            config=config,
            endpoint_url=self.__get_s3_api_endpoint_url(),
            verify=self.__get_s3_api_verify_ssl(),
        )
        return self.s3_client

    def _get_s3_client_from_static_credentials(self) -> S3Transfer:
        if self.s3_client:
            return self.s3_client

        metadata = self.__get_s3_session_credentials()
        credential = Credentials(access_key=metadata['access_key'], secret_key=metadata['secret_key'])
        botocore_session = BotocoreSession()
        botocore_session._credentials = credential
        botocore_session.set_config_variable("region", self.region_name)
        session = boto3.session.Session(botocore_session=botocore_session)
        config = botocore.client.Config(connect_timeout=120, read_timeout=120)
        self.s3_client = session.client(
            "s3",
            config=config,
            endpoint_url=self.__get_s3_api_endpoint_url(),
            verify=self.__get_s3_api_verify_ssl(),
        )
        return self.s3_client

    def __get_all_s3_objects(self, **base_kwargs):
        continuation_token = None
        while True:
            list_kwargs = dict(MaxKeys=1000, **base_kwargs)
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token

            response = self._get_s3_client().list_objects_v2(**list_kwargs)
            yield from response.get('Contents', [])

            if not response.get('IsTruncated'):
                break

            continuation_token = response.get('NextContinuationToken')

    def _get_download_file_transmissions_and_total_size(
        self, source_path: str, dest_path: str
    ) -> Tuple[List[FileTransmission], int]:
        source_path = source_path.strip("/")
        is_asterisked = source_path.endswith("/*")
        if is_asterisked:
            source_path = source_path[:-2]
        is_root = source_path == ""
        source_abs_path = os.path.join(self.prefix, source_path).replace(os.sep, "/").rstrip("/") \
            if self.prefix else source_path
        dest_abs_path = os.path.abspath(dest_path)

        objects = list(self.__get_all_s3_objects(Bucket=self.bucket_name, Prefix=source_abs_path))
        if len(objects) == 0:
            return [], 0

        if len(objects) > 1 and os.path.exists(dest_abs_path) and not os.path.isdir(dest_abs_path):
            raise InvalidParamsError(f"{dest_abs_path} is not a directory.")

        if len(objects) == 1 and source_path == remove_prefix(objects[0]["Key"], self.prefix + "/"):
            file_transmission = FileTransmission(
                source_path=source_path,
                source_abs_path=objects[0]["Key"],
                dest_abs_path=dest_abs_path,
                size=objects[0]["Size"],
            )
            if os.path.isdir(dest_abs_path):
                file_transmission.dest_abs_path = os.path.join(dest_abs_path, source_path.split("/")[-1])

            return [file_transmission], file_transmission.size

        prefix = source_abs_path if is_asterisked else source_abs_path.rsplit("/", 1)[0]
        total_size = 0
        file_transmissions = []
        for obj in objects:
            total_size += obj["Size"]
            if is_root:
                source_rel_path = remove_prefix(obj['Key'], self.prefix + "/")
            else:
                source_rel_path = remove_prefix(obj['Key'], prefix + "/")

            file_transmissions.append(
                FileTransmission(
                    source_path=source_rel_path,
                    source_abs_path=obj['Key'],
                    dest_abs_path=os.path.join(dest_abs_path, source_rel_path),
                    size=obj['Size'],
                )
            )

        return file_transmissions, total_size

    def _get_upload_file_transmissions_and_total_size(
        self, source_path: str, dest_path: str
    ) -> Tuple[List[FileTransmission], int]:
        source_path = os.path.relpath(source_path)
        if not os.path.exists(source_path):
            raise InvalidParamsError(f"{source_path} does not exist.")

        source_file_name = os.path.basename(source_path)
        if os.path.isfile(source_path):
            try:
                vessl_api.volume_file_read_api(volume_id=self.volume.id, path=dest_path)
                dest_abs_path = dest_path
            except VesslApiException as e:
                if e.code == "NotAFile":
                    dest_abs_path = f"{dest_path}/{source_file_name}"
                elif e.code == "NotFound":
                    dest_abs_path = dest_path
                else:
                    raise

            if self.prefix:
                dest_abs_path = os.path.join(self.prefix, dest_abs_path.lstrip("/"))

            source_abs_path = os.path.abspath(source_path)
            file_size = os.path.getsize(source_abs_path)
            return [
                FileTransmission(
                    source_path,
                    source_abs_path,
                    dest_abs_path,
                    file_size,
                )
            ], file_size
        else:
            try:
                vessl_api.volume_file_read_api(volume_id=self.volume.id, path=dest_path)
            except VesslApiException as e:
                if e.code not in ("NotAFile", "NotFound"):
                    raise

                result = []
                total_size = 0
                for root_path, _, file_names in os.walk(source_path):
                    for file_name in file_names:
                        source_abs_path = os.path.join(root_path, file_name)
                        dest_abs_path = os.path.join(
                            dest_path,
                            remove_prefix(source_abs_path, source_path).lstrip("/"),
                        )
                        if self.prefix:
                            dest_abs_path = os.path.join(self.prefix, dest_abs_path.lstrip("/"))
                        file_size = os.path.getsize(source_abs_path)
                        result.append(
                            FileTransmission(
                                source_path,
                                source_abs_path,
                                dest_abs_path,
                                file_size,
                            )
                        )
                        total_size += file_size

                return result, total_size

            raise InvalidVolumeFileError(f"Destination path is not a directory: {dest_path}.")

    def __get_s3_session_credentials(self):
        federation_credentials = vessl_api.volume_federate_api(volume_id=self.volume.id)
        creds = federation_credentials.token.s3
        return {
            "access_key": creds.access_key_id,
            "secret_key": creds.secret_access_key,
            "token": creds.session_token,
            "expiry_time": creds.expiration.isoformat(),
        }
