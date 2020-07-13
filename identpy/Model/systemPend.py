import numpy as np

from identpy.Model import Model


class Pendulum(Model):

    name = 'Simple Pendulum Model'

    parameters = {
        'b': 'Air friction',
        'l': 'Wire length',
        'g': 'Gravity acceleration',
        'm': 'Mass',
    }

    inputs = {
        'F': 'External force',
    }

    outputs = {
        'θ': 'Angle from vertical',
        'ω': 'Angular velocity',
    }

    states = {
        'θ': 'Angle from vertical',
        'ω': 'Angular velocity',
    }

    def __init__(self, x_0=0, u_0=0, u=0, method=None):

        super().__init__(x_0, u_0, u, method)

    def f(self, x=None, u=None, factor=0):

        x, u = super().f(x, u)

        f1 = x[1]
        f2 = -self.p[2]*np.cos(self.x_0[0])/self.p[1]*x[0] - self.p[0]/self.p[3] * x[1] + 1/(self.p[1]*self.p[3])*u[1]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        g1 = x[0]
        g2 = x[1]

        return np.array([g1, g2])
