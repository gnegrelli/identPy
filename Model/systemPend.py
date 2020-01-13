from Model.model import Model

import numpy as np


class Pendulum(Model):

    def __init__(self, x_0=0, u=0, method=None):

        super().__init__(x_0, u, method)

        self.parameters = {
            'b': 'Air friction',
            'l': 'Wire length',
            'g': 'Gravity acceleration',
            'm': 'Mass',
        }

        self.inputs = {
            'F': 'External force',
        }

        self.outputs = {
            'θ': 'Angle from vertical',
            'ω': 'Angular velocity',
        }

    def f(self, x=None, u=None):

        super().f(x, u)

        f1 = x[1]
        f2 = -self.p[2]*np.cos(self.x_0[0])/self.p[1]*x[0] - self.p[0]/self.p[3] * x[1] + 1/(self.p[1]*self.p[3])*u[0]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        super().g(x, u)

        g1 = x[0]
        g2 = x[1]

        return np.array([g1, g2])
