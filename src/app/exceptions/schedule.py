from app.exceptions.base import AppException

class ScheduleNotFoundException(AppException):
    message = 'Schedule not found'

class ScheduleAlreadyExistsException(AppException):
    message = 'Schedule already exists'