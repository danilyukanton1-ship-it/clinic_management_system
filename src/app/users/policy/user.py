from app.users.models.user import User

from common.enums.user_role import UserRole
from common.permissions.exceptions import ForbiddenException


class UserPolicy:

    @staticmethod
    def can_update(current_user: User, target_user: User):
        if current_user.role == UserRole.ADMIN:
            return
        if current_user.id == target_user.id:
            return
        raise ForbiddenException()

    @staticmethod
    def can_view(current_user: User, target_user: User):
        if current_user.role in (UserRole.ADMIN, UserRole.DOCTOR):
            return
        if current_user.id == target_user.id:
            return
        raise ForbiddenException()
