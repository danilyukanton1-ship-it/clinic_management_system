from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.repositories.schedule_slot import ScheduleSlotRepository
from app.appoinments.repositories.appointment import AppointmentRepository
from app.scheduling.repositories.schedule import ScheduleRepository
from app.users.repositories.user import UserRepository
from app.users.repositories.specialization import SpecializationRepository
from app.medical_records.repositories.disease import DiseaseRepository
from app.medical_records.repositories.drug import DrugRepository
from app.medical_records.repositories.diagnosis import DiagnosisRepository
from app.medical_records.repositories.prescription import PrescriptionRepository
from app.medical_records.repositories.prescription_item import PrescriptionItemRepository
from app.scheduling.repositories.schedule_absence import ScheduleAbsenceRepository

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_slots: ScheduleSlotRepository = ScheduleSlotRepository(session)
        self.appointments: AppointmentRepository = AppointmentRepository(session)
        self.schedules: ScheduleRepository = ScheduleRepository(session)
        self.users: UserRepository = UserRepository(session)
        self.specializations: SpecializationRepository = SpecializationRepository(session)
        self.diseases: DiseaseRepository = DiseaseRepository(session)
        self.drugs: DrugRepository = DrugRepository(session)
        self.diagnoses: DiagnosisRepository = DiagnosisRepository(session)
        self.prescriptions: PrescriptionRepository = PrescriptionRepository(session)
        self.prescription_items: PrescriptionItemRepository = PrescriptionItemRepository(session)
        self.absences: ScheduleAbsenceRepository = ScheduleAbsenceRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

