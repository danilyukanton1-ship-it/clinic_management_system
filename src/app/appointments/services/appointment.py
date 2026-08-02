from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.appointments.schemas.appointment import (
    AppointmentCreateSchema,
    AppointmentResponseSchema,
)
from app.users.models.user import User
from app.scheduling.exceptions.schedule_slot import (
    SlotNotFoundException,
    SlotNotAvailableException,
)
from app.users.exceptions.user import UserNotFoundException
from app.appointments.policy.appointment import AppointmentPolicy
from common.enums.slot_status import SlotStatus
from common.pagination.schemas import PaginationParams, PaginatedResponse
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork
from app.appointments.tasks import send_appointment_created_notification


class AppointmentService:

    def __init__(self, session: AsyncSession) -> None:
        self.policy = AppointmentPolicy()
        self.uow = UnitOfWork(session=session)

    async def create_appointment(
        self, data: AppointmentCreateSchema
    ) -> AppointmentResponseSchema:
        async with self.uow:
            slot = await self.uow.schedule_slots.get_slot_by_id(slot_id=data.slot_id)
            if not slot:
                raise SlotNotFoundException()
            if slot.status != SlotStatus.FREE:
                raise SlotNotAvailableException()
            if slot.slot_start <= datetime.now(timezone.utc):
                raise SlotNotAvailableException()
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=data.doctor_id)
            if not doctor:
                raise UserNotFoundException()
            patient = await self.uow.users.get_patient_by_id(patient_id=data.patient_id)
            if not patient:
                raise UserNotFoundException()
            appointment = await self.uow.appointments.create(data=data)
            await self.uow.schedule_slots.change_slot_status(
                slot=slot, status=SlotStatus.BOOKED
            )
            appointment = (
                await self.uow.appointments.get_appointment_by_id_with_relations(
                    appointment_id=appointment.id,
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            send_appointment_created_notification.delay(
                email=appointment.patient.email,
                username=appointment.patient.first_name,
                appointment_date=appointment.slot.slot_start.date(),
                appointment_time=appointment.slot.slot_start.time(),
                doctor_last_name=appointment.doctor.last_name,
                doctor_first_name=appointment.doctor.first_name,
                doctor_specialization=appointment.doctor.specialization.name,
            )
            return AppointmentResponseSchema.model_validate(appointment)

    async def get_future_apps_by_user_id(
        self, user_id: int, pagination: PaginationParams
    ) -> PaginatedResponse[AppointmentResponseSchema]:
        async with self.uow:
            user = await self.uow.users.get_user_by_id(user_id=user_id)
            if user is None:
                raise UserNotFoundException()
            appointments = (
                await self.uow.appointments.get_future_appointments_by_user_id(
                    user_id=user_id,
                    pagination=pagination
                )
            )
            for appointment in appointments.items:
                self.policy.can_view(user=user, appointment=appointment)
            return build_paginated_response(
                items=appointments.items,
                total=appointments.total,
                pagination=pagination,
                schema=AppointmentResponseSchema,
            )

    async def get_past_apps_by_user_id(
        self, user_id: int, pagination: PaginationParams
    ) -> PaginatedResponse[AppointmentResponseSchema]:
        async with self.uow:
            user = await self.uow.users.get_user_by_id(user_id=user_id)
            if user is None:
                raise UserNotFoundException()
            appointments = await self.uow.appointments.get_past_appointments_by_user_id(
                user_id=user_id,
                pagination=pagination
            )
            for appointment in appointments.items:
                self.policy.can_view(user=user, appointment=appointment)
            return build_paginated_response(
                items=appointments.items,
                total=appointments.total,
                pagination=pagination,
                schema=AppointmentResponseSchema,
            )

    async def get_appointment_by_id(
        self, appointment_id: int, current_user: User
    ) -> AppointmentResponseSchema:
        appointment = await self.uow.appointments.get_appointment_by_id(
            appointment_id=appointment_id
        )
        if not appointment:
            raise AppointmentNotFoundException()
        self.policy.can_view(user=current_user, appointment=appointment)
        return AppointmentResponseSchema.model_validate(appointment)

    async def delete(self, appointment_id: int) -> None:
        async with self.uow:
            appointment = await self.uow.appointments.get_appointment_by_id(
                appointment_id=appointment_id
            )
            if not appointment:
                raise AppointmentNotFoundException()
            await self.uow.appointments.delete_appointment(appointment=appointment)
            await self.uow.schedule_slots.change_slot_status(
                slot=appointment.slot, status=SlotStatus.FREE
            )
        return None

    async def get_upcoming_for_reminder(self, hours: int):
        start = datetime.now() + timedelta(hours=hours)
        end = start + timedelta(minutes=5)

        appointments = (
            await self.uow.appointments.get_upcoming_appointments_for_reminder(
                start=start,
                end=end,
            )
        )
        return appointments
