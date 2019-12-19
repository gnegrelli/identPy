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
