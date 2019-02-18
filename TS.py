# -*- coding: utf-8 -*-
"""
Created on Thu Oct 04 15:04:38 2018
Trajectory Sensibility Function
@author: gabriel
"""


# Gamma function and dJ/dp
def Gamma(A, B, C):
    
    import numpy as np
    
    gamma = np.zeros((A.shape[2], A.shape[2]))
    dJdp = 0
    line = 0

    for i in A:
        gamma += np.dot(i.T[:, 1:], i[1:, :])
        dJdp += np.dot(i.T[:, 1:], np.array([(B-C)[line, 1:]]).T)
        line += 1
            
    return gamma, dJdp


def Function(dic, tolerance):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import copy
    import datetime
    
    start_time = datetime.datetime.now()
    
    print "---------Trajectory Sensitivity---------"
    
    SIM = __import__(dic['chsn_sim'])
    ERROR = __import__(dic['chsn_err'])
    CLASS = __import__(dic['chsn_cla'])
    
    num_param = dic['TS']['p0'].shape[0]
    
#    plt.figure(1)
#    plt.plot(dic['u'][:,0], dic['u'][:,1], linewidth=2.5, color="y", label="Real System")
#    
#    plt.figure(2)
#    plt.plot(dic['u'][:,0], dic['u'][:,2], linewidth=2.5, color="y", label="Real System")
#    
#    plt.figure(3)
#    plt.plot(dic['u'][:,0], dic['u'][:,3], linewidth=2.5, color="y", label="Real System")
#    
#    plt.figure(4)
#    plt.plot(dic['u'][:,0], dic['u'][:,4], linewidth=2.5, color="y", label="Real System")

    if not dic['import_data']:
        op_real = SIM.rk4(dic, dic['real'])
    else:
        op_real = dic['u'][:, [0, 3, 4]]
    
    p = dic['TS']['p0']
    op = SIM.rk4(dic, p)

    plt.figure(1)
    plt.plot(op_real[:, 0], op_real[:, 1], linewidth=2.5, color="y", label="Real System")
    
    plt.figure(2)
    plt.plot(op_real[:, 0], op_real[:, 2], linewidth=2.5, color="y", label="Real System")
    
#    plt.figure(3)
#    plt.plot(op[:,0], op[:,1], linewidth=2.5, color="b", label = "Real System")
#    
#    plt.figure(4)
#    plt.plot(op[:,0], op[:,2], linewidth=2.5, color="b", label = "Real System")
    
    delta_p = dic['TS']['delta_p']
    
    aux = np.zeros(num_param)
    aux[0] = 1

    p_active = np.ones(num_param)
    
    evolution = copy.copy(p)
    
    dic['error_log'] = np.hstack((dic['error_log'], .5*dic['TS']['step']*ERROR.Error(op_real[:, 1:], op[:, 1:])))
    # dic['error_log'] = np.array([.5*dic['TS']['step']*ERROR.Error(dic['u'][:,3:], op[:,1:])])
    
    while dic['error_log'][-1] > tolerance and dic['TS']['counter'] < 50:
        
        for i in range(num_param):
            op_p = SIM.rk4(dic, p + np.roll(aux, i)*delta_p)
            
            if i == 0:
                dopdp = (op_p - op)/delta_p[i]
            else:
                dopdp = np.dstack((dopdp, ((op_p - op)/delta_p[i])))
                
        (gamma, dJdp) = Gamma(dopdp, op, op_real)

        # Parameters area classified due to its conditioning
        if dic['TS']['counter'] == 0:
            CLASS.Classification(gamma)
        
        # Parameters are modified (added DP) and stored
        try:
            DP = -np.linalg.solve(gamma, dJdp)
        except Exception:
            print "DEU XABU!!"
            break

        p += p_active.reshape(num_param,) * DP.reshape(num_param,)
        
        print "Iteration #%d: %s" %(dic['TS']['counter']+1, p)
        evolution = np.vstack((evolution, p))
        # x0[0,0], x0[0,1] = p[6], p[7]  # IS THIS RIGHT??????
        
        # System output is reevaluated, now with the modified parameters
        op = SIM.rk4(dic, p)
        
        # Error is recalculated and stored
        Jp = .5*dic['TS']['step']*ERROR.Error(op_real[:, 1:], op[:, 1:])
        dic['error_log'] = np.hstack((dic['error_log'], Jp))
        
        # Number of iterations is increased
        dic['TS']['counter'] += 1
    
    plt.figure(1)
    plt.plot(op[:, 0], op[:, 1], "k--", label="TS")
    plt.legend()
    
    plt.figure(2)
    plt.plot(op[:, 0], op[:, 2], "k--", label="TS")
    plt.legend()    
    
    plt.figure(3)
    if (dic['error_log'].size - dic['TS']['counter'] - 1) == 0:
        plt.plot(range(dic['error_log'].size - dic['TS']['counter'] - 1, dic['error_log'].size), dic['error_log'][dic['error_log'].size - dic['TS']['counter'] - 1:dic['error_log'].size], label="TS")
    else:
        plt.plot(range(dic['error_log'].size - dic['TS']['counter'] - 2, dic['error_log'].size - 1), dic['error_log'][dic['error_log'].size - dic['TS']['counter'] - 1:dic['error_log'].size], label="TS")
    plt.legend()
    
    print "\n\n\n"
    print "Final result: %s" % p
    print "Final Error: ", dic['error_log'][-1]
    print "Trajectory Sensitivity elapsed time: ", datetime.datetime.now() - start_time

    return p