import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from app.auth.exceptions.register import (
    EmailAlreadyExistsException,
    PhoneAlreadyExistsException,
    UserAlreadyVerifiedException,
    VerificationCodeNotFoundException,
    IncorrectVerificationCodeException,
    UserNotVerifiedException,
)
from app.users.exceptions.user import UserNotFoundException
from app.users.schemas.user import PatientResponseSchema


class TestRegisterService:

    @pytest.mark.asyncio
    async def test_register_success(
        self,
        register_service,
        register_schema,
        patient_1,
    ):
        register_service.uow.users.get_user_by_email = AsyncMock(return_value=None)

        register_service.uow.users.get_user_by_phone = AsyncMock(return_value=None)

        register_service.uow.users.create_patient = AsyncMock(return_value=patient_1)

        with (
            patch(
                "app.auth.services.register.get_password_hash",
                return_value="hashed_password",
            ) as mock_hash,
            patch(
                "app.auth.services.register.RegisterService._send_verification_email",
                new_callable=AsyncMock,
            ) as mock_send_email,
        ):
            ...
            result = await register_service.register(register_schema)

        register_service.uow.users.get_user_by_email.assert_called_once_with(
            register_schema.email
        )

        register_service.uow.users.get_user_by_phone.assert_called_once_with(
            register_schema.phone
        )

        mock_hash.assert_called_once_with(register_schema.password)

        register_service.uow.users.create_patient.assert_called_once_with(
            data=register_schema,
            password_hash="hashed_password",
        )

        mock_send_email.assert_called_once_with(
            email=patient_1.email,
            username=patient_1.first_name,
        )

        assert result == patient_1

    @pytest.mark.asyncio
    async def test_register_email_already_exists(
        self,
        register_service,
        register_schema,
        patient_1,
    ):
        register_service.uow.users.get_user_by_email = AsyncMock(return_value=patient_1)

        register_service.uow.users.get_user_by_phone = AsyncMock(return_value=None)

        register_service.uow.users.create_patient = AsyncMock()

        with pytest.raises(EmailAlreadyExistsException):
            await register_service.register(register_schema)

        register_service.uow.users.get_user_by_email.assert_called_once_with(
            register_schema.email,
        )

        register_service.uow.users.get_user_by_phone.assert_called_once_with(
            register_schema.phone,
        )

        register_service.uow.users.create_patient.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_phone_already_exists(
        self,
        register_service,
        register_schema,
        patient_1,
    ):
        register_service.uow.users.get_user_by_email = AsyncMock(return_value=None)

        register_service.uow.users.get_user_by_phone = AsyncMock(return_value=patient_1)

        register_service.uow.users.create_patient = AsyncMock()

        with pytest.raises(PhoneAlreadyExistsException):
            await register_service.register(register_schema)

        register_service.uow.users.get_user_by_email.assert_called_once_with(
            register_schema.email
        )

        register_service.uow.users.get_user_by_phone.assert_called_once_with(
            register_schema.phone
        )

        register_service.uow.users.create_patient.assert_not_called()

    @pytest.mark.asyncio
    async def test_verify_email_success(
        self,
        register_service,
        verify_email_schema,
        patient_1_unverified,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1_unverified
        )

        register_service.uow.users.change_user_verification_status = AsyncMock(
            return_value=patient_1_unverified
        )

        register_service._verify_email_code = AsyncMock()

        result = await register_service.verify_email(verify_email_schema)

        register_service.uow.users.get_patient_by_email.assert_awaited_once_with(
            email=verify_email_schema.email,
        )

        register_service._verify_email_code.assert_awaited_once_with(
            email=patient_1_unverified.email,
            verification_code=verify_email_schema.verification_code,
        )

        register_service.uow.users.change_user_verification_status.assert_awaited_once_with(
            user=patient_1_unverified,
            is_verified=True,
        )

        assert isinstance(result, PatientResponseSchema)
        assert result.id == patient_1_unverified.id

    @pytest.mark.asyncio
    async def test_verify_email_user_not_found(
        self,
        register_service,
        verify_email_schema,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(return_value=None)

        register_service.uow.users.make_user_verified = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await register_service.verify_email(verify_email_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=verify_email_schema.email,
        )

        register_service.uow.users.make_user_verified.assert_not_called()

    @pytest.mark.asyncio
    async def test_verify_email_already_verified(
        self,
        register_service,
        verify_email_schema,
        patient_1,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1
        )

        register_service.uow.users.make_user_verified = AsyncMock()

        with pytest.raises(UserAlreadyVerifiedException):
            await register_service.verify_email(verify_email_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=verify_email_schema.email,
        )

        register_service.uow.users.make_user_verified.assert_not_called()

    @pytest.mark.asyncio
    async def test_verify_email_code_not_found(
        self,
        register_service,
        verify_email_schema,
        patient_1_unverified,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1_unverified
        )

        register_service.uow.users.make_user_verified = AsyncMock()

        register_service._verify_email_code = AsyncMock(
            side_effect=VerificationCodeNotFoundException()
        )

        with pytest.raises(VerificationCodeNotFoundException):
            await register_service.verify_email(verify_email_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=verify_email_schema.email,
        )

        register_service._verify_email_code.assert_called_once_with(
            email=patient_1_unverified.email,
            verification_code=verify_email_schema.verification_code,
        )

        register_service.uow.users.make_user_verified.assert_not_called()

    @pytest.mark.asyncio
    async def test_verify_email_invalid_code(
        self,
        register_service,
        verify_email_schema,
        patient_1_unverified,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1_unverified
        )

        register_service.uow.users.make_user_verified = AsyncMock()

        register_service._verify_email_code = AsyncMock(
            side_effect=IncorrectVerificationCodeException()
        )

        with pytest.raises(IncorrectVerificationCodeException):
            await register_service.verify_email(verify_email_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=verify_email_schema.email,
        )

        register_service._verify_email_code.assert_called_once_with(
            email=patient_1_unverified.email,
            verification_code=verify_email_schema.verification_code,
        )

        register_service.uow.users.make_user_verified.assert_not_called()

    @pytest.mark.asyncio
    async def test_forgot_password_success(
        self,
        register_service,
        forgot_password_schema,
        patient_1,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1
        )

        register_service._send_verification_email = AsyncMock()

        result = await register_service.forgot_password(forgot_password_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=forgot_password_schema.email,
        )

        register_service._send_verification_email.assert_called_once_with(
            email=patient_1.email,
            username=patient_1.first_name,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_forgot_password_user_not_found(
        self,
        register_service,
        forgot_password_schema,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(return_value=None)

        register_service._send_verification_email = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await register_service.forgot_password(forgot_password_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=forgot_password_schema.email,
        )

        register_service._send_verification_email.assert_not_called()

    @pytest.mark.asyncio
    async def test_forgot_password_user_not_verified(
        self,
        register_service,
        forgot_password_schema,
        patient_1_unverified,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1_unverified
        )

        register_service._send_verification_email = AsyncMock()

        with pytest.raises(UserNotVerifiedException):
            await register_service.forgot_password(forgot_password_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=forgot_password_schema.email,
        )

        register_service._send_verification_email.assert_not_called()

    @pytest.mark.asyncio
    async def test_reset_password_success(
        self,
        register_service,
        reset_password_schema,
        patient_1,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1
        )

        register_service._verify_email_code = AsyncMock()

        register_service.uow.users.reset_password = AsyncMock(return_value=patient_1)

        with (
            patch(
                "app.auth.services.register.get_password_hash",
                return_value="hashed_password",
            ) as mock_hash,
            patch(
                "app.auth.services.register.send_success_password_reset_email"
            ) as mock_task,
        ):
            mock_task.delay = MagicMock()

            result = await register_service.reset_password(reset_password_schema)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=reset_password_schema.email,
        )

        register_service._verify_email_code.assert_called_once_with(
            email=patient_1.email,
            verification_code=reset_password_schema.verification_code,
        )

        mock_hash.assert_called_once_with(reset_password_schema.password)

        register_service.uow.users.reset_password.assert_called_once_with(
            user=patient_1,
            password_hash="hashed_password",
        )

        mock_task.delay.assert_called_once()

        assert isinstance(result, PatientResponseSchema)

    @pytest.mark.asyncio
    async def test_reset_password_user_not_found(
        self,
        register_service,
        reset_password_schema,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(return_value=None)

        register_service._verify_email_code = AsyncMock()
        register_service.uow.users.reset_password = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await register_service.reset_password(reset_password_schema)

        register_service._verify_email_code.assert_not_called()
        register_service.uow.users.reset_password.assert_not_called()

    @pytest.mark.asyncio
    async def test_reset_password_code_not_found(
        self,
        register_service,
        reset_password_schema,
        patient_1,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1
        )

        register_service._verify_email_code = AsyncMock(
            side_effect=VerificationCodeNotFoundException()
        )

        register_service.uow.users.reset_password = AsyncMock()

        with pytest.raises(VerificationCodeNotFoundException):
            await register_service.reset_password(reset_password_schema)

        register_service.uow.users.reset_password.assert_not_called()

    @pytest.mark.asyncio
    async def test_reset_password_invalid_code(
        self,
        register_service,
        reset_password_schema,
        patient_1,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1
        )

        register_service._verify_email_code = AsyncMock(
            side_effect=IncorrectVerificationCodeException()
        )

        register_service.uow.users.reset_password = AsyncMock()

        with pytest.raises(IncorrectVerificationCodeException):
            await register_service.reset_password(reset_password_schema)

        register_service.uow.users.reset_password.assert_not_called()

    @pytest.mark.asyncio
    async def test_resend_verification_email_success(
        self,
        register_service,
        patient_1_unverified,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1_unverified
        )

        register_service._send_verification_email = AsyncMock()

        result = await register_service.resend_verification_email(
            patient_1_unverified.email
        )

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=patient_1_unverified.email,
        )

        register_service._send_verification_email.assert_called_once_with(
            email=patient_1_unverified.email,
            username=patient_1_unverified.first_name,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_resend_verification_email_user_not_found(
        self,
        register_service,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(return_value=None)

        register_service._send_verification_email = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await register_service.resend_verification_email("patient@test.com")

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email="patient@test.com",
        )

        register_service._send_verification_email.assert_not_called()

    @pytest.mark.asyncio
    async def test_resend_verification_email_already_verified(
        self,
        register_service,
        patient_1,
    ):
        register_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1
        )

        register_service._send_verification_email = AsyncMock()

        with pytest.raises(UserAlreadyVerifiedException):
            await register_service.resend_verification_email(patient_1.email)

        register_service.uow.users.get_patient_by_email.assert_called_once_with(
            email=patient_1.email,
        )

        register_service._send_verification_email.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_verification_email_success(
        self,
        register_service,
    ):
        register_service.redis.set = AsyncMock()

        with (
            patch(
                "app.auth.services.register.randbelow",
                return_value=123456,
            ),
            patch(
                "app.auth.services.register.send_verify_email",
            ) as mock_task,
        ):
            mock_task.delay = MagicMock()

            await register_service._send_verification_email(
                email="patient@test.com",
                username="Patient",
            )

        register_service.redis.set.assert_called_once_with(
            "patient@test.com",
            "123456",
            ex=600,
        )

        mock_task.delay.assert_called_once_with(
            email="patient@test.com",
            username="Patient",
            verification_code="123456",
        )

    @pytest.mark.asyncio
    async def test_verify_email_code_success(
        self,
        register_service,
    ):
        register_service.redis.get.return_value = "123456"
        register_service.redis.delete = AsyncMock()

        await register_service._verify_email_code(
            email="patient@test.com",
            verification_code="123456",
        )

        register_service.redis.get.assert_called_once_with(
            "patient@test.com",
        )

        register_service.redis.delete.assert_called_once_with(
            "patient@test.com",
        )

    @pytest.mark.asyncio
    async def test_verify_email_code_bytes(
        self,
        register_service,
    ):
        register_service.redis.get.return_value = b"123456"
        register_service.redis.delete = AsyncMock()

        await register_service._verify_email_code(
            email="patient@test.com",
            verification_code="123456",
        )

        register_service.redis.delete.assert_called_once_with(
            "patient@test.com",
        )

    @pytest.mark.asyncio
    async def test_verify_email_code_not_found(
        self,
        register_service,
    ):
        register_service.redis.get.return_value = None

        register_service.redis.delete = AsyncMock()

        with pytest.raises(VerificationCodeNotFoundException):
            await register_service._verify_email_code(
                email="patient@test.com",
                verification_code="123456",
            )

        register_service.redis.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_verify_email_code_invalid(
        self,
        register_service,
    ):
        register_service.redis.get.return_value = "654321"

        register_service.redis.delete = AsyncMock()

        with pytest.raises(IncorrectVerificationCodeException):
            await register_service._verify_email_code(
                email="patient@test.com",
                verification_code="123456",
            )

        register_service.redis.delete.assert_not_called()
