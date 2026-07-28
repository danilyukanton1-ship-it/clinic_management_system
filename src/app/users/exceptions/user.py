from fastapi import status

from common.exceptions.base import AppException


class UserAlreadyExistsException(AppException):
    detail = "User already exists"
    status_code = status.HTTP_400_BAD_REQUEST


class UserIsNotPatientException(AppException):
    detail = "User is not a patient"
    status_code = status.HTTP_400_BAD_REQUEST


class UserIsNotDoctorException(AppException):
    detail = "User is not a doctor"
    status_code = status.HTTP_400_BAD_REQUEST


class UserNotFoundException(AppException):
    detail = "User not found"
    status_code = status.HTTP_404_NOT_FOUND


class UserInactiveException(AppException):
    detail = "User is inactive"
    status_code = status.HTTP_400_BAD_REQUEST


class UserAlreadyInactiveException(AppException):
    detail = "User is already inactive"
    status_code = status.HTTP_400_BAD_REQUEST


class AdminCanNotHaveSpecializationException(AppException):
    detail = "Admin can not have specialization"
    status_code = status.HTTP_400_BAD_REQUEST
