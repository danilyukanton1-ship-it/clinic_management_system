from enum import Enum

class SlotStatus(str, Enum):
    FREE = 'free'
    BOOKED = 'booked'
    BLOCKED = 'blocked'