from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.user_role import UserRole
from app.users.models.user import User
from app.users.schemas.user import (
    PatientCreateSchema,
    DoctorCreateSchema,
)

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_patient(self, patient: PatientCreateSchema) -> User:
        patient = User(
            first_name=patient.first_name,
            last_name=patient.last_name,
            middle_name=patient.middle_name,
            email=patient.email,
            phone=patient.phone,
            role=patient.role,
            password_hash=patient.password_hash
        )
        self.session.add(patient)
        await self.session.commit()
        await self.session.refresh(patient)
        return patient

    async def create_doctor(self, doctor: DoctorCreateSchema) -> User:
        doctor = User(
            first_name=doctor.first_name,
            last_name=doctor.last_name,
            middle_name=doctor.middle_name,
            email=doctor.email,
            phone=doctor.phone,
            role=doctor.role,
            password_hash=doctor.password_hash,
            specialization_id=doctor.specialization_id
        )
        self.session.add(doctor)
        await self.session.commit()
        await self.session.refresh(doctor)
        return doctor

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User:
        stmt = (
            select(User)
            .where(User.email == email)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_doctors(self) -> list[User]:
        stmt = (
            select(User)
            .where(User.role == UserRole.DOCTOR)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_patient(self) -> list[User]:
        stmt = (
            select(User)
            .where(User.role == UserRole.PATIENT)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


