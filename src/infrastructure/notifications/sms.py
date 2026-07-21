
from infrastructure.notifications.base import SMSService

class VonageService(SMSService):

    async def send(
        self,
        phone: str,
        message: str
    ):
        pass