from Method.method import Method

import numpy as np
import time


class TS(Method):

    def __init__(self, p0, delta_p=0.001, step=0.005, max_it=25, tol=.0005):

        assert isinstance(p0, np.ndarray), "Parameters must be a numpy array"

        self.p = p0
        self.delta_p = delta_p
        self.step = step
        self.max_it = max_it
        self.tol = tol

        super().__init__()

    def __call__(self, p_active=None, active_iter=0):

        start_time = time.process_time()

        # Parameters to be estimated
        if isinstance(p_active, list):
            self.p_active = np.zeros_like(self.p)
            try:
                for i in p_active:
                    self.p_active[i] = 1
            except IndexError:
                raise IndexError("While setting active parameters: Invalid index of parameter")
        else:
            self.p_active = np.ones_like(self.p)

        print(self.p_active)

        print("Trajectory Sensitivity elapsed time: ", time.process_time() - start_time)




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


# Trajectory Sensitivity estimation process
def Function(dic, tolerance):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import copy
    import datetime

    # Timestamp for Traj. Sens. Method
    start_time = datetime.datetime.now()
    
    print("---------Trajectory Sensitivity---------")
    
    SIM = __import__(dic['chsn_sim'])
    ERROR = __import__(dic['chsn_err'])
    CLASS = __import__(dic['chsn_cla'])

    if dic['import_data']:
        op_real = dic['u'][:, [0, 3, 4]]
    else:
        op_real = SIM.rk4(dic, dic['real'])
    
    p = dic['TS']['p0']
    delta_p = dic['TS']['delta_p']
    num_param = p.shape[0]

    # Output for initial values of p
    op = SIM.rk4(dic, p)

    # plt.figure(1)
    # plt.plot(op_real[:, 0], op_real[:, 1], linewidth=2.5, color="y", label="Real System")
    
    # plt.figure(2)
    # plt.plot(op_real[:, 0], op_real[:, 2], linewidth=2.5, color="y", label="Real System")
    
    # plt.figure(1)
    # plt.plot(op[:, 0], op[:, 1], linewidth=2.5, color="b", label="TS start")

    # plt.figure(2)
    # plt.plot(op[:, 0], op[:, 2], linewidth=2.5, color="b", label="TS start")

    # Auxiliary variable for Sensitivity Calculation
    aux = np.zeros(num_param)
    aux[0] = 1

    # Parameters to be estimated
    p_active = np.ones(num_param)

    evolution = copy.copy(p)

    # Error for initial values of p
    print(dic['error_log'])
    dic['error_log'] = np.hstack((dic['error_log'], .5*dic['TS']['step']*ERROR.Error(op_real[:, 1:], op[:, 1:])))

    # Iteration Process
    while dic['error_log'][-1] > tolerance and dic['TS']['counter'] < dic['TS']['max_ite']:

        # Sensitivities calculation
        for i in range(num_param):
            op_p = SIM.rk4(dic, p + np.roll(aux, i)*delta_p)
            
            if i == 0:
                dopdp = (op_p - op)/delta_p[i]
            else:
                dopdp = np.dstack((dopdp, ((op_p - op)/delta_p[i])))

        # Γ and G(p) calculation
        (gamma, dJdp) = Gamma(dopdp, op, op_real)

        # Parameters area classified due to its conditioning
        if dic['TS']['counter'] == 0:
            CLASS.Classification(gamma)
        
        # Parameters are modified (added DP) and stored
        try:
            DP = -np.linalg.solve(gamma, dJdp)
        except Exception:
            print("TS: DEU XABU!!")
            break

        p += p_active.reshape(num_param,) * DP.reshape(num_param,)

        # System output is reevaluated, now with the modified parameters
        op = SIM.rk4(dic, p)
        
        # Error is recalculated and stored
        Jp = .5*dic['TS']['step']*ERROR.Error(op_real[:, 1:], op[:, 1:])
        dic['error_log'] = np.hstack((dic['error_log'], Jp))

        # Number of iterations is increased
        dic['TS']['counter'] += 1

        print("\nIteration #%d: %s" % (dic['TS']['counter'], p))
        print("Error: ", dic['error_log'][-1])
        evolution = np.vstack((evolution, p))
        # x0[0,0], x0[0,1] = p[6], p[7]  # IS THIS RIGHT??????

    # At the end of iteration process, values of p and final error value are presented
    print("\n\n----------------------------")
    print("Final result: %s" % p)
    print("Final Error: ", dic['error_log'][-1])

    # Plot y1 from TS
    plt.figure(1)
    plt.plot(op[:, 0], op[:, 1], "k--", label="Traj. Sens.")
    plt.legend()

    # Plot y2 from TS
    plt.figure(2)
    plt.plot(op[:, 0], op[:, 2], "k--", label="Traj. Sens.")
    plt.legend()

    # Plot error evolution
    plt.figure(3)
    if (dic['error_log'].size - dic['TS']['counter'] - 1) == 0:
        plt.plot(range(dic['error_log'].size - dic['TS']['counter'] - 1, dic['error_log'].size), dic['error_log'][dic['error_log'].size - dic['TS']['counter'] - 1:dic['error_log'].size], label="Traj. Sens.")
    else:
        plt.plot(range(dic['error_log'].size - dic['TS']['counter'] - 2, dic['error_log'].size - 1), dic['error_log'][dic['error_log'].size - dic['TS']['counter'] - 1:dic['error_log'].size], label="Traj. Sens.")
    plt.legend()

    print("Trajectory Sensitivity elapsed time: ", datetime.datetime.now() - start_time)

    # Return optimal set of parameters
    return p
