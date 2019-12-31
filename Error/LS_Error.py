def ls_error(y, x):
    
    err = 0
    
    if y.shape == x.shape:
        for i in (y - x)**2:
            for j in i:
                err += j
        return err
    else:
        print("Error: Arrays must have the same shapes")


import numpy as np


if __name__ == '__main__':
    w = np.array([[1], [2]])
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    print(a.shape, b.shape)
    for i in w*((a - b) ** 2):
        print(i)
    print(ls_error(a, b))
