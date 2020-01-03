import numpy as np
import matplotlib.pyplot as plt

from Model.systemSM import SpringMass as mod
from Model.Implicit_Methods.RK4 import RK4

from Method.MVMO import MVMO

from estimator import Estimator

from Error.WLS_Error import _eval


filepath = 'SM_data.csv'

with open(filepath, 'r') as f:
    for line in f.read().split('\n'):
        if line and line[0] is not '%':
            t, x, v = line.split(',')
            t = eval(t)
            x = eval(x)
            v = eval(v)

            try:
                y_meas = np.vstack((y_meas, np.array([t, x, v])))
            except NameError:
                y_meas = np.array([t, x, v])

plt.figure(1)
plt.plot(y_meas[:, 0], y_meas[:, 1])

plt.figure(2)
plt.plot(y_meas[:, 0], y_meas[:, 2])

# plt.show()

a = mod(np.array([0, 0]), np.array([4]), RK4(final_time=2*np.pi))
a.update_output(p=np.array([3.5, 6]))

m = MVMO(np.array([2, 4]), np.array([4, 8]))

est = Estimator(y_meas, a, m)

est()

