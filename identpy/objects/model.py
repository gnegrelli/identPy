from abc import ABC

import numpy as np

from .implicit_method import ImplicitMethod as IM


class Model(ABC):

    name = 'Model'

    parameters = {}
    inputs = {}
    outputs = {}
    states = {}

    def __init__(self, x_0=0, u_0=0, u=0, method=None):

        assert isinstance(x_0, np.ndarray), "Initial states must be given in a numpy array"
        assert isinstance(u_0, np.ndarray), "Initial input must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input must be given in a numpy array"

        assert isinstance(method, IM), "Method must be of class IM"

        self.p = np.array([])

        self.x_0 = x_0
        self.u_0 = u_0
        self.u = u
        self.y = np.array([])

        self.method = method

    def __str__(self, title=True):
        string = 'Parameters: \n' if title else ''
        for name, value in list(zip(self.parameters.keys(), self.p)):
            if title:
                string += '\t'
            string += '{}: {:.4f}\n'.format(name, value)
        return string

    def f(self, x=None, u=None, factor=0):

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

        self.initial_conditions()

    def update_output(self, p=None):
        if p is not None:
            self.update_parameters(p)
        
        self.method(self)

    def save_output(self, filename='example.csv'):

        assert isinstance(self.y, np.ndarray), "Output must be a numpy array in order to save"

        np.savetxt('Sample_Data/' + filename, self.y, delimiter=',')

    def initial_conditions(self):
        pass
