from abc import ABC

import numpy as np


class Model(ABC):

    def __init__(self):
        self.param = dict()
        self.p = 0
        self.u = 0
        self.x_0 = 0
        self.output = 0

    def f(self):
        pass

    def g(self):
        pass

    def update_parameters(self, p):
        assert isinstance(p, np.ndarray), "Parameters must be given in a numpy array"

        self.p = p

    def update_output(self):
        pass
