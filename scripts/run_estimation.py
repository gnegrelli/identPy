import numpy as np
import matplotlib.pyplot as plt

from identpy.models import SpringMass, Pendulum, ZIM, DFIG, DFIG_improved
from identpy.models.implicit_methods import RK4
from identpy.methods import MVMO, PSO, TS
from identpy.objects import Estimator


def run_estimation():
    # Create instance of class Estimator
    estimator = Estimator()

    # Create figure canvas and add it to estimator
    fig = plt.figure()
    estimator.add_figure(fig)
    plt.pause(.01)

    # Read input file and add output measurements to estimator
    u_meas, y_meas = Estimator.input_read('/home/gabriel/Desktop/identPy/sample_data/DFIG_Erlich.csv',
                                          u_indices=[1, 2, 4, 5], y_indices=[4, 5])
    estimator.add_measures(y_meas)

    # Create model instance and add it to estimator
    model = DFIG_improved(np.array([0.995628884585680, 0.396820283647337]), u_meas[0], u_meas,
                          RK4(initial_time=u_meas[0][0], final_time=u_meas[-1][0]))
    estimator.add_model(model)

    # Create MVMO method instance and add it to estimator
    method_1 = MVMO(np.array([0.01, 0.05, 3, 0.01, 0.1, 1, .7]),
                    np.array([0.1, 0.8, 15, 0.2, 1, 5, 1.6]),
                    wndw_sz=3, tol=0.001)
    estimator.add_method(method_1)

    # Create TS method instance and add it to estimator
    method_2 = TS(np.array([1, 1, 1, 1, 1, 1, 1]))
    estimator.add_method(method_2)

    # Run estimation process
    estimator()

    estimator.refresh_figure()
    print('Estimated parameters: {}'.format(repr(estimator.model.p)))

    # Plot error evolution of both methods
    plt.figure()
    offset = 0
    for method in estimator.methods:
        x_ticks = list(map(lambda x: x + offset, range(len(method.error_log))))
        offset += len(method.error_log) - 1
        plt.plot(x_ticks, method.error_log, label=method.name)
    plt.title('Error Evolution')
    plt.xlabel('Iteration')
    plt.ylabel('Error')
    plt.legend()
    plt.show()


if __name__ == '__main__':

    run_estimation()
