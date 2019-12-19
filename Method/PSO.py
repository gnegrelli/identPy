from Method.method import Method

import numpy as np
import time

from copy import copy


class PSO(Method):

    def __init__(self, lo_p, hi_p, swarm_sz=5, max_it=5000, p_speed=5, g_speed=1.5, tol=1.5):

        assert isinstance(lo_p, np.ndarray), "Lower boundary of parameters must be a numpy array"
        assert isinstance(hi_p, np.ndarray), "Upper boundary of parameters must be a numpy array"
        assert len(hi_p) == len(lo_p), "Upper and lower boundaries must have the same size"

        self.lo_p = lo_p
        self.hi_p = hi_p
        self.swarm_sz = swarm_sz
        self.max_it = max_it
        self.p_speed = p_speed
        self.g_speed = g_speed
        self.tol = tol

        super().__init__()

    def __call__(self, *args, **kwargs):

        start_time = time.process_time()

        print("------------------PSO-------------------")

        particles = []

        p_best = []
        v = []

        # Create random swarm
        for i in range(self.swarm_sz):
            particles.append([0, (np.random.random(), np.random.random())])

            # TODO: pass error calculation instead of i
            # Evaluate fitness of particle
            particles[i][0] = i

            # Create personal best vector
            p_best.append(copy(particles[i]))

            # Initialize speed of particles
            v.append((0., 0.))

        # TODO: Remove reverse from sorted method
        # Create global best
        g_best = copy(sorted(particles, reverse=True)[0])

        # Add error from first particles to log
        self.error_log.append(g_best[0])

        while self.counter < self.max_it and self.error_log[-1] > self.tol:

            self.counter += 1

            # Update coordinates of particles
            for i in range(self.swarm_sz):

                # Calculate acceleration of particles
                a = (self.p_speed*(p_best[i][1][0] - particles[i][1][0]) +
                     self.g_speed*(g_best[1][0] - particles[i][1][0]),
                     self.p_speed*(p_best[i][1][1] - particles[i][1][1]) +
                     self.g_speed*(g_best[1][1] - particles[i][1][1]))

                # Update position of particles
                particles[i][1] = (min(max(particles[i][1][0] + v[i][0] + a[0], 0), 1),
                                   min(max(particles[i][1][1] + v[i][1] + a[1], 0), 1))

                # Update speed of particles
                v[i] = (v[i][0] + a[0], v[i][1] + a[1])

                # TODO: pass error calculation instead of `10 + i`
                # Update fitness value
                particles[i][0] = 10 + i

                # TODO: Change condition to `p_best[i][0] > particles[i][0]`
                # Update personal best vector
                if p_best[i][0] < particles[i][0]:
                    p_best[i] = copy(particles[i])

            # TODO: Change condition to `g_best[0] > min(particles)[0]`
            # Update global best
            if g_best[0] < max(particles)[0]:
                g_best = copy(sorted(particles, reverse=True)[0])

            self.error_log.append(g_best[0])

            # TODO: Remove this break statement when method is running ok
            if self.counter >= 1:
                break

        print("PSO elapsed time: ", time.process_time() - start_time)

        # Return best particle
        return np.array(g_best[1]*(self.hi_p - self.lo_p) + self.lo_p)


def Function(dic, tolerance):
    
    import numpy as np

    import matplotlib.pyplot as plt

    import datetime
    import copy

    # Timestamp for PSO Method
    start_time = datetime.datetime.now()

    print("------------------PSO-------------------")

    SIM = __import__(dic['chsn_sim'])
    ERROR = __import__(dic['chsn_err'])

    # Population size
    swarm_size = dic['PSO']['swarm_size']

    # Boundaries
    up_bound = dic['PSO']['p_max']
    low_bound = dic['PSO']['p_min']

    # Speed constants
    vp = dic['PSO']['p_speed']
    vg = dic['PSO']['g_speed']

    particles = []

    if not dic['import_data']:
        op_real = SIM.rk4(dic, dic['real'])
    else:
        op_real = dic['u'][:, [0, 3, 4]]

    p_best = []

    v = []

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

    # Create global best
    g_best = copy.copy(sorted(particles)[0])

    # Add error from first particles to log
    dic['error_log'] = np.hstack((dic['error_log'], g_best[0]))

    while dic['PSO']['counter'] < dic['PSO']['max_iteration'] and dic['error_log'][-1] > tolerance:

        dic['PSO']['counter'] += 1

        # Update coordinates of particles
        for i in range(swarm_size):

            # Calculate acceleration of particles
            a = (vp*(p_best[i][1][0] - particles[i][1][0]) + vg*(g_best[1][0] - particles[i][1][0]),
                 vp*(p_best[i][1][1] - particles[i][1][1]) + vg*(g_best[1][1] - particles[i][1][1]))

            # Update position of particles
            particles[i][1] = (min(max(particles[i][1][0] + v[i][0] + a[0], 0), 1),
                               min(max(particles[i][1][1] + v[i][1] + a[1], 0), 1))

            # Update speed of particles
            v[i] = (v[i][0] + a[0], v[i][1] + a[1])

            # Update fitness value
            particles[i][0] = .5*dic['TS']['step'] * \
                              ERROR.Error(op_real, SIM.rk4(dic, (particles[i][1]*(up_bound - low_bound) + low_bound)))

            # Update personal best vector
            if p_best[i][0] > particles[i][0]:
                p_best[i] = copy.copy(particles[i])

        if g_best[0] > min(particles)[0]:
            g_best = copy.copy(sorted(particles)[0])

        dic['error_log'] = np.hstack((dic['error_log'], g_best[0]))

    print(dic['PSO']['counter'])

    print(g_best, np.array(g_best[1]*(up_bound - low_bound) + low_bound))

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

    print("PSO elapsed time: ", datetime.datetime.now() - start_time)

    # Return best particle
    return np.array(g_best[1]*(up_bound - low_bound) + low_bound)
