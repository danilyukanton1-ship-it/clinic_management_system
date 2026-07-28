import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from app.users.exceptions.specialization import SpecializationNotFoundException
from app.users.exceptions.user import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserAlreadyInactiveException,
)
from app.users.schemas.user import (
    DoctorResponseSchema,
    AdminResponseSchema,
    PatientResponseSchema,
)
from common.permissions.exceptions import ForbiddenException


class TestUserService:

    @pytest.mark.asyncio
    async def test_check_email_exists_success(
        self,
        user_service,
    ):
        user_service.uow.users.get_user_by_email = AsyncMock(return_value=None)

        await user_service._check_email_exists(
            email="test@test.com",
        )

        user_service.uow.users.get_user_by_email.assert_awaited_once_with(
            email="test@test.com",
        )

    @pytest.mark.asyncio
    async def test_check_email_exists_already_exists(
        self,
        user_service,
        doctor_1,
    ):
        user_service.uow.users.get_user_by_email = AsyncMock(
            return_value=doctor_1,
        )

        with pytest.raises(UserAlreadyExistsException):
            await user_service._check_email_exists(
                email="test@test.com",
            )

        user_service.uow.users.get_user_by_email.assert_awaited_once_with(
            email="test@test.com",
        )

    @pytest.mark.asyncio
    async def test_validate_user_contacts_success(
        self,
        user_service,
    ):
        user_service.uow.users.get_user_by_email = AsyncMock(return_value=None)
        user_service.uow.users.get_user_by_phone = AsyncMock(return_value=None)

        await user_service._validate_user_contacts(
            user_id=1,
            email="test@test.com",
            phone="+375291111111",
        )

        user_service.uow.users.get_user_by_email.assert_awaited_once_with(
            email="test@test.com",
        )
        user_service.uow.users.get_user_by_phone.assert_awaited_once_with(
            phone="+375291111111",
        )

    @pytest.mark.asyncio
    async def test_validate_user_contacts_email_already_exists(
        self, user_service, doctor_2, doctor_1
    ):
        user_service.uow.users.get_user_by_email = AsyncMock(
            return_value=doctor_2,
        )

        with pytest.raises(UserAlreadyExistsException):
            await user_service._validate_user_contacts(
                user_id=doctor_1.id,
                email=doctor_2.email,
                phone=None,
            )

        user_service.uow.users.get_user_by_email.assert_awaited_once_with(
            email=doctor_2.email,
        )

    @pytest.mark.asyncio
    async def test_validate_user_contacts_phone_already_exists(
        self,
        user_service,
        doctor_2,
        doctor_1,
    ):
        user_service.uow.users.get_user_by_email = AsyncMock(return_value=None)
        user_service.uow.users.get_user_by_phone = AsyncMock(
            return_value=doctor_2,
        )

        with pytest.raises(UserAlreadyExistsException):
            await user_service._validate_user_contacts(
                user_id=doctor_1.id,
                email="test@test.com",
                phone=doctor_2.phone,
            )

        user_service.uow.users.get_user_by_phone.assert_awaited_once_with(
            phone=doctor_2.phone,
        )

    @pytest.mark.asyncio
    async def test_get_doctor_success(
        self,
        user_service,
        doctor_1,
    ):
        user_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        result = await user_service._get_doctor(
            doctor_id=doctor_1.id,
        )

        assert result == doctor_1

        user_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

    @pytest.mark.asyncio
    async def test_get_doctor_not_found(
        self,
        user_service,
    ):
        user_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(UserNotFoundException):
            await user_service._get_doctor(
                doctor_id=1,
            )

        user_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_patient_success(
        self,
        user_service,
        patient_1,
    ):
        user_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1,
        )

        result = await user_service._get_patient(
            patient_id=patient_1.id,
        )

        assert result == patient_1

        user_service.uow.users.get_patient_by_id.assert_awaited_once_with(
            patient_id=patient_1.id,
        )

    @pytest.mark.asyncio
    async def test_get_patient_not_found(
        self,
        user_service,
    ):
        user_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(UserNotFoundException):
            await user_service._get_patient(
                patient_id=1,
            )

        user_service.uow.users.get_patient_by_id.assert_awaited_once_with(
            patient_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_admin_success(
        self,
        user_service,
        admin_1,
    ):
        user_service.uow.users.get_admin_by_id = AsyncMock(
            return_value=admin_1,
        )

        result = await user_service._get_admin(
            admin_id=admin_1.id,
        )

        assert result == admin_1

        user_service.uow.users.get_admin_by_id.assert_awaited_once_with(
            admin_id=admin_1.id,
        )

    @pytest.mark.asyncio
    async def test_get_admin_not_found(
        self,
        user_service,
    ):
        user_service.uow.users.get_admin_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(UserNotFoundException):
            await user_service._get_admin(
                admin_id=1,
            )

        user_service.uow.users.get_admin_by_id.assert_awaited_once_with(
            admin_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_specialization_success(
        self,
        user_service,
        specialization,
    ):
        user_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=specialization,
        )

        result = await user_service._get_specialization(
            specialization_id=specialization.id,
        )

        assert result == specialization

        user_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=specialization.id,
        )

    @pytest.mark.asyncio
    async def test_get_specialization_not_found(
        self,
        user_service,
    ):
        user_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(SpecializationNotFoundException):
            await user_service._get_specialization(
                specialization_id=1,
            )

        user_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_success(
        self,
        user_service,
        doctor_1,
    ):
        user_service.uow.users.make_user_inactive = AsyncMock(
            return_value=doctor_1,
        )

        result = await user_service._deactivate(
            user=doctor_1,
        )

        assert result == doctor_1

        user_service.uow.users.make_user_inactive.assert_awaited_once_with(
            user=doctor_1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_already_inactive(
        self,
        user_service,
        doctor_1,
    ):
        doctor_1.is_active = False

        user_service.uow.users.make_user_inactive = AsyncMock()

        with pytest.raises(UserAlreadyInactiveException):
            await user_service._deactivate(
                user=doctor_1,
            )

        user_service.uow.users.make_user_inactive.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_doctor_success(
        self,
        user_service,
        doctor_create_schema,
        doctor_1,
        specialization,
    ):
        user_service._check_email_exists = AsyncMock()
        user_service._get_specialization = AsyncMock(
            return_value=specialization,
        )

        user_service.uow.users.create_doctor = AsyncMock(
            return_value=doctor_1,
        )

        with patch(
            "app.users.services.user.get_password_hash",
            return_value="hashed_password",
        ) as password_hash_mock:
            result = await user_service.create_doctor(
                data=doctor_create_schema,
            )

        assert result == DoctorResponseSchema.model_validate(doctor_1)

        user_service._check_email_exists.assert_awaited_once_with(
            email=doctor_create_schema.email,
        )

        user_service._get_specialization.assert_awaited_once_with(
            specialization_id=doctor_create_schema.specialization_id,
        )

        password_hash_mock.assert_called_once_with(
            password=doctor_create_schema.password,
        )

        user_service.uow.users.create_doctor.assert_awaited_once_with(
            data=doctor_create_schema,
            specialization_id=specialization.id,
            password_hash="hashed_password",
        )

    @pytest.mark.asyncio
    async def test_create_doctor_email_exists(
        self,
        user_service,
        doctor_create_schema,
    ):
        user_service._check_email_exists = AsyncMock(
            side_effect=UserAlreadyExistsException,
        )

        user_service._get_specialization = AsyncMock()
        user_service.uow.users.create_doctor = AsyncMock()

        with pytest.raises(UserAlreadyExistsException):
            await user_service.create_doctor(
                data=doctor_create_schema,
            )

        user_service._get_specialization.assert_not_awaited()
        user_service.uow.users.create_doctor.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_doctor_specialization_not_found(
        self,
        user_service,
        doctor_create_schema,
    ):
        user_service._check_email_exists = AsyncMock()

        user_service._get_specialization = AsyncMock(
            side_effect=SpecializationNotFoundException,
        )

        user_service.uow.users.create_doctor = AsyncMock()

        with pytest.raises(SpecializationNotFoundException):
            await user_service.create_doctor(
                data=doctor_create_schema,
            )

        user_service.uow.users.create_doctor.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_admin_success(
        self,
        user_service,
        admin_create_schema,
        admin_1,
    ):
        user_service._check_email_exists = AsyncMock()

        user_service.uow.users.create_admin = AsyncMock(
            return_value=admin_1,
        )

        with patch(
            "app.users.services.user.get_password_hash",
            return_value="hashed_password",
        ) as password_hash_mock:
            result = await user_service.create_admin(
                data=admin_create_schema,
            )

        assert result == AdminResponseSchema.model_validate(admin_1)

        user_service._check_email_exists.assert_awaited_once_with(
            email=admin_create_schema.email,
        )

        password_hash_mock.assert_called_once_with(
            password=admin_create_schema.password,
        )

        user_service.uow.users.create_admin.assert_awaited_once_with(
            data=admin_create_schema,
            password_hash="hashed_password",
        )

    @pytest.mark.asyncio
    async def test_create_admin_email_exists(
        self,
        user_service,
        admin_create_schema,
    ):
        user_service._check_email_exists = AsyncMock(
            side_effect=UserAlreadyExistsException,
        )

        user_service.uow.users.create_admin = AsyncMock()

        with pytest.raises(UserAlreadyExistsException):
            await user_service.create_admin(
                data=admin_create_schema,
            )

        user_service.uow.users.create_admin.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_all_doctors_success(
        self,
        user_service,
        doctor_1,
        doctor_2,
    ):
        user_service.uow.users.get_all_doctors = AsyncMock(
            return_value=[doctor_1, doctor_2],
        )

        result = await user_service.get_all_doctors()

        assert result == [
            DoctorResponseSchema.model_validate(doctor_1),
            DoctorResponseSchema.model_validate(doctor_2),
        ]

        user_service.uow.users.get_all_doctors.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_doctors_by_specialization_id_success(
        self,
        user_service,
        doctor_1,
        doctor_2,
    ):
        user_service.uow.users.get_doctors_by_specialization_id = AsyncMock(
            return_value=[doctor_1, doctor_2],
        )

        result = await user_service.get_doctors_by_specialization_id(
            specialization_id=1,
        )

        assert result == [
            DoctorResponseSchema.model_validate(doctor_1),
            DoctorResponseSchema.model_validate(doctor_2),
        ]

        user_service.uow.users.get_doctors_by_specialization_id.assert_awaited_once_with(
            specialization_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_all_patients_success(
        self,
        user_service,
        patient_1,
        patient_2,
    ):
        user_service.uow.users.get_all_patients = AsyncMock(
            return_value=[patient_1, patient_2],
        )

        result = await user_service.get_all_patients()

        assert result == [
            PatientResponseSchema.model_validate(patient_1),
            PatientResponseSchema.model_validate(patient_2),
        ]

        user_service.uow.users.get_all_patients.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_doctor_by_id_success(
        self,
        user_service,
        doctor_1,
    ):
        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        result = await user_service.get_doctor_by_id(
            doctor_id=doctor_1.id,
        )

        assert result == DoctorResponseSchema.model_validate(doctor_1)

        user_service._get_doctor.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

    @pytest.mark.asyncio
    async def test_get_admin_by_id_success(
        self,
        user_service,
        admin_1,
    ):
        user_service._get_admin = AsyncMock(
            return_value=admin_1,
        )

        result = await user_service.get_admin_by_id(
            admin_id=admin_1.id,
        )

        assert result == AdminResponseSchema.model_validate(admin_1)

        user_service._get_admin.assert_awaited_once_with(
            admin_id=admin_1.id,
        )

    @pytest.mark.asyncio
    async def test_get_patient_by_id_success(
        self,
        user_service,
        patient_1,
        current_admin,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_view = MagicMock()

        result = await user_service.get_patient_by_id(
            patient_id=patient_1.id,
            current_user=current_admin,
        )

        assert result == PatientResponseSchema.model_validate(patient_1)

        user_service._get_patient.assert_awaited_once_with(
            patient_id=patient_1.id,
        )

        user_service.policy.can_view.assert_called_once_with(
            current_user=current_admin,
            target_user=patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_doctor_by_id_not_found(
        self,
        user_service,
    ):
        user_service._get_doctor = AsyncMock(
            side_effect=UserNotFoundException,
        )

        with pytest.raises(UserNotFoundException):
            await user_service.get_doctor_by_id(
                doctor_id=1,
            )

        user_service._get_doctor.assert_awaited_once_with(
            doctor_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_admin_by_id_not_found(
        self,
        user_service,
    ):
        user_service._get_admin = AsyncMock(
            side_effect=UserNotFoundException,
        )

        with pytest.raises(UserNotFoundException):
            await user_service.get_admin_by_id(
                admin_id=1,
            )

        user_service._get_admin.assert_awaited_once_with(
            admin_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_patient_by_id_not_found(
        self,
        user_service,
        current_admin,
    ):
        user_service._get_patient = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service.policy.can_view = MagicMock()

        with pytest.raises(UserNotFoundException):
            await user_service.get_patient_by_id(
                patient_id=1,
                current_user=current_admin,
            )

        user_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_patient_by_id_permission_denied(
        self,
        user_service,
        patient_1,
        current_patient,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException,
        )

        with pytest.raises(ForbiddenException):
            await user_service.get_patient_by_id(
                patient_id=patient_1.id,
                current_user=current_patient,
            )

    @pytest.mark.asyncio
    async def test_get_doctor_by_email_success(
        self,
        user_service,
        doctor_1,
        current_admin,
    ):
        user_service.uow.users.get_doctor_by_email = AsyncMock(
            return_value=doctor_1,
        )
        user_service.policy.can_view = MagicMock()

        result = await user_service.get_doctor_by_email(
            email=doctor_1.email,
            current_user=current_admin,
        )

        assert result == DoctorResponseSchema.model_validate(doctor_1)

        user_service.uow.users.get_doctor_by_email.assert_awaited_once_with(
            email=doctor_1.email,
        )

        user_service.policy.can_view.assert_called_once_with(
            current_user=current_admin,
            target_user=doctor_1,
        )

    @pytest.mark.asyncio
    async def test_get_doctor_by_email_not_found(
        self,
        user_service,
        current_admin,
    ):
        user_service.uow.users.get_doctor_by_email = AsyncMock(
            return_value=None,
        )
        user_service.policy.can_view = MagicMock()

        with pytest.raises(UserNotFoundException):
            await user_service.get_doctor_by_email(
                email="test@test.com",
                current_user=current_admin,
            )

        user_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_doctor_by_email_permission_denied(
        self,
        user_service,
        doctor_1,
        current_patient,
    ):
        user_service.uow.users.get_doctor_by_email = AsyncMock(
            return_value=doctor_1,
        )

        user_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException,
        )

        with pytest.raises(ForbiddenException):
            await user_service.get_doctor_by_email(
                email=doctor_1.email,
                current_user=current_patient,
            )

    @pytest.mark.asyncio
    async def test_get_patient_by_email_success(
        self,
        user_service,
        patient_1,
        current_admin,
    ):
        user_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_view = MagicMock()

        result = await user_service.get_patient_by_email(
            email=patient_1.email,
            current_user=current_admin,
        )

        assert result == PatientResponseSchema.model_validate(patient_1)

        user_service.uow.users.get_patient_by_email.assert_awaited_once_with(
            email=patient_1.email,
        )

        user_service.policy.can_view.assert_called_once_with(
            current_user=current_admin,
            target_user=patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_patient_by_email_not_found(
        self,
        user_service,
        current_admin,
    ):
        user_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=None,
        )

        user_service.policy.can_view = MagicMock()

        with pytest.raises(UserNotFoundException):
            await user_service.get_patient_by_email(
                email="test@test.com",
                current_user=current_admin,
            )

        user_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_patient_by_email_permission_denied(
        self,
        user_service,
        patient_1,
        current_doctor,
    ):
        user_service.uow.users.get_patient_by_email = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException,
        )

        with pytest.raises(ForbiddenException):
            await user_service.get_patient_by_email(
                email=patient_1.email,
                current_user=current_doctor,
            )

    @pytest.mark.asyncio
    async def test_get_patient_by_phone_success(
        self,
        user_service,
        patient_1,
        current_admin,
    ):
        user_service.uow.users.get_patient_by_phone = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_view = MagicMock()

        result = await user_service.get_patient_by_phone(
            phone=patient_1.phone,
            current_user=current_admin,
        )

        assert result == PatientResponseSchema.model_validate(patient_1)

        user_service.uow.users.get_patient_by_phone.assert_awaited_once_with(
            phone=patient_1.phone,
        )

        user_service.policy.can_view.assert_called_once_with(
            current_user=current_admin,
            target_user=patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_patient_by_phone_not_found(
        self,
        user_service,
        current_admin,
    ):
        user_service.uow.users.get_patient_by_phone = AsyncMock(
            return_value=None,
        )

        user_service.policy.can_view = MagicMock()

        with pytest.raises(UserNotFoundException):
            await user_service.get_patient_by_phone(
                phone="+375291111111",
                current_user=current_admin,
            )

        user_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_patient_by_phone_permission_denied(
        self,
        user_service,
        patient_1,
        current_doctor,
    ):
        user_service.uow.users.get_patient_by_phone = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException,
        )

        with pytest.raises(ForbiddenException):
            await user_service.get_patient_by_phone(
                phone=patient_1.phone,
                current_user=current_doctor,
            )

    @pytest.mark.asyncio
    async def test_update_admin_success(
        self,
        user_service,
        admin_1,
        admin_2,
        admin_update_schema,
    ):
        user_service._get_admin = AsyncMock(
            return_value=admin_1,
        )

        user_service._validate_user_contacts = AsyncMock()

        user_service.uow.users.update_admin = AsyncMock(
            return_value=admin_2,
        )

        result = await user_service.update_admin(
            admin_id=admin_1.id,
            data=admin_update_schema,
        )

        assert result == AdminResponseSchema.model_validate(admin_2)

        user_service._get_admin.assert_awaited_once_with(
            admin_id=admin_1.id,
        )

        user_service._validate_user_contacts.assert_awaited_once_with(
            user_id=admin_1.id,
            email=admin_update_schema.email,
            phone=admin_update_schema.phone,
        )

        user_service.uow.users.update_admin.assert_awaited_once_with(
            admin=admin_1,
            data=admin_update_schema,
        )

    @pytest.mark.asyncio
    async def test_update_admin_not_found(
        self,
        user_service,
        admin_update_schema,
    ):
        user_service._get_admin = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service._validate_user_contacts = AsyncMock()
        user_service.uow.users.update_admin = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await user_service.update_admin(
                admin_id=1,
                data=admin_update_schema,
            )

        user_service._validate_user_contacts.assert_not_awaited()
        user_service.uow.users.update_admin.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_admin_contacts_already_exists(
        self,
        user_service,
        admin_1,
        admin_update_schema,
    ):
        user_service._get_admin = AsyncMock(
            return_value=admin_1,
        )

        user_service._validate_user_contacts = AsyncMock(
            side_effect=UserAlreadyExistsException,
        )

        user_service.uow.users.update_admin = AsyncMock()

        with pytest.raises(UserAlreadyExistsException):
            await user_service.update_admin(
                admin_id=admin_1.id,
                data=admin_update_schema,
            )

        user_service.uow.users.update_admin.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_doctor_success(
        self,
        user_service,
        doctor_1,
        doctor_2,
        doctor_update_schema,
        current_admin,
    ):
        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        user_service.policy.can_update = MagicMock()

        user_service._validate_user_contacts = AsyncMock()

        user_service._get_specialization = AsyncMock()

        user_service.uow.users.update_doctor = AsyncMock(
            return_value=doctor_2,
        )

        result = await user_service.update_doctor(
            doctor_id=doctor_1.id,
            data=doctor_update_schema,
            current_user=current_admin,
        )

        assert result == DoctorResponseSchema.model_validate(doctor_2)

        user_service.policy.can_update.assert_called_once_with(
            current_user=current_admin,
            target_user=doctor_1,
        )

        user_service._validate_user_contacts.assert_awaited_once()

        user_service._get_specialization.assert_awaited_once_with(
            specialization_id=doctor_update_schema.specialization_id,
        )

        user_service.uow.users.update_doctor.assert_awaited_once_with(
            doctor=doctor_1,
            data=doctor_update_schema,
        )

    @pytest.mark.asyncio
    async def test_update_doctor_not_found(
        self,
        user_service,
        doctor_update_schema,
        current_admin,
    ):
        user_service._get_doctor = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service.policy.can_update = MagicMock()

        with pytest.raises(UserNotFoundException):
            await user_service.update_doctor(
                doctor_id=1,
                data=doctor_update_schema,
                current_user=current_admin,
            )

        user_service.policy.can_update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_doctor_permission_denied(
        self,
        user_service,
        doctor_1,
        doctor_update_schema,
        current_patient,
    ):
        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        user_service.policy.can_update = MagicMock(
            side_effect=ForbiddenException,
        )
        user_service._validate_user_contacts = AsyncMock()
        with pytest.raises(ForbiddenException):
            await user_service.update_doctor(
                doctor_id=doctor_1.id,
                data=doctor_update_schema,
                current_user=current_patient,
            )

        user_service._validate_user_contacts.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_doctor_contacts_already_exists(
        self,
        user_service,
        doctor_1,
        doctor_update_schema,
        current_admin,
    ):
        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        user_service.policy.can_update = MagicMock()

        user_service._validate_user_contacts = AsyncMock(
            side_effect=UserAlreadyExistsException,
        )
        user_service.uow.users.update_doctor = AsyncMock()

        with pytest.raises(UserAlreadyExistsException):
            await user_service.update_doctor(
                doctor_id=doctor_1.id,
                data=doctor_update_schema,
                current_user=current_admin,
            )

        user_service.uow.users.update_doctor.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_doctor_specialization_not_found(
        self,
        user_service,
        doctor_1,
        doctor_update_schema,
        current_admin,
    ):
        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        user_service.policy.can_update = MagicMock()

        user_service._validate_user_contacts = AsyncMock()

        user_service._get_specialization = AsyncMock(
            side_effect=SpecializationNotFoundException,
        )

        user_service.uow.users.update_doctor = AsyncMock()

        with pytest.raises(SpecializationNotFoundException):
            await user_service.update_doctor(
                doctor_id=doctor_1.id,
                data=doctor_update_schema,
                current_user=current_admin,
            )

        user_service.uow.users.update_doctor.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_patient_success(
        self,
        user_service,
        patient_1,
        patient_2,
        patient_update_schema,
        current_admin,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_update = MagicMock()

        user_service._validate_user_contacts = AsyncMock()

        user_service.uow.users.update_patient = AsyncMock(
            return_value=patient_2,
        )

        result = await user_service.update_patient(
            patient_id=patient_1.id,
            data=patient_update_schema,
            current_user=current_admin,
        )

        assert result == PatientResponseSchema.model_validate(patient_2)

        user_service.policy.can_update.assert_called_once_with(
            current_user=current_admin,
            target_user=patient_1,
        )

        user_service._validate_user_contacts.assert_awaited_once_with(
            user_id=patient_1.id,
            email=patient_update_schema.email,
            phone=patient_update_schema.phone,
        )

        user_service.uow.users.update_patient.assert_awaited_once_with(
            patient=patient_1,
            data=patient_update_schema,
        )

    @pytest.mark.asyncio
    async def test_update_patient_not_found(
        self,
        user_service,
        patient_update_schema,
        current_admin,
    ):
        user_service._get_patient = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service.policy.can_update = MagicMock()

        with pytest.raises(UserNotFoundException):
            await user_service.update_patient(
                patient_id=1,
                data=patient_update_schema,
                current_user=current_admin,
            )

        user_service.policy.can_update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_patient_permission_denied(
        self,
        user_service,
        patient_1,
        patient_update_schema,
        current_doctor,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_update = MagicMock(
            side_effect=ForbiddenException,
        )

        user_service._validate_user_contacts = AsyncMock()

        with pytest.raises(ForbiddenException):
            await user_service.update_patient(
                patient_id=patient_1.id,
                data=patient_update_schema,
                current_user=current_doctor,
            )

        user_service._validate_user_contacts.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_patient_contacts_already_exists(
        self,
        user_service,
        patient_1,
        patient_update_schema,
        current_admin,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service.policy.can_update = MagicMock()

        user_service._validate_user_contacts = AsyncMock(
            side_effect=UserAlreadyExistsException,
        )

        user_service.uow.users.update_patient = AsyncMock()

        with pytest.raises(UserAlreadyExistsException):
            await user_service.update_patient(
                patient_id=patient_1.id,
                data=patient_update_schema,
                current_user=current_admin,
            )

        user_service.uow.users.update_patient.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_deactivate_doctor_success(
        self,
        user_service,
        doctor_1,
        current_admin,
    ):
        doctor_1.is_active = True

        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        user_service._deactivate = AsyncMock(
            return_value=doctor_1,
        )

        result = await user_service.deactivate_doctor(
            doctor_id=doctor_1.id,
        )

        assert result == DoctorResponseSchema.model_validate(doctor_1)

        user_service._get_doctor.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        user_service._deactivate.assert_awaited_once_with(
            user=doctor_1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_doctor_not_found(
        self,
        user_service,
    ):
        user_service._get_doctor = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service._deactivate = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await user_service.deactivate_doctor(
                doctor_id=1,
            )

        user_service._deactivate.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_deactivate_doctor_already_inactive(
        self,
        user_service,
        doctor_1,
    ):
        user_service._get_doctor = AsyncMock(
            return_value=doctor_1,
        )

        user_service._deactivate = AsyncMock(
            side_effect=UserAlreadyInactiveException,
        )

        with pytest.raises(UserAlreadyInactiveException):
            await user_service.deactivate_doctor(
                doctor_id=doctor_1.id,
            )

        user_service._deactivate.assert_awaited_once_with(
            user=doctor_1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_patient_success(
        self,
        user_service,
        patient_1,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service._deactivate = AsyncMock(
            return_value=patient_1,
        )

        result = await user_service.deactivate_patient(
            patient_id=patient_1.id,
        )

        assert result == PatientResponseSchema.model_validate(patient_1)

        user_service._get_patient.assert_awaited_once_with(
            patient_id=patient_1.id,
        )

        user_service._deactivate.assert_awaited_once_with(
            user=patient_1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_patient_not_found(
        self,
        user_service,
    ):
        user_service._get_patient = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service._deactivate = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await user_service.deactivate_patient(
                patient_id=1,
            )

        user_service._deactivate.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_deactivate_patient_already_inactive(
        self,
        user_service,
        patient_1,
    ):
        user_service._get_patient = AsyncMock(
            return_value=patient_1,
        )

        user_service._deactivate = AsyncMock(
            side_effect=UserAlreadyInactiveException,
        )

        with pytest.raises(UserAlreadyInactiveException):
            await user_service.deactivate_patient(
                patient_id=patient_1.id,
            )

        user_service._deactivate.assert_awaited_once_with(
            user=patient_1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_admin_success(
        self,
        user_service,
        admin_1,
    ):
        user_service._get_admin = AsyncMock(
            return_value=admin_1,
        )

        user_service._deactivate = AsyncMock(
            return_value=admin_1,
        )

        result = await user_service.deactivate_admin(
            admin_id=admin_1.id,
        )

        assert result == AdminResponseSchema.model_validate(admin_1)

        user_service._get_admin.assert_awaited_once_with(
            admin_id=admin_1.id,
        )

        user_service._deactivate.assert_awaited_once_with(
            user=admin_1,
        )

    @pytest.mark.asyncio
    async def test_deactivate_admin_not_found(
        self,
        user_service,
    ):
        user_service._get_admin = AsyncMock(
            side_effect=UserNotFoundException,
        )

        user_service._deactivate = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await user_service.deactivate_admin(
                admin_id=1,
            )

        user_service._deactivate.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_deactivate_admin_already_inactive(
        self,
        user_service,
        admin_1,
    ):
        user_service._get_admin = AsyncMock(
            return_value=admin_1,
        )

        user_service._deactivate = AsyncMock(
            side_effect=UserAlreadyInactiveException,
        )

        with pytest.raises(UserAlreadyInactiveException):
            await user_service.deactivate_admin(
                admin_id=admin_1.id,
            )

        user_service._deactivate.assert_awaited_once_with(
            user=admin_1,
        )
