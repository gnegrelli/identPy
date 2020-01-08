from Method.method import Method
from Error.WLS_Error import _eval

import numpy as np
import time

from copy import copy

import matplotlib.pyplot as plt


class TS(Method):

    def __init__(self, p0, delta_p=0.001, step=0.005, max_it=25, tol=.0005):

        assert isinstance(p0, np.ndarray), "Parameters must be a numpy array"

        self.p = p0.astype(float)
        self.delta_p = delta_p
        self.step = step
        self.max_it = max_it
        self.tol = tol
        self.num_param = len(self.p)

        super().__init__()

    def __call__(self, parent, p_active=None, active_iter=0):

        start_time = time.process_time()

        print("---------Trajectory Sensitivity---------")

        assert isinstance(p_active, list) or p_active is None, "Active parameters must be given as a list"

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

        # Evaluate error for p_0
        parent.model.update_output(self.p)
        self.error_log.append(_eval(parent.model.y, parent.y_meas))

        # Iteration Process
        while self.error_log[-1] > self.tol and self.counter < self.max_it:

            self.counter += 1

            y = copy(parent.model.y)

            # Auxiliary vector for Sensitivity Calculation
            aux = np.ones_like(self.p, dtype=float)
            aux[0] += self.delta_p

            # Sensitivities calculation
            for i in range(self.num_param):
                parent.model.update_output(self.p*np.roll(aux, i))

                if i == 0:
                    dy_dp = (parent.model.y - y) / (self.p[i]*self.delta_p)
                else:
                    dy_dp = np.dstack((dy_dp, (parent.model.y - y) / (self.p[i]*self.delta_p)))

            # Γ and dJ/dp calculation
            dj_dp, gamma = self.gamma_function(dy_dp, parent.y_meas - y)

            # TODO: Create classification method and call it
            # Parameters area classified due to its conditioning
            # if dic['TS']['counter'] == 0:
            #     CLASS.Classification(gamma)

            # Parameters are modified (added DP) and stored
            try:
                delta_p = -np.linalg.solve(gamma, dj_dp)
            except np.linalg.LinAlgError:
                raise Exception("Singular matrix")

            # Update parameters and model output
            self.p += self.p_active*delta_p.reshape(self.num_param, )
            parent.model.update_output(self.p)

            

            # TODO: Remove this if clause when method is working fine
            if self.counter >= 2:
                break

        print("Trajectory Sensitivity elapsed time: ", time.process_time() - start_time)

    @staticmethod
    def gamma_function(sens, diff):
        """
        Calculation of G(p) and Hessian Matrix Γ(p)
        :param sens: Sensibility Matrix dy(p)/dp
        :param diff: Matrix containing the difference between modeled and real systems
        :return: G(p) and Γ(p)
        """

        gamma = np.zeros((sens.shape[2], sens.shape[2]))
        djdp = 0

        for i, m in enumerate(sens):
            gamma += np.dot(m.T[:, 1:], m[1:, :])
            djdp += np.dot(m.T[:, 1:], np.array([diff[i, 1:]]).T)

        return djdp, gamma


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
