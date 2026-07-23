from fastapi import status

from common.exceptions.base import AppException

class AppointmentNotFoundException(AppException):
    detail = 'Appointment not found'
    status_code = status.HTTP_404_NOT_FOUND

class AppointmentRelatesToDifferentPatientException(AppException):
    detail = 'Appointment relates to different patient'
    status_code = status.HTTP_400_BAD_REQUEST
