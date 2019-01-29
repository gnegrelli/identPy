# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 11:24:59 2018
MVMO Method
University of Sao Paulo
@author: Gabriel
"""
   

import numpy as np
import random, copy, os, datetime
import matplotlib.pyplot as plt


#__import__('os')

#methods = {"Runge": "rk4.py"}
method = {"Runge": 'rk4'}
#runfile(methods['Runge'])

Rmethod = __import__(method["Runge"])
ERROR = __import__("Error")

os.system('cls')

plt.close('all')

#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
start_time = datetime.datetime.now()


#    runfile('rk4.py')
#runfile('Matrix.py')
#    runfile('Error.py')

### Função h
def hFunc(m, s1, s2, u):
    h = m*(1 - np.power(np.e,-u*s1)) + (1 - m)*np.power(np.e,(-(1-u)*s2))
    return h
###

population = 5
new_generation = 1

selected_genes = []

real = np.array([5., 8.])

x_o = np.array([[0, 0]])
u0 = np.array([1])
delta_p = .001*np.ones_like(real)
u = np.array([[4]])

#    op_real = rk4(0,2*np.pi,.0005,x_o,u0,real,delta_p,u,-1)
op_real = Rmethod.rk4(0,2*np.pi,.0005,x_o,u0,real,delta_p,u,-1)
#plt.plot(op_real)


lim_min = np.array([0., 0.])
lim_max = np.array([10., 10.])
f_s = 1


rndm = not True
seq_rndm = not True
moving_wndw = True
block = not True
wndw_size = 1
wndw_step = 1

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

indiv = np.zeros(len(real))
list_inds = []
error_log = []

#First generation of random genes
for i in range(population):
    for j in range(len(real)):
        indiv[j] = random.random()

#    asd = rk4(0,2*np.pi,.0005,x_o,u0,(indiv*(lim_max-lim_min)+lim_min),delta_p,u,-1)
#    list_inds.append((Error(op_real, asd), copy.copy(indiv)))
    list_inds.append((ERROR.Error(op_real, Rmethod.rk4(0,2*np.pi,.0005,x_o,u0,(indiv*(lim_max-lim_min)+lim_min),delta_p,u,-1)), copy.copy(indiv)))

list_inds.sort()
error_log.append(list_inds[0][0])

#plt.figure()
#for i in range(len(list_inds))
#plt.scatter()


gen = 0
while list_inds[0][0] > 0.01:
    
    for i in range(population):
        print "Gen. %d - Specimen #%d: %s" %(gen, i, list_inds[i][1])
    gen += 1
    
    mean = np.zeros((1,len(real)))
    var = np.zeros((1,len(real)))

    #Mean calculation
    for i in range(population):
        mean += list_inds[i][1]
    mean /= population
    
    #Variance calculation
    for i in range(population):
        var += np.power(list_inds[i][1]-mean,2)
    var /= population
    
    if 0 in var:
        print "DEU PAU!!!!"
        break
    
    print "----------------------------"
    print "Mean: ", mean
    print "Variance: ", var
    print "----------------------------\n\n"
    
    #Shape factor calculation
    s = -f_s*np.log(var)
    
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
        for j in range(len(real)):
            if j in selected_genes:
                #Mutation
                x_rnd = random.random()
                indiv[j] = hFunc(mean[0][j],s[0][j],s[0][j],x_rnd) + x_rnd*(1 - hFunc(mean[0][j],s[0][j],s[0][j],1) + hFunc(mean[0][j],s[0][j],s[0][j],0)) - hFunc(mean[0][j],s[0][j],s[0][j],0)
            else:
                #Crossover
                indiv[j] = copy.copy(list_inds[0][1][j])
        
        list_inds.append((ERROR.Error(op_real, Rmethod.rk4(0,2*np.pi,.0005,x_o,u0,(indiv*(lim_max-lim_min)+lim_min),delta_p,u,-1)), copy.copy(indiv)))
    
    list_inds = sorted(list_inds)[:population]
    error_log.append(list_inds[0][0])

#plt.show()

print "----------------------------"
print "Mean: ", mean
print "Variance: ", var
print "----------------------------" 


for i in range(population):
    print "Final Generation #%d - Specimen #%d: %s" %(gen, i, list_inds[i][1])
print "Final Error: %f" %list_inds[0][0]

plt.figure()
plt.plot(op_real[:,1:])
plt.plot(Rmethod.rk4(0,2*np.pi,.0005,x_o,u0,(list_inds[0][1]*(lim_max-lim_min)+lim_min),delta_p,u,-1)[:,1:],'--')

plt.figure()
plt.plot(error_log)
plt.title("Error evolution")
plt.xlabel("Generation")
plt.ylabel("Error")

#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
print "Elapsed time: ", datetime.datetime.now() - start_time