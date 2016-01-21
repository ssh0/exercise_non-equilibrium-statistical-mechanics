#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto

import numpy as np
import scipy.optimize as optimize
import matplotlib.pyplot as plt


def fitting(X, Y, fit_func, parameters, fitted, xscale='log', yscale='log',
            xlabel=r'$X$', ylabel=r'$Y$', param_to_show={'param0': 0}):
    """Fitting method to calcurate the hurst exponent."""

    # set the data set to be fitted by user input.
    # User should specify the data length by its index(not the true value).
    cut_from = int(raw_input("fit from ? (index) >>> "))
    cut_to = int(raw_input("fit to ? (index) >>> "))
    cut_X = np.array(X[cut_from:cut_to])
    cut_Y = np.array(Y[cut_from:cut_to])

    # fitting by least aquare method
    # fit_func(parameters, X, Y)
    result = optimize.leastsq(fit_func, parameters, args=(cut_X, cut_Y))
    # it returns fitted parameters
    fitted_params = result[0]
    print "fitted parameters: "
    print fitted_params

    # Plot the result and fitting func with fitted parameters
    fig = plt.figure("Fitting")
    ax = fig.add_subplot(111)
    ax.plot(X, Y, '-o')
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.set_ymargin(0.05)
    labels = '\n'.join([s + ': ' + str(fitted_params[i])
                       for s, i in param_to_show.iteritems()])
    ax.plot(cut_X, fitted(cut_X, *fitted_params), lw=2, label=labels)
    plt.legend(loc='best')
    fig.tight_layout()
    plt.show()
