from abc import ABC


class Method(ABC):

    def __init__(self):
        self.counter = 0
        self.error_log = []

    def __call__(self, *args, **kwargs):
        pass
