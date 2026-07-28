from fastapi import status

from common.exceptions.base import AppException


class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not allowed to perform this action"
