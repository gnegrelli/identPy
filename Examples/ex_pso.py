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

tol = 3.

max_gen = 10

list_ind = []

real = (3., 5.)

p_best = []

# Create random population
for i in range(pop_size):
    list_ind.append([0, (np.random.random(), np.random.random())])

    # Evaluate fitness of individual
    list_ind[i][0] = abs(real[0] - list_ind[i][1][0]*(xmax - xmin) + xmin) + \
                     abs(real[1] - list_ind[i][1][1]*(ymax - ymin) + ymin)

# Create personal best vector
for i in range(len(list_ind)):
    try:
        if p_best[i][0] > list_ind[i][0]:
            p_best[i] = list_ind[i]
    except IndexError:
        p_best.append(list_ind[i])

# Create global best
g_best = copy.copy(sorted(list_ind)[0])

# Plotting population
for indiv in list_ind:
    plt.plot(indiv[1][0]*(xmax - xmin) + xmin, indiv[1][1]*(ymax - ymin) + ymin, "ro")

plt.plot(real[0], real[1], 'gx')
plt.axis([xmin, xmax, ymin, ymax])

delta = []
# Update coordinates of individuals
for i in range(pop_size):
    delta.append((.3*(p_best[i][1][0] - list_ind[i][1][0]) + .2*(g_best[1][0] - list_ind[i][1][0]),\
        .3*(p_best[i][1][1] - list_ind[i][1][1]) + .2*(g_best[1][1] - list_ind[i][1][1])))

plt.show()