from fastapi import FastAPI
from fastapi.responses import JSONResponse

from common.exceptions.base import AppException


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
