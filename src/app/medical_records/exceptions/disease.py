from fastapi import status
from common.exceptions.base import AppException

class DiseaseNotFoundException(AppException):
    detail = 'Disease Not Found'
    status_code = status.HTTP_404_NOT_FOUND