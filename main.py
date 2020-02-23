import numpy as np
import matplotlib.pyplot as plt

import os

from Model import SpringMass, Pendulum, ZIM, DFIG
from Model import RK4

from Method import MVMO, PSO, TS

from estimator import Estimator

from Error.WLS_Error import _eval


def input_read(file_path=None, u_indices=None, y_indices=None):

    assert isinstance(u_indices, list), 'Input indices must be given in a list'
    assert isinstance(y_indices, list), 'Output indices must be given in a list'
    assert os.path.exists(file_path), 'Data file must exist'
    assert file_path.split('.')[-1] in ['csv', 'txt', 'dat'], 'Only .csv, .txt and .dat file supported'

    with open(file_path, 'r') as f:
        for line in f.read().split('\n'):
            if line and line[0] is not '%':
                values = line.split(',')

                input = np.array([eval(values[0])])
                output = np.array([eval(values[0])])

                for i in u_indices:
                    input = np.hstack((input, np.array([eval(values[i])])))
                for i in y_indices:
                    output = np.hstack((output, np.array([eval(values[i])])))

                try:
                    y_m = np.vstack((y_m, output))
                except NameError:
                    y_m = output

                try:
                    u_m = np.vstack((u_m, input))
                except NameError:
                    u_m = input

    return u_m, y_m


u_meas, y_meas = input_read('Sample_Data/Sample_DFIG_Erlich_pu_fault.csv', u_indices=[1, 2, 4, 5], y_indices=[4, 5])

# plt.figure(1)
# plt.plot(y_meas[:, 0], y_meas[:, 1])

# plt.figure(2)
# plt.plot(y_meas[:, 0], y_meas[:, 2])

# plt.show()

# TODO: Read input vector u_meas on the model side
a = DFIG(np.array([0.995529958481552, 0.394837954500335]), u_meas[0], u_meas, RK4(final_time=1))
a.update_output(p=np.array([0.4022/(33**2/90), 2.3861/(33**2/90), 10.516, 0.038, 0.393, 2.0, 1.1]))

plt.figure(3)
plt.plot(a.y[:, 0], a.y[:, 1])
plt.show()

m = MVMO(np.array([0., 0., 0., 0., 0., 0., 0.8, -0.5]), np.array([.5, .2, 1., 1., 7., 5., 1.2, 0.5]))
m = PSO(np.array([0., 0., 0., 0., 0., 0., 0.8, -0.5]), np.array([.5, .2, 1., 1., 7., 5., 1.2, 0.5]))
# m = TS(np.array([3, 5]))

est = Estimator(y_meas, a, m)

est()
print(est.method.error_log)

