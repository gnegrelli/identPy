# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 11:24:59 2018
MVMO Function
University of Sao Paulo
@author: Gabriel
"""
### Função h
def hFunc(m, s1, s2, u):
    
    import numpy as np
    
    h = m*(1 - np.power(np.e,-u*s1)) + (1 - m)*np.power(np.e,(-(1-u)*s2))
    return h
###

### Sorting mehtod
def takeFirst(elem):
    return elem[0]
###

def Function(dic, tolerance):
        
    import numpy as np
    import random, copy, datetime
    import matplotlib.pyplot as plt
    

    start_time = datetime.datetime.now()
    
    print "------------------MVMO------------------"
        
    SIM = __import__(dic['chsn_sim'])
    ERROR = __import__(dic['chsn_err'])
    

    population = dic['MVMO']['population']
    new_generation = dic['MVMO']['new_gen']
    
    selected_genes = []
    
    if not dic['import_data']:
        op_real = SIM.rk4(dic, dic['real'])
    else:
        op_real = dic['u'][:,[0,3,4]]
    
#    plt.figure(1)
#    plt.plot(op_real[:,1], label = str(real))
#    plt.legend()
#    
#    plt.figure(2)    
#    plt.plot(op_real[:,2], label = str(real))
#    plt.legend()
#    return
    
    lim_min = dic['MVMO']['p_min']
    lim_max = dic['MVMO']['p_max']
    fs = dic['MVMO']['fs']
    
    
    rndm = dic['MVMO']['rndm']
    seq_rndm = dic['MVMO']['seq_rndm']
    moving_wndw = dic['MVMO']['moving_wndw']
    block = dic['MVMO']['block']
    wndw_size = dic['MVMO']['wndw_size']
    wndw_step = dic['MVMO']['wndw_step']

    
    if block:
        selected_genes.append(random.randint(0,len(lim_min)))
        for i in range(1,wndw_size):
            selected_genes.append(selected_genes[-1] + 1)
        while selected_genes[-1] >= len(lim_min):
            selected_genes[-1] -= len(lim_min)
            selected_genes.sort()
    else:
        selected_genes = sorted(random.sample(range(0,len(lim_min)),wndw_size))
    print "Genes selected at the beginning: ", selected_genes

    
    indiv = np.zeros(len(lim_min))
    list_inds = []
#    error_log = []

    
    #First generation of random genes
    for i in range(population):
        for j in range(len(lim_min)):
            indiv[j] = random.random()
    
        list_inds.append((ERROR.Error(op_real, SIM.rk4(dic,(indiv*(lim_max-lim_min)+lim_min))), copy.copy(indiv)))
    
    list_inds.sort(key = takeFirst)
#    error_log.append(list_inds[0][0])
    dic['error_log'] =  np.hstack((dic['error_log'], list_inds[0][0]))
    
    print "error :", dic['error_log'][-1]
        
    nonzero_var = None
    mean = None
    var = None
    
    while dic['error_log'][-1] > tolerance and dic['MVMO']['counter'] < dic['MVMO']['max_gen']:
        
                
        for i in range(population):
            print "Gen. %d - Specimen #%d: %s" %(dic['MVMO']['counter'], i, list_inds[i][1])
        dic['MVMO']['counter'] += 1
        
        mean = np.zeros((1,len(lim_min)))
        var = np.zeros((1,len(lim_min)))
    
        #Mean calculation
        for i in range(population):
            mean += list_inds[i][1]
        mean /= population
        
        #Variance calculation
        for i in range(population):
            var += np.power(list_inds[i][1] - mean,2)
        var /= population
        
        if 0 in var:
            var = nonzero_var
        nonzero_var = copy.copy(var)
        
        print "----------------------------"
        print "Mean: ", mean
        print "Variance: ", var
        print "Error: ", dic['error_log'][-1]
        print "----------------------------\n\n"
        
        #Shape factor calculation
        s = -fs*np.log(var)
        
    #    h=[]
    #    for i in np.linspace(0,1,101):
    #        h.append(hFunc(mean[0][0],s[0][0],s[0][0],i) + i*(1 - hFunc(mean[0][0],s[0][0],s[0][0],1) + hFunc(mean[0][0],s[0][0],s[0][0],0)) - hFunc(mean[0][0],s[0][0],s[0][0],0))
    #    plt.plot(np.linspace(0,1,101),h)
    #    plt.ylabel("Mutated gene")
    #    plt.xlabel("Random gene")
    #    plt.legend(loc='best')
    #    plt.show()
        
        #Gene selection for mutation
        if rndm:
            if not seq_rndm:
                selected_genes = sorted(random.sample(range(0,len(lim_min)),wndw_size))
            else:
                selected_genes[0] += wndw_step
                while selected_genes[0] >= len(lim_min):
                    selected_genes[0] -= len(lim_min)                             
                selected_genes[1:] = sorted(random.sample(range(0,selected_genes[0])+range(selected_genes[0]+1,len(lim_min)),wndw_size-1))
        elif moving_wndw:
            selected_genes += wndw_step*np.ones(len(selected_genes))
            while selected_genes[-1] >= len(lim_min):
                selected_genes[-1] -= len(lim_min)
                selected_genes.sort()
        print "Genes selected for mutation: ", selected_genes
        
        
        #Creating a new geration
        for i in range(new_generation):
            for j in range(len(lim_min)):
                if j in selected_genes:
                    #Mutation
                    x_rnd = random.random()
                    indiv[j] = hFunc(mean[0][j],s[0][j],s[0][j],x_rnd) + x_rnd*(1 - hFunc(mean[0][j],s[0][j],s[0][j],1) + hFunc(mean[0][j],s[0][j],s[0][j],0)) - hFunc(mean[0][j],s[0][j],s[0][j],0)
                else:
                    #Crossover
                    indiv[j] = copy.copy(list_inds[0][1][j])
            
            list_inds.append((ERROR.Error(op_real, SIM.rk4(dic,(indiv*(lim_max-lim_min)+lim_min))), copy.copy(indiv)))
        
        list_inds = sorted(list_inds, key = takeFirst)[:population]
#        error_log.append(list_inds[0][0])
        dic['error_log'] =  np.hstack((dic['error_log'], list_inds[0][0]))
        
#        print error_log
#        print dic['error_log']

    
    print "----------------------------"
    print "Mean: ", mean
    print "Variance: ", var
    print "Error: ", dic['error_log'][-1]
    print "----------------------------" 
    
    
    for i in range(population):
        print "Final Generation #%d - Specimen #%d: %s" %(dic['MVMO']['counter'], i, list_inds[i][1])
    print "Final Error: %f" %dic['error_log'][-1]
    
    plt.figure(1)
    plt.plot(op_real[:,0], op_real[:,1], linewidth=2.5, color="y", label = "Real System")
    plt.plot(SIM.rk4(dic,(list_inds[0][1]*(lim_max-lim_min)+lim_min))[:,0],SIM.rk4(dic,(list_inds[0][1]*(lim_max-lim_min)+lim_min))[:,1],"--", label = "MVMO")
    plt.title("Active Power")
    plt.xlabel("Time (s)")
    plt.ylabel(r'$\Delta$P')
    
    plt.figure(2)
    plt.plot(op_real[:,0], op_real[:,2], linewidth=2.5, color="y", label = "Real System")
    plt.plot(SIM.rk4(dic,(list_inds[0][1]*(lim_max-lim_min)+lim_min))[:,0],SIM.rk4(dic,(list_inds[0][1]*(lim_max-lim_min)+lim_min))[:,2], "--", label = "MVMO")
    plt.title("Reactive Power")
    plt.xlabel("Time (s)")
    plt.ylabel(r'$\Delta$Q')
    
    plt.figure(3)
    plt.plot(range(0,dic['MVMO']['counter'] + 1), dic['error_log'][:dic['MVMO']['counter'] + 1], label = "MVMO")
    plt.title("Error evolution")
    plt.xlabel("Generation")
    plt.ylabel("Error")
    
    print "MVMO elapsed time: ", datetime.datetime.now() - start_time

    return (list_inds[0][1]*(lim_max-lim_min)+lim_min)   