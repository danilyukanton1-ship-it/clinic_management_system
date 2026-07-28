from fastapi import status
from common.exceptions.base import AppException


class DrugAlreadyExistsException(AppException):
    detail = "Drug already exists"
    status_code = status.HTTP_409_CONFLICT


class DrugNotFoundException(AppException):
    detail = "Drug not found"
    status_code = status.HTTP_404_NOT_FOUND
