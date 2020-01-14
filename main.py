import numpy as np
import matplotlib.pyplot as plt

from Model.systemSM import SpringMass as mod
from Model.Implicit_Methods.RK4 import RK4

from Method.MVMO import MVMO
from Method.PSO import PSO
from Method.TS import TS

from estimator import Estimator

from Error.WLS_Error import _eval


filepath = 'Sample_Data/Sample_SpringMass.csv'

with open(filepath, 'r') as f:
    for line in f.read().split('\n'):
        if line and line[0] is not '%':
            t, x, v, u = line.split(',')
            t = eval(t)
            x = eval(x)
            v = eval(v)
            u = eval(u)

            try:
                y_meas = np.vstack((y_meas, np.array([t, x, v])))
            except NameError:
                y_meas = np.array([t, x, v])

            try:
                u_meas = np.vstack((u_meas, np.array([t, u])))
            except NameError:
                u_meas = np.array([t, u])

plt.figure(1)
plt.plot(y_meas[:, 0], y_meas[:, 1])

plt.figure(2)
plt.plot(y_meas[:, 0], y_meas[:, 2])

# plt.show()

a = mod(np.array([0, 0]), u_meas[:, 1], RK4(final_time=2*np.pi))
a.update_output(p=np.array([3.5, 6]))

m = MVMO(np.array([0, 0]), np.array([10, 10]))
m = PSO(np.array([0, 0]), np.array([10, 10]))
m = TS(np.array([3, 5]))

est = Estimator(y_meas, a, m)

est()

