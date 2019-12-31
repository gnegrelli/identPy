from Model.model import Model

import numpy as np


class SpringMass(Model):

    def __init__(self, x_0=0, u=0, method=None):

        super().__init__(x_0, u, method)

        self.parameters = {
            'k': 'Stiffness coefficient',
            'm': 'Mass',
        }

        self.inputs = {
            'F': 'External force',
        }

        self.outputs = {
            'x': 'Mass position',
            'v': 'Mass speed',
        }

    def f(self, x=None, u=None):

        if x is None:
            x = self.x_0
        if u is None:
            u = self.u

        assert isinstance(x, np.ndarray), "States vector must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input vector must be given in a numpy array"

        f1 = x[1]
        f2 = -self.p[1]/self.p[0]*x[0] + 1/self.p[0]*u[0]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        if x is None:
            x = self.x_0
        if u is None:
            u = self.u

        assert isinstance(x, np.ndarray), "States vector must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input vector must be given in a numpy array"

        g1 = x[0]
        g2 = x[1]

        return np.array([g1, g2])

    def update_parameters(self, p):
        assert len(p) == len(self.parameters), "Parameter vector must be of length %d" % len(self.parameters)

        super().update_parameters(p)

    def update_output(self):
        pass
