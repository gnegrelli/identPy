import os

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

    @staticmethod
    def input_read(file_path=None, u_indices=None, y_indices=None):

        assert isinstance(u_indices, list), 'Input indices must be given in a list'
        assert isinstance(y_indices, list), 'Output indices must be given in a list'
        assert os.path.exists(file_path), 'Data file must exist'
        assert file_path.split('.')[-1] in ['csv', 'txt', 'dat'], 'Only .csv, .txt and .dat file supported'

        with open(file_path, 'r') as f:
            for line in f.read().split('\n'):
                if line and line[0] is not '%':
                    values = line.split(',')

                    # Add data from input columns
                    input_ = np.array([eval(values[0])])
                    for i in u_indices:
                        input_ = np.hstack((input_, np.array([eval(values[i])])))
                    try:
                        u_m = np.vstack((u_m, input_))
                    except NameError:
                        u_m = input_

                    # Add data from output columns
                    output = np.array([eval(values[0])])
                    for i in y_indices:
                        output = np.hstack((output, np.array([eval(values[i])])))
                    try:
                        y_m = np.vstack((y_m, output))
                    except NameError:
                        y_m = output

        return u_m, y_m
