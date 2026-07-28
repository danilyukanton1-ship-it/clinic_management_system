from fastapi import status
from common.exceptions.base import AppException


class PrescriptionItemNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Prescription item not found"
