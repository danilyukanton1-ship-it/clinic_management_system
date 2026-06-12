from fastapi import FastAPI
from core.router import router

from app.handlers import register_exception_handlers
app = FastAPI()

register_exception_handlers(app)
app.include_router(router)