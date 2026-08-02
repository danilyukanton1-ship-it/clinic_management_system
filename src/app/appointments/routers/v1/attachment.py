from typing import Annotated

from fastapi import APIRouter, File, Depends, status, UploadFile

from common.pagination.schemas import PaginationParams, PaginatedResponse
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
from infrastructure.storages.schemas import DownloadUrl

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
    data: Annotated[
        AttachmentCreateSchema,
        Depends(AttachmentCreateSchema.as_form),
    ],
    file: Annotated[UploadFile, File(...)],
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(
        current_user,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    attachment = await attachment_service.create(
        file=file, data=data, current_user=current_user
    )
    return attachment


@router.patch(
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
    check_role(current_user, UserRole.DOCTOR, UserRole.ADMIN)
    return await attachment_service.get_by_id(attachment_id=attachment_id)


@router.get(
    path="/appointments/{appointment_id}",
    response_model=PaginatedResponse[AttachmentResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_by_appointment_id(
    appointment_id: ID,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(current_user, UserRole.DOCTOR, UserRole.ADMIN)
    return await attachment_service.get_by_appointment_id(
        appointment_id=appointment_id,
        pagination=pagination
    )


@router.get(
    path="/patients/{patient_id}",
    response_model=PaginatedResponse[AttachmentResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_by_patient_id(
    patient_id: ID,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(current_user, UserRole.DOCTOR, UserRole.ADMIN)
    return await attachment_service.get_by_patient_id(
        patient_id=patient_id,
        pagination=pagination,
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
        attachment_id=attachment_id, current_user=current_user
    )


@router.get(
    path="/{attachment_id}/download",
    response_model=DownloadUrl,
    status_code=status.HTTP_200_OK,
)
async def get_download_url(
    attachment_id: ID,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    check_role(current_user, UserRole.DOCTOR, UserRole.ADMIN)
    return await attachment_service.get_download_url(attachment_id=attachment_id)
