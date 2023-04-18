from abc import ABC, abstractmethod

# The base class for all Command subclasses to ensure each subclass has the two main functions
# Inherits from Abstract Base Classes
class CommandBase(ABC):
    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def execute(self):
        pass