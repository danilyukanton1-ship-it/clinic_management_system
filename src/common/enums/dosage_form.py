from enum import Enum


class DosageForm(str, Enum):
    TABLET = "tablet"
    CAPSULE = "capsule"
    SYRUP = "syrup"
    INJECTION = "injection"
    OINTMENT = "ointment"
    GEL = "gel"
    DROPS = "drops"
