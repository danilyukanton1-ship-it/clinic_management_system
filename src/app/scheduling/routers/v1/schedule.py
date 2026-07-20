from fastapi import APIRouter, Depends, status

from app.scheduling.dependencies import get_schedule_service

from app.scheduling.services.schedule import ScheduleService
from app.scheduling.schemas.schedule import ScheduleResponseSchema, ScheduleCreateSchema, ScheduleUpdateSchema
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

from common.enums.weekday import Weekday

router = APIRouter(prefix="/schedule", tags=["Schedules"])

@router.get(
    path='/{doctor_id}/{weekday}',
    status_code=status.HTTP_200_OK,
    response_model=ScheduleResponseSchema
)
async def get_by_doctor_id_and_weekday(
        doctor_id: int,
        weekday: Weekday,
        schedule_service: ScheduleService = Depends(get_schedule_service),
        current_user: User = Depends(get_current_user),
) -> ScheduleResponseSchema:
    schedule = await schedule_service.get_schedule_by_doctor_id_and_weekday(
        doctor_id=doctor_id,
        weekday=weekday,
        current_user=current_user
    )
    return schedule

@router.get(
    path="/all/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ScheduleResponseSchema]
)
async def get_all_by_doctor_id(
    doctor_id: int,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    return await schedule_service.get_all_schedule_by_doctor_id(
        doctor_id=doctor_id,
        current_user=current_user
    )


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ScheduleResponseSchema
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
    path='/{doctor_id}/{weekday}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScheduleResponseSchema
)
async def update(
    data: ScheduleUpdateSchema,
    doctor_id: int,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await schedule_service.update(doctor_id=doctor_id, data=data)

@router.delete(
    path="/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    schedule_id: int,
    schedule_service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await schedule_service.delete(schedule_id=schedule_id)
    
