from abc import ABC, abstractmethod

class SMSService(ABC):

    @abstractmethod
    async def send(
        self,
        phone: str,
        message: str,
        html: str | None = None,
    ) -> None:
        pass

class EmailService(ABC):


    @abstractmethod
    async def send(self, email_receiver: str, subject: str, body: str) -> None:
        pass