from Model.model import Model

import numpy as np


class SpringMass(Model):

    def __init__(self, x_0=0, u=0):

        super().__init__(x_0, u)

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

    def update_parameters(self, p):
        assert len(p) == len(self.parameters), "Parameter vector must be of length %d" % len(self.parameters)

        super().update_parameters(p)

    def f(self, x=None, u=None):

        if not x:
            x = self.x_0
        if not u:
            u = self.u

        f1 = x[1]
        f2 = -self.p[1]/self.p[0]*x[0] + 1/self.p[0]*u[0]

        return np.array([[f1], [f2]])

    def g(self, x=None, u=None):

        if not x:
            x = self.x_0
        if not u:
            u = self.u

        g1 = x[0]
        g2 = x[1]

        return np.array([[g1], [g2]])



def Matrix(p, x0, u0):
    
    import numpy as np

    """
    p[0] = k
    p[1] = m

    u = [F]

    x = [x, v]
    """
    A = np.array([[0., 1.],[-p[1]/p[0], 0.]])
    
    B = np.array([[0.],[1./p[0]]])
    
    C = np.array([[1, 0],[0, 1]])

    D = 0
    
    return A, B, C, D