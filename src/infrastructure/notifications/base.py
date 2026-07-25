from abc import ABC, abstractmethod

class EmailService(ABC):


    @abstractmethod
    async def send(self, email_receiver: str, subject: str, body: str) -> None:
        pass