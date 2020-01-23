from Method.method import Method
from Error.WLS_Error import _eval

import numpy as np
import time

from copy import copy

import matplotlib.pyplot as plt


class PSO(Method):

    def __init__(self, lo_p, hi_p, swarm_sz=5, max_it=5000, p_speed=0.5, g_speed=0.15, tol=0.05, plot=False):

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

        self.plot = plot

        super().__init__()

    def __call__(self, parent):

        start_time = time.process_time()

        print("------------------PSO-------------------")

        # Create figure
        if self.plot:
            fig = plt.figure()
            ax1 = fig.add_subplot(1, 1, 1)
            axis_lst = []
            for limits in list(zip(self.lo_p, self.hi_p)):
                axis_lst.extend(limits)
            ax1.axis(axis_lst)

        particles = []

        p_best = []
        v = []

        # Create random swarm
        for i in range(self.swarm_sz):
            particles.append([0, (np.random.random(), np.random.random())])

            # Evaluate fitness of particle
            parent.model.update_output(particles[i][1]*(self.hi_p - self.lo_p) + self.lo_p)
            particles[i][0] = _eval(parent.model.y, parent.y_meas)

            # Create personal best vector
            p_best.append(copy(particles[i]))

            # Initialize speed of particles
            v.append((0., 0.))

            if self.plot:
                plot_particle = particles[i][1]*(self.hi_p - self.lo_p) + self.lo_p
                ax1.plot(plot_particle[0], plot_particle[1], PSO.color[i % len(PSO.color)] + '*')

        # Create global best
        g_best = copy(sorted(particles)[0])

        # Add error from first particles to log
        self.error_log.append(g_best[0])

        while self.counter < self.max_it and self.error_log[-1] > self.tol:

            self.counter += 1

            # Redraw graph
            if self.plot:
                plt.pause(.1)
                ax1.clear()
                ax1.axis(axis_lst)

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

                # Update fitness value
                parent.model.update_output(particles[i][1]*(self.hi_p - self.lo_p) + self.lo_p)
                particles[i][0] = _eval(parent.model.y, parent.y_meas)

                # Update personal best vector
                if p_best[i][0] > particles[i][0]:
                    p_best[i] = copy(particles[i])

                if self.plot:
                    # Plot new population
                    plot_particle = particles[i][1]*(self.hi_p - self.lo_p) + self.lo_p
                    ax1.plot(plot_particle[0], plot_particle[1],
                             PSO.color[i % len(PSO.color)] + PSO.marker[i % len(PSO.marker)])

            # Update global best
            if g_best[0] > min(particles)[0]:
                g_best = copy(sorted(particles)[0])

            self.error_log.append(g_best[0])

        print("PSO elapsed time: ", time.process_time() - start_time)

        # Return best particle
        return np.array(g_best[1]*(self.hi_p - self.lo_p) + self.lo_p)

    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    marker = ['.', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'D', 'd']
