from enum import Enum

class AbsenceReason(str, Enum):
    VACATION = 'vacation'
    SICK_LEAVE = 'sick_leave'
    PERSONAL = 'personal'
    TRAINING = 'training'
    BUSINESS_TRIP = 'business_trip'
