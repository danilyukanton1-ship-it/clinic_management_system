from fastapi import status
from common.exceptions.base import AppException

class PrescriptionNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Prescription not found'