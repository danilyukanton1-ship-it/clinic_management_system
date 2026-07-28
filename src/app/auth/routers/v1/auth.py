from fastapi import APIRouter, Depends, status, Request

from app.auth.schemas.me import MeSchema
from app.auth.schemas.register import (
    RegisterSchema,
    VerifyEmailSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)
from app.auth.services.register import RegisterService
from app.auth.services.token import TokenService
from app.users.models.user import User
from app.users.schemas.user import UserResponseSchema, PatientResponseSchema
from app.auth.dependencies import (
    get_login_service,
    get_current_user,
    get_token_service,
    get_register_service,
)
from app.auth.schemas.login import LoginSchema
from app.auth.schemas.token import (
    TokenResponseSchema,
    AccessTokenSchema,
    RefreshTokenSchema,
)
from app.auth.services.login import LoginService
from core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=PatientResponseSchema,
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    data: RegisterSchema,
    service: RegisterService = Depends(get_register_service),
) -> PatientResponseSchema:
    return await service.register(data)


@router.post(
    path="/email-verify",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
@limiter.limit("10/minute")
async def verify_email(
    request: Request,
    data: VerifyEmailSchema,
    service: RegisterService = Depends(get_register_service),
) -> PatientResponseSchema:
    return await service.verify_email(data=data)


@router.post(
    path="/email-verify/resend",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("3/minute")
async def resend_email_verification_code(
    email: str,
    request: Request,
    service: RegisterService = Depends(get_register_service),
) -> dict:
    await service.resend_verification_email(email=email)
    return {"detail": "Email verification sent."}


@router.post(
    path="/forgot-password",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
async def forgot_password(
    request: Request,
    data: ForgotPasswordSchema,
    service: RegisterService = Depends(get_register_service),
) -> None:
    return await service.forgot_password(data=data)


@router.post(
    path="/reset-password",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    data: ResetPasswordSchema,
    service: RegisterService = Depends(get_register_service),
) -> PatientResponseSchema:
    return await service.reset_password(data=data)


@router.post(
    path="/login",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: LoginSchema,
    service: LoginService = Depends(get_login_service),
) -> TokenResponseSchema:
    return await service.login(data)


@router.get(
    path="/me",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: User = Depends(get_current_user),
) -> MeSchema:
    return UserResponseSchema.model_validate(current_user)


@router.post(
    path="/refresh",
    response_model=AccessTokenSchema,
    status_code=status.HTTP_201_CREATED,
)
async def refresh(
    refresh_token: RefreshTokenSchema,
    token_service: TokenService = Depends(get_token_service),
) -> AccessTokenSchema:
    return await token_service.get_access_token(refresh_token.refresh_token)


@router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    refresh_token: RefreshTokenSchema,
    token_service: TokenService = Depends(get_token_service),
) -> None:
    return await token_service.blacklist_token(refresh_token.refresh_token)
