from minio import Minio

from core.config import settings
from infrastructure.notifications.smtp import SMTPEmailService
from infrastructure.notifications.template_renderer import TemplateRenderer
from infrastructure.storages.services import MinioStorageService

minio_client = Minio(
    endpoint=settings.minio.ENDPOINT,
    access_key=settings.minio.ACCESS_KEY,
    secret_key=settings.minio.SECRET_KEY,
    secure=settings.minio.SECURE,
)


def get_smtp_service() -> SMTPEmailService:
    return SMTPEmailService()


def get_template_renderer() -> TemplateRenderer:
    return TemplateRenderer()


def get_minio_service() -> MinioStorageService:
    return MinioStorageService(
        bucket=settings.minio.BUCKET,
        client=minio_client,
    )
