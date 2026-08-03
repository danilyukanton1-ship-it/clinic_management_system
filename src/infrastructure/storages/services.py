from datetime import timedelta
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from minio import Minio

from infrastructure.storages.interface import StorageInterface
from infrastructure.storages.schemas import DownloadUrl, StoredFileSchema


class MinioStorageService(StorageInterface):
    def __init__(self, client: Minio, bucket: str) -> None:
        self._bucket = bucket
        self._client = client

    async def save(self, file: UploadFile) -> StoredFileSchema:
        extension = Path(file.filename).suffix
        object_key = f"{uuid4()}{extension}"

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        self._client.put_object(
            bucket_name=self._bucket,
            object_name=object_key,
            data=file.file,
            length=size,
            content_type=file.content_type,
        )
        return StoredFileSchema(
            key=object_key, size=size, content_type=file.content_type
        )

    async def delete(self, key: str) -> None:
        return self._client.remove_object(bucket_name=self._bucket, object_name=key)

    async def get_download_url(self, key: str) -> DownloadUrl:
        url = self._client.presigned_get_object(
            bucket_name=self._bucket,
            object_name=key,
            expires=timedelta(minutes=15),
        )
        return DownloadUrl(
            url=url,
        )
