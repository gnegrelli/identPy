from abc import ABC

import numpy as np
import time


class Method(ABC):

    def __init__(self):
        self.counter = 0
        self.error_log = []

    def __call__(self, *args, **kwargs):
        pass
