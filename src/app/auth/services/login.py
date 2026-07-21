from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas.login import LoginSchema
from app.auth.schemas.token import TokenResponseSchema
from app.auth.exceptions.login import InvalidCredentialsException
from db.unit_of_work import UnitOfWork
from common.enums.token_type import TokenType
from app.auth.security import verify_password
from app.auth.services.token import TokenService

class LoginService:
    def __init__(self, session: AsyncSession):
        self.uow = UnitOfWork(session)

    async def login(self, data: LoginSchema) -> TokenResponseSchema:
        user = await self.uow.users.get_user_by_email(data.email)

        if not user or not user.is_active:
            raise InvalidCredentialsException()

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsException()

        access_token = TokenService.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type=TokenType.ACCESS
        )

        refresh_token = TokenService.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type=TokenType.REFRESH
        )

        return TokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )