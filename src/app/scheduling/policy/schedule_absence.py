from app.scheduling.models.schedule_absence import ScheduleAbsence
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.exceptions import ForbiddenException


class ScheduleAbsencePolicy:
    @staticmethod
    def can_view(user: User, schedule_absence: ScheduleAbsence):
        if user.role == UserRole.ADMIN:
            return
        if schedule_absence.doctor_id == user.id:
            return
        raise ForbiddenException()
