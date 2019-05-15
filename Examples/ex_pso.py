import numpy as np
import matplotlib.pyplot as plt

# Population size
pop_size = 5

# Boundaries
xmax = 10.
xmin = 0.

ymax = 10.
ymin = 0.

list_ind = []

real = (3, 5)

# Create random population
for i in range(pop_size):
    list_ind.append([0, (np.random.random(), np.random.random())])
    list_ind[i][0] = abs(real[0] - list_ind[i][1][0]*(xmax - xmin) + xmin) + abs(real[1] - list_ind[i][1][1]*(ymax - ymin) + ymin)

# Sort individuals by their fitness
list_ind.sort()

for indiv in list_ind:
    print indiv

