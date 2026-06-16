from fastapi import APIRouter, Depends, status

from app.dependencies import get_schedule_service

from app.servicies.schedule import ScheduleService
from app.schemas.schedule import ScheduleResponseSchema, ScheduleCreateSchema, ScheduleUpdateSchema

from app.exceptions.schedule import (
    ScheduleNotFoundException,
    ScheduleAlreadyExistsException,
)

router = APIRouter()

@router.get(
    path='/schedule/{doctor_id}',
    tags=['Schedule'],
    status_code=status.HTTP_200_OK,
    response_model=list[ScheduleResponseSchema]
)
async def get_schedule(
        doctor_id: int,
        schedule_service: ScheduleService = Depends(get_schedule_service)
) -> list[ScheduleResponseSchema]:
    if not await schedule_service.if_exists(doctor_id=doctor_id):
        raise ScheduleNotFoundException()
    schedule = await schedule_service.get_schedule_by_doctor_id(doctor_id)
    return schedule

@router.post(
    path='/schedule',
    tags=['Schedule'],
    status_code=status.HTTP_201_CREATED,
    response_model=ScheduleResponseSchema
)
async def create_schedule(
    schedule: ScheduleCreateSchema,
    schedule_service: ScheduleService = Depends(get_schedule_service)
):
    if await schedule_service.if_exists(doctor_id=schedule.doctor_id):
        raise ScheduleAlreadyExistsException()
    schedule = await schedule_service.create_schedule(schedule)
    return schedule

@router.put(
    path='/schedule/{doctor_id}/{weekday}',
    tags=['Schedule'],
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScheduleResponseSchema
)
async def update_schedule(
        schedule: ScheduleUpdateSchema,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    if not await schedule_service.if_exists(doctor_id=schedule.doctor_id):
        raise ScheduleNotFoundException()
    schedule = await schedule_service.update_schedule(schedule)
    return schedule
