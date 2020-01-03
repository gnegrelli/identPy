import numpy as np
from Model.model import Model
from Method.method import Method


class Estimator:

    def __init__(self, real_output, model, method):
        assert isinstance(model, Model), "Model must be of class Model"
        assert isinstance(method, Method), "Method must be of class Method"
        assert isinstance(real_output, np.ndarray), "Real output must be a numpy array"

        self.y_meas = real_output

        self.model = model
        self.method = method

    def __call__(self):

        self.method(self)
