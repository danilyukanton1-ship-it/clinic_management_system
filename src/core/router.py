from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.dependencies import get_session

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": status.HTTP_200_OK}

@router.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"status": result.scalar()}

