# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:07:00 2019
Test shape factor asymmetrical
University of Sao Paulo
@author: Gabriel
"""

import numpy as np

s = np.array([[2., 5.]])

sf = np.array([s[0], s[0]])

d = np.array([[1., 6.]])

dd = np.array([[1.5, 3.]])

print np.greater(s, d)[0]

counts = 0
for v in np.greater(s, d)[0]:
    if v:
        d[0][counts] *= dd[0][counts]
        sf[1][counts] = d[0][counts]
    else:
        d[0][counts] /= dd[0][counts]
        sf[0][counts] = d[0][counts]
    counts += 1

print "\n", counts
print "--"*10
print sf[0]
print sf[1]
