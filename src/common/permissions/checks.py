from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.exceptions import ForbiddenException


def check_role(
    user: User,
    *roles: UserRole,
):
    if user.role not in roles:
        raise ForbiddenException()

