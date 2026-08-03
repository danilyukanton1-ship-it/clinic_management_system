from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.scheduling.dependencies import get_schedule_slot_service
from app.scheduling.schemas.schedule_slot import (
    ScheduleSlotBulkCreateSchema,
    ScheduleSlotResponseSchema,
    ScheduleSlotUpdateSchema,
)
from app.scheduling.services.schedule_slot import ScheduleSlotService
from app.users.models.user import User
from common.enums.slot_status import SlotStatus
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(prefix="/schedule-slots", tags=["Schedule slots"])


@router.get(
    path="/future/{doctor_id}/{slot_status}",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ScheduleSlotResponseSchema],
)
async def get_future_slots_by_doctor_id_status(
    doctor_id: ID,
    slot_status: SlotStatus,
    pagination: PaginationParams = Depends(),
    schedule_slot_service: ScheduleSlotService = Depends(get_schedule_slot_service),
):
    slots = await schedule_slot_service.get_future_slots_by_doctor_id_status(
        doctor_id=doctor_id,
        status=slot_status,
        pagination=pagination,
    )
    return slots


@router.get(
    path="/past/{doctor_id}/{slot_status}",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ScheduleSlotResponseSchema],
)
async def get_past_slots_by_doctor_id_status(
    doctor_id: ID,
    slot_status: SlotStatus,
    pagination: PaginationParams = Depends(),
    schedule_slot_service: ScheduleSlotService = Depends(get_schedule_slot_service),
):
    slots = await schedule_slot_service.get_past_slots_by_doctor_id_status(
        doctor_id=doctor_id, status=slot_status, pagination=pagination
    )
    return slots


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=list[ScheduleSlotResponseSchema],
)
async def create_schedule_slots(
    data: ScheduleSlotBulkCreateSchema,
    schedule_slot_service: ScheduleSlotService = Depends(get_schedule_slot_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    slots = await schedule_slot_service.create_slots(data=data)
    return slots


@router.put(
    path="/{slot_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScheduleSlotResponseSchema,
)
async def update_slot(
    slot_id: ID,
    data: ScheduleSlotUpdateSchema,
    slot_schedule_service: ScheduleSlotService = Depends(get_schedule_slot_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    slot = await slot_schedule_service.update(slot_id=slot_id, data=data)
    return slot


@router.patch(
    path="/{slot_id}/{slot_status}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScheduleSlotResponseSchema,
)
async def change_slot_status(
    slot_id: ID,
    slot_status: SlotStatus,
    slot_schedule_service: ScheduleSlotService = Depends(get_schedule_slot_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN, UserRole.PATIENT)
    slot = await slot_schedule_service.change_slot_status(
        slot_id=slot_id,
        status=slot_status,
    )
    return slot
