import numpy as np
import matplotlib.pyplot as plt

from identpy.Model import SpringMass, Pendulum, ZIM, DFIG
from identpy.Model.Implicit_Methods import RK4
from identpy.Method import MVMO, PSO, TS
from identpy.Objects import Estimator


def estimate():
    # Create instance of class Estimator
    est = Estimator()

    # Create figure canvas and add it to estimator
    fig = plt.figure()
    est.add_figure(fig)

    # Read input file and add output measurements to estimator
    u_meas, y_meas = Estimator.input_read('Sample_Data/Sample_DFIG_Erlich.csv', u_indices=[1, 2, 4, 5],
                                          y_indices=[4, 5])
    est.add_measures(y_meas)

    # Create model instance and add it to estimator
    model = DFIG(np.array([0.995628884585680, 0.396820283647337]), u_meas[0], u_meas,
                 RK4(initial_time=u_meas[0][0], final_time=u_meas[-1][0]))
    est.add_model(model)

    # Create MVMO method instance and add it to estimator
    m1 = MVMO(np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972, 0.269505715408350,
                        1.998406311405870, 1.099838352995214])*.8,
              np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972, 0.269505715408350,
                        1.998406311405870, 1.099838352995214])*1.1,
              wndw_sz=3, tol=0.1)
    est.add_method(m1)

    # Create TS method instance and add it to estimator
    m2 = TS(np.array([1, 1, 1, 1, 1, 1, 1]))
    est.add_method(m2)

    # Run estimation process
    est()

    est.refresh_figure()

    # Plot error evolution of both methods
    plt.figure()
    plt.plot(est.method1.error_log, label='MVMO')
    plt.plot(range(len(est.method1.error_log) - 1, len(est.method1.error_log) + len(est.method2.error_log) - 1),
             est.method2.error_log, label='TS')
    plt.title('Error Evolution')
    plt.xlabel('Iteration')
    plt.ylabel('Error')

    plt.show()


if __name__ == '__main__':
    estimate()
