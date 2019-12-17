 # -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
Spring-Mass System Matrices
University of Sao Paulo
@author: Gabriel
"""


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