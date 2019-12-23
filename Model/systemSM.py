from Model.model import Model


class SpringMass(Model):

    def __init__(self):

        super().__init__()
        self.param = {
            'k': 'Stiffness coefficient',
            'm': 'Mass'
        }

    def update_parameters(self, p):
        assert len(p) == len(self.param), "Parameter vector must be of length %d" % len(self.param)

        super().update_parameters(p)


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