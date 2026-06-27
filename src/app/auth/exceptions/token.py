from starlette import status

from common.exceptions.base import AppException

class InvalidTokenTypeException(AppException):
    detail = "Invalid token type"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpiredException(AppException):
    detail = "Token expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenException(AppException):
    detail = "Invalid token"
    status_code = status.HTTP_401_UNAUTHORIZED