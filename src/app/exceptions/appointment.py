from app.exceptions.base import AppException

class AppointmentNotFound(AppException):
    message = 'Appointment not found'
