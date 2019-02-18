# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:12:45 2018

@author: gabriel
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.system('cls')
plt.close('all')

dic = {}

chosen_estimation1 = "MVMO"
chosen_estimation2 = "Trajectory Sensitivity"

chosen_system = "Type-3 Wind Turbine"  # "Linearized Load Model Z-IM"  # "Simple Pendulum"  # "Spring-Mass"  #
chosen_simulation = "Runge-Kutta Method1"
chosen_error = "Least-Square Method"
chosen_classification = "QR Decomposition"

estimation_methods = {"-": "", "Kalman Filter": "KF", "MVMO": "MVMO_func", "Trajectory Sensitivity": "TS"}
systems = {"Spring-Mass": "systemSM", "Simple Pendulum": "systemPend", "Linearized Load Model Z-IM": "systemZIM", "Type-3 Wind Turbine": "systemDFIG"}
simulations = {"Runge-Kutta Method": "rk4", "Runge-Kutta Method1": "rk4_function"}
error_methods = {"Least-Square Method": "Error"}
classification_methods = {"-": "", "QR Decomposition": "Classification"}


# Global instances
dic['chsn_est1'] = estimation_methods[chosen_estimation1]
dic['chsn_est2'] = estimation_methods[chosen_estimation2]
dic['chsn_sys'] = systems[chosen_system]
dic['chsn_sim'] = simulations[chosen_simulation]
dic['chsn_err'] = error_methods[chosen_error]
dic['chsn_cla'] = classification_methods[chosen_classification]

dic['error_log'] = np.array([])

dic['import_data'] = True


# Declare file to import from or real parameter values
if dic['import_data']:
    # dic['file'] = 'Datatest.csv'  # For Windows
    dic['file'] = '/home/gabriel/Desktop/PyMod/Datatest.csv'  # For Linux
else:
    # dic['real'] = np.array([3., 6.])  # Spring Mass
    # dic['real'] = np.array([.1, 1., 9.8, 1.])  # Pendulum
    # dic['real'] = np.array([0.2089, 0.0446, 0.0963, 0.0139, 4.1358, 2.8004, 1.0750, -0.3689])  # Z-IM Load Model
    dic['real'] = np.array([2.0, 10.516, 0.038, 0.393, 0.4022, 2.3861])  # DFIG


if dic['import_data']:
    # Reading real measurement file
    pullData = open(dic['file'], "r").read()
    dataList = pullData.split("\n")

    dic['u'] = np.array([])
    for eachLine in dataList:
        if len(eachLine) > 1:
            t, v, theta, trash, p, q, garbage, litter = eachLine.split(";")
            if dic['u'].size:
                dic['u'] = np.vstack((dic['u'], np.array([float(t), float(v)/33, float(theta), float(p)/90, float(q)/90])))
            else:
                dic['u'] = np.array([float(t), float(v)/33, float(theta), float(p)/90, float(q)/90])


# Tolerances
tol1 = 1
tol2 = 0.0005


# MVMO
dic['MVMO'] = {}
dic['MVMO']['population'] = 5
dic['MVMO']['new_gen'] = 1
dic['MVMO']['max_gen'] = 50000

# Pendulum
# dic['MVMO']['p_min'] = np.array([0., .5, 9., 0.])
# dic['MVMO']['p_max'] = np.array([1., 1.5, 11., 2.])

# Z-IM Load Model
# dic['MVMO']['p_min'] = np.array([0., 0., 0., 0., 0., 0., 0.8, -0.5])
# dic['MVMO']['p_max'] = np.array([.5, .2, 1., 1., 7., 5., 1.2, 0.5])

# DFIG
dic['MVMO']['p_min'] = np.array([1., 5., 0., 0., 0., 0.])
dic['MVMO']['p_max'] = np.array([5., 20., .1, 1., 1., 5.])


dic['MVMO']['fs'] = 1.
dic['MVMO']['rndm'] = not True
dic['MVMO']['seq_rndm'] = not True
dic['MVMO']['moving_wndw'] = True
dic['MVMO']['block'] = True
dic['MVMO']['wndw_size'] = 3
dic['MVMO']['wndw_step'] = 1
dic['MVMO']['counter'] = 0


# TS
dic['TS'] = {}

# dic['TS']['p0'] = np.array([.8, 9.])  # Spring-Mass
# dic['TS']['p0'] = np.array([.1, .8, 10, 1.])  # Pendulum
# dic['TS']['p0'] = np.array([.32620312, .0453461, .165223186, .01357852, 3.536177, 5.8111137, .976726836, -0.38856365])  # Z-IM
dic['TS']['p0'] = np.array([2.0, 10.516, 0.038, 0.393, 0.4022, 2.3861])  # DFIG

dic['TS']['delta_p'] = .001*np.ones_like(dic['TS']['p0'])
dic['TS']['counter'] = 0
dic['TS']['step'] = 0.005


# KF
dic['KF'] = {}


# RK4
dic['RK4'] = {}
dic['RK4']['t0'] = 0.
dic['RK4']['tf'] = 1.
dic['RK4']['step'] = 0.001

# dic['RK4']['x0'] = np.array([[0., 0.]])
# dic['RK4']['u0'] = np.array([1.])
# dic['RK4']['u'] = np.array([[4.]])

# dic['RK4']['x0'] = np.array([[1.0750, -0.3689, 364.381]])  # Para Load Model
# dic['RK4']['u0'] = np.array([1.])
# dic['RK4']['u'] = np.array([[0.0165]])

dic['RK4']['x0'] = np.array([[0.9904, 0.2002]])  # Para DFIG
dic['RK4']['u0'] = np.array([1., 0., 1., 0.2])
dic['RK4']['u'] = np.array([[0.9, 0.1, 0.97, 0.32]])

"""
Start of Estimation Process
"""

# estMTHD = __import__(dic['chsn_est1'])


# dic['TS']['p0'] = estMTHD.Function(dic, tol1)

print '\007'  # Warning Sound

print "\n\n", dic['TS']['p0'], "\n\n"

estMTHD = __import__(dic['chsn_est2'])

print estMTHD.Function(dic, tol2)

plt.show()

os.system('spd-say "Your estimation has finished"')
