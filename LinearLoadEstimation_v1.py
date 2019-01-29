# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 02:16:07 2017
Parameters Evaluation using RK4 Method
University of Sao Paulo
@author: Gabriel
"""

#Clearing system, importing libraries and setting flags
from os import system
system('cls')

import datetime

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

from numpy import *
import copy

convergence = False
print_figs = not False
step_by_step = False

if print_figs:
    import matplotlib.pyplot as plt
    plt.close('all')


#Run function files
runfile('Error.py')
runfile('Gamma.py')
runfile('Matrix.py')
runfile('Classification.py')
runfile('rk4.py')

#Real parameters
X_r = 0.2089
Xl_r = 0.0446
To_r = 0.0963
M_r = 0.0139
Gs_r = 4.1358
Bs_r = 2.8004
E0_r = 1.0750
delta0_r = -0.3689
omega0_r = 364.381
p_real = array([X_r, Xl_r, To_r, M_r, Gs_r, Bs_r, E0_r, delta0_r])#, omega0_r])

#Entrances
u = array([[0.0165]])

#Guessed parameters
k = .82

X = k*X_r
Xl = k*Xl_r
To = k*To_r
M = k*M_r
Gs = k*Gs_r
Bs = k*Bs_r
E0 = k*E0_r
delta0 = k*delta0_r
omega0 = 364
p = array([X, Xl, To, M, Gs, Bs, E0, delta0])#, omega0])

#Initial values of voltage magnitude and angle and angular speed
x_o = array([[1.0750, -0.3689, 364.381]])

#Initial values of line voltage
u0 = array([1])

#Variation on parameters in order to evaluate sensibilities
delta_p = .001*ones_like(p)

#Method presets
init_time = 0
final_time = .5
step = .0005


#Number of parameters analyzed
num_param = p.shape[0]

#Variable storing parameters evolution at each iteration
evolution = copy.copy(p)

#Loop Restrictions
tolerance = .0005   #Error tolerance
count = 0           #Number of iterations
p_ativo = ones_like(p)

#Real System Behaviour
op_real = rk4(init_time,final_time,step,x_o,u0,p_real,delta_p,u,-1)

#Chosen Parameters' System Beahviour
op = rk4(init_time,final_time,step,x_o,u0,p,delta_p,u,-1)

pold = copy.copy(op)

#Error Evaluation (Least-Mean Square)
Jp = .5*step*Error(op_real[:,1:],op[:,1:])
err = Jp          #Variable Storing Error Evolution


if print_figs:    
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(op[:,0],op[:,1],'-.',label="Model", lw=5)
    axarr[0].plot(op_real[:,0],op_real[:,1],label="Real")
    axarr[0].set_title('Real Power')
    axarr[0].set_ylabel(r'$\Delta$P')
    axarr[0].set_xlabel("Time (s)")
    axarr[0].legend(loc="upper right")
    
    axarr[1].plot(op[:,0],op[:,2],'-.',label="Model",lw=5)
    axarr[1].plot(op_real[:,0],op_real[:,2],label="Real")
    axarr[1].set_title('Reactive Power')
    axarr[1].set_ylabel(r'$\Delta$Q')
    axarr[1].set_xlabel("Time (s)")
    axarr[1].legend(loc="upper right")

    f.show()
    plt.pause(0.0001)


"""
 The following 'while' loop builds matrices containing the sensibilities 
 (derivatives) of each state variable for each parameter in order to 
 calculate both the Gamma Function and the Error sensisibility. Later, it
 refreshes the paramenters values and recalculates the error.
"""

while Jp > tolerance and count < 50:

#If analysis at each iteration is needed, this will pause at each run
    if step_by_step:
        raw_input("Press Enter to continue.")

    if count == 10:
        p_ativo = ones_like(p)
    
    """
    This 'for' loop builds matrices containing the sensibilities for each
    parameter. The 3D Matrix 'dopdp' contains all of them, e.g.,
    dopdp(:,:,1) contains the Matrix of Sensibility for parameter p(1), in
    this case, 'b'.
    """
    for i in range(0,num_param):
        op_p = rk4(init_time,final_time,step,x_o,u0,p,delta_p,u,i)
    
        if i == 0:
            dopdp = (op_p - op)/delta_p[i]
        else:
            dopdp = dstack((dopdp,((op_p - op)/delta_p[i])))


    #Gamma Function and dJ/dp are calculated by the following function
    (gamma, dJdp) = Gamma(dopdp,op,op_real)


    #Parameters area classified due to its conditioning
    if count == 0:
        Classification(gamma)


    #Parameters are modified (added DP) and stored
    DP = -linalg.solve(gamma, dJdp)
    p += p_ativo.reshape(num_param,) * DP.reshape(num_param,)
    evolution = vstack((evolution,p))

    print p


    #System output is reevaluated, now with the modified parameters
    op = rk4(init_time,final_time,step,x_o,u0,p,delta_p,u,-1)


    #Error is recalculated and stored
    Jp = .5*step*Error(op_real[:,1:],op[:,1:])
    err = hstack((err, Jp))


    #Number of iterations is increased
    count += 1


    #Plot of outputs at each iteration
    if print_figs:
        axarr[0].cla()
        axarr[0].plot(op[:,0],op[:,1],'-.',label="Model",lw=5)
        axarr[0].plot(op_real[:,0],op_real[:,1],label="Real")        
        axarr[0].set_title('Real Power')
        axarr[0].set_ylabel(r'$\Delta$P')
        axarr[0].set_xlabel("Time (s)")
        axarr[0].legend(loc="upper right")
    
    
        axarr[1].cla()
        axarr[1].plot(op[:,0],op[:,2],'-.',label="Model",lw=5)
        axarr[1].plot(op_real[:,0],op_real[:,2],label="Real")        
        axarr[1].set_title('Reactive Power')
        axarr[1].set_ylabel(r'$\Delta$Q')
        axarr[1].set_xlabel("Time (s)")
        axarr[1].legend(loc="upper right")
    
        plt.draw()
        plt.pause(0.0001)

print "\n\nNumber of iterations: %d\n\n" %count
print p
print p_real

if print_figs:
    plt.figure()
    plt.plot(pold[:,0],pold[:,1],'.',label="Initial",lw=2.5)
    plt.plot(op[:,0],op[:,1],'-.',label="Final", lw=5)
    plt.plot(op_real[:,0],op_real[:,1],label="Real")
    plt.title('Real Power')
    plt.ylabel(r'$\Delta$P')
    plt.xlabel("Time (s)")
    plt.legend()

print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))