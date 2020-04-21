import numpy as np

from identpy.Model import Model
from identpy.Method import Method


class Estimator:

    def __init__(self, real_output, model, method1, method2=None):
        assert isinstance(real_output, np.ndarray), "Real output must be a numpy array"

        assert isinstance(model, Model), "Model must be an instance of Model class"

        assert isinstance(method1, Method), "First method must be an instance of Method class"
        assert isinstance(method2, Method) or method2 is None, "Second method must be an instance of Method class"

        self.y_meas = real_output

        self.model = model
        self.method1 = method1
        self.method2 = method2

    def __call__(self):

        self.method1(self)
        if self.method2:
            self.method2(self)
