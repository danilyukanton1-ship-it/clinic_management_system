from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.dependencies import get_session

from app.routers.v1.appointment import router as appointment_router
from app.routers.v1.schedule_slot import router as schedule_slot_router
from app.routers.v1.schedule import router as schedule_router
from app.routers.v1.user import router as user_router

router = APIRouter()

@router.get(
    path="/health",
    tags=["Health"],
)
async def health():
    return {"status": status.HTTP_200_OK}

@router.get(
    path="/health/db",
    tags=["Health"],
)
async def db_health(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"status": result.scalar()}

router.include_router(appointment_router)
router.include_router(schedule_slot_router)
router.include_router(schedule_router)
router.include_router(user_router)