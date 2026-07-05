from fastapi import status
from common.exceptions.base import AppException

class DiagnosisNotFoundException(AppException):
    detail = 'Diagnosis not found'
    status_code = status.HTTP_404_NOT_FOUND

class DiagnosisCantBeEmptyInPrescriptionException(AppException):
    detail = 'Diagnosis cannot be empty in prescription'
    status_code = status.HTTP_400_BAD_REQUEST