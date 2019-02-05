# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:50:23 2017
Gamma function and dJ/dp
University of Sao Paulo
@author: Gabriel
"""

def Gamma(A,B,C):
    
    import numpy as np
    
    gamma = np.zeros((A.shape[2],A.shape[2]))
    dJdp = 0
    line = 0

    for i in A:
        gamma += np.dot(i.T[:,1:], i[1:,:])
        dJdp += np.dot(i.T[:,1:], np.array([(B-C)[line,1:]]).T)
        line += 1
            
    return gamma,dJdp