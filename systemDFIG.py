# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
DFIG System Functions
University of Sao Paulo
@author: Gabriel
"""


# f function for DFIG Model
def f(p, x, u, t):
    
    import numpy as np

    """
    p[0] = Kvc
    p[1] = Ki
    p[2] = Ti
    p[3] = Tv
    p[4] = r
    p[5] = X
    
    u = [t, Vt, thetav, P, Q]
    
    x = [Vd, Vq]
    """

    qtref = 0.0576
    vtref = 1.0105
    ptref = 0.982
    imax = 1.1
    vtmin = 0.9
    stepi = 0.1

    pos = np.where(u == t)[0][0]

    Ix = 0.
    Iy = 0.

    Ire = qtref/vtref + p[0]*(vtref - u[pos, 1])
    
    Iac = ptref/vtref

    # Current Priority Block
    if np.sqrt(Iac**2 + Ire**2) < imax:
        ipref = Iac
        iqref = Ire
    else:
        if u[pos, 0] < vtmin:
            iqref = min(Ire, imax)
            ipref = np.sqrt(imax**2 - iqref**2)
        else:
            ipref = min(Iac, imax)
            iqref = np.sqrt(imax**2 - ipref**2)

    # Integration
    for ti in [x/(1/stepi) for x in range(0, int(t/stepi + 1))]:
        tx = np.where(u == ti)[0][0]
        Ix += (ipref - u[tx, 3]/u[tx, 1])*stepi/p[2]
        Iy += (u[tx, 4]/u[tx, 1] - iqref)*stepi/p[2]

    Vpa = p[1]*(ipref - u[pos, 3]/u[pos, 1] + Ix)
    Vqa = p[1]*(u[pos, 4]/u[pos, 1] - iqref + Ix)
    
    U = np.array([Vpa, Vqa])
    
    A = np.array([[-1./p[3], 0], [0, -1./p[3]]])
    
    B = np.array([[-np.cos(u[pos, 2])/p[3], -np.sin(u[pos, 2])/p[3]], [np.sin(u[pos, 2])/p[3], -np.cos(u[pos, 2])/p[3]]])
    
    return np.dot(A, x) + np.dot(B, U)
    

# g function for DFIG Model
def g(p, x, u, t):
    
    import numpy as np

    pos = np.where(u == t)[0][0]
    
    Vtd = u[pos, 1]*np.cos(u[pos, 2])
    Vtq = u[pos, 1]*np.sin(u[pos, 2])
    
    P = (p[4]*(Vtd*x[0, 0] + Vtq*x[1, 0] - u[pos, 0]**2) + p[5]*(Vtq*x[0, 0] - Vtd*x[1, 0]))/(p[4]**2 + p[5]**2)
    Q = (p[5]*(Vtd*x[0, 0] + Vtq*x[1, 0] - u[pos, 0]**2) - p[4]*(Vtq*x[0, 0] - Vtd*x[1, 0]))/(p[4]**2 + p[5]**2)
    
    return np.array([[P], [Q]])
