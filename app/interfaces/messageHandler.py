from abc import ABC, abstractmethod


class MessageHandler(ABC):
    @abstractmethod
    def send_message(self, message: str):
        pass

    @abstractmethod
    def receive_messages(self):
        pass

