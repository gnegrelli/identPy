# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 00:09:25 2017
RK4 Method with Master-Slave Coupling
@author: Gabriel
"""

"""
This function evaluates the behaviour of the system using the RK4 Method to
do so. The returned output will be a matrix where the columns are 
op = | time  x(1) x(2) ... x(n) |
"""

def MS_rk4(ini,end,step,x0,u0,P,deltap,u,j,real):
    t = ini
#    x = x0
    x = x0.T
    i = 0
    p = copy.copy(P)
    
    #The variable 'j' points out if sensibility evaluation is being required
    #and at what parameter
    if j != -1:
        p[j] += deltap[j]
    
    A, B, C, D = Matrix(p, x0,u0)
    
    y = dot(C,x) + dot(D,u)
    
    output = append(t, y.T)
    
    while t < end:
        #transpose(x) é a transposta de x
#        K1 = step*(dot(A,transpose(array([append(real[i],x[0,1:])]))) + dot(B,u.T))
        K1 = step*(dot(A,vstack((real[i],x[1:,:]))) + dot(B,u.T))
#        K2 = step*(dot(A,transpose(array([append(real[i+1],x[0,1:])])) + vstack((0,K1[1:,:]))) + dot(B,u.T))
        K2 = step*(dot(A,(vstack((real[i+1],x[1:,:])) + vstack((0,K1[1:,:])))) + dot(B,u.T) )
#        K3 = step*(dot(A,transpose(array([append(real[i+1],x[0,1:])])) + vstack((0,K2[1:,:]))) + dot(B,u.T))
        K3 = step*(dot(A,(vstack((real[i+1],x[1:,:])) + vstack((0,K2[1:,:])))) + dot(B,u.T) )
#        K4 = step*(dot(A,transpose(array([append(real[i+2],x[0,1:])])) + vstack((0,K3[1:,:]))) + dot(B,u.T))
        K4 = step*(dot(A,(vstack((real[i+2],x[1:,:])) + vstack((0,K3[1:,:])))) + dot(B,u.T) )
        
        t += step
        i += 2
        
        #Update state vector
#        x = atleast_2d(x) + atleast_2d((K1 + 2*K2 + 2*K3 + K4)/6).T
        x = x + (K1 + 2*K2 + 2*K3 + K4)/6
        
        y = dot(C,x) + dot(D,u)
        
        output = vstack((output, append(t, y.T)))
    
    return output