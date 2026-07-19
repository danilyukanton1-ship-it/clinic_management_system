from fastapi import APIRouter, Depends, status

from app.appoinments.dependencies import get_attachment_service


from app.appoinments.schemas.attachment import AttachmentUpdateSchema, AttachmentCreateSchema, AttachmentResponseSchema
from app.appoinments.services.attachment import AttachmentService
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"],
)

@router.post(
    path="/",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: AttachmentCreateSchema,
    current_user: User = Depends(get_current_user),
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    attachment = await attachment_service.create(
        data=data,
        uploaded_by_id=current_user.id
    )
    return attachment

@router.put(
    path="/{attachment_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(
    attachment_id: int,
    data: AttachmentUpdateSchema,
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    attachment = await attachment_service.update(
        data=data,
        attachment_id=attachment_id
    )
    return attachment

@router.get(
    path="/{attachment_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    attachment_id: int,
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    return await attachment_service.get_by_id(attachment_id)

@router.get(
    path="/appointment/{appointment_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_appointment_id(
    appointment_id: int,
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    return await attachment_service.get_by_appointment_id(appointment_id)

@router.get(
    path="/patient/{patient_id}",
    response_model=AttachmentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_patient_id(
    patient_id: int,
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    return await attachment_service.get_by_patient_id(patient_id)