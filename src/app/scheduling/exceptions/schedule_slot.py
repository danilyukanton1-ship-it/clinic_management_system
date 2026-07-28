from fastapi import status

from common.exceptions.base import AppException

class SlotNotFoundException(AppException):
    detail = 'Slot not found'
    status_code = status.HTTP_404_NOT_FOUND

class SlotNotAvailableException(AppException):
    detail = 'Slot is not available'
    status_code = status.HTTP_403_FORBIDDEN

class SlotAlreadyBookedException(AppException):
    detail = 'Slot already booked'
    status_code = status.HTTP_403_FORBIDDEN

class SlotStatusCanNotBeChangedException(AppException):
    detail = 'Slot status can\'t be changed'
    status_code = status.HTTP_403_FORBIDDEN

class SlotCanNotBeChangedException(AppException):
    detail = 'Slot can not be changed'
    status_code = status.HTTP_403_FORBIDDEN

class SlotCanNotBeCreatedException(AppException):
    detail = 'Slot can not be created'
    status_code = status.HTTP_400_BAD_REQUEST
