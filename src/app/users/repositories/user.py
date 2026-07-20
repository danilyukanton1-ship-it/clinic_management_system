from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.user_role import UserRole
from app.users.models.user import User
from app.users.schemas.user import (
    PatientCreateSchema,
    DoctorCreateSchema, DoctorUpdateSchema, PatientUpdateSchema,
)

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_patient(self, patient: PatientCreateSchema, password_hash: str) -> User:
        patient = User(
            first_name=patient.first_name,
            last_name=patient.last_name,
            middle_name=patient.middle_name,
            email=patient.email,
            phone=patient.phone,
            role=patient.role,
            password_hash=password_hash
        )
        self.session.add(patient)
        await self.session.flush()
        await self.session.refresh(patient)
        return patient

    async def create_doctor(self, data: DoctorCreateSchema, password_hash: str, specialization_id: int) -> User:
        doctor = User(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            email=data.email,
            phone=data.phone,
            role=data.role,
            password_hash=password_hash,
            specialization_id=specialization_id
        )
        self.session.add(doctor)
        await self.session.flush()
        await self.session.refresh(doctor)
        return doctor

    async def update_doctor(self, doctor: User, data: DoctorUpdateSchema) -> User:
        doctor.first_name = data.first_name
        doctor.last_name = data.last_name
        doctor.middle_name = data.middle_name
        doctor.email = data.email
        doctor.phone = data.phone
        doctor.specialization_id = data.specialization_id
        await self.session.flush()
        await self.session.refresh(doctor)
        return doctor

    async def update_patient(self, patient: User, data: PatientUpdateSchema) -> User:
        patient.first_name = data.first_name
        patient.last_name = data.last_name
        patient.email = data.email
        patient.phone = data.phone
        patient.middle_name = data.middle_name
        await self.session.flush()
        await self.session.refresh(patient)
        return patient

    async def get_doctor_by_id(self, doctor_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == doctor_id, User.role == UserRole.DOCTOR)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_patient_by_id(self, patient_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == patient_id, User.role == UserRole.PATIENT)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str) -> User | None:
        stmt = (
            select(User)
            .where(User.phone == phone)
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

    async def get_all_patients(self) -> list[User]:
        stmt = (
            select(User)
            .where(User.role == UserRole.PATIENT)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_doctor_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email, User.role == UserRole.DOCTOR)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_patient_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email, User.role == UserRole.PATIENT)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_doctors_by_specialization_id(self, specialization_id: int) -> list[User]:
        stmt = (
            select(User)
            .where(User.specialization_id == specialization_id, User.role == UserRole.DOCTOR)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_patient_by_phone(self, phone: str) -> User | None:
        stmt = (
            select(User)
            .where(User.phone == phone, User.role == UserRole.PATIENT)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_doctor_by_phone(self, phone: str) -> User | None:
        stmt = (
            select(User)
            .where(User.phone == phone, User.role == UserRole.DOCTOR)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def make_user_inactive(self, user: User) -> User:
        user.is_active = False
        await self.session.flush()
        await self.session.refresh(user)
        return user

