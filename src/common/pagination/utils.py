import math
from common.pagination.schemas import PaginatedResponse, PaginationParams

def build_paginated_response(
    *,
    items,
    total,
    pagination: PaginationParams,
    schema
):
    return PaginatedResponse(
        items=[
            schema.model_validate(item) for item in items
        ],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=math.ceil(total / pagination.page_size)
    )