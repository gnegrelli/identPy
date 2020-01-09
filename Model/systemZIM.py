from Model.model import Model

import numpy as np


# TODO: Test class and confirm equations
class ZIM(Model):

    def __init__(self, x_0=0, u=0, method=None):

        super().__init__(x_0, u, method)

        self.parameters = {
            'X': 'Reactance',
            "X'": 'Reactance',
            'T_0': 'Time constant',
            'M': 'Inertia',
            'G_s': 'Admittance',
            'B_s': 'Susceptance',
            'E_0': 'Initial voltage',
            'δ_0': 'Initial angle',
        }

        self.inputs = {
            'ΔV': 'Voltage variation',
        }

        self.outputs = {
            'ΔP': 'Active power variation',
            'ΔQ': 'Reactive power variation',
        }

    def f(self, x=None, u=None):

        # TODO: Move asserts and x and u designation to super

        if x is None:
            x = self.x_0
        if u is None:
            u = self.u

        assert isinstance(x, np.ndarray), "States vector must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input vector must be given in a numpy array"

        f1 = - self.p[0]/(self.p[1] * self.p[2])*x[0] \
             - (self.p[0] - self.p[1])*self.u[0]*np.sin(self.p[7])/(self.p[1]*self.p[2])*x[1] \
             + (self.p[0] - self.p[1])*np.cos(self.p[7])/(self.p[1]*self.p[2])*u[0]

        f2 = (self.p[0] - self.p[1])*self.u[0]*np.sin(self.p[7])/(self.p[1] * self.p[2]*(self.p[6] ** 2))*x[0] \
             - (self.p[0] - self.p[1])*self.u[0]*np.cos(self.p[7])/(self.p[1]*self.p[2]*self.p[6])*x[1] \
             + x[2] \
             - (self.p[0] - self.p[1])*np.sin(self.p[7])/(self.p[1]*self.p[2]*self.p[6])*u[0]

        f3 = - self.u[0]*np.sin(self.p[7])/(self.p[3]*self.p[1])*x[0] \
             - self.u[0]*self.p[6]*np.cos(self.p[7])/(self.p[3]*self.p[1])*x[1] \
             - self.p[6]*np.sin(self.p[7])/(self.p[1]*self.p[3])*u[0]

        return np.array([f1, f2, f3])

    def g(self, x=None, u=None):

        # TODO: Move asserts and x and u designation to super

        if x is None:
            x = self.x_0
        if u is None:
            u = self.u

        assert isinstance(x, np.ndarray), "States vector must be given in a numpy array"
        assert isinstance(u, np.ndarray), "Input vector must be given in a numpy array"

        g1 = - self.u[0]*np.sin(self.p[7])/self.p[1]*x[0] \
             - self.u[0]*self.p[6]*np.cos(self.p[7])/self.p[1]*x[1] \
             + 2*self.p[4]*self.u[0] - (self.p[6]*np.sin(self.p[7])/self.p[1])*u[0]

        g2 = - self.u[0]*np.cos(self.p[7])/self.p[1]*x[0] \
             + self.u[0]*self.p[6]*np.sin(self.p[7])/self.p[1]*x[1] \
             + 2*self.p[5]*self.u[0] + (2*self.u[0] - self.p[6]*np.cos(self.p[7]))/self.p[1]*u[0]

        return np.array([g1, g2])
