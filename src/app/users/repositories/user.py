from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.auth.schemas.register import RegisterSchema
from common.enums.user_role import UserRole
from app.users.models.user import User
from app.users.schemas.user import (
    DoctorCreateSchema,
    DoctorUpdateSchema,
    PatientUpdateSchema,
    AdminCreateSchema,
    AdminUpdateSchema,
)

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _create_user(
            self,
            data,
            role: UserRole,
            password_hash: str,
            specialization_id: int | None = None,
    ) -> User:
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            email=data.email,
            phone=data.phone,
            role=role,
            password_hash=password_hash,
            specialization_id=specialization_id,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def _update_user(
            self,
            user: User,
            data: BaseModel,
    ) -> User:
        for field, value in data.model_dump().items():
            setattr(user, field, value)

        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def _get_by_id(
        self,
        user_id: int,
        role: UserRole | None = None,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)

        if role is not None:
            stmt = stmt.where(User.role == role)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_by_email(
        self,
        email: str,
        role: UserRole | None = None,
    ) -> User | None:
        stmt = select(User).where(User.email == email)

        if role is not None:
            stmt = stmt.where(User.role == role)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_by_phone(
        self,
        phone: str,
        role: UserRole | None = None,
    ) -> User | None:
        stmt = select(User).where(User.phone == phone)

        if role is not None:
            stmt = stmt.where(User.role == role)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_all(self, role: UserRole) -> list[User]:
        stmt =(
            select(User)
            .where(User.role == role)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_patient(self, data: RegisterSchema, password_hash: str) -> User:
        return await self._create_user(
            data=data,
            role=UserRole.PATIENT,
            password_hash=password_hash,
        )

    async def create_doctor(self, data: DoctorCreateSchema, password_hash: str, specialization_id: int) -> User:
        return await self._create_user(
            data=data,
            role=UserRole.DOCTOR,
            password_hash=password_hash,
            specialization_id=specialization_id,
        )

    async def create_admin(self, data: AdminCreateSchema, password_hash: str) -> User:
        return await self._create_user(
            data=data,
            role=UserRole.ADMIN,
            password_hash=password_hash,
        )

    async def update_doctor(self, doctor: User, data: DoctorUpdateSchema) -> User:
        return await self._update_user(user=doctor, data=data)

    async def update_patient(self, patient: User, data: PatientUpdateSchema) -> User:
        return await self._update_user(user=patient, data=data)

    async def update_admin(self, admin: User, data: AdminUpdateSchema) -> User:
        return await self._update_user(user=admin, data=data)

    async def get_doctor_by_id(self, doctor_id: int) -> User | None:
        return await self._get_by_id(user_id=doctor_id, role=UserRole.DOCTOR)

    async def get_patient_by_id(self, patient_id: int) -> User | None:
        return await self._get_by_id(user_id=patient_id, role=UserRole.PATIENT)

    async def get_admin_by_id(self, admin_id: int) -> User | None:
        return await self._get_by_id(user_id=admin_id, role=UserRole.ADMIN)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self._get_by_id(user_id=user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self._get_by_email(email=email)

    async def get_doctor_by_email(self, email: str) -> User | None:
        return await self._get_by_email(email=email, role=UserRole.DOCTOR)

    async def get_patient_by_email(self, email: str) -> User | None:
        return await self._get_by_email(email=email, role=UserRole.PATIENT)

    async def get_user_by_phone(self, phone: str) -> User | None:
        return await self._get_by_phone(phone=phone)

    async def get_patient_by_phone(self, phone: str) -> User | None:
        return await self._get_by_phone(phone=phone, role=UserRole.PATIENT)

    async def get_doctor_by_phone(self, phone: str) -> User | None:
        return await self._get_by_phone(phone=phone, role=UserRole.DOCTOR)

    async def get_all_doctors(self) -> list[User]:
        return await self._get_all(role=UserRole.DOCTOR)

    async def get_all_patients(self) -> list[User]:
        return await self._get_all(role=UserRole.PATIENT)

    async def get_all_admins(self) -> list[User]:
        return await self._get_all(role=UserRole.ADMIN)

    async def get_doctors_by_specialization_id(self, specialization_id: int) -> list[User]:
        stmt = (
            select(User)
            .where(User.specialization_id == specialization_id, User.role == UserRole.DOCTOR)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def make_user_inactive(self, user: User) -> User:
        user.is_active = False
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def make_user_verified(self, user: User) -> User:
        user.is_verified = True
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def reset_password(self, user: User, password_hash: str) -> User:
        user.password_hash = password_hash
        await self.session.flush()
        await self.session.refresh(user)
        return user

