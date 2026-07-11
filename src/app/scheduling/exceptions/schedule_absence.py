from fastapi import status

from common.exceptions.base import AppException

class AbsenceAlreadyScheduledException(AppException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Already scheduled for these dates"

class AbsenceNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Absence not found"