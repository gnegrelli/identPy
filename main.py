import numpy as np
import matplotlib.pyplot as plt


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

plt.show()
