from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.user_role import UserRole
from core.security import get_password_hash

from app.users.models.user import User

from app.users.repositories.user import UserRepository
from app.users.repositories.specialization import SpecializationRepository

from app.users.schemas.user import DoctorCreateSchema, PatientCreateSchema

from app.users.exceptions.user import UserAlreadyExistsException, UserIsNotPatientException, UserNotFoundException, UserIsNotDoctorException

from app.users.exceptions.specialization import SpecializationNotFoundException

class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repo = UserRepository(session)
        self.specialization_repo = SpecializationRepository(session)

    @staticmethod
    async def exists(user_role: UserRole, user: User) -> bool:
        if not user:
            raise UserNotFoundException()
        if user.role != user_role:
            if user.role == UserRole.DOCTOR:
                raise UserIsNotDoctorException()
            else:
                raise UserIsNotPatientException()
        return True

    async def create_doctor(self, user: DoctorCreateSchema) -> User:
        if await self.user_repo.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        specialization = await self.specialization_repo.get_by_id(user.specialization_id)
        if not specialization:
            raise SpecializationNotFoundException()
        user.specialization_id = specialization.id
        hashed_password = get_password_hash(user.password_hash)
        user.password_hash = hashed_password
        doctor = await self.user_repo.create_doctor(user)
        return doctor

    async def create_patient(self, user: PatientCreateSchema) -> User:
        if await self.user_repo.get_user_by_email(user.email):
            raise UserAlreadyExistsException()
        hashed_password = get_password_hash(user.password_hash)
        user.password_hash = hashed_password
        patient = await self.user_repo.create_patient(user)
        return patient

    async def get_all_doctors(self) -> list[User]:
        doctors = await self.user_repo.get_all_doctors()
        return doctors

    async def get_all_patients(self) -> list[User]:
        patients = await self.user_repo.get_all_patient()
        return patients

    async def get_user_by_id(self, user_role: UserRole, user_id: int) -> User:
        user = await self.user_repo.get_user_by_id(user_id)
        if self.exists(user_role=user_role, user=user):
            return user
        raise UserNotFoundException()

    async def get_user_by_email(self,user_role: UserRole, user_email: str) -> User:
        user = await self.user_repo.get_user_by_email(user_email)
        if self.exists(user_role=user_role, user=user):
            return user
        raise UserNotFoundException()
