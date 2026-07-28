from fastapi import status

from common.exceptions.base import AppException


class AttachmentDoesNotExistException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Attachment does not exist"
