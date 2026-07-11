from app.scheduling.schemas.schedule_absence import ScheduleAbsenceCreateSchema, ScheduleAbsenceResponseSchema, \
    ScheduleAbsenceUpdateSchema
from app.scheduling.exceptions.schedule_absence import AbsenceAlreadyScheduledException, AbsenceNotFoundException
from app.users.exceptions.user import UserNotFoundException
from db.unit_of_work import UnitOfWork


class ScheduleAbsenceService:

    def __init__(self,session):
        self.session = session

        self.uow = UnitOfWork(self.session)

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
        return ScheduleAbsenceResponseSchema.model_validate(absence)

    async def update(self, absence_id: int, data: ScheduleAbsenceUpdateSchema) -> ScheduleAbsenceResponseSchema:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id=absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            updated_absence = await self.uow.absences.update_absence(absence=absence, data=data)
        return ScheduleAbsenceResponseSchema.model_validate(updated_absence)

    async def get_future_by_doctor_id(self, doctor_id: int) -> list[ScheduleAbsenceResponseSchema]:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            absences = await self.uow.absences.get_future_absences_by_doctor_id(doctor_id=doctor_id)
            if not absences:
                raise AbsenceNotFoundException()
        return absences

    async def get_past_by_doctor_id(self, doctor_id: int) -> list[ScheduleAbsenceResponseSchema]:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            absences = await self.uow.absences.get_past_absences_by_doctor_id(doctor_id=doctor_id)
            if not absences:
                raise AbsenceNotFoundException()
        return absences

    async def delete(self, absence_id: int) -> None:
        async with self.uow:
            absence = await self.uow.absences.get_absence_by_id(absence_id=absence_id)
            if not absence:
                raise AbsenceNotFoundException()
            await self.uow.absences.delete_absence(absence=absence)
        return None

