# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 14:59:34 2017
Parameters Evaluation using RK4 Method
University of Sao Paulo
@author: Gabriel
"""

def Precalc():    
    
    from os import system
#    system('cls')
    
    from numpy import *
    
    global Figs, Step, Conv
    
    master_slave = False
    
    if Figs:
        import matplotlib.pyplot as plt
        plt.close('all')

    runfile('rk4.py')
    runfile('Matrix.py')
    runfile('Error.py')
    
    global p, op, op_real, err, u, x0, u0, delta_p, init_time, final_time, step
    
    
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
    
    
    op_real = rk4(init_time,final_time,step,x0,u0,p_real,delta_p,u,-1)
    
    op = rk4(init_time,final_time,step,x0,u0,p,delta_p,u,-1)
    print op_real
    print op
    
    Jp = .5*step*Error(op_real[:,1:],op[:,1:])
    err = hstack((err, Jp))         #Variable Storing Error Evolution


    if Figs:
        PrintImg()
    else:
        print p
        

def PrintImg():
    global axarr0, axarr1
    
    axarr0.cla()
    axarr0.plot(op[:,0],op[:,1],'-.',label="Model",lw=2)
    axarr0.plot(op_real[:,0],op_real[:,1],label="Real")
    axarr0.legend(loc="lower right")
    axarr0.set_title('Real Power')
    axarr0.set_ylabel(r'$\Delta$P')
    axarr0.set_xlabel("Time (s)")

    axarr1.cla()
    axarr1.plot(op[:,0],op[:,2],'-.',label="Model",lw=2)
    axarr1.plot(op_real[:,0],op_real[:,2],label="Real")
    axarr1.legend(loc="lower right")
    axarr1.set_title('Reactive Power')
    axarr1.set_ylabel(r'$\Delta$Q')
    axarr1.set_xlabel("Time (s)")
    
    f.canvas.draw()