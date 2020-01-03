import numpy as np


class Estimator:

    def __init__(self, model, method):
        self.model = model
        self.method = method

    def __call__(self):

        self.method(self)
