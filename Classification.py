# -*- coding: utf-8 -*-
"""
Created on Wed May 10 22:29:55 2017

@author: Gabriel
"""

def Classification(A):
    
    from scipy.linalg import qr as QRS
    import numpy as np
    
#    print A
    
    V, U = np.linalg.eig(A)
    Vnorm = np.sqrt(abs(np.amax(V)/V))
    
    """
    from numpy import *

    A = array([[144.9, 325.5],[325.5, 5298.1]])

    A = array([[373578.259736529, -75959.1753700779, 107886.540739222, -911851.666529192, -4372.36884977606, 9.70566096510859, -576.948411888186],
           [-75959.1753700779,15598.1583827228,-22258.4899241412,189047.624322781,902.590009048401,-2.85505513579881,117.788193401234],
           [107886.540739222,-22258.4899241412,33476.4122301726,-298238.386542411,-1392.16298076536,9.20059171036572,-163.477888321700],
           [-911851.666529192,189047.624322781,-298238.386542411,2772982.33892791,12640.1219891103,-183.135384780116,1348.89391477318],
           [-4372.36884977606,902.590009048401,-1392.16298076536,12640.1219891103,59.1562556682830,0.184217618636096,6.56962009773013],
           [9.70566096510859,-2.85505513579881,9.20059171036572,-183.135384780116,0.184217618636096,0.930258362200925,0],
           [-576.948411888186,117.788193401234,-163.477888321700,1348.89391477318,6.56962009773013,0,0.930258362200925]])
"""

    Up = np.empty(shape=[U.shape[0],0])
    
    print Vnorm

    for j in Vnorm:
        if j < 1000:
            Up = np.hstack((Up,U[:,np.where(Vnorm==j)].reshape((U.shape[0],-1))))
            print j, np.where(Vnorm==j)

    print "\nParameters Classification:\n"
    print QRS(Up.T, pivoting=True)[2] + 1
    print "\n"

