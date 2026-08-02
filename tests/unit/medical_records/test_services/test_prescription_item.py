import pytest

from unittest.mock import MagicMock, AsyncMock

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.drug import DrugNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.exceptions.prescription_items import (
    PrescriptionItemNotFoundException,
)
from app.medical_records.schemas.prescription_item import PrescriptionItemResponseSchema
from common.permissions.exceptions import ForbiddenException
from common.pagination.schemas import PaginationResult


class TestPrescriptionItemService:

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_success(
        self,
        prescription_item_service,
        prescription_item_1,
        appointment_patient_1,
        current_doctor,
        pagination,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[prescription_item_1],
                total=1,
            )
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1,
        )

        prescription_item_service.policy.can_view = MagicMock()

        result = await prescription_item_service.get_by_prescription_id(
            prescription_id=prescription_item_1.prescription_id,
            current_user=current_doctor,
            pagination=pagination,
        )

        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=prescription_item_1.prescription_id,
            pagination=pagination,
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )

        prescription_item_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert isinstance(result.items[0], PrescriptionItemResponseSchema)
        assert result.items[0].id == prescription_item_1.id
        assert result.items[0].prescription_id == prescription_item_1.prescription_id
        assert result.items[0].drug_id == prescription_item_1.drug_id
        assert result.items[0].dosage == prescription_item_1.dosage
        assert result.items[0].frequency == prescription_item_1.frequency
        assert result.items[0].duration_days == prescription_item_1.duration_days

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_prescription_item_not_found(
        self,
        prescription_item_service,
        current_doctor,
        pagination,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[],
                total=0,
            )
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = (
            AsyncMock()
        )

        prescription_item_service.policy.can_view = MagicMock()

        result = await prescription_item_service.get_by_prescription_id(
            prescription_id=1,
            current_user=current_doctor,
            pagination=pagination,
        )

        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=1,
            pagination=pagination,
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_not_called()
        prescription_item_service.policy.can_view.assert_not_called()

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert (
            result.pages == 0
        )  # либо 1, если build_paginated_response использует max(1, ...)
        assert result.items == []

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_appointment_not_found(
        self,
        prescription_item_service,
        prescription_item_1,
        current_doctor,
        pagination,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[prescription_item_1],
                total=1,
            )
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=None,
        )

        prescription_item_service.policy.can_view = MagicMock()

        with pytest.raises(AppointmentNotFoundException):
            await prescription_item_service.get_by_prescription_id(
                prescription_id=prescription_item_1.prescription_id,
                current_user=current_doctor,
                pagination=pagination,
            )

        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=prescription_item_1.prescription_id,
            pagination=pagination,
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )

        prescription_item_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_forbidden(
        self,
        prescription_item_service,
        prescription_item_1,
        appointment_patient_1,
        current_doctor,
        pagination,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[prescription_item_1],
                total=1,
            )
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1,
        )

        prescription_item_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )

        with pytest.raises(ForbiddenException):
            await prescription_item_service.get_by_prescription_id(
                prescription_id=prescription_item_1.prescription_id,
                current_user=current_doctor,
                pagination=pagination,
            )

        prescription_item_service.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=prescription_item_1.prescription_id,
            pagination=pagination,
        )

        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )

        prescription_item_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        prescription_item_service,
        prescription_item_1,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1
        )
        prescription_item_service.policy.can_view = MagicMock()

        result = await prescription_item_service.get_by_id(
            prescription_item_id=prescription_item_1.id,
            current_user=current_doctor,
        )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        assert result.id == prescription_item_1.id
        assert result.prescription_id == prescription_item_1.prescription_id
        assert result.drug_id == prescription_item_1.drug_id
        assert result.dosage == prescription_item_1.dosage
        assert result.frequency == prescription_item_1.frequency
        assert result.duration_days == prescription_item_1.duration_days

    @pytest.mark.asyncio
    async def test_get_by_id_prescription_item_not_found(
        self,
        prescription_item_service,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=None)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = (
            AsyncMock()
        )
        prescription_item_service.policy.can_view = MagicMock()
        with pytest.raises(PrescriptionItemNotFoundException):
            await prescription_item_service.get_by_id(
                prescription_item_id=1,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=1,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_not_awaited()
        prescription_item_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_appointment_not_found(
        self,
        prescription_item_service,
        prescription_item_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=None
        )
        prescription_item_service.policy.can_view = MagicMock()
        with pytest.raises(AppointmentNotFoundException):
            await prescription_item_service.get_by_id(
                prescription_item_id=prescription_item_1.id,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_forbidden(
        self,
        prescription_item_service,
        prescription_item_1,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1
        )
        prescription_item_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await prescription_item_service.get_by_id(
                prescription_item_id=prescription_item_1.id,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        prescription_item_service,
        prescription_item_1,
        prescription_item_1_updated,
        prescription_item_update_schema,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1
        )
        prescription_item_service.uow.prescription_items.update_prescription_item = (
            AsyncMock(return_value=prescription_item_1_updated)
        )
        prescription_item_service.policy.can_update = MagicMock()
        result = await prescription_item_service.update(
            prescription_item_id=prescription_item_1.id,
            data=prescription_item_update_schema,
            current_user=current_doctor,
        )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_update.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        prescription_item_service.uow.prescription_items.update_prescription_item.assert_awaited_once_with(
            prescription_item=prescription_item_1,
            data=prescription_item_update_schema,
        )
        assert result.id == prescription_item_1_updated.id
        assert result.prescription_id == prescription_item_1_updated.prescription_id
        assert result.drug_id == prescription_item_1_updated.drug_id
        assert result.dosage == prescription_item_1_updated.dosage
        assert result.frequency == prescription_item_1_updated.frequency
        assert result.duration_days == prescription_item_1_updated.duration_days

    @pytest.mark.asyncio
    async def test_update_prescription_item_not_found(
        self,
        prescription_item_service,
        prescription_item_update_schema,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=None)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = (
            AsyncMock()
        )
        prescription_item_service.uow.prescription_items.update_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_update = MagicMock()
        with pytest.raises(PrescriptionItemNotFoundException):
            await prescription_item_service.update(
                prescription_item_id=1,
                data=prescription_item_update_schema,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=1,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_not_awaited()
        prescription_item_service.policy.can_update.assert_not_called()
        prescription_item_service.uow.prescription_items.update_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_appointment_not_found(
        self,
        prescription_item_service,
        prescription_item_1,
        prescription_item_update_schema,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=None
        )
        prescription_item_service.uow.prescription_items.update_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_update = MagicMock()
        with pytest.raises(AppointmentNotFoundException):
            await prescription_item_service.update(
                prescription_item_id=prescription_item_1.id,
                data=prescription_item_update_schema,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_update.assert_not_called()
        prescription_item_service.uow.prescription_items.update_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_forbidden(
        self,
        prescription_item_service,
        prescription_item_1,
        prescription_item_update_schema,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1
        )
        prescription_item_service.uow.prescription_items.update_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_update = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await prescription_item_service.update(
                prescription_item_id=prescription_item_1.id,
                data=prescription_item_update_schema,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_update.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        prescription_item_service.uow.prescription_items.update_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        prescription_item_service,
        prescription_item_1,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1
        )
        prescription_item_service.uow.prescription_items.delete_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_delete = MagicMock()
        result = await prescription_item_service.delete(
            prescription_item_id=prescription_item_1.id,
            current_user=current_doctor,
        )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_delete.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        prescription_item_service.uow.prescription_items.delete_prescription_item.assert_awaited_once_with(
            prescription_item=prescription_item_1,
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_prescription_item_not_found(
        self,
        prescription_item_service,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=None)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = (
            AsyncMock()
        )
        prescription_item_service.uow.prescription_items.delete_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_delete = MagicMock()
        with pytest.raises(PrescriptionItemNotFoundException):
            await prescription_item_service.delete(
                prescription_item_id=1,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=1,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_not_awaited()
        prescription_item_service.policy.can_delete.assert_not_called()
        prescription_item_service.uow.prescription_items.delete_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_appointment_not_found(
        self,
        prescription_item_service,
        prescription_item_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=None
        )
        prescription_item_service.uow.prescription_items.delete_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_delete = MagicMock()
        with pytest.raises(AppointmentNotFoundException):
            await prescription_item_service.delete(
                prescription_item_id=prescription_item_1.id,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_delete.assert_not_called()
        prescription_item_service.uow.prescription_items.delete_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self,
        prescription_item_service,
        prescription_item_1,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id = (
            AsyncMock(return_value=prescription_item_1)
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id = AsyncMock(
            return_value=appointment_patient_1
        )
        prescription_item_service.uow.prescription_items.delete_prescription_item = (
            AsyncMock()
        )
        prescription_item_service.policy.can_delete = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await prescription_item_service.delete(
                prescription_item_id=prescription_item_1.id,
                current_user=current_doctor,
            )
        prescription_item_service.uow.prescription_items.get_prescription_item_by_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.uow.appointments.get_appointment_by_prescription_item_id.assert_awaited_once_with(
            prescription_item_id=prescription_item_1.id,
        )
        prescription_item_service.policy.can_delete.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        prescription_item_service.uow.prescription_items.delete_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        prescription_item_service,
        prescription,
        drug_1,
        prescription_item_create_schema,
        prescription_item_1,
    ):
        prescription_item_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        prescription_item_service.uow.drugs.get_drug_by_id = AsyncMock(
            return_value=drug_1
        )
        prescription_item_service.uow.prescription_items.create_prescription_item = (
            AsyncMock(return_value=prescription_item_1)
        )
        result = await prescription_item_service.create(
            data=prescription_item_create_schema,
        )
        prescription_item_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription_item_create_schema.prescription_id,
        )
        prescription_item_service.uow.drugs.get_drug_by_id.assert_awaited_once_with(
            drug_id=prescription_item_create_schema.drug_id,
        )
        prescription_item_service.uow.prescription_items.create_prescription_item.assert_awaited_once_with(
            data=prescription_item_create_schema,
        )
        assert result.id == prescription_item_1.id
        assert result.prescription_id == prescription_item_1.prescription_id
        assert result.drug_id == prescription_item_1.drug_id
        assert result.dosage == prescription_item_1.dosage
        assert result.frequency == prescription_item_1.frequency
        assert result.duration_days == prescription_item_1.duration_days

    @pytest.mark.asyncio
    async def test_create_prescription_not_found(
        self,
        prescription_item_service,
        prescription_item_create_schema,
    ):
        prescription_item_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=None
        )
        prescription_item_service.uow.drugs.get_drug_by_id = AsyncMock()
        prescription_item_service.uow.prescription_items.create_prescription_item = (
            AsyncMock()
        )
        with pytest.raises(PrescriptionNotFoundException):
            await prescription_item_service.create(
                data=prescription_item_create_schema,
            )
        prescription_item_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription_item_create_schema.prescription_id,
        )
        prescription_item_service.uow.drugs.get_drug_by_id.assert_not_awaited()
        prescription_item_service.uow.prescription_items.create_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_drug_not_found(
        self,
        prescription_item_service,
        prescription,
        prescription_item_create_schema,
    ):
        prescription_item_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        prescription_item_service.uow.drugs.get_drug_by_id = AsyncMock(
            return_value=None
        )
        prescription_item_service.uow.prescription_items.create_prescription_item = (
            AsyncMock()
        )
        with pytest.raises(DrugNotFoundException):
            await prescription_item_service.create(
                data=prescription_item_create_schema,
            )
        prescription_item_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription_item_create_schema.prescription_id,
        )
        prescription_item_service.uow.drugs.get_drug_by_id.assert_awaited_once_with(
            drug_id=prescription_item_create_schema.drug_id,
        )
        prescription_item_service.uow.prescription_items.create_prescription_item.assert_not_awaited()
