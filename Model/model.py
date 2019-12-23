from abc import ABC


class Model(ABC):

    def __init__(self):
        self.param = dict()

    def f(self):
        pass

    def g(self):
        pass

    def update_parameters(self):
        pass

    def update_output(self):
        pass
