from app.exceptions.base import AppException

class SlotNotFoundException(AppException):
    message = 'Slot not found'

class SlotNotAvailableException(AppException):
    message = 'Slot is not available'

class SlotAlreadyBookedException(AppException):
    message = 'Slot already booked'