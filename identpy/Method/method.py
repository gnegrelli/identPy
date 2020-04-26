from abc import ABC


class Method(ABC):

    def __init__(self, plot=False, verbose=False):
        self.counter = 0
        self.error_log = []

        self.plot = plot
        self.verbose = verbose

    def __call__(self, *args, **kwargs):
        pass
