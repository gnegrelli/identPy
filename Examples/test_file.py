# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:42:42 2018

@author: gabriel
"""

f= open("log.csv","w+")
for i in range(100):
    Loop()
    f.write("%f, %f,\n" %(i,i**2))
f.close()
