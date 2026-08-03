from fastapi import APIRouter, Depends, Request, status

from app.auth.dependencies import (
    get_current_user,
    get_login_service,
    get_register_service,
    get_token_service,
)
from app.auth.schemas.login import LoginSchema
from app.auth.schemas.me import MeSchema
from app.auth.schemas.register import (
    ForgotPasswordSchema,
    RegisterSchema,
    ResetPasswordSchema,
    VerifyEmailSchema,
)
from app.auth.schemas.token import (
    AccessTokenSchema,
    RefreshTokenSchema,
    TokenResponseSchema,
)
from app.auth.services.login import LoginService
from app.auth.services.register import RegisterService
from app.auth.services.token import TokenService
from app.users.models.user import User
from app.users.schemas.user import PatientResponseSchema, UserResponseSchema
from common.types import Email
from core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/register",
    summary="Register patient",
    description=(
        "Registers a new patient account and sends an email verification code.\n\n"
        "Available for unauthenticated users."
    ),
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
    summary="Verify email",
    description=(
        "Verifies a user's email address using the verification code sent during registration.\n\n"
        "Available for unauthenticated users."
    ),
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
    summary="Resend email verification code",
    description=(
        "Sends a new email verification code to the specified email address.\n\n"
        "Available for unauthenticated users."
    ),
    status_code=status.HTTP_200_OK,
)
@limiter.limit("3/minute")
async def resend_email_verification_code(
    email: Email,
    request: Request,
    service: RegisterService = Depends(get_register_service),
) -> dict:
    await service.resend_verification_email(email=email)
    return {"detail": "Email verification sent."}


@router.post(
    path="/forgot-password",
    summary="Request password reset",
    description=(
        "Sends a password reset code to the user's email address.\n\n"
        "Available for unauthenticated users."
    ),
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
    summary="Reset password",
    description=(
        "Resets the user's password using the password reset code.\n\n"
        "Available for unauthenticated users."
    ),
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
    summary="Authenticate user",
    description=(
        "Authenticates a user and returns a pair of JWT access and refresh tokens.\n\n"
        "Available for unauthenticated users."
    ),
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
    summary="Get current user",
    description=("Returns information about the currently authenticated user."),
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: User = Depends(get_current_user),
) -> MeSchema:
    return UserResponseSchema.model_validate(current_user)


@router.post(
    path="/refresh",
    summary="Refresh access token",
    description=("Generates a new access token using a valid refresh token."),
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
    summary="Log out",
    description=(
        "Invalidates the provided refresh token by adding it to the token blacklist."
    ),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    refresh_token: RefreshTokenSchema,
    token_service: TokenService = Depends(get_token_service),
) -> None:
    return await token_service.blacklist_token(refresh_token.refresh_token)
