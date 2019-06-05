# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 11:24:59 2018
MVMO Estimation Method
University of Sao Paulo
@author: Gabriel
"""

# H Function: Mapping function of mutation
def hFunc(m, s1, s2, u):

    import numpy as np
    
    h = m*(1 - np.power(np.e, -u*s1)) + (1 - m)*np.power(np.e, (-(1-u)*s2))
    return h

# Sorting method: Sorts individuals by lowest error (first element on the list of individuals)
def takeFirst(elem):

    return elem[0]


# MVMO Estimation Process
def Function(dic, tolerance):
        
    import numpy as np
    import random
    import copy
    import datetime
    import matplotlib.pyplot as plt

    # Timestamp for MVMO Method
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
        op_real = dic['u'][:, [0, 3, 4]]
    
    # plt.figure(1)
    # plt.plot(op_real[:, 1], label = str(real))
    # plt.legend()

    # plt.figure(2)
    # plt.plot(op_real[:, 2], label = str(real))
    # plt.legend()
    
    lim_min = dic['MVMO']['p_min']
    lim_max = dic['MVMO']['p_max']

    fs = dic['MVMO']['fs']
    d = np.array([dic['MVMO']['d']*np.ones(lim_min.shape)])
    dd = np.array([dic['MVMO']['delta_d']*np.ones(lim_min.shape)])

    rndm = dic['MVMO']['rndm']
    seq_rndm = dic['MVMO']['seq_rndm']
    moving_wndw = dic['MVMO']['moving_wndw']
    block = dic['MVMO']['block']
    wndw_size = dic['MVMO']['wndw_size']
    wndw_step = dic['MVMO']['wndw_step']

    # First set of genes for mutation
    if block:
        selected_genes.append(random.randint(0, len(lim_min)))
        for i in range(1, wndw_size):
            selected_genes.append(selected_genes[-1] + 1)
        while selected_genes[-1] >= len(lim_min):
            selected_genes[-1] -= len(lim_min)
            selected_genes.sort()
    else:
        selected_genes = sorted(random.sample(range(0, len(lim_min)), wndw_size))
    # print "Genes selected at the beginning: ", selected_genes

    indiv = np.zeros(len(lim_min))
    list_inds = []

    # First generation of random genes
    for i in range(population):
        for j in range(len(lim_min)):
            indiv[j] = random.random()
    
        list_inds.append((.5*dic['TS']['step']*ERROR.Error(op_real, SIM.rk4(dic, (indiv*(lim_max-lim_min)+lim_min))), copy.copy(indiv)))

    # Sorting and error calculation of first individuals
    list_inds.sort(key=takeFirst)
    dic['error_log'] = np.hstack((dic['error_log'], list_inds[0][0]))
    
    # print "error :", dic['error_log'][-1]
        
    nonzero_var = None
    mean = None
    var = None

    # Iteration process
    while dic['error_log'][-1] > tolerance and dic['MVMO']['counter'] < dic['MVMO']['max_gen']:

        # for i in range(population):
        #     print "Gen. %d - Specimen #%d: %s" % (dic['MVMO']['counter'], i, list_inds[i][1])
        dic['MVMO']['counter'] += 1

        mean = np.zeros((1, len(lim_min)))
        var = np.zeros((1, len(lim_min)))

        # Mean calculation
        for i in range(population):
            mean += list_inds[i][1]
        mean /= population
        
        # Variance calculation
        for i in range(population):
            var += np.power(list_inds[i][1] - mean, 2)
        var /= population

        # Repeat last non-null variance in case the new one is null
        if 0 in var:
            for i in np.where(var == 0)[1]:
                # print var
                var[0][i] = nonzero_var[0][i]
                # print var
        nonzero_var = copy.copy(var)
        
        # print "----------------------------"
        # print "Mean: ", mean
        # print "Variance: ", var
        # print "Error: ", dic['error_log'][-1]
        # print "----------------------------\n\n"
        
        # Shape factor calculation - At every 100 iterations fs is set to zero in order to provide a broad search
        if dic['MVMO']["counter"] % 97. == 0.:
            sf = 0*np.ones(sf.shape)
        else:
            s = -fs*np.log(var)

            sf = np.array([s[0], s[0]])

            counts = 0
            for v in np.greater(s, d)[0]:
                if v:
                    d[0][counts] *= dd[0][counts]
                    sf[1][counts] = d[0][counts]
                else:
                    d[0][counts] /= dd[0][counts]
                    sf[0][counts] = d[0][counts]
                counts += 1

        # h = []
        # for i in np.linspace(0, 1, 101):
        #     h.append(hFunc(mean[0][0], sf[0][0], sf[1][0], i) + i*(1 - hFunc(mean[0][0], sf[0][0], sf[1][0], 1) + hFunc(mean[0][0], sf[0][0], sf[1][0], 0)) - hFunc(mean[0][0], sf[0][0], sf[1][0], 0))
        # plt.plot(np.linspace(0, 1, 101), h)
        # plt.ylabel("Mutated gene")
        # plt.xlabel("Random gene")
        # plt.legend(loc='best')
        # plt.show()
        
        # Gene selection for mutation
        if rndm:
            if not seq_rndm:
                selected_genes = sorted(random.sample(range(0, len(lim_min)), wndw_size))
            else:
                selected_genes[0] += wndw_step
                while selected_genes[0] >= len(lim_min):
                    selected_genes[0] -= len(lim_min)                             
                selected_genes[1:] = sorted(random.sample(range(0, selected_genes[0])+range(selected_genes[0]+1, len(lim_min)), wndw_size-1))
        elif moving_wndw:
            selected_genes += wndw_step*np.ones(len(selected_genes))
            while selected_genes[-1] >= len(lim_min):
                selected_genes[-1] -= len(lim_min)
                selected_genes.sort()

        # print "Genes selected for mutation: ", selected_genes
        
        # Creating a new generation
        for i in range(new_generation):
            for j in range(len(lim_min)):
                if j in selected_genes:
                    # Mutation
                    x_rnd = random.random()
                    indiv[j] = hFunc(mean[0][j], s[0][j], s[0][j], x_rnd) + x_rnd*(1 - hFunc(mean[0][j], s[0][j], s[0][j], 1) + hFunc(mean[0][j], s[0][j], s[0][j], 0)) - hFunc(mean[0][j], s[0][j], s[0][j], 0)
                else:
                    # Crossover
                    indiv[j] = copy.copy(list_inds[0][1][j])
            
            list_inds.append((.5*dic['TS']['step']*ERROR.Error(op_real, SIM.rk4(dic, (indiv*(lim_max-lim_min)+lim_min))), copy.copy(indiv)))

        # Sorting new list of individuals and discarding the worst individuals
        list_inds = sorted(list_inds, key=takeFirst)[:population]
        dic['error_log'] = np.hstack((dic['error_log'], list_inds[0][0]))

        # Increase scaling factor fs in 1% after each iteration, capping it around 15
        if fs < 15:
            fs *= 1.01

    # At the end of iteration process, mean, variance and final error value are presented
    # print "----------------------------"
    # print "Mean: ", mean
    # print "Variance: ", var
    # print "Error: ", dic['error_log'][-1]
    # print "----------------------------"

    # Final generation with fittest individuals
    # for i in range(population):
    #     print "Final Generation #%d - Specimen #%d: %s" % (dic['MVMO']['counter'], i, list_inds[i][1])
    # print "Final Error: %f" % dic['error_log'][-1]

    # Plot y1 real and from MVMO
    # plt.figure(1)
    # plt.plot(op_real[:, 0], op_real[:, 1], linewidth=3, color="y", label="Real System")
    # plt.plot(SIM.rk4(dic, (list_inds[0][1]*(lim_max - lim_min) + lim_min))[:, 0], SIM.rk4(dic, (list_inds[0][1]*(lim_max - lim_min) + lim_min))[:, 1], "-.", label="MVMO")
    # plt.title("Active Power")
    # plt.xlabel("Time (s)")
    # plt.ylabel(r'$\Delta$P')

    # Plot y2 real and from MVMO
    # plt.figure(2)
    # plt.plot(op_real[:, 0], op_real[:, 2], linewidth=3, color="y", label="Real System")
    # plt.plot(SIM.rk4(dic, (list_inds[0][1]*(lim_max-lim_min) + lim_min))[:, 0], SIM.rk4(dic, (list_inds[0][1]*(lim_max - lim_min) + lim_min))[:, 2], "-.", label="MVMO")
    # plt.title("Reactive Power")
    # plt.xlabel("Time (s)")
    # plt.ylabel(r'$\Delta$Q')

    # Plot error evolution
    # plt.figure(3)
    # if (dic['error_log'].size - dic['MVMO']['counter'] - 1) == 0:
    #     plt.plot(range(dic['error_log'].size - dic['MVMO']['counter'] - 1, dic['error_log'].size), dic['error_log'][dic['error_log'].size - dic['MVMO']['counter'] - 1:dic['error_log'].size], label="MVMO")
    # else:
    #     plt.plot(range(dic['error_log'].size - dic['MVMO']['counter'] - 2, dic['error_log'].size - 1), dic['error_log'][dic['error_log'].size - dic['MVMO']['counter'] - 1:dic['error_log'].size], label="MVMO")
    # plt.title("Error evolution")
    # plt.xlabel("Generation")
    # plt.ylabel("Error")

    print "MVMO elapsed time: ", datetime.datetime.now() - start_time

    # Return best individual
    return list_inds[0][1]*(lim_max-lim_min) + lim_min
