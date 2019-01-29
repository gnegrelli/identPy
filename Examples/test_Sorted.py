# -*- coding: utf-8 -*-
"""
Created on Mon Dec 03 11:23:29 2018

@author: gabriel
"""

###
def takeSecond(elem):
    return elem[0]
###


import numpy

a = [(1,numpy.array([2,3])),(3,numpy.array([5,7])),(7,numpy.array([1,6])),(1,numpy.array([1,9])),(2,numpy.array([8,0]))]

print sorted(a, key = takeSecond)