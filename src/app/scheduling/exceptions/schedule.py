from fastapi import status

from common.exceptions.base import AppException

class ScheduleNotFoundException(AppException):
    detail = 'Schedule not found'
    status_code = status.HTTP_404_NOT_FOUND

class ScheduleAlreadyExistsException(AppException):
    detail = 'Schedule already exists'
    status_code = status.HTTP_409_CONFLICT