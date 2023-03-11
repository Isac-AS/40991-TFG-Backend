from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Interface for all the strategies within the different stages of the pipeline.
    """
    
    @abstractmethod
    def execute():
        raise NotImplementedError