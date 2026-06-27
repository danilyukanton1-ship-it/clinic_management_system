from fastapi import APIRouter, Depends, status

from app.auth.schemas.register import RegisterSchema
from app.auth.services.register import RegisterService
from app.auth.services.token import TokenService
from app.users.models.user import User
from app.users.schemas.user import UserResponseSchema, PatientResponseSchema
from app.auth.dependencies import get_login_service, get_current_user, get_token_service, get_register_service
from app.auth.schemas.login import LoginSchema
from app.auth.schemas.token import TokenResponseSchema, AccessTokenSchema, RefreshTokenSchema
from app.auth.services.login import LoginService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    response_model=PatientResponseSchema,
)
async def register(
    data: RegisterSchema,
    service: RegisterService = Depends(get_register_service),
) -> PatientResponseSchema:
    return await service.register(data)

@router.post(
    path="/login",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginSchema,
    service: LoginService = Depends(get_login_service),
):
    return await service.login(data)

@router.get(
    path='/me',
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: User = Depends(get_current_user),
) -> UserResponseSchema:
    return current_user


@router.post(
    path='/refresh',
    response_model=AccessTokenSchema,
    status_code=status.HTTP_201_CREATED,
)
async def refresh(
    refresh_token: RefreshTokenSchema,
    token_service: TokenService = Depends(get_token_service),
):
    return await token_service.get_access_token(refresh_token.refresh_token)

@router.post(
    path='/logout',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    refresh_token: RefreshTokenSchema,
    token_service: TokenService = Depends(get_token_service),
):
    return await token_service.blacklist_token(refresh_token.refresh_token)


