# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:05:59 2019
PSO Estimation Method
University of Sao Paulo
@author: Gabriel
"""


def Function(dic, tolerance):
    
    import numpy as np

    import matplotlib.pyplot as plt
    from matplotlib import style

    import datetime
    import copy

    # Timestamp for PSO Method
    start_time = datetime.datetime.now()

    print "------------------PSO-------------------"

    SIM = __import__(dic['chsn_sim'])
    ERROR = __import__(dic['chsn_err'])

    # Population size
    pop_size = dic['PSO']['population']

    # Boundaries
    up_bound = dic['PSO']['p_max']
    low_bound = dic['PSO']['p_min']

    xmax = 10.
    xmin = 0.

    ymax = 10.
    ymin = 0.

    # Speed constants
    vp = .3
    vg = .2

    # Control variables
    max_it = dic['PSO']['max_iteration']
    iter = 0

    list_ind = []

    real = (3., 5.)
    real = np.array([3., 5.])

    p_best = []

    v = []

    # Plot configuration
    style.use('ggplot')

    # Create figure
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.axis([xmin, xmax, ymin, ymax])

    # Plotting real values
    ax1.plot(real[0], real[1], 'gx')

    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    marker = ['.', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'D', 'd']

    # Create random population
    for i in range(pop_size):
        list_ind.append([0, (np.random.random(), np.random.random())])

        # Evaluate fitness of individual
        list_ind[i][0] = sum(abs(real - list_ind[i][1]*(up_bound - low_bound) + low_bound))

        print list_ind

        list_ind[i][0] = abs(real[0] - list_ind[i][1][0]*(xmax - xmin) + xmin) + \
                         abs(real[1] - list_ind[i][1][1]*(ymax - ymin) + ymin)

        print list_ind

        # Create personal best vector
        p_best.append(copy.copy(list_ind[i]))

        # Initialize speed of particles
        v.append((0., 0.))

        # Plot new population
        ax1.plot(list_ind[i][1][0] * (xmax - xmin) + xmin, list_ind[i][1][1] * (ymax - ymin) + ymin,
                 color[i % len(color)] + '*')

    # Create global best
    g_best = copy.copy(sorted(list_ind)[0])

    while iter < max_it and g_best[0] > tolerance:

        plt.pause(.1)

        # Redraw graph
        ax1.clear()
        ax1.axis([xmin, xmax, ymin, ymax])

        iter += 1

        # Update coordinates of individuals
        for i in range(pop_size):

            # Calculate acceleration of particles
            a = (vp*(p_best[i][1][0] - list_ind[i][1][0]) + vg*(g_best[1][0] - list_ind[i][1][0]),
                 vp*(p_best[i][1][1] - list_ind[i][1][1]) + vg*(g_best[1][1] - list_ind[i][1][1]))

            # Update position of particles
            list_ind[i][1] = (min(max(list_ind[i][1][0] + v[i][0] + a[0], xmin), xmax),
                              min(max(list_ind[i][1][1] + v[i][1] + a[1], ymin), ymax))

            # Update speed of particles
            v[i] = (v[i][0] + a[0], v[i][1] + a[1])

            # Update fitness value
            list_ind[i][0] = abs(real[0] - list_ind[i][1][0] * (xmax - xmin) + xmin) + \
                             abs(real[1] - list_ind[i][1][1] * (ymax - ymin) + ymin)

            # Update personal best vector
            if p_best[i][0] > list_ind[i][0]:
                p_best[i] = copy.copy(list_ind[i])

            # Plot new population
            ax1.plot(list_ind[i][1][0]*(xmax - xmin) + xmin, list_ind[i][1][1]*(ymax - ymin) + ymin,
                     color[i % len(color)] + marker[i % len(marker)])

        # Plotting real values
        ax1.plot(real[0], real[1], 'gx')

        if g_best[0] > min(list_ind)[0]:
            g_best = copy.copy(sorted(list_ind)[0])

    print iter

    print g_best

    plt.show()

    print "PSO elapsed time: ", datetime.datetime.now() - start_time

    # Return best individual
    return g_best
