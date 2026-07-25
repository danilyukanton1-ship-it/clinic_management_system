import resend
import asyncio
from infrastructure.notifications.base import EmailService

from core.config import settings

class SMTPEmailService(EmailService):

    def __init__(self) -> None:
        resend.api_key = settings.smtp.API_KEY
        self._from = settings.smtp.FROM


    async def send(
            self,
            email_receiver: str,
            subject: str,
            body: str,
            html: str | None = None,
    ) -> None:
        payload = {
            'from': self._from,
            'to': [email_receiver],
            'subject': subject,
            'text': body,
        }

        if html:
            payload['html'] = html
        try:
            resend.Emails.send(payload)
        except Exception as e:
            raise e
