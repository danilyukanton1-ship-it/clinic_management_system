from fastapi import APIRouter, Depends, status
from app.medical_records.dependencies import get_drug_service
from app.medical_records.services.drug import DrugService
from app.medical_records.schemas.drug import DrugUpdateSchema, DrugCreateSchema, DrugResponseSchema
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(
    prefix="/drugs",
    tags=["Drugs"],
)

@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[DrugResponseSchema]
)
async def get_drugs(
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR,
    )
    return await drug_service.get_all()

@router.get(
    path="/name",
    status_code=status.HTTP_200_OK,
    response_model=DrugResponseSchema
)
async def get_by_name(
    drug_name: str,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR,
    )
    return await drug_service.get_by_name(name=drug_name)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DrugResponseSchema
)
async def create(
    data: DrugCreateSchema,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await drug_service.create(data=data)

@router.put(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DrugResponseSchema
)
async def update(
    drug_id: int,
    data: DrugUpdateSchema,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await drug_service.update(drug_id=drug_id, data=data)

@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    drug_id: int,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await drug_service.delete(drug_id=drug_id)

