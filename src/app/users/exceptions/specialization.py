from fastapi import status

from common.exceptions.base import AppException


class SpecializationNotFoundException(AppException):
    detail = "Specialization not found"
    status_code = status.HTTP_404_NOT_FOUND


class SpecializationAlreadyExistsException(AppException):
    detail = "Specialization already exists"
    status_code = status.HTTP_409_CONFLICT
