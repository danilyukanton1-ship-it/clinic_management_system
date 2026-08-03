from unittest.mock import AsyncMock

import pytest

from app.medical_records.exceptions.drug import (
    DrugAlreadyExistsException,
    DrugNotFoundException,
)
from app.medical_records.schemas.drug import DrugResponseSchema
from common.pagination.schemas import PaginationResult


class TestDrugService:

    @pytest.mark.asyncio
    async def test_create_drug_success(
        self,
        drug_service,
        drug_1,
        drug_create_schema,
    ):
        drug_service.uow.drugs.get_drug_by_name = AsyncMock(return_value=None)
        drug_service.uow.drugs.create_drug = AsyncMock(return_value=drug_1)
        result = await drug_service.create(drug_create_schema)
        drug_service.uow.drugs.get_drug_by_name.assert_awaited_once_with(
            drug_name=drug_create_schema.name
        )
        drug_service.uow.drugs.create_drug.assert_awaited_once_with(
            data=drug_create_schema
        )
        assert isinstance(result, DrugResponseSchema)

    @pytest.mark.asyncio
    async def test_create_drug_exists(
        self,
        drug_service,
        drug_1,
        drug_create_schema,
    ):
        drug_service.uow.drugs.get_drug_by_name = AsyncMock(return_value=drug_1)
        with pytest.raises(DrugAlreadyExistsException):
            await drug_service.create(drug_create_schema)
        drug_service.uow.drugs.create_drug.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        drug_service,
        drug_1,
        drug_1_updated,
        drug_update_schema,
    ):
        drug_service.uow.drugs.get_drug_by_id = AsyncMock(return_value=drug_1)
        drug_service.uow.drugs.get_drug_by_name = AsyncMock(return_value=None)
        drug_service.uow.drugs.update_drug = AsyncMock(return_value=drug_1_updated)
        result = await drug_service.update(
            drug_1.id,
            drug_update_schema,
        )
        drug_service.uow.drugs.get_drug_by_id.assert_awaited_once_with(
            drug_id=drug_1.id
        )
        drug_service.uow.drugs.get_drug_by_name.assert_awaited_once_with(
            drug_name=drug_update_schema.name
        )
        drug_service.uow.drugs.update_drug.assert_awaited_once_with(
            drug=drug_1,
            data=drug_update_schema,
        )
        assert result.id == drug_1_updated.id
        assert result.name == drug_1_updated.name
        assert result.international_name == drug_1_updated.international_name

    @pytest.mark.asyncio
    async def test_update_drug_not_found(
        self,
        drug_service,
        drug_update_schema,
    ):
        drug_service.uow.drugs.get_drug_by_id = AsyncMock(return_value=None)
        with pytest.raises(DrugNotFoundException):
            await drug_service.update(
                1,
                drug_update_schema,
            )
        drug_service.uow.drugs.update_drug.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_drug_exists(
        self,
        drug_service,
        drug_1,
        drug_update_schema,
    ):
        drug_service.uow.drugs.get_drug_by_id = AsyncMock(return_value=drug_1)
        drug_service.uow.drugs.get_drug_by_name = AsyncMock(return_value=drug_1)
        with pytest.raises(DrugAlreadyExistsException):
            await drug_service.update(
                drug_1.id,
                drug_update_schema,
            )
        drug_service.uow.drugs.update_drug.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_success(
        self,
        drug_service,
        drug_1,
        pagination,
    ):
        drug_service.uow.drugs.get_all_drugs = AsyncMock(
            return_value=PaginationResult(
                items=[drug_1],
                total=1,
            )
        )

        result = await drug_service.get_all(
            pagination=pagination,
        )

        drug_service.uow.drugs.get_all_drugs.assert_awaited_once_with(
            pagination=pagination,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert isinstance(result.items[0], DrugResponseSchema)
        assert result.items[0].id == drug_1.id
        assert result.items[0].name == drug_1.name

    @pytest.mark.asyncio
    async def test_get_all_not_found(
        self,
        drug_service,
        pagination,
    ):
        drug_service.uow.drugs.get_all_drugs = AsyncMock(
            return_value=PaginationResult(
                items=[],
                total=0,
            )
        )

        result = await drug_service.get_all(
            pagination=pagination,
        )

        drug_service.uow.drugs.get_all_drugs.assert_awaited_once_with(
            pagination=pagination,
        )

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 0
        assert result.items == []

    @pytest.mark.asyncio
    async def test_get_by_name_success(
        self,
        drug_service,
        drug_1,
    ):
        drug_service.uow.drugs.get_drug_by_name = AsyncMock(return_value=drug_1)
        result = await drug_service.get_by_name(
            drug_1.name,
        )
        drug_service.uow.drugs.get_drug_by_name.assert_awaited_once_with(
            drug_name=drug_1.name
        )
        assert isinstance(result, DrugResponseSchema)
        assert result.id == drug_1.id
        assert result.name == drug_1.name

    @pytest.mark.asyncio
    async def test_get_by_name_not_found(
        self,
        drug_service,
    ):
        drug_service.uow.drugs.get_drug_by_name = AsyncMock(return_value=None)
        with pytest.raises(DrugNotFoundException):
            await drug_service.get_by_name("Paracetamol")

    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        drug_service,
        drug_1,
    ):
        drug_service.uow.drugs.get_drug_by_id = AsyncMock(return_value=drug_1)
        drug_service.uow.drugs.delete_drug = AsyncMock()
        result = await drug_service.delete(
            drug_1.id,
        )
        drug_service.uow.drugs.get_drug_by_id.assert_awaited_once_with(
            drug_id=drug_1.id
        )
        drug_service.uow.drugs.delete_drug.assert_awaited_once_with(drug=drug_1)

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self,
        drug_service,
    ):
        drug_service.uow.drugs.get_drug_by_id = AsyncMock(return_value=None)
        with pytest.raises(DrugNotFoundException):
            await drug_service.delete(1)

        drug_service.uow.drugs.delete_drug.assert_not_called()
