from abc import abstractmethod


class Command:
    @abstractmethod
    def __init__(self,body_json):
        None
    @abstractmethod
    def execute(self):
        None
