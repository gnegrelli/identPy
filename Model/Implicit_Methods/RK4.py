import numpy as np


class RK4:

    def __init__(self, initial_time=0., final_time=1., step=0.001):
        self.t0 = initial_time
        self.tf = final_time
        self.h = step

    def __call__(self, *args, **kwargs):

        pass
