from infrastructure.notifications.base import EmailService

from email.message import EmailMessage

import aiosmtplib

from core.config import settings

class SMTPEmailService(EmailService):

    def __init__(self) -> None:
        self._host = settings.smtp.HOST
        self._port = settings.smtp.PORT
        self._username = settings.smtp.USERNAME
        self._password = settings.smtp.PASSWORD
        self._from = settings.smtp.FROM
        self._use_ssl = settings.smtp.USE_SSL
        self._use_tls = settings.smtp.USE_TLS

    async def send(
            self,
            email_receiver: str,
            subject: str,
            body: str,
            html: str | None = None,
    ) -> None:
        message = EmailMessage()
        message["From"] = self._from
        message["To"] = email_receiver
        message["Subject"] = subject

        message.set_content(body)

        if html:
            message.add_alternative(html, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=self._host,
            port=self._port,
            username=self._username or None,
            password=self._password or None,
            start_tls=self._use_tls,
            use_tls=self._use_ssl
        )

