import pytest
from unittest.mock import MagicMock, AsyncMock

from app.medical_records.exceptions.disease import DiseaseAlreadyExistsException, DiseaseNotFoundException
from app.medical_records.schemas.disease import DiseaseResponseSchema


class TestDiseaseService:

    @pytest.mark.asyncio
    async def test_create_success(
            self,
            disease_service,
            disease_1,
            disease_create_schema,
    ):
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=None
        )
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=None
        )
        disease_service.uow.diseases.create_disease = AsyncMock(
            return_value=disease_1
        )
        result = await disease_service.create(disease_create_schema)
        disease_service.uow.diseases.get_disease_by_code.assert_awaited_once_with(
            disease_code=disease_create_schema.code
        )
        disease_service.uow.diseases.get_disease_by_name.assert_awaited_once_with(
            disease_name=disease_create_schema.name
        )
        disease_service.uow.diseases.create_disease.assert_awaited_once_with(
            data=disease_create_schema
        )
        assert isinstance(result, DiseaseResponseSchema)

    @pytest.mark.asyncio
    async def test_create_disease_code_exists(
            self,
            disease_service,
            disease_1,
            disease_create_schema,
    ):
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=disease_1
        )
        with pytest.raises(DiseaseAlreadyExistsException):
            await disease_service.create(disease_create_schema)
        disease_service.uow.diseases.get_disease_by_name.assert_not_called()
        disease_service.uow.diseases.create_disease.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_disease_name_exists(
            self,
            disease_service,
            disease_1,
            disease_create_schema,
    ):
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=None
        )
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=disease_1
        )
        with pytest.raises(DiseaseAlreadyExistsException):
            await disease_service.create(disease_create_schema)

        disease_service.uow.diseases.create_disease.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_success(
            self,
            disease_service,
            disease_1,
            disease_1_updated,
            disease_update_schema,
    ):
        disease_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1
        )
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=None
        )
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=None
        )
        disease_service.uow.diseases.update_disease = AsyncMock(
            return_value=disease_1_updated
        )
        result = await disease_service.update(
            disease_1.id,
            disease_update_schema,
        )
        disease_service.uow.diseases.update_disease.assert_awaited_once_with(
            disease=disease_1,
            data=disease_update_schema,
        )
        disease_service.uow.diseases.get_disease_by_id.assert_awaited_once_with(
            disease_1.id
        )
        disease_service.uow.diseases.get_disease_by_name.assert_awaited_once_with(
            disease_name=disease_update_schema.name
        )
        disease_service.uow.diseases.get_disease_by_code.assert_awaited_once_with(
            disease_code=disease_update_schema.code
        )
        assert isinstance(result, DiseaseResponseSchema)
        assert result.name == disease_1_updated.name

    @pytest.mark.asyncio
    async def test_update_disease_not_found(
            self,
            disease_service,
            disease_update_schema,
    ):
        disease_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiseaseNotFoundException):
            await disease_service.update(
                1,
                disease_update_schema,
            )
        disease_service.uow.diseases.update_disease.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_disease_name_exists(
            self,
            disease_service,
            disease_1,
            disease_update_schema,
    ):
        disease_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1
        )
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=disease_1
        )
        with pytest.raises(DiseaseAlreadyExistsException):
            await disease_service.update(
                disease_1.id,
                disease_update_schema,
            )
        disease_service.uow.diseases.update_disease.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_disease_code_exists(
            self,
            disease_service,
            disease_1,
            disease_update_schema,
    ):
        disease_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1
        )
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=None
        )
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=disease_1
        )
        with pytest.raises(DiseaseAlreadyExistsException):
            await disease_service.update(
                disease_1.id,
                disease_update_schema,
            )
        disease_service.uow.diseases.update_disease.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_success(
            self,
            disease_service,
            disease_1,
    ):
        disease_service.uow.diseases.get_all_diseases = AsyncMock(
            return_value=[disease_1]
        )
        result = await disease_service.get_all()
        disease_service.uow.diseases.get_all_diseases.assert_awaited_once()
        assert len(result) == 1
        assert isinstance(result[0], DiseaseResponseSchema)
        assert result[0].id == disease_1.id
        assert result[0].code == disease_1.code

    @pytest.mark.asyncio
    async def test_get_all_not_found(
            self,
            disease_service,
    ):
        disease_service.uow.diseases.get_all_diseases = AsyncMock(
            return_value=[]
        )
        with pytest.raises(DiseaseNotFoundException):
            await disease_service.get_all()

    @pytest.mark.asyncio
    async def test_get_by_code_success(
            self,
            disease_service,
            disease_1,
    ):
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=disease_1
        )
        result = await disease_service.get_by_code(
            disease_1.code,
        )
        disease_service.uow.diseases.get_disease_by_code.assert_awaited_once_with(
            disease_code=disease_1.code
        )
        assert isinstance(result, DiseaseResponseSchema)
        assert result.id == disease_1.id
        assert result.code == disease_1.code

    @pytest.mark.asyncio
    async def test_get_by_code_not_found(
            self,
            disease_service,
    ):
        disease_service.uow.diseases.get_disease_by_code = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiseaseNotFoundException):
            await disease_service.get_by_code("A00")

    @pytest.mark.asyncio
    async def test_get_by_name_success(
            self,
            disease_service,
            disease_1,
    ):
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=disease_1
        )
        result = await disease_service.get_by_name(
            disease_1.name,
        )
        disease_service.uow.diseases.get_disease_by_name.assert_awaited_once_with(
            disease_name=disease_1.name
        )
        assert isinstance(result, DiseaseResponseSchema)
        assert result.id == disease_1.id
        assert result.code == disease_1.code

    @pytest.mark.asyncio
    async def test_get_by_name_not_found(
            self,
            disease_service,
    ):
        disease_service.uow.diseases.get_disease_by_name = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiseaseNotFoundException):
            await disease_service.get_by_name("Test")

    @pytest.mark.asyncio
    async def test_delete_success(
            self,
            disease_service,
            disease_1,
    ):
        disease_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1
        )
        disease_service.uow.diseases.delete_disease = AsyncMock()
        result = await disease_service.delete(
            disease_1.id,
        )
        disease_service.uow.diseases.get_disease_by_id.assert_awaited_once_with(
            disease_id=disease_1.id
        )
        disease_service.uow.diseases.delete_disease.assert_awaited_once_with(
            disease=disease_1
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_not_found(
            self,
            disease_service,
    ):
        disease_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiseaseNotFoundException):
            await disease_service.delete(1)
        disease_service.uow.diseases.delete_disease.assert_not_called()