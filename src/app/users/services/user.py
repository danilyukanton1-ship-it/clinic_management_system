from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_password_hash

from app.users.schemas.user import DoctorCreateSchema, DoctorResponseSchema, PatientResponseSchema, DoctorUpdateSchema, \
    PatientUpdateSchema

from app.users.exceptions.user import UserAlreadyExistsException, UserNotFoundException

from app.users.exceptions.specialization import SpecializationNotFoundException
from db.unit_of_work import UnitOfWork


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(self.session)

    async def _check_user_exists(self, email: str):
        if await self.uow.users.get_user_by_email(email):
            raise UserAlreadyExistsException()

    async def _validate_user_contacts(
        self,
        user_id: int,
        email: str,
        phone: str | None,
    ) -> None:
        email_user = await self.uow.users.get_user_by_email(email)
        if email_user and email_user.id != user_id:
            raise UserAlreadyExistsException()
        if phone:
            phone_user = await self.uow.users.get_user_by_phone(phone)
            if phone_user and phone_user.id != user_id:
                raise UserAlreadyExistsException()

    async def create_doctor(self, user: DoctorCreateSchema) -> DoctorResponseSchema:
        async with self.uow:
            await self._check_user_exists(user.email)
            specialization = await self.uow.specializations.get_specialization_by_id(user.specialization_id)
            if not specialization:
                raise SpecializationNotFoundException()
            user.specialization_id = specialization.id
            user.password_hash = get_password_hash(user.password_hash)
            doctor = await self.uow.users.create_doctor(user)
        return DoctorResponseSchema.model_validate(doctor)

    async def get_all_doctors(self) -> list[DoctorResponseSchema]:
        doctors = await self.uow.users.get_all_doctors()
        if not doctors:
            raise UserNotFoundException()
        return [DoctorResponseSchema.model_validate(doctor) for doctor in doctors]

    async def get_doctors_by_specialization_id(self, specialization_id: int) -> list[DoctorResponseSchema]:
        doctors = await self.uow.users.get_doctors_by_specialization_id(specialization_id=specialization_id)
        if not doctors:
            raise UserNotFoundException()
        return [DoctorResponseSchema.model_validate(doctor) for doctor in doctors]

    async def get_all_patients(self) -> list[PatientResponseSchema]:
        patients = await self.uow.users.get_all_patient()
        if not patients:
            raise UserNotFoundException()
        return [PatientResponseSchema.model_validate(patient) for patient in patients]

    async def get_doctor_by_id(self, doctor_id: int) -> DoctorResponseSchema:
        doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
        if not doctor:
            raise UserNotFoundException()
        return DoctorResponseSchema.model_validate(doctor)

    async def get_patient_by_id(self, patient_id: int) -> PatientResponseSchema:
        patient = await self.uow.users.get_patient_by_id(patient_id)
        if not patient:
            raise UserNotFoundException()
        return PatientResponseSchema.model_validate(patient)

    async def get_doctor_by_email(self, email: str) -> DoctorResponseSchema:
        doctor = await self.uow.users.get_doctor_by_email(email=email)
        if not doctor:
            raise UserNotFoundException()
        return DoctorResponseSchema.model_validate(doctor)

    async def get_patient_by_email(self, email: str) -> PatientResponseSchema:
        patient = await self.uow.users.get_patient_by_email(email=email)
        if not patient:
            raise UserNotFoundException()
        return PatientResponseSchema.model_validate(patient)

    async def get_patient_by_phone(self, phone: str) -> PatientResponseSchema:
        patient = await self.uow.users.get_patient_by_phone(phone=phone)
        if not patient:
            raise UserNotFoundException()
        return PatientResponseSchema.model_validate(patient)

    async def update_doctor(self, doctor_id: int, data: DoctorUpdateSchema) -> DoctorResponseSchema:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            await self._validate_user_contacts(
                user_id=doctor.id,
                email=doctor.email,
                phone=doctor.phone,
            )
            specialization = await self.uow.specializations.get_specialization_by_id(specialization_id=data.specialization_id)
            if not specialization:
                raise SpecializationNotFoundException()
            updated_doctor = await self.uow.users.update_doctor(doctor=doctor, data=data)
        return DoctorResponseSchema.model_validate(updated_doctor)

    async def update_patient(self, patient_id: int, data: PatientUpdateSchema) -> PatientResponseSchema:
        async with self.uow:
            patient = await self.uow.users.get_patient_by_id(patient_id=patient_id)
            if not patient:
                raise UserNotFoundException()
            await self._validate_user_contacts(
                user_id=patient.id,
                email=patient.email,
                phone=patient.phone,
            )
            updated_patient = await self.uow.users.update_patient(patient=patient, data=data)
        return PatientResponseSchema.model_validate(updated_patient)
