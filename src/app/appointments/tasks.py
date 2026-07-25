import asyncio
from datetime import date, time, datetime, timedelta

from db.database import AsyncSessionLocal
from db.unit_of_work import UnitOfWork
from infrastructure.celery import celery_app
from infrastructure.notifications.smtp import SMTPEmailService
from infrastructure.notifications.template_renderer import TemplateRenderer


@celery_app.task
def send_appointment_created_notification(
        email: str,
        username: str,
        appointment_date: date,
        appointment_time: time,
        doctor_last_name: str,
        doctor_first_name: str,
        doctor_specialization: str,
    ):
    renderer = TemplateRenderer()
    email_service = SMTPEmailService()

    html = renderer.render(
        "appointment_created.html",
        username=username,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        doctor_first_name=doctor_first_name,
        doctor_last_name=doctor_last_name,
        doctor_specialization=doctor_specialization,
        year=datetime.now().year,
    )
    asyncio.run(
        email_service.send(
            email_receiver=email,
            subject="Doctor's appointment",
            body="You were scheduled for a doctor's appointment.",
            html=html,
        )
    )

@celery_app.task
def send_appointment_reminder(
        email: str,
        username: str,
        appointment_date: date,
        appointment_time: time,
        doctor_last_name: str,
        doctor_first_name: str,
        doctor_specialization: str,
    ):
    renderer = TemplateRenderer()
    email_service = SMTPEmailService()

    html = renderer.render(
        "appointment_remind.html",
        username=username,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        doctor_first_name=doctor_first_name,
        doctor_last_name=doctor_last_name,
        doctor_specialization=doctor_specialization,
        year=datetime.now().year,
    )

    asyncio.run(
        email_service.send(
            email_receiver=email,
            subject="Appointment remind",
            body="You have an appointment with a doctor soon",
            html=html,
        )
    )

@celery_app.task(
    name="app.appointments.tasks.appointment_reminder"
)
def appointment_reminder(
        hours:int,
    ):
    asyncio.run(
        _check_appointments_for_reminder(
            hours=hours,
        )
    )

async def _check_appointments_for_reminder(
        hours: int,
    ):
    async with AsyncSessionLocal() as session:
        async with UnitOfWork(session) as uow:
            start = datetime.now() + timedelta(hours=hours)
            end = start + timedelta(minutes=5)
            appointments = await uow.appointments.get_upcoming_appointments_for_reminder(
                start=start,
                end=end,
            )
            for appointment in appointments:
                send_appointment_reminder.delay(
                    email=appointment.patient.email,
                    username=appointment.patient.first_name,
                    appointment_date=appointment.slot.slot_start.date(),
                    appointment_time=appointment.slot.slot_start.time(),
                    doctor_first_name=appointment.doctor.first_name,
                    doctor_last_name=appointment.doctor.last_name,
                    doctor_specialization=appointment.doctor.specialization.name,
                )


