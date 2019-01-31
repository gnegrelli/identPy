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
    """
    qtref = 0.
    vtref = 1.
    ptref = 1.
    imax = 1.
    vtmin = 0.8
    stepi = 0.1
    
    Ix = 0.
    Iy = 0.
    
    
        
    Ire = qtref/vtref + p[0]*(vtref - u[0,t])
    
    Iac = ptref/vtref
    
    if np.sqrt(Iac**2 +Ire**2) < imax:
        ipref = Iac
        iqref = Ire
    else:
        if u[0,t] < vtmin:
            iqref = min(Ire, imax)
            ipref = np.sqrt(imax**2 - iqref**2)
        else:
            ipref = min(Iac, imax)
            iqref = np.sqrt(imax**2 - ipref**2)
    
    for ti in range(0,t,stepi):
        Ix += (ipref - u[2,ti]/u[0,ti])*stepi/p[2]
        Iy += (u[3,ti]/u[0,ti] - iqref)*stepi/p[2]
        
        
    Vpa = p[1]*(ipref - u[2,t]/u[0,t] + Ix)
    Vqa = p[1]*(u[3,t]/u[0,t] - iqref + Ix)
    
    U = np.array([[Vpa],[Vqa]])
    
    A = np.array([[-1./p[3], 0],[0, -1./p[3]]])    
    
    B = np.array([[-np.cos(u[1,t])/p[3], -np.sin(u[1,t])/p[3]],[np.sin(u[1,t])/p[3], -np.cos(u[1,t])/p[3]]])
    
    x = np.dot(A,x) + np.dot(B,U)
    
    return x
    
    
def g(p, x, u, t)