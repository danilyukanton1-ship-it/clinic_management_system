from fastapi import FastAPI
from core.router import router

from common.exceptions.handlers import register_exception_handlers
app = FastAPI(title='Clinic Management System')
app.include_router(router)
register_exception_handlers(app)

register_exception_handlers(app)
app.include_router(router)