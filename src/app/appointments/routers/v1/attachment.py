from fastapi import APIRouter, Depends, status
from common.types import ID
from app.appointments.dependencies import get_attachment_service
from common.permissions.checks import check_role
from common.enums.user_role import UserRole

from app.appointments.schemas.attachment import (
    AttachmentUpdateSchema,
    AttachmentCreateSchema,
    AttachmentResponseSchema,
)
from app.appointments.services.attachment import AttachmentService
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"],
)


@router.post(
    path="",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: AttachmentCreateSchema,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(
        current_user,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    attachment = await attachment_service.create(data=data, current_user=current_user)
    return attachment


@router.put(
    path="/{attachment_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(
    attachment_id: ID,
    data: AttachmentUpdateSchema,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(
        current_user,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    attachment = await attachment_service.update(
        data=data, attachment_id=attachment_id, current_user=current_user
    )
    return attachment


@router.get(
    path="/{attachment_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    attachment_id: ID,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    return await attachment_service.get_by_id(
        attachment_id=attachment_id,
        current_user=current_user,
    )


@router.get(
    path="/appointment/{appointment_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_appointment_id(
    appointment_id: ID,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    return await attachment_service.get_by_appointment_id(
        appointment_id=appointment_id,
        current_user=current_user,
    )


@router.get(
    path="/patient/{patient_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_patient_id(
    patient_id: ID,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    return await attachment_service.get_by_patient_id(
        patient_id=patient_id,
        current_user=current_user,
    )


@router.delete(
    path="/{attachment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    attachment_id: ID,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(
        current_user,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    return await attachment_service.delete(
        attachment_id=attachment_id,
        current_user=current_user
    )
