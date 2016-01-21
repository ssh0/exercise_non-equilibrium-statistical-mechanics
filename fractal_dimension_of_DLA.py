#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto

import matplotlib.pyplot as plt
import numpy as np
from SetParameter import SetParameter
from DLA import DLA
from fitting import fitting


class Main(object):

    def __init__(self):
        import sys
        self.sp = SetParameter()
        self.N = None
        self.dla = None

        self.sp.show_setting_window(
            [
                {'N': 200}
            ],
            [
                {'start': self.grow_cluster},
                {'plot graph': self.plot__N_R},
                {'calcurate D': self.fit_to_powerlow},
                {'save': self.save_to_file},
                {'quit': sys.exit}
            ]
        )

    def grow_cluster(self):
        """Create a DLA cluster with N particles by dla.grow_cluster method."""
        self.N = int(self.sp.entry[0].get())
        self.dla = DLA(self.N)
        self.lattice = self.dla.grow_cluster()
        self.center = self.dla.center

    def plot__N_R(self):
        """Plot a N-R_g graph to calcurate DLA cluster's fractal dimension."""
        self.N = int(self.sp.entry[0].get())
        self.dla = DLA(self.N)
        self.lattice = self.dla.grow_cluster()
        self.center = self.dla.center
        self.Narr = np.array([2**x for x in range(1, int(np.log2(self.N))+1)])
        self.R_g = np.array([self.dla.R_g[n-1] for n in self.Narr])

        # plot
        fig = plt.figure("Fractal Dimension")
        self.ax = fig.add_subplot(111)
        self.ax.loglog(self.R_g, self.Narr, '-o')
        self.ax.set_xlabel(r'$R_{g}$', fontsize=16)
        self.ax.set_ylabel(r'$N$', fontsize=16)
        self.ax.set_ymargin(0.05)
        fig.tight_layout()
        plt.show()

    def fit_to_powerlow(self):
        """Fitting method to calcurate the fractal dimension of DLA cluster."""

        def fit_func(parameter0, R_g, Narr):
            """Fitting function: Narr ~ R_{g}^{D}"""
            log = np.log
            c1 = parameter0[0]
            c2 = parameter0[1]
            residual = log(Narr) - c1 - c2*log(R_g)
            return residual

        def fitted(R, c1, D):
            return np.exp(c1)*(R**D)

        fitting(self.R_g, self.Narr,
                fit_func, [0.1, 1.7], fitted,
                xlabel=r'$R_{g}$', ylabel=r'$N$',
                param_to_show={'D': 1}
                )

    def save_to_file(self):
        """Save the figure of the DLA cluster with eps format."""
        import tkFileDialog
        import os

        if self.dla is None:
            print "No figure exists."
            return

        ftype = [('eps flle', '*.eps'), ('all files', '*')]
        filename = tkFileDialog.asksaveasfilename(
            filetypes=ftype,
            initialdir=os.getcwd(),
            initialfile="figure_1.eps"
        )
        if filename is None:
            return
        self.dla.canvas.postscript(file=filename)


if __name__ == '__main__':
    Main()
