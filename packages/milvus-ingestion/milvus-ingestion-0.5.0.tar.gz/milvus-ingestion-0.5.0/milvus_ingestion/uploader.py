# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

import os
import time

from minio import Minio
from minio.error import S3Error
from minio.error import MinioException
from logging import Logger
from typing import List

from .util import (
    Base,
    default_logger,
)

DEFAULT_BUCKET_NAME = "a-bucket"
DEFAULT_REMOTE_PATH = "milvus-ingestion"

class Uploader(Base):
    def __init__(self, logger: Logger = default_logger):
        self._logger = logger

    def upload(self,
               files: List[str],
               relative_path: str):
        msg = "The upload() interface of Uploader is not implemented"
        self._print_err(msg)
        raise Exception(msg)

    def remove(self, files: List[str]):
        msg = "The remove() interface of Uploader is not implemented"
        self._print_err(msg)
        raise Exception(msg)


class MinioUploader(Base):
    def __init__(
            self,
            bucket_name: str=DEFAULT_BUCKET_NAME,
            remote_path: str=DEFAULT_REMOTE_PATH,
            endpoint: str=None,
            access_key: str=None,
            secret_key: str=None,
            secure: bool=True,
            session_token: str=None,
            region: str=None,
            http_client=None,
            credentials=None,
            logger: Logger = default_logger
         ):
        super().__init__(logger=logger)
        self._client = None
        self._bucket_name = bucket_name
        self._remote_path = remote_path
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._secure = secure,
        self._session_token = session_token,
        self._region = region,
        self._http_client = http_client, # urllib3.poolmanager.PoolManager
        self._credentials = credentials, # minio.credentials.Provider

    def _get_client(self):
        if self._client is None:
            def arg_parse(arg):
                return arg[0] if isinstance(arg, tuple) else arg
            self._client = Minio(endpoint=arg_parse(self._endpoint),
                                 access_key=arg_parse(self._access_key),
                                 secret_key=arg_parse(self._secret_key),
                                 secure=arg_parse(self._secure),
                                 session_token=arg_parse(self._session_token),
                                 region=arg_parse(self._region),
                                 http_client=arg_parse(self._http_client),
                                 credentials=arg_parse(self._credentials))
        return self._client

    def _exists(self, file: str)->bool:
        try:
            minio_client = self._get_client()
            minio_client.stat_object(bucket_name=self._bucket_name, object_name=file)
            return True
        except MinioException as err:
            return False

    def upload(self, files: List[str],
               relative_path: str)->(bool, List[str], str):
        remote_files = []
        try:
            self._print_info("Prepare upload files")
            minio_client = self._get_client()
            found = minio_client.bucket_exists(self._bucket_name)
            if not found:
                msg = "MinIO bucket '{}' doesn't exist".format(self._bucket_name)
                self._print_err(msg)
                return False, [], msg

            for file_path in files:
                ext = os.path.splitext(file_path)
                if len(ext) != 2 or (ext[1] != ".json" and ext[1] != ".npy"):
                    continue

                relative_file_path = file_path.strip(relative_path).lstrip('/')
                minio_file_path = os.path.join(self._remote_path, relative_file_path)

                if not self._exists(minio_file_path):
                    minio_client.fput_object(bucket_name=self._bucket_name,
                                             object_name=minio_file_path,
                                             file_path=file_path)
                    self._print_info("Upload file '{}' to '{}'".format(file_path, minio_file_path))
                else:
                    self._print_info("Remote file '{}' already exists".format(minio_file_path))
                remote_files.append(minio_file_path)
        except Exception as e:
            msg = "Failed to call MinIO/S3 api, error: {}".format(e)
            self._print_err(msg)
            return False, [], msg

        self._print_info("Successfully upload files: {}".format(files))
        return True, remote_files, ""

    def remove(self, files: List[str])->bool:
        try:
            self._print_info("Prepare delete remote files")
            minio_client = self._get_client()
            found = minio_client.bucket_exists(self._bucket_name)
            if not found:
                self._print_err("MinIO bucket '{}' doesn't exist".format(self._bucket_name))
                return False

            for file_path in files:
                minio_client = self._get_client()
                minio_client.remove_object(self._bucket_name, file_path)
                self._print_info("Remote file deleted: {}".format(file_path))
        except Exception as e:
            self._print_err("Failed to call MinIO/S3 api, error: {}".format(e))
            return False


default_uploader = MinioUploader(endpoint="0.0.0.0:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)