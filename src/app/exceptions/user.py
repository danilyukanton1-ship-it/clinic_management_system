from app.exceptions.base import AppException

class UserAlreadyExistsException(AppException):
    message = "User already exists"

class UserIsNotPatientException(AppException):
    message = "User is not a patient"