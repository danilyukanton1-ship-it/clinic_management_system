from fastapi import status

from app.exceptions.base import AppException

class SlotNotFoundException(AppException):
    detail = 'Slot not found'
    status_code = status.HTTP_404_NOT_FOUND

class SlotNotAvailableException(AppException):
    detail = 'Slot is not available'
    status_code = status.HTTP_403_FORBIDDEN

class SlotAlreadyBookedException(AppException):
    detail = 'Slot already booked'
    status_code = status.HTTP_403_FORBIDDEN