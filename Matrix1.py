 # -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
System Matrices
University of Sao Paulo
@author: Gabriel
"""

def Matrix(p, x0,u0):
    
    from numpy import *

    A = array([[-p[0]/(p[1]*p[2]), -(p[0]-p[1])*u0[0]*sin(p[7])/(p[1]*p[2]), 0],
                [(p[0]-p[1])*u0[0]*sin(p[7])/(p[1]*p[2]*(p[6]**2)), -(p[0]-p[1])*u0[0]*cos(p[7])/(p[1]*p[2]*p[6]), 1],
                 [-u0[0]*sin(p[7])/(p[3]*p[1]), -u0[0]*p[6]*cos(p[7])/(p[3]*p[1]), 0]])
    B = array([[(p[0]-p[1])*cos(p[7])/(p[1]*p[2])],
                [-(p[0]-p[1])*sin(p[7])/(p[1]*p[2]*p[6])],
                 [-p[6]*sin(p[7])/(p[1]*p[3])]])
    C = array([[-u0[0]*sin(p[7])/p[1], -u0[0]*p[6]*cos(p[7])/p[1], 0],
                [-u0[0]*cos(p[7])/p[1], u0[0]*p[6]*sin(p[7])/p[1], 0]])
    D = array([[2*p[4]*u0[0]-(p[6]*sin(p[7])/p[1])],
                [2*p[5]*u0[0]+(2*u0[0]-p[6]*cos(p[7]))/p[1]]])    
    
    return A, B, C, D