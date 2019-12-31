import numpy as np


class RK4:

    def __init__(self, initial_time=0, final_time=1, step=0.001):
        assert isinstance(initial_time, float) or isinstance(initial_time, int), "Initial time must be a number"
        assert isinstance(final_time, float) or isinstance(final_time, int), "Final time must be a number"
        assert isinstance(step, float) or isinstance(step, int), "Step must be a number"

        self.t0 = initial_time
        self.tf = final_time
        self.h = step

    def __call__(self, *args, **kwargs):

        pass
