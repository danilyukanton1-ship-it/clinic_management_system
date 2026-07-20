from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models.user import User
from app.scheduling.policy.schedule_absence import ScheduleAbsencePolicy
from app.scheduling.schemas.schedule_absence import ScheduleAbsenceCreateSchema, ScheduleAbsenceResponseSchema, \
    ScheduleAbsenceUpdateSchema
from app.scheduling.exceptions.schedule_absence import AbsenceAlreadyScheduledException, AbsenceNotFoundException
from app.users.exceptions.user import UserNotFoundException
from common.enums.slot_status import SlotStatus
from db.unit_of_work import UnitOfWork


class ScheduleAbsenceService:

    def __init__(self,session: AsyncSession):
        self.session = session
        self.policy = ScheduleAbsencePolicy()
        self.uow = UnitOfWork(self.session)

    async def _make_slots_unavailable(self, doctor_id: int, start_date: datetime, end_date: datetime):
        slots = await self.uow.schedule_slots.get_slots_overlapping_period(
            doctor_id=doctor_id,
            start_date=start_date,
            end_date=end_date
        )
        if slots:
            for slot in slots:
                await self.uow.schedule_slots.change_slot_status(slot=slot, status=SlotStatus.BLOCKED)

    async def create(self, data: ScheduleAbsenceCreateSchema) -> ScheduleAbsenceResponseSchema:
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

    async def update(self, absence_id: int, data: ScheduleAbsenceUpdateSchema) -> ScheduleAbsenceResponseSchema:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id=absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            updated_absence = await self.uow.absences.update_absence(absence=absence, data=data)
            await self._make_slots_unavailable(
                doctor_id=absence.doctor_id,
                start_date=absence.start_date,
                end_date=absence.end_date,
            )
        return ScheduleAbsenceResponseSchema.model_validate(updated_absence)

    async def delete(self, absence_id: int) -> None:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            await self.uow.absences.delete_absence(absence)
        return None

    async def get_future_by_doctor_id(self, doctor_id: int, current_user: User) -> list[ScheduleAbsenceResponseSchema]:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            absences = await self.uow.absences.get_future_absences_by_doctor_id(doctor_id=doctor_id)
            if not absences:
                raise AbsenceNotFoundException()
            self.policy.can_view(user=current_user, schedule_absence=absences[0])
        return [ScheduleAbsenceResponseSchema.model_validate(s) for s in absences]

    async def get_past_by_doctor_id(self, doctor_id: int, current_user: User) -> list[ScheduleAbsenceResponseSchema]:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            absences = await self.uow.absences.get_past_absences_by_doctor_id(doctor_id=doctor_id)
            if not absences:
                raise AbsenceNotFoundException()
            self.policy.can_view(user=current_user, schedule_absence=absences[0])
            return [ScheduleAbsenceResponseSchema.model_validate(s) for s in absences]

    async def get_absence_by_id(self, absence_id: int, current_user: User) -> ScheduleAbsenceResponseSchema:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id=absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            self.policy.can_view(user=current_user, schedule_absence=absence)
            return ScheduleAbsenceResponseSchema.model_validate(absence)