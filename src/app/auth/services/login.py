from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas.login import LoginSchema
from app.auth.schemas.token import TokenResponseSchema
from app.auth.exceptions.login import InvalidCredentialsException
from db.unit_of_work import UnitOfWork
from app.auth.security import verify_password
from app.auth.services.token import TokenService

class LoginService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session)
        self.token_serv = TokenService

    async def login(self, data: LoginSchema):
        user = await self.uow.users.get_user_by_email(data.email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            data.password,
            user.password_hash
        ):
            raise InvalidCredentialsException()

        access_token = TokenService.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type='access'
        )

        refresh_token = TokenService.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type='refresh'
        )

        return TokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )