import numpy as np

from identpy.models import SpringMass, Pendulum, ZIM, DFIG, DFIG_improved
from identpy.models.implicit_methods import RK4
from identpy.methods import MVMO, PSO, TS
from identpy.objects import Estimator


def analyse_pop_size(n=5, file=None):
    estimator = Estimator()

    # Read measurement data and add it to estimator
    u_meas, y_meas = Estimator.input_read('Sample_Data/Sample_DFIG_Erlich.csv', u_indices=[1, 2, 4, 5],
                                          y_indices=[4, 5])
    estimator.add_measures(y_meas)

    # Create model instance and add it to estimator
    model = DFIG(np.array([0.995628884585680, 0.396820283647337]), u_meas[0], u_meas,
                 RK4(initial_time=u_meas[0][0], final_time=u_meas[-1][0]))
    estimator.add_model(model)

    # Create MVMO method instance and add it to estimator
    method_1 = MVMO(np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972,
                              0.269505715408350, 1.998406311405870, 1.099838352995214])*.8,
                    np.array([0.033626225647791, 0.199200232546442, 6.977405042044428, 0.035473950408972,
                              0.269505715408350, 1.998406311405870, 1.099838352995214])*1.2,
                    wndw_sz=3, tol=0.1, pop_sz=n)
    estimator.add_method(method_1)

    # Run estimation process
    estimator()

    if file is not None:
        string = ''
        with open(file, 'a+') as f:
            string += '{},{},{}'.format(repr(estimator.methods[0].elapsed_time),
                                        repr(estimator.model.p),
                                        repr(estimator.methods[0].error_log)
                                        )
            print(string, file=f)


if __name__ == '__main__':

    populations = [5, 10, 20, 50, 100]

    for p in populations:
        for i in range(35):
            print('Population {}: Case {}'.format(p, i))
            analyse_pop_size(p, '{}_pop.csv'.format(p))
