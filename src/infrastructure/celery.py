from celery import Celery
from celery.schedules import crontab

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
    "app.users.tasks",
)

celery_app.conf.beat_schedule = {
    "appointment-reminder-24h": {
        "task": "app.appointments.tasks.appointment_reminder",
        "schedule": crontab(minute="*/5"),
        "args": (24,),
    },
    "appointment-reminder-1h": {
        "task": "app.appointments.tasks.appointment_reminder",
        "schedule": crontab(minute="*/5"),
        "args": (1,),
    },
    "delete_unverified_users": {
        "task": "app.users.tasks.delete_unverified_users",
        "schedule": crontab(minute="*/10"),
        "args": (),
    },
    "cleanup_schedules": {
        "task": "app.schedules.tasks.cleanup_schedules",
        "schedule": crontab(hour=3, minute=0),
        "args": (),
    }
}