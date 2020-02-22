from Model.model import Model

import numpy as np


class SpringMass(Model):

    def __init__(self, x_0=0, u_0=0, u=0, method=None):

        super().__init__(x_0, u_0, u, method)

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

        x, u = super().f(x, u)

        f1 = x[1]
        f2 = -self.p[1]/self.p[0]*x[0] + 1/self.p[0]*u[1]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        g1 = x[0]
        g2 = x[1]

        return np.array([g1, g2])
