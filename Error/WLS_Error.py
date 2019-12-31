def wls_error(y, x, w=None):

    assert (y.shape == x.shape), "Arrays must have the same shape"
    
    if w is None:
        w = np.ones((y.shape[0], 1))

    assert w.shape[0] == y.shape[0], "Weight array must have the same number of rows as y and x"

    err = 0

    for i in w*(y - x)**2:
        for j in i:
            err += j
    return err


import numpy as np


if __name__ == '__main__':
    w = np.array([[1], [2], [1]])
    a = np.array([[1, 2], [3, 4], [10, 11]])
    b = np.array([[5, 6], [7, 8], [13, 49]])
    print(wls_error(a, b, w))
