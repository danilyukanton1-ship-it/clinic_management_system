from fastapi import status

from app.exceptions.base import AppException

class AppointmentNotFound(AppException):
    detail = 'Appointment not found'
    status_code = status.HTTP_404_NOT_FOUND
