import numpy as np

from identpy.Model import Model


# TODO: Test class and confirm equations
class ZIM(Model):

    parameters = {
        'X': 'Reactance',
        "X'": 'Reactance',
        'T<sub>0</sub>': 'Time constant',
        'M': 'Inertia',
        'G<sub>s</sub>': 'Admittance',
        'B<sub>s</sub>': 'Susceptance',
        'E<sub>0</sub>': 'Initial voltage',
        'δ<sub>0</sub>': 'Initial angle',
    }

    inputs = {
        'ΔV': 'Voltage variation',
    }

    outputs = {
        'ΔP': 'Active power variation',
        'ΔQ': 'Reactive power variation',
    }

    def __init__(self, x_0=0, u_0=0, u=0, method=None):

        super().__init__(x_0, u_0, u, method)

    def f(self, x=None, u=None):

        x, u = super().f(x, u)

        f1 = - self.p[0]/(self.p[1] * self.p[2])*x[0] \
             - (self.p[0] - self.p[1])*self.u_0[0]*np.sin(self.p[7])/(self.p[1]*self.p[2])*x[1] \
             + (self.p[0] - self.p[1])*np.cos(self.p[7])/(self.p[1]*self.p[2])*u[1]

        f2 = (self.p[0] - self.p[1])*self.u_0[0]*np.sin(self.p[7])/(self.p[1] * self.p[2]*(self.p[6] ** 2))*x[0] \
             - (self.p[0] - self.p[1])*self.u_0[0]*np.cos(self.p[7])/(self.p[1]*self.p[2]*self.p[6])*x[1] \
             + x[2] \
             - (self.p[0] - self.p[1])*np.sin(self.p[7])/(self.p[1]*self.p[2]*self.p[6])*u[1]

        f3 = - self.u_0[0]*np.sin(self.p[7])/(self.p[3]*self.p[1])*x[0] \
             - self.u_0[0]*self.p[6]*np.cos(self.p[7])/(self.p[3]*self.p[1])*x[1] \
             - self.p[6]*np.sin(self.p[7])/(self.p[1]*self.p[3])*u[1]

        return np.array([f1, f2, f3])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        g1 = - self.u_0[0]*np.sin(self.p[7])/self.p[1]*x[0] \
             - self.u_0[0]*self.p[6]*np.cos(self.p[7])/self.p[1]*x[1] \
             + 2*self.p[4]*self.u_0[0] - (self.p[6]*np.sin(self.p[7])/self.p[1])*u[1]

        g2 = - self.u_0[0]*np.cos(self.p[7])/self.p[1]*x[0] \
             + self.u_0[0]*self.p[6]*np.sin(self.p[7])/self.p[1]*x[1] \
             + 2*self.p[5]*self.u_0[0] + (2*self.u_0[0] - self.p[6]*np.cos(self.p[7]))/self.p[1]*u[1]

        return np.array([g1, g2])
