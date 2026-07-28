from fastapi import status

from common.exceptions.base import AppException


class InvalidCredentialsException(AppException):
    detail = "Invalid credentials"
    status_code = status.HTTP_401_UNAUTHORIZED
