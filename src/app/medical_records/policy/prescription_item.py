from app.appointments.models.appointment import Appointment
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.exceptions import ForbiddenException


class PrescriptionItemPolicy:
    @staticmethod
    def can_delete(user: User, appointment: Appointment):
        if user.role == UserRole.ADMIN:
            return
        if appointment.doctor_id == user.id:
            return
        raise ForbiddenException()

    @staticmethod
    def can_view(user: User, appointment: Appointment):
        if user.role in (UserRole.ADMIN, UserRole.DOCTOR):
            return
        if appointment.patient_id == user.id:
            return
        raise ForbiddenException()

    @staticmethod
    def can_update(user: User, appointment: Appointment):
        if user.role == UserRole.ADMIN:
            return
        if appointment.doctor_id == user.id:
            return
        raise ForbiddenException()
