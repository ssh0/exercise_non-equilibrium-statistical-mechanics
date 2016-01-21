#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto

import numpy as np
import matplotlib.pyplot as plt
from fitting import fitting


def brownian_curve_1d(N, plot=True):
    """Create basic N step brownian motion"""
    p = 0.5
    l = 1
    x0 = 0

    xi = np.random.random(N)
    xi[xi > p] = l
    xi[xi <= p] = -l

    X = [x0, ]
    for i in range(N):
        X.append(X[i] + xi[i])
    # X = [x0, x1, ... , xN]
    # len(X) == N+1
    X = np.array(X)

    if plot:
        # plot
        fig = plt.figure("Brownian motion")
        ax = fig.add_subplot(111)
        ax.axhline(color='k')
        ax.plot(range(len(X)), X, '-')
        ax.set_xlabel(r'$t$', fontsize=16)
        ax.set_ylabel(r'$x$', fontsize=16)
        ax.set_ymargin(0.05)
        fig.tight_layout()
        plt.show(block=False)

    return X


def calc_hurst(X, plot=True):
    """Calucurate hurst exponent"""

    def std(start, T):
        return np.std(X[start:start+T])

    # Tarr = [ 1, 2, 4, ... , 2^{int(log2(N))} ]
    Tarr = np.array([2**x for x in range(1, int(np.log2(len(X)-1))+1)])
    # sigma_T: list of the average of the deviation in a time-width T.
    sigma_T = [np.average([std(i, T) for i in range(N+3-T)]) for T in Tarr]

    if plot:
        # plot
        fig = plt.figure("Hurst exponent")
        ax = fig.add_subplot(111)
        ax.loglog(sigma_T, Tarr, '-o')
        ax.set_xlabel(r'$T$', fontsize=16)
        ax.set_ylabel(r'$\sigma_{x}$', fontsize=16)
        ax.set_ymargin(0.05)
        fig.tight_layout()
        plt.show(block=False)

    return (Tarr, sigma_T)


def main(N):

    def fit_func(parameter, Tarr, sigma_T):
        """Fitting function: sigma ~ T^{H}"""
        log = np.log
        c1 = parameter[0]
        c2 = parameter[1]
        residual = log(sigma_T) - c1 - c2*log(Tarr)
        return residual

    def fitted(T, c1, H):
        return np.exp(c1)*(T**H)

    # Create brownian motion and calcurate deviations for each T
    Tarr, sigma_T = calc_hurst(brownian_curve_1d(N, plot=True), plot=True)

    # Fitting
    fitting(Tarr, sigma_T,
            fit_func, [0.1, 0.5], fitted,
            xlabel=r'$T$', ylabel=r'$\sigma_{x}$',
            param_to_show={'D': 1}
            )


if __name__ == '__main__':
    # N = 16383  # = 16384(=2**14) - 1
    N = 1023  # = 1024(=2**10) - 1
    main(N)
