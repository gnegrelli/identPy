import os

import numpy as np
import matplotlib.pyplot as plt

from identpy.Model import Model
from identpy.Method import Method


class Estimator:

    def __init__(self):
        self.y_meas = None
        self.model = None
        self.method1 = None
        self.method2 = None
        self.figure = None
        self.axs = None

    def __call__(self):
        assert self.y_meas is not None, "Real output is missing"
        assert self.model is not None, "Model is missing"
        assert self.method1 is not None, "Method is missing"

        if isinstance(self.figure, plt.Figure):
            self.axs = self.figure.subplots(nrows=1, ncols=len(self.model.outputs))
            for ax, op in zip(self.axs, self.model.outputs.values()):
                ax.set_xlabel('Time (s)')
                ax.set_ylabel(op)
            plt.subplots_adjust(wspace=.4)

        self.method1(self)
        if self.method2:
            self.method2(self)

    def add_measures(self, real_output):
        assert isinstance(real_output, np.ndarray), "Real output must be a numpy array"

        self.y_meas = real_output

    def add_model(self, model):
        assert isinstance(model, Model), "Model must be an instance of Model class"

        self.model = model

    def add_method(self, method):
        assert isinstance(method, Method), "Method must be an instance of Method class"

        if self.method1 is None:
            self.method1 = method
        else:
            self.method2 = method

    def add_figure(self, fig):
        assert isinstance(fig, plt.Figure), "Figure must be an instance of matplotlib.pyplot.Figure"

        self.figure = fig

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
