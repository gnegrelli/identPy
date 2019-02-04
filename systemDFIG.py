 # -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
System Matrices
University of Sao Paulo
@author: Gabriel
"""

def f(p, x, u ,t):
    
    import numpy as np

    """
    p[0] = Kvc
    p[1] = Ki
    p[2] = Ti
    p[3] = Tv
    p[4] = r
    p[5] = X
    
    u = [Vt, thetav, P, Q]
    
    x = [Vd, Vq]
    """
    qtref = 0.0576
    vtref = 1.0105
    ptref = 0.982
    imax = 1.1
    vtmin = 0.9
    stepi = 0.1
    
    Ix = 0.
    Iy = 0.
    
    
        
    Ire = qtref/vtref + p[0]*(vtref - u[t,0])
    
    Iac = ptref/vtref
    
    
    if np.sqrt(Iac**2 + Ire**2) < imax:
        ipref = Iac
        iqref = Ire
    else:
        if u[t,0] < vtmin:
            iqref = min(Ire, imax)
            ipref = np.sqrt(imax**2 - iqref**2)
        else:
            ipref = min(Iac, imax)
            iqref = np.sqrt(imax**2 - ipref**2)
    
    for ti in range(0, t, stepi):
        Ix += (ipref - u[ti,2]/u[ti,0])*stepi/p[2]
        Iy += (u[ti,3]/u[ti,0] - iqref)*stepi/p[2]
        
        
    Vpa = p[1]*(ipref - u[t,2]/u[t,0] + Ix)
    Vqa = p[1]*(u[t,3]/u[t,0] - iqref + Ix)
    
    U = np.array([[Vpa],[Vqa]])
    
    A = np.array([[-1./p[3], 0],[0, -1./p[3]]])    
    
    B = np.array([[-np.cos(u[t,1])/p[3], -np.sin(u[t,1])/p[3]],[np.sin(u[1,t])/p[3], -np.cos(u[1,t])/p[3]]])
    
    x = np.dot(A,x) + np.dot(B,U)
    
    return x
    
    
def g(p, x, u, t):
    
    import numpy as np
    
    Vtd = u[t,0]*np.cos(u[t,1])
    Vtq = u[t,0]*np.sin(u[t,1])
    
    P = (p[4]*(Vtd*x[0] + Vtq*x[1] - u[t,0]**2) + p[5]*(Vtq*x[0] - Vtd*x[1]))/(p[4]**2 + p[5]**2)
    
    Q = (p[5]*(Vtd*x[0] + Vtq*x[1] - u[t,0]**2) - p[4]*(Vtq*x[0] - Vtd*x[1]))/(p[4]**2 + p[5]**2)    
    
    return P + Q