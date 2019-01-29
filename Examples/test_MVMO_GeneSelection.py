# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 18:52:05 2018

@author: gabriel
"""

import numpy as np

x = np.array([1, 3, 12, 20])
for i in range(15):
    if i in x:
        print "%d foi selecionado" %i
    else:
        print "%d não está na lista" %i

for j in range(30):
    x += np.ones(len(x))
    print x
    while x[-1] >= 12:
        x[-1] = x[-1] - 12
        x.sort()
        print "Sorting: ", x