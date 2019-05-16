import numpy as np
import matplotlib.pyplot as plt
import copy

# Population size
pop_size = 5

# Boundaries
xmax = 10.
xmin = 0.

ymax = 10.
ymin = 0.

# Speed constants
vp = .3
vg = .2

# Control variables
tol = .3
max_gen = 50
gen = 0

list_ind = []

real = (3., 5.)

p_best = []

v = []

plt.plot(real[0], real[1], 'gx')
plt.axis([xmin, xmax, ymin, ymax])

color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
marker = ['.', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'D', 'd']

# Create random population
for i in range(pop_size):
    list_ind.append([0, (np.random.random(), np.random.random())])

    # Evaluate fitness of individual
    list_ind[i][0] = abs(real[0] - list_ind[i][1][0]*(xmax - xmin) + xmin) + \
                     abs(real[1] - list_ind[i][1][1]*(ymax - ymin) + ymin)

    # Create personal best vector
    p_best.append(copy.copy(list_ind[i]))

    # Initialize speed of particles
    v.append((0., 0.))

    # Plot new population
    plt.plot(list_ind[i][1][0] * (xmax - xmin) + xmin, list_ind[i][1][1] * (ymax - ymin) + ymin,
             color[i] + '*')

# Create global best
g_best = copy.copy(sorted(list_ind)[0])

while gen < max_gen and g_best[0] > tol:

    gen += 1

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
        plt.plot(list_ind[i][1][0]*(xmax - xmin) + xmin, list_ind[i][1][1]*(ymax - ymin) + ymin,
                 color[i] + marker[i])

    if g_best[0] > min(list_ind)[0]:
        g_best = copy.copy(sorted(list_ind)[0])

for p in p_best:
    print p

print gen

print "**", g_best, "**"

plt.show()
