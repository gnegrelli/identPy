import os

import numpy as np
import matplotlib.pyplot as plt

from identpy.Model import SpringMass, Pendulum, ZIM, DFIG
from identpy.Model.Implicit_Methods import RK4
from identpy.Method import MVMO, PSO, TS
from identpy.Objects import Estimator


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


u_meas, y_meas = input_read('Sample_Data/Sample_DFIG_Erlich_pu.csv', u_indices=[1, 2, 4, 5], y_indices=[4, 5])

# TODO: Read input vector u_meas on the model side
a = DFIG(np.array([0.995628884585680, 0.396820283647337]), u_meas[0], u_meas,
         RK4(initial_time=u_meas[0][0], final_time=u_meas[-1][0]))
a.update_output(p=np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972, 0.269505715408350, 1.998406311405870, 1.099838352995214]))

plt.figure()
plt.plot(a.y[:, 0], a.y[:, 1], label='model')
plt.plot(y_meas[:, 0], y_meas[:, 1], label='real')
plt.legend()

plt.figure()
plt.plot(a.y[:, 0], a.y[:, 2], label='model')
plt.plot(y_meas[:, 0], y_meas[:, 2], label='real')
plt.legend()

plt.show()
