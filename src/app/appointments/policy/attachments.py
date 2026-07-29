from app.appointments.models.attachment import Attachment
from app.users.models.user import User

from common.enums.user_role import UserRole
from common.permissions.exceptions import ForbiddenException


class AttachmentPolicy:

    @staticmethod
    def can_delete(user: User, attachment: Attachment):
        if user.role == UserRole.ADMIN:
            return
        if attachment.uploaded_by_id == user.id:
            return
        raise ForbiddenException()

    @staticmethod
    def can_update(user: User, attachment: Attachment):
        if user.role == UserRole.ADMIN:
            return
        if attachment.uploaded_by_id == user.id:
            return
        raise ForbiddenException()
