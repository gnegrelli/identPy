from abc import ABC

from blinker import signal


class Method(ABC):

    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    marker = ['.', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'D', 'd']

    name = 'Method'

    string = '{}\tError: {:.6f}\tIter.: {}'

    def __init__(self, plot=False, verbose=False):
        self.counter = 0
        self.error_log = []

        self.plot = plot
        self.verbose = verbose

        self.elapsed_time = 0

    def __call__(self, *args, **kwargs):
        signal('start_method').send(self)

    def __str__(self):
        if self.counter > 0:
            string = self.string.format(self.name, self.error_log[-1], self.counter)
        else:
            string = str(None)
        return string
