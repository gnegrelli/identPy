import numpy as np
import matplotlib.pyplot as plt

from Model.systemSM import SpringMass as mod
from Model.systemZIM import ZIM as mod
from Model.systemDFIG import DFIG as mod
from Model.Implicit_Methods.RK4 import RK4

from Method.MVMO import MVMO
from Method.PSO import PSO
from Method.TS import TS

from estimator import Estimator

from Error.WLS_Error import _eval


filepath = 'Sample_Data/Sample_DFIG_Erlich_pu_fault.csv'

with open(filepath, 'r') as f:
    for line in f.read().split('\n'):
        if line and line[0] is not '%':
            values = line.split(',')
            t = eval(values[0])
            v = eval(values[1])
            theta = eval(values[2])
            p = eval(values[4])
            q = eval(values[5])

            try:
                y_meas = np.vstack((y_meas, np.array([t, p, q])))
            except NameError:
                y_meas = np.array([t, p, q])

            try:
                u_meas = np.vstack((u_meas, np.array([t, v, theta, p, q])))
            except NameError:
                u_meas = np.array([t, v, theta, p, q])

# plt.figure(1)
# plt.plot(y_meas[:, 0], y_meas[:, 1])

# plt.figure(2)
# plt.plot(y_meas[:, 0], y_meas[:, 2])

# plt.show()

# TODO: Read input vector u_meas on the model side
a = mod(np.array([0.995529958481552, 0.394837954500335]), u_meas[0], u_meas, RK4(final_time=1))
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

