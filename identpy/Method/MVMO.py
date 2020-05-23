import time
import random

import numpy as np
import matplotlib.pyplot as plt

from identpy.Method import Method
from identpy.Error import wls_eval


class MVMO(Method):

    # TODO: include p_active on kwargs so user can choose which parameters to estimate
    def __init__(self, lo_p, hi_p, pop_sz=5, offsp_sz=1, max_gen=5000, d=5, delta_d=1.5, fs=1, rnd=False, seq_rnd=False,
                 mv_wndw=True, block=True, wndw_sz=1, wndw_step=1, tol=0.5, plot=False, verbose=False):

        assert isinstance(lo_p, np.ndarray), "Lower boundary of parameters must be a numpy array"
        assert isinstance(hi_p, np.ndarray), "Upper boundary of parameters must be a numpy array"
        assert len(hi_p) == len(lo_p), "Upper and lower boundaries must have the same size"
        assert wndw_sz <= len(lo_p), "Gene selection window can't be bigger than actual number of parameters"

        self.lo_p = lo_p
        self.hi_p = hi_p
        self.pop_sz = pop_sz
        self.offsp_sz = offsp_sz
        self.max_gen = max_gen
        self.d = d*np.ones_like(self.lo_p)
        self.delta_d = delta_d*np.ones_like(self.lo_p)
        self.fs = fs

        self.rnd = rnd
        self.seq_rnd = seq_rnd
        self.mv_wndw = mv_wndw
        self.block = block

        self.wndw_sz = wndw_sz
        self.wndw_step = wndw_step

        self.tol = tol

        super().__init__(plot, verbose)

    def __call__(self, parent):

        self.elapsed_time = time.process_time()

        print("------------------MVMO------------------")

        # Create figure
        if self.plot:
            fig = plt.figure()
            ax1 = fig.add_subplot(1, 1, 1)
            axis_lst = []
            for limits in list(zip(self.lo_p, self.hi_p)):
                axis_lst.extend(limits)
            ax1.axis(axis_lst)

        selected_genes = []

        num_genes = len(self.lo_p)

        # Setting gene selection window
        if self.block:
            selected_genes.append(random.randint(0, num_genes))
            for i in range(self.wndw_sz - 1):
                selected_genes.append(selected_genes[-1] + 1)
            while selected_genes[-1] >= num_genes:
                selected_genes[-1] -= num_genes
                selected_genes.sort()
        else:
            selected_genes = sorted(random.sample(range(0, num_genes), self.wndw_sz))

        list_inds = []

        # First generation of random individuals
        for i in range(self.pop_sz):
            indiv = np.zeros(num_genes)
            for j in range(num_genes):
                indiv[j] = random.random()

            # Evaluate individual
            parent.model.update_output(indiv*(self.hi_p - self.lo_p) + self.lo_p)
            list_inds.append([wls_eval(parent.model.y, parent.y_meas), indiv])

        # Sorting individuals and storing error
        list_inds.sort(key=lambda x: x[0])
        self.error_log.append(list_inds[0][0])

        if self.verbose:
            print("Genes selected at the beginning: ", selected_genes)
            print("Error :", self.error_log[-1])

        nonzero_var = None
        self.mean = np.zeros(num_genes)
        var = np.zeros(num_genes)

        # Iteration process
        while self.error_log[-1] > self.tol and self.counter < self.max_gen:

            # Redraw graph
            if self.plot:
                plt.pause(.1)
                ax1.clear()
                ax1.axis(axis_lst)

            for i, indiv in enumerate(list_inds):
                # Print generation
                if self.verbose:
                    print("Gen. %d - Specimen #%d: %s" % (self.counter, i, indiv[1]))

                # Plot individuals
                if self.plot:
                    plot_indiv = indiv[1]*(self.hi_p - self.lo_p) + self.lo_p
                    ax1.plot(plot_indiv[0], plot_indiv[1],
                             MVMO.color[i % len(MVMO.color)] + MVMO.marker[i % len(MVMO.marker)])

            # Obtain mean and variance values of parameters
            individuals = [i for err, i in list_inds]
            self.mean = np.mean(individuals, axis=0)
            var = np.var(individuals, axis=0)

            # Repeat last non-null variance in case the new one is null
            if 0 in var:
                for i in np.where(var == 0)[0]:
                    var[i] = nonzero_var[i]
            nonzero_var = var

            if self.verbose:
                print("----------------------------")
                print("Mean: ", self.mean)
                print("Variance: ", var)
                print("Error: ", self.error_log[-1])
                print("----------------------------\n\n")

            self.counter += 1

            # Shape factor calculation - At every 100 iterations fs is set to zero in order to provide a broad search
            if self.counter % 97 != 0:
                self.s = -self.fs*np.log(var)
                self.sf = np.array([self.s, self.s])

                # TODO: Vary shape factor using d and Delta_d
                # counts = 0
                # for v in np.greater(s, self.d):
                #     if v:
                #         self.d[0][counts] *= self.delta_d[0][counts]
                #         sf[1][counts] = self.d[0][counts]
                #     else:
                #         self.d[0][counts] /= self.delta_d[0][counts]
                #         sf[0][counts] = self.d[0][counts]
                #     counts += 1
            else:
                self.sf = 0*np.ones(self.sf.shape)

            # Gene selection for mutation
            # Random selection
            if self.rnd:
                # First gene sequential and remaining random
                if self.seq_rnd:
                    selected_genes[0] += self.wndw_step
                    while selected_genes[0] >= num_genes:
                        selected_genes[0] -= num_genes
                    other_genes = [i for i in range(num_genes) if i != selected_genes[0]]
                    selected_genes[1:] = sorted(random.sample(other_genes, self.wndw_sz - 1))
                # All genes random
                else:
                    selected_genes = sorted(random.sample(range(0, num_genes), self.wndw_sz))
            # Moving window selection
            elif self.mv_wndw:
                selected_genes += self.wndw_step*np.ones(len(selected_genes))
                while selected_genes[-1] >= num_genes:
                    selected_genes[-1] -= num_genes
                    selected_genes.sort()

            if self.verbose:
                print("Genes selected for mutation: ", selected_genes)

            # Creating a new generation
            for i in range(self.offsp_sz):
                indiv = np.zeros(num_genes)
                for j in range(num_genes):
                    # Mutation
                    if j in selected_genes:
                        x_rnd = random.random()
                        h_1 = self.h_function(1, j)
                        h_0 = self.h_function(0, j)
                        h_x = self.h_function(x_rnd, j)
                        indiv[j] = h_x + (1 - h_1 + h_0)*x_rnd - h_0
                    # Crossover
                    else:
                        indiv[j] = list_inds[0][1][j]

                # Evaluate individual
                parent.model.update_output(indiv * (self.hi_p - self.lo_p) + self.lo_p)
                list_inds.append([wls_eval(parent.model.y, parent.y_meas), indiv])

            # Sorting new list of individuals and discarding the worst individuals
            list_inds = sorted(list_inds, key=lambda x: x[0])[:self.pop_sz]
            self.error_log.append(list_inds[0][0])

            # Increase scaling factor fs in 1% after each iteration, capping it around 15
            if self.fs < 15:
                self.fs *= 1.01

        # At the end of iteration process, mean, variance and final error value are presented
        if self.verbose:
            print("----------------------------")
            print("Mean: ", self.mean)
            print("Variance: ", var)
            print("Error: ", self.error_log[-1])
            print("----------------------------")

            # Final generation with fittest individuals
            for i, indiv in enumerate(list_inds):
                print("Final Generation #%d - Specimen #%d: %s" % (self.counter, i, indiv[1]))
            print("Final Error: %f" % self.error_log[-1])

        self.elapsed_time = time.process_time() - self.elapsed_time
        print("MVMO elapsed time: {0:.2f} s".format(self.elapsed_time))

        # Set parameters of model according to best individual found
        parent.model.update_output(list_inds[0][1] * (self.hi_p - self.lo_p) + self.lo_p)

    # Mapping function h
    def h_function(self, u, i):

        m = self.mean[i]
        s1 = self.sf[0][i]
        s2 = self.sf[1][i]

        return m*(1 - np.power(np.e, -u*s1)) + (1 - m)*np.power(np.e, (-(1 - u)*s2))
