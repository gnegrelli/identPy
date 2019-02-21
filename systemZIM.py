 # -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
Z-IM Load Model System Matrices
University of Sao Paulo
@author: Gabriel
"""


def Matrix(p, x0, u0):
    
    import numpy as np
    
    """
    p[0] = X
    p[1] = X'
    p[2] = T0
    p[3] = M
    p[4] = Gs
    p[5] = Bs
    p[6] = E0
    p[7] = delta0
    """

    A = np.array([[-p[0]/(p[1]*p[2]), -(p[0]-p[1])*u0[0]*np.sin(p[7])/(p[1]*p[2]), 0],
                  [(p[0]-p[1])*u0[0]*np.sin(p[7])/(p[1]*p[2]*(p[6]**2)), -(p[0]-p[1])*u0[0]*np.cos(p[7])/(p[1]*p[2]*p[6]), 1],
                  [-u0[0]*np.sin(p[7])/(p[3]*p[1]), -u0[0]*p[6]*np.cos(p[7])/(p[3]*p[1]), 0]])
    
    B = np.array([[(p[0]-p[1])*np.cos(p[7])/(p[1]*p[2])],
                  [-(p[0]-p[1])*np.sin(p[7])/(p[1]*p[2]*p[6])],
                  [-p[6]*np.sin(p[7])/(p[1]*p[3])]])
    
    C = np.array([[-u0[0]*np.sin(p[7])/p[1], -u0[0]*p[6]*np.cos(p[7])/p[1], 0],
                  [-u0[0]*np.cos(p[7])/p[1], u0[0]*p[6]*np.sin(p[7])/p[1], 0]])
    
    D = np.array([[2*p[4]*u0[0]-(p[6]*np.sin(p[7])/p[1])],
                  [2*p[5]*u0[0]+(2*u0[0]-p[6]*np.cos(p[7]))/p[1]]])
    
    return A, B, C, D