from abc import ABC, abstractmethod

class CommandBase(ABC):
    @abstractmethod
    def get_metrics(self):
        pass

    @abstractmethod
    def execute(self):
        pass