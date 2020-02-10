from Model.model import Model

import numpy as np


class DFIG(Model):

    def __init__(self, x_0=0, u_0=0, u=0, method=None, step_int=0.1, v_tref=1.0105, p_tref=0.982, v_tmin=0.9):
        super().__init__(x_0, u_0, u, method)

        self.step_int = step_int
        self.v_tref = v_tref
        self.p_tref = p_tref
        self.v_tmin = v_tmin

        self.v_pa_adj = 0
        self.v_qa_adj = 0

        self.parameters = {
            'R': 'Equivalent Resistance',
            'X': 'Equivalent Reactance',
            'k_I': 'PI Gain',
            'T_I': 'PI Time Constant',
            'T_V': 'Delay Time Constant',
            'k_VC': 'Voltage Controller Gain',
            'i_max': 'Maximum Current',
        }

        self.inputs = {
            'v_T': 'Terminal Voltage Magnitude',
            'i_P': 'Current Active Component',
            'i_Q': 'Current Reactive Component',
        }

        self.outputs = {
            'P_e': 'Active Power',
            'Q_e': 'Reactive Power',
        }

    def f(self, x=None, u=None):

        x, u = super().f(x, u)

        i_ac = self.p_tref/self.v_tref
        i_re = self.p[5]*(self.v_tref - u[1])

        print('i_ac:', i_ac)
        print('i_re:', i_re)
        print(30*'-')

        # Current Priority Block
        if np.sqrt(i_ac**2 + i_re**2) < self.p[6]:
            i_pref = i_ac
            i_qref = i_re
        else:
            if u[1] < self.v_tmin:
                i_qref = min(np.abs(i_re), self.p[6])*i_re/np.abs(i_re)
                i_pref = np.sqrt(self.p[6]**2 - i_qref**2)
            else:
                i_pref = min(np.abs(i_ac), self.p[6])*i_ac/np.abs(i_ac)
                i_qref = np.sqrt(self.p[6]**2 - i_pref**2)

        print('i_pref:', i_pref)
        print('i_qref:', i_qref)
        print(30 * '-')

        # PI Block
        v_pa = self.p[2]*(self.p[3] + self.step_int)/self.p[3]*(i_pref - u[3]/u[1]) + self.v_pa_adj
        v_qa = self.p[2]*(self.p[3] + self.step_int)/self.p[3]*(u[3]/u[1] - i_qref) + self.v_qa_adj

        self.v_pa_adj = v_pa - self.p[2]*(i_pref - u[3]/u[1])
        self.v_qa_adj = v_qa - self.p[2]*(u[3]/u[1] - i_qref)

        print('v_pa:', v_pa)
        print('v_qa:', v_qa)

        pass

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        # TODO: Check calculation of vtd and vtq. Which angle should I use.
        vtd = u[1]*np.cos(u[2])
        vtq = u[1]*np.sin(u[2])

        g1 = (self.p[0]*(vtd*x[0] + vtq*x[1] - u[1]**2) + self.p[1]*(vtq*x[0] - vtd*x[1]))/(self.p[0]**2 + self.p[1]**2)
        g2 = (self.p[1]*(vtd*x[0] + vtq*x[1] - u[1]**2) - self.p[0]*(vtq*x[0] - vtd*x[1]))/(self.p[0]**2 + self.p[1]**2)

        return np.array([g1, g2])


# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:36:44 2017
DFIG System Functions
University of Sao Paulo
@author: Gabriel
"""


# f function for DFIG Model
def f(p, x, u, t):
    
    import numpy as np

    """
    p[0] = Kvc
    p[1] = Ki
    p[2] = Ti
    p[3] = Tv
    p[4] = r
    p[5] = X
    
    u = [t, Vt, thetav, P, Q]
    
    x = [Vd, Vq]
    """

    qtref = 0.0576
    vtref = 1.0105
    ptref = 0.982
    imax = 1.1
    vtmin = 0.9
    stepi = 0.1

    pos = np.where(u == t)[0][0]

    Ix = 0.
    Iy = 0.

    Ire = qtref/vtref + p[0]*(vtref - u[pos, 1])
    
    Iac = ptref/vtref

    # Current Priority Block
    if np.sqrt(Iac**2 + Ire**2) < imax:
        ipref = Iac
        iqref = Ire
    else:
        if u[pos, 0] < vtmin:
            iqref = (Ire/np.abs(Ire))*min(np.abs(Ire), imax)
            ipref = np.sqrt(imax**2 - iqref**2)
        else:
            ipref = (Iac/np.abs(Iac))*min(np.abs(Iac), imax)
            iqref = np.sqrt(imax**2 - ipref**2)

    # Integration
    for ti in [x/(1/stepi) for x in range(0, int(t/stepi + 1))]:
        tx = np.where(u == ti)[0][0]
        Ix += (ipref - u[tx, 3]/u[tx, 1])*stepi/p[2]
        Iy += (u[tx, 4]/u[tx, 1] - iqref)*stepi/p[2]

    Vpa = p[1]*(ipref - u[pos, 3]/u[pos, 1] + Ix)
    Vqa = p[1]*(u[pos, 4]/u[pos, 1] - iqref + Ix)
    
    U = np.array([Vpa, Vqa])
    
    A = np.array([[-1./p[3], 0], [0, -1./p[3]]])
    
    B = np.array([[-np.cos(u[pos, 2])/p[3], -np.sin(u[pos, 2])/p[3]], [np.sin(u[pos, 2])/p[3], -np.cos(u[pos, 2])/p[3]]])
    
    return np.dot(A, x) + np.dot(B, U)
    

# g function for DFIG Model
def g(p, x, u, t):
    
    import numpy as np

    pos = np.where(u == t)[0][0]
    
    Vtd = u[pos, 1]*np.cos(u[pos, 2])
    Vtq = u[pos, 1]*np.sin(u[pos, 2])
    
    P = (p[4]*(Vtd*x[0, 0] + Vtq*x[1, 0] - u[pos, 0]**2) + p[5]*(Vtq*x[0, 0] - Vtd*x[1, 0]))/(p[4]**2 + p[5]**2)
    Q = (p[5]*(Vtd*x[0, 0] + Vtq*x[1, 0] - u[pos, 0]**2) - p[4]*(Vtq*x[0, 0] - Vtd*x[1, 0]))/(p[4]**2 + p[5]**2)
    
    return np.array([[P], [Q]])
