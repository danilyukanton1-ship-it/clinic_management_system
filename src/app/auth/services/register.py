from datetime import datetime
from secrets import randbelow
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.tasks import send_verify_email, send_success_password_reset_email
from app.users.exceptions.user import UserNotFoundException
from app.users.schemas.user import PatientResponseSchema
from db.unit_of_work import UnitOfWork
from app.auth.security import get_password_hash
from app.auth.schemas.register import RegisterSchema, VerifyEmailSchema, ForgotPasswordSchema, ResetPasswordSchema
from app.auth.exceptions.register import EmailAlreadyExistsException, PhoneAlreadyExistsException, \
    UserAlreadyVerifiedException, VerificationCodeNotFoundException, IncorrectVerificationCodeException, \
    UserNotVerifiedException


class RegisterService:

    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.uow = UnitOfWork(session)
        self.redis = redis

    async def _send_verification_email(self, email: str, username: str) -> None:
        verification_code = f"{randbelow(1_000_000):06d}"

        await self.redis.set(email, verification_code, ex=600)

        send_verify_email.delay(
            email=email,
            username=username,
            verification_code=verification_code,
        )

    async def _verify_email_code(self, email: str, verification_code: str) -> None:
        stored_verification_code = await self.redis.get(email)
        if not stored_verification_code:
            raise VerificationCodeNotFoundException()
        if isinstance(stored_verification_code, bytes):
            stored_verification_code = stored_verification_code.decode()

        if verification_code != stored_verification_code:
            raise IncorrectVerificationCodeException()
        await self.redis.delete(email)

    async def verify_email(self, data: VerifyEmailSchema) -> PatientResponseSchema:
        async with self.uow:
            user = await self.uow.users.get_patient_by_email(
                email=data.email,
            )
            if not user:
                raise UserNotFoundException()
            if user.is_verified:
                raise UserAlreadyVerifiedException()
            await self._verify_email_code(
                email=user.email,
                verification_code=data.verification_code,
            )
            verified_user = await self.uow.users.change_user_verification_status(user=user, is_verified=True)
        return PatientResponseSchema.model_validate(verified_user)

    async def forgot_password(self, data: ForgotPasswordSchema) -> None:
        async with self.uow:
            user = await self.uow.users.get_patient_by_email(
                email=data.email,
            )
            if not user:
                raise UserNotFoundException()
            if not user.is_verified:
                raise UserNotVerifiedException()
            await self._send_verification_email(
                email=user.email,
                username=user.first_name,
            )

    async def reset_password(self, data: ResetPasswordSchema) -> PatientResponseSchema:
        async with self.uow:
            user = await self.uow.users.get_patient_by_email(
                email=data.email,
            )
            if not user:
                raise UserNotFoundException()
            await self._verify_email_code(
                email=user.email,
                verification_code=data.verification_code,
            )
            password_hash = get_password_hash(data.password)
            user = await self.uow.users.reset_password(
                user=user,
                password_hash=password_hash,
            )
            send_success_password_reset_email.delay(
                email=user.email,
                username=user.first_name,
                changed_at=datetime.now(),
            )
        return PatientResponseSchema.model_validate(user)


    async def register(self, data: RegisterSchema) -> PatientResponseSchema:
        async with self.uow:
            existing_email = await self.uow.users.get_user_by_email(data.email)
            existing_phone = await self.uow.users.get_user_by_phone(data.phone)

            if existing_email:
                raise EmailAlreadyExistsException()
            if existing_phone:
                raise PhoneAlreadyExistsException()
            password_hash = get_password_hash(data.password)

            created_user = await self.uow.users.create_patient(
                data=data,
                password_hash=password_hash,
            )
            await self._send_verification_email(
                email=created_user.email,
                username=created_user.first_name,
            )
        return created_user

    async def resend_verification_email(self, email: str) -> None:
        async with self.uow:
            user = await self.uow.users.get_patient_by_email(email=email)

            if not user:
                raise UserNotFoundException()
            if user.is_verified:
                raise UserAlreadyVerifiedException()

            await self._send_verification_email(
                email=user.email,
                username=user.first_name,
            )