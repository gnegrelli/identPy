import numpy as np


def _eval(y, x, w=None):
    """
    Method to evaluate error using weighted least squares method (WLS)
    :param y: Array to evaluate error
    :type y: numpy array (np.ndarray)
    :param x: Array to evaluate error
    :type x: numpy array (np.ndarray)
    :param w: Weight array. If no argument is passed, weights are considered to be 1 (LS method)
    :type w: numpy array (np.ndarray)
    :return: WLS error
    :rtype: float
    """

    assert (y.shape == x.shape), "Arrays must have the same shape"
    
    if w is None:
        w = np.ones((y.shape[0], 1))

    assert w.shape[0] == y.shape[0], "Weight array must have the same number of rows as y and x"

    # Calculate step between each row of y
    steps = []
    for i in range(len(y) - 1):
        steps.append(round(y[i + 1, 0] - y[i, 0], 5))
    steps.append(steps[-1])

    err = 0

    for i, row in enumerate(w*(y - x)**2):
        for diff in row:
            err += steps[i]*diff
    return err
