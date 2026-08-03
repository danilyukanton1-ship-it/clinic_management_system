from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.medical_records.dependencies import get_diagnosis_service
from app.medical_records.schemas.diagnosis import (
    DiagnosisCreateSchema,
    DiagnosisResponseSchema,
    DiagnosisUpdateSchema,
)
from app.medical_records.services.diagnosis import DiagnosisService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    prefix="/diagnoses",
    tags=["Diagnoses"],
)


@router.get(
    path="/id/{diagnosis_id}",
    status_code=status.HTTP_200_OK,
    response_model=DiagnosisResponseSchema,
)
async def get_by_id(
    diagnosis_id: ID,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
    current_user: User = Depends(get_current_user),
):
    return await diagnosis_service.get_by_id(
        diagnosis_id=diagnosis_id, current_user=current_user
    )


@router.get(
    path="/prescription/{prescription_id}",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[DiagnosisResponseSchema],
)
async def get_by_prescription_id(
    prescription_id: ID,
    pagination: PaginationParams = Depends(),
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
    current_user: User = Depends(get_current_user),
):
    return await diagnosis_service.get_by_prescription_id(
        prescription_id=prescription_id,
        current_user=current_user,
        pagination=pagination,
    )


@router.get(
    path="/disease/{disease_id}",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[DiagnosisResponseSchema],
)
async def get_by_disease_id(
    disease_id: ID,
    pagination: PaginationParams = Depends(),
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    return await diagnosis_service.get_by_disease_id(
        disease_id=disease_id, pagination=pagination
    )


@router.put(
    path="/{diagnosis_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DiagnosisResponseSchema,
)
async def update(
    diagnosis_id: ID,
    data: DiagnosisUpdateSchema,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
    current_user: User = Depends(get_current_user),
):
    return await diagnosis_service.update(
        diagnosis_id=diagnosis_id, data=data, current_user=current_user
    )


@router.delete(
    path="/{diagnosis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    diagnosis_id: ID,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
    current_user: User = Depends(get_current_user),
):
    return await diagnosis_service.delete(
        diagnosis_id=diagnosis_id, current_user=current_user
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=DiagnosisResponseSchema,
)
async def create(
    data: DiagnosisCreateSchema,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.DOCTOR,
    )
    return await diagnosis_service.create(data=data)
