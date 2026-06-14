from app.exceptions.base import AppException

class SpecializationNotFoundException(AppException):
    message = "Specialization not found"