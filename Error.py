# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 00:11:20 2017
Least square erro
University of Sao Paulo
@author: Gabriel
"""

def Error(y,x):
    
    err = 0
    
    if y.shape == x.shape:
        for i in (y - x)**2:
            for j in i:
                err += j
        return err
    else:
        print "Estoy aqui!!!!"
        print("Error: Arrays must have the same shapes")