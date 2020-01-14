from abc import ABC
from Model.Implicit_Methods.i_method import IMethod as IM

import numpy as np


class Model(ABC):

    def __init__(self, x_0=0, u=0, method=None):

        assert isinstance(x_0, np.ndarray), "Initial states must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input must be given in a numpy array"

        assert isinstance(method, IM), "Method must be of class IM"

        self.parameters = dict()
        self.inputs = dict()
        self.outputs = dict()

        self.p = 0

        self.x_0 = x_0
        self.u = u
        self.y = 0

        self.method = method

    def f(self, x=None, u=None):

        if x is None:
            x = self.x_0
        if u is None:
            u = self.u

        assert isinstance(x, np.ndarray), "States vector must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input vector must be given in a numpy array"

        return x, u

    def g(self, x=None, u=None):

        if x is None:
            x = self.x_0
        if u is None:
            u = self.u

        assert isinstance(x, np.ndarray), "States vector must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input vector must be given in a numpy array"

        return x, u

    def update_parameters(self, p):
        assert isinstance(p, np.ndarray), "Parameters must be given in a numpy array"
        assert len(p) == len(self.parameters), "Parameter vector must be of length %d" % len(self.parameters)

        self.p = p

    def update_output(self, p=None):
        if p is not None:
            self.update_parameters(p)
        
        self.method(self)

    def save_output(self, filename='example.csv'):

        assert isinstance(self.y, np.ndarray), "Output must be a numpy array in order to save"

        np.savetxt('Sample_Data/' + filename, self.y, delimiter=',')
