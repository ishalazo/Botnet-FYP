from abc import ABC, abstractmethod

class CommandBase(ABC):
    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def execute(self):
        pass

