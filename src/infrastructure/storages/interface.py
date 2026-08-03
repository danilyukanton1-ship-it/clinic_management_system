from abc import ABC, abstractmethod

from fastapi import UploadFile

from infrastructure.storages.schemas import DownloadUrl, StoredFileSchema


class StorageInterface(ABC):
    @abstractmethod
    async def save(self, file: UploadFile) -> StoredFileSchema:
        """Upload a file to storage."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a file from storage."""
        raise NotImplementedError

    @abstractmethod
    async def get_download_url(self, key: str) -> DownloadUrl:
        """Generate a temporary download URL."""
        raise NotImplementedError
