from fastapi import status

from app.exceptions.base import AppException

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