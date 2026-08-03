from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.scheduling.dependencies import get_schedule_service
from app.scheduling.schemas.schedule import (
    ScheduleCreateSchema,
    ScheduleResponseSchema,
    ScheduleUpdateSchema,
)
from app.scheduling.services.schedule import ScheduleService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.enums.weekday import Weekday
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(prefix="/schedule", tags=["Schedules"])


@router.get(
    path="/all/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ScheduleResponseSchema],
)
async def get_all_by_doctor_id(
    doctor_id: ID,
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    return await schedule_service.get_all_schedule_by_doctor_id(doctor_id=doctor_id)


@router.get(
    path="/admin/all/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ScheduleResponseSchema],
)
async def get_all_by_doctor_id_for_admin(
    doctor_id: ID,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await schedule_service.get_all_schedule_by_doctor_id(
        doctor_id=doctor_id, admin=True
    )


@router.get(
    path="/{doctor_id}/{weekday}",
    status_code=status.HTTP_200_OK,
    response_model=ScheduleResponseSchema,
)
async def get_by_doctor_id_and_weekday(
    doctor_id: ID,
    weekday: Weekday,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
) -> ScheduleResponseSchema:
    schedule = await schedule_service.get_schedule_by_doctor_id_and_weekday(
        doctor_id=doctor_id,
        weekday=weekday,
    )
    return schedule


@router.get(
    path="/admin/{doctor_id}/{weekday}",
    status_code=status.HTTP_200_OK,
    response_model=list[ScheduleResponseSchema],
)
async def get_by_doctor_id_and_weekday_for_admin(
    doctor_id: ID,
    weekday: Weekday,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    schedules = await schedule_service.get_schedule_by_doctor_id_and_weekday_for_admin(
        doctor_id=doctor_id,
        weekday=weekday,
    )
    return schedules


@router.get(
    path="/id/{schedule_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScheduleResponseSchema,
)
async def get_by_schedule_id(
    schedule_id: ID,
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    return await schedule_service.get_schedule_by_id(schedule_id=schedule_id)


@router.get(
    path="/admin/id/{schedule_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScheduleResponseSchema,
)
async def get_by_schedule_id_for_admin(
    schedule_id: ID,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await schedule_service.get_schedule_by_id(
        schedule_id=schedule_id, admin=True
    )


@router.post(
    path="", status_code=status.HTTP_201_CREATED, response_model=ScheduleResponseSchema
)
async def create(
    schedule: ScheduleCreateSchema,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await schedule_service.create(schedule)


@router.put(
    path="/{doctor_id}/{weekday}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScheduleResponseSchema,
)
async def update(
    data: ScheduleUpdateSchema,
    doctor_id: ID,
    weekday: Weekday,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await schedule_service.update(
        doctor_id=doctor_id, data=data, weekday=weekday
    )


@router.patch(
    path="/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate(
    schedule_id: ID,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await schedule_service.deactivate_schedule(schedule_id=schedule_id)
