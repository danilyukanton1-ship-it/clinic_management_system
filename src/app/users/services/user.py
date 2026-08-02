from secrets import randbelow

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models.user import User
from app.users.models.specialization import Specialization
from app.auth.security import get_password_hash
from app.users.policy.user import UserPolicy

from app.users.schemas.user import (
    DoctorCreateSchema,
    DoctorResponseSchema,
    PatientResponseSchema,
    DoctorUpdateSchema,
    PatientUpdateSchema,
    AdminResponseSchema,
    AdminUpdateSchema,
    AdminCreateSchema,
    UserUpdateSchema,
)

from app.users.exceptions.user import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserAlreadyInactiveException,
)
from app.auth.tasks import send_verify_email
from app.users.exceptions.specialization import SpecializationNotFoundException
from common.pagination.schemas import PaginationParams, PaginatedResponse
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork


class UserService:

    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.policy = UserPolicy()
        self.redis = redis
        self.uow = UnitOfWork(session)

    async def _send_verification_email(self, email: str, username: str) -> None:
        verification_code = f"{randbelow(1_000_000):06d}"

        await self.redis.set(email, verification_code, ex=600)

        send_verify_email.delay(
            email=email,
            username=username,
            verification_code=verification_code,
        )

    async def _new_email_verification(
        self,
        user: User,
        data: UserUpdateSchema,
    ):
        if user.email != data.email:
            await self.uow.users.change_user_verification_status(
                user=user,
                is_verified=False,
            )
            await self._send_verification_email(
                email=data.email, username=data.first_name
            )

    async def _check_email_exists(self, email: str):
        if await self.uow.users.get_user_by_email(email=email):
            raise UserAlreadyExistsException()

    async def _validate_user_contacts(
        self,
        user_id: int,
        email: str,
        phone: str | None,
    ) -> None:
        email_user = await self.uow.users.get_user_by_email(email=email)
        if email_user and email_user.id != user_id:
            raise UserAlreadyExistsException()
        if phone:
            phone_user = await self.uow.users.get_user_by_phone(phone=phone)
            if phone_user and phone_user.id != user_id:
                raise UserAlreadyExistsException()

    async def _get_doctor(self, doctor_id: int) -> User:
        doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
        if not doctor:
            raise UserNotFoundException()
        return doctor

    async def _get_patient(self, patient_id: int, admin: bool | None = None) -> User:
        patient = await self.uow.users.get_patient_by_id(
            patient_id=patient_id, admin=admin
        )
        if not patient:
            raise UserNotFoundException()
        return patient

    async def _get_admin(self, admin_id: int) -> User:
        admin = await self.uow.users.get_admin_by_id(admin_id=admin_id)
        if not admin:
            raise UserNotFoundException()
        return admin

    async def _get_specialization(self, specialization_id: int) -> Specialization:
        specialization = await self.uow.specializations.get_specialization_by_id(
            specialization_id=specialization_id
        )
        if specialization is None:
            raise SpecializationNotFoundException()
        return specialization

    async def _deactivate(self, user: User) -> User:
        if not user.is_active:
            raise UserAlreadyInactiveException()

        return await self.uow.users.make_user_inactive(user=user)

    async def create_doctor(self, data: DoctorCreateSchema) -> DoctorResponseSchema:
        async with self.uow:
            await self._check_email_exists(email=data.email)
            specialization = await self._get_specialization(
                specialization_id=data.specialization_id
            )
            hashed_password = get_password_hash(password=data.password)
            doctor = await self.uow.users.create_doctor(
                data=data,
                specialization_id=specialization.id,
                password_hash=hashed_password,
            )
            await self._send_verification_email(
                email=doctor.email, username=doctor.first_name
            )
        return DoctorResponseSchema.model_validate(doctor)

    async def create_admin(self, data: AdminCreateSchema) -> AdminResponseSchema:
        async with self.uow:
            await self._check_email_exists(email=data.email)
            hashed_password = get_password_hash(password=data.password)
            admin = await self.uow.users.create_admin(
                data=data, password_hash=hashed_password
            )
            await self._send_verification_email(
                email=admin.email, username=admin.first_name
            )
        return AdminResponseSchema.model_validate(admin)

    async def get_all_doctors(self, pagination: PaginationParams) -> PaginatedResponse[DoctorResponseSchema]:
        doctors = await self.uow.users.get_all_doctors(pagination=pagination)
        return build_paginated_response(
            items=doctors.items,
            total=doctors.total,
            pagination=pagination,
            schema=DoctorResponseSchema
        )

    async def get_all_doctors_for_admin(self, pagination: PaginationParams) -> PaginatedResponse[DoctorResponseSchema]:
        doctors = await self.uow.users.get_all_doctors_for_admin(pagination=pagination)
        return build_paginated_response(
            items=doctors.items,
            total=doctors.total,
            pagination=pagination,
            schema=DoctorResponseSchema
        )

    async def get_doctors_by_specialization_id(
        self, specialization_id: int, admin: bool | None = None
    ) -> list[DoctorResponseSchema]:
        specialization = await self.uow.specializations.get_specialization_by_id(
            specialization_id=specialization_id
        )
        if not specialization:
            raise SpecializationNotFoundException()
        doctors = await self.uow.users.get_doctors_by_specialization_id(
            specialization_id=specialization_id, admin=admin
        )
        return [DoctorResponseSchema.model_validate(doctor) for doctor in doctors]

    async def get_all_patients(self, pagination: PaginationParams) -> PaginatedResponse[PatientResponseSchema]:
        patients = await self.uow.users.get_all_patients(pagination=pagination)
        return build_paginated_response(
            items=patients.items,
            total=patients.total,
            pagination=pagination,
            schema=PatientResponseSchema
        )

    async def get_all_admins(self, pagination: PaginationParams) -> PaginatedResponse[AdminResponseSchema]:
        admins = await self.uow.users.get_all_admins(pagination=pagination)
        return build_paginated_response(
            items=admins.items,
            total=admins.total,
            pagination=pagination,
            schema=AdminResponseSchema
        )

    async def get_doctor_by_id(self, doctor_id: int) -> DoctorResponseSchema:
        doctor = await self._get_doctor(doctor_id=doctor_id)
        schedule = await self.uow.schedules.get_all_by_doctor_id(doctor_id=doctor_id)
        if not schedule:
            raise UserNotFoundException()
        return DoctorResponseSchema.model_validate(doctor)

    async def get_doctor_by_id_for_admin(self, doctor_id: int) -> DoctorResponseSchema:
        doctor = await self.uow.users.get_doctor_by_id_for_admin(doctor_id=doctor_id)
        if not doctor:
            raise UserNotFoundException()
        return DoctorResponseSchema.model_validate(doctor)

    async def get_admin_by_id(self, admin_id: int) -> AdminResponseSchema:
        admin = await self._get_admin(admin_id=admin_id)
        return AdminResponseSchema.model_validate(admin)

    async def get_patient_by_id(
        self, patient_id: int, current_user: User, admin: bool | None = None
    ) -> PatientResponseSchema:
        patient = await self._get_patient(patient_id=patient_id, admin=admin)
        self.policy.can_view(
            current_user=current_user,
            target_user=patient,
        )
        return PatientResponseSchema.model_validate(patient)

    async def get_doctor_by_email(
        self, email: str, current_user: User
    ) -> DoctorResponseSchema:
        doctor = await self.uow.users.get_doctor_by_email(email=email)
        if not doctor:
            raise UserNotFoundException()
        self.policy.can_view(current_user=current_user, target_user=doctor)
        return DoctorResponseSchema.model_validate(doctor)

    async def get_patient_by_email(
        self, email: str, current_user: User
    ) -> PatientResponseSchema:
        patient = await self.uow.users.get_patient_by_email(email=email)
        if not patient:
            raise UserNotFoundException()
        self.policy.can_view(
            current_user=current_user,
            target_user=patient,
        )
        return PatientResponseSchema.model_validate(patient)

    async def get_patient_by_phone(
        self, phone: str, current_user: User
    ) -> PatientResponseSchema:
        patient = await self.uow.users.get_patient_by_phone(phone=phone)
        if not patient:
            raise UserNotFoundException()
        self.policy.can_view(
            current_user=current_user,
            target_user=patient,
        )
        return PatientResponseSchema.model_validate(patient)

    async def update_admin(
        self, admin_id: int, data: AdminUpdateSchema
    ) -> AdminResponseSchema:
        async with self.uow:
            admin = await self._get_admin(admin_id=admin_id)
            await self._validate_user_contacts(
                user_id=admin.id,
                email=data.email,
                phone=data.phone,
            )
            await self._new_email_verification(
                user=admin,
                data=data,
            )
            updated_admin = await self.uow.users.update_admin(
                admin=admin,
                data=data,
            )
        return AdminResponseSchema.model_validate(updated_admin)

    async def update_doctor(
        self, doctor_id: int, data: DoctorUpdateSchema, current_user: User
    ) -> DoctorResponseSchema:
        async with self.uow:
            doctor = await self._get_doctor(doctor_id=doctor_id)
            self.policy.can_update(
                current_user=current_user,
                target_user=doctor,
            )
            await self._validate_user_contacts(
                user_id=doctor.id,
                email=data.email,
                phone=data.phone,
            )
            await self._get_specialization(specialization_id=data.specialization_id)
            await self._new_email_verification(
                user=doctor,
                data=data,
            )
            updated_doctor = await self.uow.users.update_doctor(
                doctor=doctor, data=data
            )
        return DoctorResponseSchema.model_validate(updated_doctor)

    async def update_patient(
        self, patient_id: int, data: PatientUpdateSchema, current_user: User
    ) -> PatientResponseSchema:
        async with self.uow:
            patient = await self._get_patient(patient_id=patient_id)
            self.policy.can_update(
                current_user=current_user,
                target_user=patient,
            )
            await self._validate_user_contacts(
                user_id=patient.id,
                email=data.email,
                phone=data.phone,
            )
            await self._new_email_verification(
                user=patient,
                data=data,
            )
            updated_patient = await self.uow.users.update_patient(
                patient=patient, data=data
            )
        return PatientResponseSchema.model_validate(updated_patient)

    async def deactivate_doctor(self, doctor_id: int) -> DoctorResponseSchema:
        async with self.uow:
            doctor = await self._get_doctor(doctor_id=doctor_id)
            doctor = await self._deactivate(user=doctor)
        return DoctorResponseSchema.model_validate(doctor)

    async def deactivate_patient(self, patient_id: int) -> PatientResponseSchema:
        async with self.uow:
            patient = await self._get_patient(patient_id=patient_id)
            patient = await self._deactivate(user=patient)
        return PatientResponseSchema.model_validate(patient)

    async def deactivate_admin(self, admin_id: int) -> AdminResponseSchema:
        async with self.uow:
            admin = await self._get_admin(admin_id=admin_id)
            admin = await self._deactivate(user=admin)
        return AdminResponseSchema.model_validate(admin)
