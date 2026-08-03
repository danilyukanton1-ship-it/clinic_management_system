import asyncio

from db.database import AsyncSessionLocal
from db.unit_of_work import UnitOfWork
from infrastructure.celery import celery_app


async def _cleanup_inactive_old_schedules():
    async with AsyncSessionLocal() as session, UnitOfWork(session) as uow:
        schedules = await uow.schedules.get_inactive_expired_schedules()
        if not schedules:
            return
        schedule_ids = [schedule.id for schedule in schedules]
        appointments = (
            await uow.appointments.get_appointments_to_delete_by_schedule_ids(
                schedule_ids=schedule_ids
            )
        )
        for appointment in appointments:
            await uow.appointments.delete_appointment(appointment=appointment)
        slots = await uow.schedule_slots.get_slots_by_schedule_ids(
            schedule_ids=schedule_ids
        )
        for slot in slots:
            await uow.schedule_slots.delete_slot(slot=slot)
        for schedule in schedules:
            await uow.schedules.delete_schedule(schedule=schedule)


@celery_app.task(name="app.scheduling.tasks.cleanup_schedules")
def cleanup_schedules() -> None:
    asyncio.run(_cleanup_inactive_old_schedules())
