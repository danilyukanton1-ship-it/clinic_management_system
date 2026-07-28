from fastapi import FastAPI
from core.router import router

from common.exceptions.handlers import register_exception_handlers
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from core.limiter import limiter

app = FastAPI(title="Clinic Management System")

app.include_router(router)

register_exception_handlers(app)

app.include_router(router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
