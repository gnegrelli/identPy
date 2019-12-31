from abc import ABC


class IMethod(ABC):

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
