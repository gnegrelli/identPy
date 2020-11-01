import numpy as np
from scipy.linalg import qr


def velez_reyes(matrix, verbose=False):

    v, u = np.linalg.eig(matrix)
    v_norm = np.sqrt(abs(np.amax(v)/v))

    u_p = np.empty(shape=[u.shape[0], 0])
    
    for j in v_norm:
        if j < 1000:
            u_p = np.hstack((u_p, u[:, np.where(v_norm == j)].reshape((u.shape[0], -1))))

    if verbose:
        print("Parameters classification: ", qr(u_p.T, pivoting=True)[2])
    return qr(u_p.T, pivoting=True)[2]
