import numpy as np
import matplotlib.pyplot as plt

from identpy.Model import SpringMass, Pendulum, ZIM, DFIG
from identpy.Model.Implicit_Methods import RK4
from identpy.Method import MVMO, PSO, TS
from identpy.Objects import Estimator


def estimate():
    u_meas, y_meas = Estimator.input_read('Sample_Data/Sample_DFIG_Erlich.csv', u_indices=[1, 2, 4, 5],
                                          y_indices=[4, 5])

    a = DFIG(np.array([0.995628884585680, 0.396820283647337]), u_meas[0], u_meas,
             RK4(initial_time=u_meas[0][0], final_time=u_meas[-1][0]))
    a.update_output(p=np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972,
                                0.269505715408350, 1.998406311405870, 1.099838352995214]))

    m1 = MVMO(np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972, 0.269505715408350,
                        1.998406311405870, 1.099838352995214])*.8,
              np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972, 0.269505715408350,
                        1.998406311405870, 1.099838352995214])*1.1,
              wndw_sz=3, tol=0.1)

    m2 = TS(np.array([1, 1, 1, 1, 1, 1, 1]))

    est = Estimator()
    est.add_measures(y_meas)
    est.add_model(a)
    est.add_method(m1)
    est.add_method(m2)

    est()

    plt.figure()
    plt.plot(est.model.y[:, 0], est.model.y[:, 1], label='model')
    plt.plot(y_meas[:, 0], y_meas[:, 1], '--', label='real')
    plt.legend()

    plt.figure()
    plt.plot(est.model.y[:, 0], est.model.y[:, 2], label='model')
    plt.plot(y_meas[:, 0], y_meas[:, 2], '--', label='real')
    plt.legend()

    plt.figure()
    plt.plot(est.method1.error_log)

    if est.method2:
        plt.figure()
        plt.plot(est.method2.error_log)

    plt.show()


if __name__ == '__main__':
    estimate()
