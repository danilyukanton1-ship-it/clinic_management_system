from fastapi import status

from common.exceptions.base import AppException

class EmailAlreadyExistsException(AppException):
    detail = "Email already exists"
    status_code = status.HTTP_400_BAD_REQUEST

class PhoneAlreadyExistsException(AppException):
    detail = "Phone already exists"
    status_code = status.HTTP_400_BAD_REQUEST