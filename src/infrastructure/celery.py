import asyncio

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_process_init, worker_process_shutdown

from core.config import settings

celery_app = Celery(
    "Clinic_management_system",
    broker=settings.celery.BROKER_URL,
    backend=settings.celery.RESULT_BACKEND,
)

_loop: asyncio.AbstractEventLoop | None = None


def get_loop() -> asyncio.AbstractEventLoop:
    if _loop is None:
        raise RuntimeError("Event loop not initialized")
    return _loop


@worker_process_init.connect
def init_worker(**kwargs):
    global _loop
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global _loop

    if _loop is not None:
        asyncio.set_event_loop(None)
        _loop.close()
        _loop = None


def run(coro):
    return get_loop().run_until_complete(coro)


celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.imports = (
    "app.appointments.tasks",
    "app.auth.tasks",
    "app.users.tasks",
    "app.scheduling.tasks",
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
        "task": "app.scheduling.tasks.cleanup_schedules",
        "schedule": crontab(hour=3, minute=0),
        "args": (),
    },
}
