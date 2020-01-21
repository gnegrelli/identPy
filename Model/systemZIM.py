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

        x, u = super().f(x, u)

        f1 = - self.p[0]/(self.p[1] * self.p[2])*x[0] \
             - (self.p[0] - self.p[1])*1*np.sin(self.p[7])/(self.p[1]*self.p[2])*x[1] \
             + (self.p[0] - self.p[1])*np.cos(self.p[7])/(self.p[1]*self.p[2])*u[1]

        f2 = (self.p[0] - self.p[1])*1*np.sin(self.p[7])/(self.p[1] * self.p[2]*(self.p[6] ** 2))*x[0] \
             - (self.p[0] - self.p[1])*1*np.cos(self.p[7])/(self.p[1]*self.p[2]*self.p[6])*x[1] \
             + x[2] \
             - (self.p[0] - self.p[1])*np.sin(self.p[7])/(self.p[1]*self.p[2]*self.p[6])*u[1]

        f3 = - 1*np.sin(self.p[7])/(self.p[3]*self.p[1])*x[0] \
             - 1*self.p[6]*np.cos(self.p[7])/(self.p[3]*self.p[1])*x[1] \
             - self.p[6]*np.sin(self.p[7])/(self.p[1]*self.p[3])*u[1]

        return np.array([f1, f2, f3])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        g1 = - 1*np.sin(self.p[7])/self.p[1]*x[0] \
             - 1*self.p[6]*np.cos(self.p[7])/self.p[1]*x[1] \
             + 2*self.p[4]*1 - (self.p[6]*np.sin(self.p[7])/self.p[1])*u[1]

        g2 = - 1*np.cos(self.p[7])/self.p[1]*x[0] \
             + 1*self.p[6]*np.sin(self.p[7])/self.p[1]*x[1] \
             + 2*self.p[5]*1 + (2*self.u[0] - self.p[6]*np.cos(self.p[7]))/self.p[1]*u[1]

        return np.array([g1, g2])
