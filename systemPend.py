 # -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
System Matrices
University of Sao Paulo
@author: Gabriel
"""

def Matrix(p, x0, u0):
    
    import numpy as np

#    Pendulo
    A = np.array([[0., 1.], [-p[2]*np.cos(x0[0, 0])/p[1], -p[0]/p[3]]])
    B = np.array([[0.],[1./(p[1]*p[3])]])
    C = np.array([[1., 0.],[0., 1.]])
    D = 0
    
    return A, B, C, D