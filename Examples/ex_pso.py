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

# Velocities
vp = .3
vg = .2

# Control variables
tol = 3.
max_gen = 10
gen = 0

list_ind = []

real = (3., 5.)

p_best = []

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

    # Plot new population
    plt.plot(list_ind[i][1][0] * (xmax - xmin) + xmin, list_ind[i][1][1] * (ymax - ymin) + ymin,
             color[gen % len(color)] + marker[gen % len(marker)])

gen += 1

# Update/Create personal best vector
for i in range(len(list_ind)):
    try:
        if p_best[i][0] > list_ind[i][0]:
            p_best[i] = list_ind[i]
    except IndexError:
        p_best.append(list_ind[i])

# Update/Create global best
try:
    if g_best[0] > min(list_ind)[0]:
        g_best = copy.copy(sorted(list_ind)[0])
except NameError:
    g_best = copy.copy(sorted(list_ind)[0])

# Update coordinates of individuals
for i in range(pop_size):
    list_ind[i][1] = (list_ind[i][1][0] + vp*(p_best[i][1][0] - list_ind[i][1][0]) + vg*(g_best[1][0] - list_ind[i][1][0]),
                      list_ind[i][1][1] + vp*(p_best[i][1][1] - list_ind[i][1][1]) + vg*(g_best[1][1] - list_ind[i][1][1]))

    # Update fitness value
    list_ind[i][0] = abs(real[0] - list_ind[i][1][0] * (xmax - xmin) + xmin) + \
                     abs(real[1] - list_ind[i][1][1] * (ymax - ymin) + ymin)

    # Plot new population
    plt.plot(list_ind[i][1][0]*(xmax - xmin) + xmin, list_ind[i][1][1]*(ymax - ymin) + ymin,
             color[gen % len(color)] + marker[gen % len(marker)])

plt.show()
