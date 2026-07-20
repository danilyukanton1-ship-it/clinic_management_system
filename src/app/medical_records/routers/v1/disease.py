from fastapi import APIRouter, Depends, status
from app.medical_records.dependencies import get_disease_service
from app.medical_records.services.disease import DiseaseService
from app.medical_records.schemas.disease import DiseaseResponseSchema, DiseaseCreateSchema, DiseaseUpdateSchema
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(
    tags=["Diseases"],
    prefix='/disease',
)

@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[DiseaseResponseSchema]
)
async def get_all(
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR
    )
    return await disease_service.get_all()

@router.get(
    path="/{disease_code}",
    status_code=status.HTTP_200_OK,
    response_model=DiseaseResponseSchema
)
async def get_by_code(
    disease_code: str,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR
    )
    return await disease_service.get_by_code(disease_code=disease_code)

@router.get(
    path="/{name}",
    status_code=status.HTTP_200_OK,
    response_model=DiseaseResponseSchema
)
async def get_by_name(
    disease_name: str,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR
    )
    return await disease_service.get_by_name(name=disease_name)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DiseaseResponseSchema
)
async def create(
    data: DiseaseCreateSchema,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN
    )
    return await disease_service.create(data=data)

@router.put(
    path="/{disease_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=DiseaseResponseSchema
)
async def update(
    disease_id: int,
    data: DiseaseUpdateSchema,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN
    )
    return await disease_service.update(disease_id=disease_id, data=data)

@router.delete(
    path="/{disease_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    disease_id: int,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN
    )
    return await disease_service.delete(disease_id=disease_id)
