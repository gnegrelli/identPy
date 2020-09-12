from abc import ABC, abstractmethod


class ImplicitMethod(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
