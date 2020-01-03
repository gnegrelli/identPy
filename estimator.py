import numpy as np
from Model.model import Model
from Method.method import Method


class Estimator:

    def __init__(self, model, method):
        assert isinstance(model, Model), "Model must be of class Model"
        assert isinstance(method, Method), "Method must be of class Method"

        self.model = model
        self.method = method

    def __call__(self):

        self.method(self)
