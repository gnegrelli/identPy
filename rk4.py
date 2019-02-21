# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 02:05:44 2017
RK4 Method for matrices
University of Sao Paulo
@author: Gabriel
"""


def rk4(dic, P):
    
    import numpy as np
    import copy
    
    SYS = __import__(dic['chsn_sys'])
    
    t = dic['RK4']['t0']
    tf = dic['RK4']['tf']
    
    x0 = dic['RK4']['x0']
    x = x0.T  # x0.T is x0 transposed
    
    u0 = dic['RK4']['u0']
    u = dic['RK4']['u']

    step = dic['RK4']['step']

    p = copy.copy(P)
    
    A, B, C, D = SYS.Matrix(p, x0, u0)
    
    y = np.dot(C, x) + np.dot(D, u.T)
    output = np.append(t, y.T)
    
    while t < tf:

        K1 = step*(np.dot(A, x) + np.dot(B, u.T))
        K2 = step*(np.dot(A, x + K1) + np.dot(B, u.T))
        K3 = step*(np.dot(A, x + K2) + np.dot(B, u.T))
        K4 = step*(np.dot(A, x + K3) + np.dot(B, u.T))
        
        t = round(t + step, 5)

        x = x + (K1 + 2*K2 + 2*K3 + K4)/6
        y = np.dot(C, x) + np.dot(D, u.T)
        
        output = np.vstack((output, np.append(t, y.T)))

    return output
