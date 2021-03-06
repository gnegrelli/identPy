import numpy as np

from identpy.objects import Model


class SpringMass(Model):

    name = 'Spring-Mass System Model'

    parameters = {
        'm': 'Mass',
        'k': 'Stiffness coefficient',
    }

    inputs = {
        'F': 'External force',
    }

    outputs = {
        'x': 'Mass position',
        'v': 'Mass speed',
    }

    states = {
        'x': 'Mass position',
        'v': 'Mass speed',
    }

    def __init__(self, x_0=0, u_0=0, u=0, method=None):

        super().__init__(x_0, u_0, u, method)

    def f(self, x=None, u=None, factor=0):

        x, u = super().f(x, u)

        f1 = x[1]
        f2 = -self.p[1]/self.p[0]*x[0] + 1/self.p[0]*u[1]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        g1 = x[0]
        g2 = x[1]

        return np.array([g1, g2])
