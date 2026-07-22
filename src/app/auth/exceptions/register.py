from fastapi import status

from common.exceptions.base import AppException

class EmailAlreadyExistsException(AppException):
    detail = "Email already exists"
    status_code = status.HTTP_400_BAD_REQUEST

class PhoneAlreadyExistsException(AppException):
    detail = "Phone already exists"
    status_code = status.HTTP_400_BAD_REQUEST

class UserAlreadyVerifiedException(AppException):
    detail = "User already verified"
    status_code = status.HTTP_400_BAD_REQUEST

class VerificationCodeNotFoundException(AppException):
    detail = "Verification code does not exist"
    status_code = status.HTTP_400_BAD_REQUEST

class IncorrectVerificationCodeException(AppException):
    detail = "Verification code is incorrect"
    status_code = status.HTTP_400_BAD_REQUEST

class UserNotVerifiedException(AppException):
    detail = "User not verified"
    status_code = status.HTTP_400_BAD_REQUEST

class TooManyLoginAttemptsException(AppException):
    detail = "Too many login attempts"
    status_code = status.HTTP_400_BAD_REQUEST