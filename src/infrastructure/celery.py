from celery import Celery
from core.config import settings

celery_app = Celery(
    'Clinic_management_system',
    broker=settings.celery.BROKER_URL,
    backend=settings.celery.RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.imports = (
    "app.appointments.tasks",
    "app.auth.tasks",
)