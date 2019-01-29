# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 18:41:34 2017

@author: Gabriel
"""

def soma(a, b, pai):
    from time import sleep
    print a+b
    pai.MS.set(True)
    while pai.MS.get() == True:
        raw_input("Press Enter to continue.")
        sleep(20)