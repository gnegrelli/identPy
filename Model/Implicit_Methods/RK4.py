import numpy as np

from copy import copy
from Model.Implicit_Methods.i_method import IMethod as IM
from Model.model import Model as MD


class RK4(IM):

    def __init__(self, model, initial_time=0, final_time=1, step=0.001):
        assert isinstance(initial_time, float) or isinstance(initial_time, int), "Initial time must be a number"
        assert isinstance(final_time, float) or isinstance(final_time, int), "Final time must be a number"
        assert isinstance(step, float) or isinstance(step, int), "Step must be a number"

        assert isinstance(model, MD), "Model must be of class Model"

        self.t0 = initial_time
        self.tf = final_time
        self.h = step

        self.model = model

    def __call__(self, *args, **kwargs):

        x = copy(self.model.x_0)
        t = self.t0

        self.model.y = np.append(t, self.model.g())

        while t < self.tf:
            k1 = self.h*(self.model.f(x))
            k2 = self.h*(self.model.f(x + k1))
            k3 = self.h*(self.model.f(x + k2))
            k4 = self.h*(self.model.f(x + k3))

            t = round(t + self.h, 5)

            x = x + (k1 + 2*k2 + 2*k3 + k4)/6

            self.model.y = np.vstack((self.model.y, np.append(t, self.model.g(x))))
