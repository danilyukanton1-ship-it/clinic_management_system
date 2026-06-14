from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.user_role import UserRole
from core.security import password_hash

from app.models.user import User

from app.repositories.user import UserRepository
from app.repositories.specialization import SpecializationRepository

from app.schemas.user import DoctorCreateSchema, PatientCreateSchema

from app.exceptions.user import UserAlreadyExistsException, UserIsNotPatientException
from app.exceptions.specialization import SpecializationNotFoundException

class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repo = UserRepository(session)
        self.specialization_repo = SpecializationRepository(session)

    async def create_doctor(self, user: DoctorCreateSchema) -> User:
        if await self.user_repo.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        specialization = await self.specialization_repo.get_by_id(user.specialization_id)
        if not specialization:
            raise SpecializationNotFoundException()
        user.specialization_id = specialization.id
        hashed_password = password_hash(user.password)
        user.password = hashed_password
        doctor = await self.user_repo.create_doctor(user)
        return doctor

    async def create_patient(self, user: PatientCreateSchema) -> User:
        if await self.user_repo.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        hashed_password = password_hash(user.password)
        user.password = hashed_password
        patient = await self.user_repo.create_patient(user)
        return patient

    async def get_all_doctors(self) -> list[User]:
        doctors = await self.user_repo.get_all_doctors()
        return doctors

    async def get_user_by_id_or_email(self, user_role: UserRole, user: int | str) -> User:
        if isinstance(user, int):
            patient = await self.user_repo.get_user_by_id(user)
            if patient.role != user_role:
                raise UserIsNotPatientException()
            return patient
        patient = await self.user_repo.get_user_by_email(user)
        if patient.role != user_role:
            raise UserIsNotPatientException()
        return patient

