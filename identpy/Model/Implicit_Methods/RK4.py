import numpy as np

from copy import copy

from identpy.Model.Implicit_Methods.i_method import IMethod as IM


class RK4(IM):

    def __init__(self, initial_time=0, final_time=1, step=0.001):
        assert isinstance(initial_time, float) or isinstance(initial_time, int), "Initial time must be a number"
        assert isinstance(final_time, float) or isinstance(final_time, int), "Final time must be a number"
        assert isinstance(step, float) or isinstance(step, int), "Step must be a number"

        self.t0 = initial_time
        self.tf = final_time
        self.h = step

    def __call__(self, model):

        x = copy(model.x_0)
        t = self.t0
        u = iter(model.u)

        u_t = next(u)

        model.y = np.append(t, model.g(x, u_t))

        while t < self.tf:

            # TODO: Modify the usage of u on f and g. Maybe read it from a file would be better
            k1 = self.h*(model.f(x, u_t, factor=0))
            try:
                u_t = next(u)
            except StopIteration:
                break
            k2 = self.h*(model.f(x + k1/2, u_t, factor=1/2))
            k3 = self.h*(model.f(x + k2/2, u_t, factor=1/2))
            k4 = self.h*(model.f(x + k3, u_t, factor=1))

            t = round(t + self.h, 5)

            x = x + (k1 + 2*k2 + 2*k3 + k4)/6

            model.y = np.vstack((model.y, np.append(t, model.g(x, u_t))))
