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
            dj_dp, gamma = self.gamma_function(dy_dp, y - parent.y_meas)

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

            # Error is recalculated and stored
            self.error_log.append(_eval(parent.model.y, parent.y_meas))

            print("\nIteration #%d: %s" % (self.counter, self.p))
            print("Error: ", self.error_log[-1])

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
