from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.user import PatientCreateSchema
from app.users.models.user import User
from common.enums.user_role import UserRole
from db.unit_of_work import UnitOfWork
from app.auth.security import get_password_hash
from app.auth.schemas.register import RegisterSchema
from app.auth.exceptions.register import EmailAlreadyExistsException, PhoneAlreadyExistsException

class RegisterService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(self.session)

    async def register(self, data: RegisterSchema) -> User:
        async with self.uow:
            existing_user = await self.uow.users.get_user_by_email(data.email)

            existing_phone = await self.uow.users.get_user_by_phone(data.phone)

            if existing_user is not None:
                raise EmailAlreadyExistsException()
            if existing_phone is not None:
                raise PhoneAlreadyExistsException()

            password_hash = get_password_hash(data.password)

            patient = PatientCreateSchema(
                first_name=data.first_name,
                last_name=data.last_name,
                middle_name=data.middle_name,
                email=data.email,
                phone=data.phone,
                password=data.password,
                role=UserRole.PATIENT,
            )

            created_user = await self.uow.users.create_patient(
                patient=patient,
                password_hash=password_hash,
            )
        return created_user