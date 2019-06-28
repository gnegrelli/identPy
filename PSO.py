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
    swarm_size = dic['PSO']['swarm_size']

    # Boundaries
    up_bound = dic['PSO']['p_max']
    low_bound = dic['PSO']['p_min']

    xmax = 10.
    xmin = 0.

    ymax = 10.
    ymin = 0.

    # Speed constants
    vp = dic['PSO']['p_speed']
    vg = dic['PSO']['g_speed']

    particles = []

    if not dic['import_data']:
        op_real = SIM.rk4(dic, dic['real'])
    else:
        op_real = dic['u'][:, [0, 3, 4]]

    real = (3., 6.)

    p_best = []

    v = []

    # Plot configuration
    style.use('ggplot')

    # Create figure
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.axis([xmin, xmax, ymin, ymax])

    # Plotting real values
    ax1.plot(dic['real'][0], dic['real'][1], 'gx')

    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    marker = ['.', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'D', 'd']

    # Create random swarm
    for i in range(swarm_size):
        particles.append([0, (np.random.random(), np.random.random())])

        # Evaluate fitness of particle
        particles[i][0] = .5*dic['TS']['step'] * \
                          ERROR.Error(op_real, SIM.rk4(dic, (particles[i][1]*(up_bound - low_bound) + low_bound)))

        # Create personal best vector
        p_best.append(copy.copy(particles[i]))

        # Initialize speed of particles
        v.append((0., 0.))

        # Plot new population
        ax1.plot((particles[i][1]*(up_bound - low_bound) + low_bound)[0],
                 (particles[i][1]*(up_bound - low_bound) + low_bound)[1],
                 color[i % len(color)] + '*')

    # Create global best
    g_best = copy.copy(sorted(particles)[0])

    while dic['PSO']['counter'] < dic['PSO']['max_iteration'] and g_best[0] > tolerance:

        plt.pause(.001)

        # Redraw graph
        ax1.clear()
        ax1.axis([xmin, xmax, ymin, ymax])

        dic['PSO']['counter'] += 1

        # Update coordinates of particles
        for i in range(swarm_size):

            # Calculate acceleration of particles
            a = (vp*(p_best[i][1][0] - particles[i][1][0]) + vg*(g_best[1][0] - particles[i][1][0]),
                 vp*(p_best[i][1][1] - particles[i][1][1]) + vg*(g_best[1][1] - particles[i][1][1]))

            # Update position of particles
            particles[i][1] = (min(max(particles[i][1][0] + v[i][0] + a[0], xmin), xmax),
                               min(max(particles[i][1][1] + v[i][1] + a[1], ymin), ymax))

            # Update speed of particles
            v[i] = (v[i][0] + a[0], v[i][1] + a[1])

            # Update fitness value
            particles[i][0] = .5*dic['TS']['step'] * \
                              ERROR.Error(op_real, SIM.rk4(dic, (particles[i][1]*(up_bound - low_bound) + low_bound)))

            # Update personal best vector
            if p_best[i][0] > particles[i][0]:
                p_best[i] = copy.copy(particles[i])

            # Plot swarm
            ax1.plot(particles[i][1][0]*(xmax - xmin) + xmin, particles[i][1][1]*(ymax - ymin) + ymin,
                     color[i % len(color)] + marker[i % len(marker)])

        # Plotting real values
        ax1.plot(dic['real'][0], dic['real'][1], 'gx')

        if g_best[0] > min(particles)[0]:
            g_best = copy.copy(sorted(particles)[0])

    print dic['PSO']['counter']

    print g_best, np.array(g_best[1]*(up_bound - low_bound) + low_bound)

    plt.show()

    # Plot y1 real and from MVMO
    plt.figure(1)
    plt.plot(op_real[:, 0], op_real[:, 1], linewidth=2.5, color="y", label="Real System")
    plt.plot(SIM.rk4(dic, (g_best[1]*(up_bound - low_bound) + low_bound))[:, 0],
             SIM.rk4(dic, (g_best[1]*(up_bound - low_bound) + low_bound))[:, 1], "--", label="PSO")
    plt.title("Active Power")
    plt.xlabel("Time (s)")
    plt.ylabel(r'$\Delta$P')

    # Plot y2 real and from MVMO
    plt.figure(2)
    plt.plot(op_real[:, 0], op_real[:, 2], linewidth=2.5, color="y", label="Real System")
    plt.plot(SIM.rk4(dic, (g_best[1]*(up_bound - low_bound) + low_bound))[:, 0],
             SIM.rk4(dic, (g_best[1]*(up_bound - low_bound) + low_bound))[:, 2], "--", label="PSO")
    plt.title("Reactive Power")
    plt.xlabel("Time (s)")
    plt.ylabel(r'$\Delta$Q')

    # # Plot error evolution
    # plt.figure(3)
    # if (dic['error_log'].size - dic['MVMO']['counter'] - 1) == 0:
    #     plt.plot(range(dic['error_log'].size - dic['MVMO']['counter'] - 1, dic['error_log'].size),
    #              dic['error_log'][dic['error_log'].size - dic['MVMO']['counter'] - 1:dic['error_log'].size],
    #              label="PSO")
    # else:
    #     plt.plot(range(dic['error_log'].size - dic['MVMO']['counter'] - 2, dic['error_log'].size - 1),
    #              dic['error_log'][dic['error_log'].size - dic['MVMO']['counter'] - 1:dic['error_log'].size],
    #              label="PSO")
    # plt.title("Error evolution")
    # plt.xlabel("Generation")
    # plt.ylabel("Error")

    print "PSO elapsed time: ", datetime.datetime.now() - start_time

    # Return best particle
    return np.array(g_best[1]*(up_bound - low_bound) + low_bound)
