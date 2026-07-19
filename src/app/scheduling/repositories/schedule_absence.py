from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.scheduling.models.schedule_absence import ScheduleAbsence
from app.scheduling.schemas.schedule_absence import ScheduleAbsenceCreateSchema, ScheduleAbsenceUpdateSchema

class ScheduleAbsenceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_absence(self, data: ScheduleAbsenceCreateSchema):
        absence = ScheduleAbsence(
            doctor_id=data.doctor_id,
            start_date=data.start_date,
            end_date=data.end_date,
            reason=data.reason,
            description=data.description,
        )
        self.session.add(absence)
        await self.session.flush()
        return absence

    async def update_absence(self, absence: ScheduleAbsence, data: ScheduleAbsenceUpdateSchema):
        absence.start_date = data.start_date
        absence.end_date = data.end_date
        absence.reason = data.reason
        absence.description = data.description
        await self.session.flush()
        return absence

    async def get_absence_by_id(self, absence_id: int) -> ScheduleAbsence | None:
        stmt = (
            select(ScheduleAbsence)
            .where(ScheduleAbsence.id == absence_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_past_absences_by_doctor_id(self, doctor_id: int) -> list[ScheduleAbsence]:
        stmt = (
            select(ScheduleAbsence)
            .where(ScheduleAbsence.doctor_id == doctor_id, ScheduleAbsence.end_date <= datetime.now())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_future_absences_by_doctor_id(self, doctor_id: int) -> list[ScheduleAbsence]:
        stmt = (
            select(ScheduleAbsence)
            .where(ScheduleAbsence.doctor_id == doctor_id, ScheduleAbsence.end_date >= datetime.now())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_overlapping_absence(self, doctor_id: int, start_date: datetime, end_date: datetime) -> ScheduleAbsence | None:
        stmt = (
            select(ScheduleAbsence)
            .where(
                ScheduleAbsence.doctor_id == doctor_id,
                ScheduleAbsence.start_date <= end_date,
                ScheduleAbsence.end_date >= start_date,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete_absence(self, absence: ScheduleAbsence) -> None:
        await self.session.delete(absence)
        await self.session.flush()
        return None