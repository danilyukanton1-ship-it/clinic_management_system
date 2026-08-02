from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models.user import User
from app.scheduling.policy.schedule_absence import ScheduleAbsencePolicy
from app.scheduling.schemas.schedule_absence import (
    ScheduleAbsenceCreateSchema,
    ScheduleAbsenceResponseSchema,
    ScheduleAbsenceUpdateSchema,
)
from app.scheduling.exceptions.schedule_absence import (
    AbsenceAlreadyScheduledException,
    AbsenceNotFoundException,
    AbsenceAlreadyFinishedException,
    AbsenceAlreadyStartedException,
    AbsenceCanNotBeChangedException,
)
from app.users.exceptions.user import UserNotFoundException
from common.enums.slot_status import SlotStatus
from common.pagination.schemas import PaginationParams, PaginatedResponse
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork


class ScheduleAbsenceService:

    def __init__(self, session: AsyncSession):
        self.policy = ScheduleAbsencePolicy()
        self.uow = UnitOfWork(session)

    async def _make_slots_unavailable(
        self, doctor_id: int, start_date: datetime, end_date: datetime
    ):
        slots = await self.uow.schedule_slots.get_slots_overlapping_period(
            doctor_id=doctor_id, start_date=start_date, end_date=end_date
        )
        for slot in slots:
            await self.uow.schedule_slots.change_slot_status(
                slot=slot, status=SlotStatus.BLOCKED
            )

    async def _unblock_slots_for_absence(
        self, start_date: datetime, end_date: datetime, doctor_id: int
    ):
        slots_to_unblock = (
            await self.uow.schedule_slots.get_future_blocked_slots_in_period(
                doctor_id=doctor_id,
                start_date=start_date,
                end_date=end_date,
            )
        )
        for slot in slots_to_unblock:
            await self.uow.schedule_slots.change_slot_status(
                slot=slot,
                status=SlotStatus.FREE,
            )

    async def create(
        self, data: ScheduleAbsenceCreateSchema
    ) -> ScheduleAbsenceResponseSchema:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=data.doctor_id)
            if not doctor:
                raise UserNotFoundException()
            existing_absence = await self.uow.absences.get_overlapping_absence(
                doctor_id=data.doctor_id,
                start_date=data.start_date,
                end_date=data.end_date,
            )
            if existing_absence:
                raise AbsenceAlreadyScheduledException()
            absence = await self.uow.absences.create_absence(data=data)
            await self._make_slots_unavailable(
                doctor_id=data.doctor_id,
                start_date=data.start_date,
                end_date=data.end_date,
            )
        return ScheduleAbsenceResponseSchema.model_validate(absence)

    async def update(
        self, absence_id: int, data: ScheduleAbsenceUpdateSchema
    ) -> ScheduleAbsenceResponseSchema:
        async with self.uow:
            now = datetime.now()
            absence = await self.uow.absences.get_absence_by_id(absence_id=absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            if absence.end_date <= now:
                raise AbsenceAlreadyFinishedException()
            if absence.start_date <= now:
                if data.start_date.replace(microsecond=0) != absence.start_date.replace(
                    microsecond=0
                ):
                    raise AbsenceAlreadyStartedException()
                if data.end_date <= now:
                    raise AbsenceCanNotBeChangedException()
                if data.reason != absence.reason:
                    raise AbsenceCanNotBeChangedException()
                old_start_date = now
                old_end_date = absence.end_date
                new_start_date = now
                new_end_date = data.end_date
            else:
                old_start_date = absence.start_date
                old_end_date = absence.end_date
                new_start_date = data.start_date
                new_end_date = data.end_date
            existing_absence = await self.uow.absences.get_overlapping_absence(
                doctor_id=absence.doctor_id,
                start_date=new_start_date,
                end_date=new_end_date,
                exclude_absence_id=absence.id,
            )
            if existing_absence:
                raise AbsenceAlreadyScheduledException()
            updated_absence = await self.uow.absences.update_absence(
                absence=absence, data=data
            )
            await self._unblock_slots_for_absence(
                start_date=old_start_date,
                end_date=old_end_date,
                doctor_id=updated_absence.doctor_id,
            )
            await self._make_slots_unavailable(
                doctor_id=updated_absence.doctor_id,
                start_date=new_start_date,
                end_date=new_end_date,
            )
        return ScheduleAbsenceResponseSchema.model_validate(updated_absence)

    async def delete(self, absence_id: int) -> None:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            if absence.start_date <= datetime.now():
                raise AbsenceAlreadyStartedException()
            await self._unblock_slots_for_absence(
                doctor_id=absence.doctor_id,
                start_date=absence.start_date,
                end_date=absence.end_date,
            )
            await self.uow.absences.delete_absence(absence)
        return None

    async def get_future_by_doctor_id(
        self, doctor_id: int, current_user: User, pagination: PaginationParams
    ) -> PaginatedResponse[ScheduleAbsenceResponseSchema]:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            absences = await self.uow.absences.get_future_absences_by_doctor_id(
                doctor_id=doctor_id, pagination=pagination
            )
            if absences.items:
                self.policy.can_view(
                    user=current_user, schedule_absence=absences.items[0]
                )
        return build_paginated_response(
            items=absences.items,
            total=absences.total,
            pagination=pagination,
            schema=ScheduleAbsenceResponseSchema,
        )

    async def get_past_by_doctor_id(
        self, doctor_id: int, current_user: User, pagination: PaginationParams
    ) -> list[ScheduleAbsenceResponseSchema]:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            absences = await self.uow.absences.get_past_absences_by_doctor_id(
                doctor_id=doctor_id, pagination=pagination
            )
            if absences.items:
                self.policy.can_view(
                    user=current_user, schedule_absence=absences.items[0]
                )
            return build_paginated_response(
                items=absences.items,
                total=absences.total,
                pagination=pagination,
                schema=ScheduleAbsenceResponseSchema,
            )

    async def get_absence_by_id(
        self, absence_id: int, current_user: User
    ) -> ScheduleAbsenceResponseSchema:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id=absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            self.policy.can_view(user=current_user, schedule_absence=absence)
            return ScheduleAbsenceResponseSchema.model_validate(absence)
