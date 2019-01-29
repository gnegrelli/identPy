# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 13:44:47 2017

@author: Gabriel
"""

from numpy import *

pullData = open("myFile.dat","r").read()
dataList = pullData.split("\n")

y = array([])
for eachLine in dataList:
    if len(eachLine) > 1:
        t, p , q= eachLine.split(",")
        y = vstack((y, array([float(t), float(p), float(q)]))) if y.size else array([float(t), float(p), float(q)])


p = array([0., 0., 0., 0., 0., 0., 0., 0.])

dp = .001
delta_p = dp*ones_like(p)
