# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 13:32:57 2017
Parameters Evaluation using RK4 Method
University of Sao Paulo
@author: Gabriel
"""

def LoadModel2():
    
#    import datetime
#    print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    

    from numpy import *
    
    global Step, Conv
    
    if Figs:
        import matplotlib.pyplot as plt
        plt.close('all')
    
    runfile('Error.py')
    runfile('Gamma.py')
    runfile('Matrix.py')
    runfile('Classification.py')
    runfile('rk4.py')
    
    global counter, err, tolerance
    
    if Step and not Conv:
        Function()
    elif not Conv:
        while err[-1] > tolerance and counter < 50:
            Function()
    
    if err[-1] <= tolerance:
        Conv = True
    print Conv
    print "------"
    print "Iteration #%d\nError: %.6f" %(counter, err[-1])
    
#    print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
    
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
    axarr1.plot(op[:,0],op[:,2],'-.',label="Model", lw=2)
    axarr1.plot(op_real[:,0],op_real[:,2],label="Real")
    axarr1.legend(loc="lower right")
    axarr1.set_title('Reactive Power')
    axarr1.set_ylabel(r'$\Delta$Q')
    axarr1.set_xlabel("Time (s)")
    
    f.canvas.draw()


def Function():
    global Figs, TwoSteps
    global p, op, op_real, counter, err, u, evolution, x0, u0, delta_p, init_time, final_time, step
    
    p_ativo = ones_like(p)
    #Number of parameters analyzed
    num_param = p.shape[0]
    
    for i in range(0,num_param):
        op_p = rk4(init_time,final_time,step,x0,u0,p,delta_p,u,i)
        
        if i == 0:
            dopdp = (op_p - op)/delta_p[i]
        else:
            dopdp = dstack((dopdp,((op_p - op)/delta_p[i])))
            
    (gamma, dJdp) = Gamma(dopdp,op,op_real)


    #Parameters area classified due to its conditioning
    if counter == 0 and TwoSteps:
        Classification(gamma)
    
    #Parameters are modified (added DP) and stored
    DP = -linalg.solve(gamma, dJdp)
    p += p_ativo.reshape(num_param,) * DP.reshape(num_param,)
    evolution = vstack((evolution,p))
#    x0[0,0], x0[0,1] = p[6], p[7]  # IS THIS RIGHT??????
    
    #System output is reevaluated, now with the modified parameters
    op = rk4(init_time,final_time,step,x0,u0,p,delta_p,u,-1)
    
    #Error is recalculated and stored
    Jp = .5*step*Error(op_real[:,1:],op[:,1:])
    err = hstack((err, Jp))
    
    #Number of iterations is increased
    counter += 1
    
    #Plot of outputs at each iteration
    if Figs:
        PrintImg()
    else:
        print p

        