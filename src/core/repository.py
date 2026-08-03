from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination.schemas import PaginationParams, PaginationResult, T


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(
        self, stmt: Select, pagination: PaginationParams
    ) -> PaginationResult[T]:
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt)
        result = await self.session.execute(
            stmt.offset(pagination.offset).limit(pagination.page_size)
        )
        return PaginationResult(
            items=list(result.scalars().all()),
            total=total or 0,
        )
