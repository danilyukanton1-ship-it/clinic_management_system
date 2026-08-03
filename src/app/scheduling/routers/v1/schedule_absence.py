from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.scheduling.dependencies import get_schedule_absence_service
from app.scheduling.schemas.schedule_absence import (
    ScheduleAbsenceCreateSchema,
    ScheduleAbsenceResponseSchema,
    ScheduleAbsenceUpdateSchema,
)
from app.scheduling.services.schedule_absence import ScheduleAbsenceService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    prefix="/absences",
    tags=["Absences"],
)


@router.post(
    path="",
    summary="Create schedule absence",
    description=(
        "Creates a new schedule absence for a doctor.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=ScheduleAbsenceResponseSchema,
)
async def create(
    data: ScheduleAbsenceCreateSchema,
    schedule_absence_service: ScheduleAbsenceService = Depends(
        get_schedule_absence_service
    ),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await schedule_absence_service.create(data=data)


@router.put(
    path="/{absence_id}",
    summary="Update schedule absence",
    description=(
        "Updates an existing schedule absence.\n\nAvailable for:\n- Administrator"
    ),
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScheduleAbsenceResponseSchema,
)
async def update(
    absence_id: ID,
    data: ScheduleAbsenceUpdateSchema,
    schedule_absence_service: ScheduleAbsenceService = Depends(
        get_schedule_absence_service
    ),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await schedule_absence_service.update(absence_id=absence_id, data=data)


@router.delete(
    path="/{absence_id}",
    summary="Delete schedule absence",
    description=("Deletes a schedule absence.\n\nAvailable for:\n- Administrator"),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    absence_id: ID,
    schedule_absence_service: ScheduleAbsenceService = Depends(
        get_schedule_absence_service
    ),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await schedule_absence_service.delete(absence_id=absence_id)


@router.get(
    path="/past/{doctor_id}",
    summary="Get past schedule absences by doctor ID",
    description=(
        "Returns a paginated list of past schedule absences for the specified doctor.\n\n"
        "Available for:\n"
        "- Doctor (only their own schedule absences)\n"
        "- Administrator (any schedule absences)"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ScheduleAbsenceResponseSchema],
)
async def get_past(
    doctor_id: ID,
    pagination: PaginationParams = Depends(),
    schedule_absence_service: ScheduleAbsenceService = Depends(
        get_schedule_absence_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await schedule_absence_service.get_past_by_doctor_id(
        doctor_id=doctor_id, current_user=current_user, pagination=pagination
    )


@router.get(
    path="/future/{doctor_id}",
    summary="Get future schedule absences by doctor ID",
    description=(
        "Returns a paginated list of upcoming schedule absences for the specified doctor.\n\n"
        "Available for:\n"
        "- Doctor (only their own schedule absences)\n"
        "- Administrator (any schedule absences)"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ScheduleAbsenceResponseSchema],
)
async def get_future(
    doctor_id: ID,
    pagination: PaginationParams = Depends(),
    schedule_absence_service: ScheduleAbsenceService = Depends(
        get_schedule_absence_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await schedule_absence_service.get_future_by_doctor_id(
        doctor_id=doctor_id, current_user=current_user, pagination=pagination
    )


@router.get(
    path="/{absence_id}",
    summary="Get schedule absence by ID",
    description=(
        "Returns a schedule absence by its unique identifier.\n\n"
        "Available for:\n"
        "- Doctor (only their own schedule absences)\n"
        "- Administrator (any schedule absences)"
    ),
    status_code=status.HTTP_200_OK,
    response_model=ScheduleAbsenceResponseSchema,
)
async def get_absence(
    absence_id: ID,
    schedule_absence_service: ScheduleAbsenceService = Depends(
        get_schedule_absence_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await schedule_absence_service.get_absence_by_id(
        absence_id=absence_id,
        current_user=current_user,
    )
