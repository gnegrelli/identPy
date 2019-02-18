# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 02:05:44 2017
RK4 Method
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
    x = x0.T  # x0.T é a transposta de x0

    # u0 = dic['RK4']['u0']
    # u = dic['RK4']['u']
    
    u0 = dic['u']
    u = dic['u']

    # print 'A: ', np.where(u0 == t)[0]
    # print 'B: ', np.where(u0 == t)
    # print 'C: ', np.where(u0 == t)[0][0]

    step = dic['RK4']['step']

    p = copy.copy(P)

    y = SYS.g(p, x, u0, t)

    # print "y1: ", y

    output = np.append(t, y.T)
    # print "Output1: ", output
    
    while t < tf:

        K1 = step*(SYS.f(p, x, u, t))
        K2 = step*(SYS.f(p, x + K1, u, t))
        K3 = step*(SYS.f(p, x + K2, u, t))
        K4 = step*(SYS.f(p, x + K3, u, t))
        
        # t += step

        t = round(t + step, 5)

        # print t, step

        # if t == 0.009:
        #     print "EQUAL"
        # print np.where(u0 == 0.009)
        # print np.where(u0 == t)

        x = x + (K1 + 2*K2 + 2*K3 + K4)/6
        y = SYS.g(p, x, u, t)

        # print "y2: ", y.T
        # print "output2: ", output

        output = np.vstack((output, np.append(t, y.T)))

    return output
