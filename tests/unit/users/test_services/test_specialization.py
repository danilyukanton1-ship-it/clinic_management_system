from unittest.mock import AsyncMock

import pytest

from app.users.exceptions.specialization import (
    SpecializationAlreadyExistsException,
    SpecializationNotFoundException,
)
from app.users.schemas.specialization import SpecializationResponseSchema
from common.pagination.schemas import PaginationResult


class TestSpecializationService:

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        specialization_service,
        specialization,
    ):
        specialization.id = 1

        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=specialization,
        )

        result = await specialization_service.get_by_id(
            specialization_id=specialization.id,
        )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=specialization.id,
        )

        assert result == SpecializationResponseSchema.model_validate(
            specialization,
        )

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        specialization_service,
    ):
        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(
            SpecializationNotFoundException,
        ):
            await specialization_service.get_by_id(
                specialization_id=1,
            )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_by_name_success(
        self,
        specialization_service,
        specialization,
    ):
        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock(
                return_value=specialization,
            )
        )

        result = await specialization_service.get_by_name(
            specialization_name=specialization.name,
        )

        specialization_service.uow.specializations.get_specialization_by_name.assert_awaited_once_with(
            specialization_name=specialization.name,
        )

        assert result == SpecializationResponseSchema.model_validate(
            specialization,
        )

    @pytest.mark.asyncio
    async def test_get_by_name_not_found(
        self,
        specialization_service,
    ):
        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock(
                return_value=None,
            )
        )

        with pytest.raises(
            SpecializationNotFoundException,
        ):
            await specialization_service.get_by_name(
                specialization_name="test specialization",
            )

        specialization_service.uow.specializations.get_specialization_by_name.assert_awaited_once_with(
            specialization_name="test specialization",
        )

    @pytest.mark.asyncio
    async def test_get_all_success(
        self,
        specialization_service,
        specialization,
        specialization_updated,
        pagination,
    ):
        specialization_service.uow.specializations.get_all_specializations = AsyncMock(
            return_value=PaginationResult(
                items=[
                    specialization,
                    specialization_updated,
                ],
                total=2,
            )
        )
        result = await specialization_service.get_all(
            pagination=pagination,
        )
        specialization_service.uow.specializations.get_all_specializations.assert_awaited_once_with(
            pagination=pagination,
        )
        assert result.total == 2
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1
        assert result.items == [
            SpecializationResponseSchema.model_validate(
                specialization,
            ),
            SpecializationResponseSchema.model_validate(
                specialization_updated,
            ),
        ]

    @pytest.mark.asyncio
    async def test_get_all_empty(
        self,
        specialization_service,
        pagination,
    ):
        specialization_service.uow.specializations.get_all_specializations = AsyncMock(
            return_value=PaginationResult(
                items=[],
                total=0,
            )
        )
        result = await specialization_service.get_all(
            pagination=pagination,
        )
        specialization_service.uow.specializations.get_all_specializations.assert_awaited_once_with(
            pagination=pagination,
        )
        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert (
            result.pages == 0
        )  # либо 1, если build_paginated_response использует max(1, ...)
        assert result.items == []

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        specialization_service,
        specialization,
        specialization_create_schema,
    ):
        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock(
                return_value=None,
            )
        )

        specialization_service.uow.specializations.create_specialization = AsyncMock(
            return_value=specialization,
        )

        result = await specialization_service.create(
            data=specialization_create_schema,
        )

        specialization_service.uow.specializations.get_specialization_by_name.assert_awaited_once_with(
            specialization_name=specialization_create_schema.name,
        )

        specialization_service.uow.specializations.create_specialization.assert_awaited_once_with(
            data=specialization_create_schema,
        )

        assert result == SpecializationResponseSchema.model_validate(
            specialization,
        )

    @pytest.mark.asyncio
    async def test_create_already_exists(
        self,
        specialization_service,
        specialization,
        specialization_create_schema,
    ):
        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock(
                return_value=specialization,
            )
        )

        specialization_service.uow.specializations.create_specialization = AsyncMock()

        with pytest.raises(
            SpecializationAlreadyExistsException,
        ):
            await specialization_service.create(
                data=specialization_create_schema,
            )

        specialization_service.uow.specializations.get_specialization_by_name.assert_awaited_once_with(
            specialization_name=specialization_create_schema.name,
        )

        specialization_service.uow.specializations.create_specialization.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        specialization_service,
        specialization,
    ):
        specialization.id = 1

        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=specialization,
        )

        specialization_service.uow.specializations.delete_specialization = AsyncMock()

        result = await specialization_service.delete(
            specialization_id=specialization.id,
        )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=specialization.id,
        )

        specialization_service.uow.specializations.delete_specialization.assert_awaited_once_with(
            specialization=specialization,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self,
        specialization_service,
    ):
        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=None,
        )

        specialization_service.uow.specializations.delete_specialization = AsyncMock()

        with pytest.raises(
            SpecializationNotFoundException,
        ):
            await specialization_service.delete(
                specialization_id=1,
            )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=1,
        )

        specialization_service.uow.specializations.delete_specialization.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        specialization_service,
        specialization,
        specialization_updated,
        specialization_update_schema,
    ):
        specialization.id = 1

        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=specialization,
        )

        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock(
                return_value=None,
            )
        )

        specialization_service.uow.specializations.update_specialization = AsyncMock(
            return_value=specialization_updated,
        )

        result = await specialization_service.update(
            specialization_id=specialization.id,
            data=specialization_update_schema,
        )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=specialization.id,
        )

        specialization_service.uow.specializations.get_specialization_by_name.assert_awaited_once_with(
            specialization_name=specialization_update_schema.name,
        )

        specialization_service.uow.specializations.update_specialization.assert_awaited_once_with(
            specialization=specialization,
            data=specialization_update_schema,
        )

        assert result == SpecializationResponseSchema.model_validate(
            specialization_updated,
        )

    @pytest.mark.asyncio
    async def test_update_not_found(
        self,
        specialization_service,
        specialization_update_schema,
    ):
        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=None,
        )

        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock()
        )

        specialization_service.uow.specializations.update_specialization = AsyncMock()

        with pytest.raises(
            SpecializationNotFoundException,
        ):
            await specialization_service.update(
                specialization_id=1,
                data=specialization_update_schema,
            )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=1,
        )

        specialization_service.uow.specializations.get_specialization_by_name.assert_not_awaited()

        specialization_service.uow.specializations.update_specialization.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_already_exists(
        self,
        specialization_service,
        specialization,
        specialization_update_schema,
    ):
        specialization.id = 1

        specialization_service.uow.specializations.get_specialization_by_id = AsyncMock(
            return_value=specialization,
        )

        specialization_service.uow.specializations.get_specialization_by_name = (
            AsyncMock(
                return_value=specialization,
            )
        )

        specialization_service.uow.specializations.update_specialization = AsyncMock()

        with pytest.raises(
            SpecializationAlreadyExistsException,
        ):
            await specialization_service.update(
                specialization_id=specialization.id,
                data=specialization_update_schema,
            )

        specialization_service.uow.specializations.get_specialization_by_id.assert_awaited_once_with(
            specialization_id=specialization.id,
        )

        specialization_service.uow.specializations.get_specialization_by_name.assert_awaited_once_with(
            specialization_name=specialization_update_schema.name,
        )

        specialization_service.uow.specializations.update_specialization.assert_not_awaited()
