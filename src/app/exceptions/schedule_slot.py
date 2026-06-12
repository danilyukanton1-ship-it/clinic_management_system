from app.exceptions.base import AppException

class SlotNotFound(AppException):
    message = 'Slot not found'

class SlotNotAvailable(AppException):
    message = 'Slot is not available'

class SlotAlreadyBooked(AppException):
    message = 'Slot already booked'