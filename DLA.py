#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, January 2016.

from Tkinter import Tk, Canvas
import numpy as np
import time


class DLA(object):

    def __init__(self, N, view=True, color=True):
        self.R = 3
        self.sum_rxr = 0
        # radius of gyration
        self.R_g = []
        self.N = N
        self.view = view
        self.color = color
        self.L = int(self.N**(0.76)) + 2

        if self.view:
            self.default_size = 640  # default size of canvas
            self.rsize = int(self.default_size/(2 * self.L)) or 1
            fig_size = 2 * self.rsize * self.L
            self.margin = 10
            self.sub = Tk()
            canvas_w = fig_size + 2 * self.margin
            canvas_h = fig_size + 2 * self.margin
            self.canvas = Canvas(self.sub, width=canvas_w, height=canvas_h)
            self.c = self.canvas.create_rectangle
            self.update = self.canvas.update

            self.sub.title('DLA cluster')

            self.c(
                self.margin,
                self.margin,
                fig_size + self.margin,
                fig_size + self.margin,
                outline='black',
                fill='white'
            )

            self.canvas.pack()
            self.start_time = time.time()

    def grow_cluster(self):
        """Glow the DLA cluster by random walking particles.  """
        rn = np.random.rand

        # Set the lattice size
        lattice = np.zeros([self.L * 2 + 1, self.L * 2 + 1], dtype=int)
        # center of the lattice
        self.center = self.L
        # the center of lattice is occupied by a particle from start.
        lattice[self.center, self.center] = 1

        # visualization
        if self.view:
            self.c(
                (2 * self.center - self.L)*self.rsize + self.margin,
                (2 * self.center - self.L)*self.rsize + self.margin,
                (2 * (self.center + 1) - self.L)*self.rsize + self.margin - 1,
                (2 * (self.center + 1) - self.L)*self.rsize + self.margin - 1,
                outline='black',
                fill='black'
            )
            self.update()

        def reset_particle_postion():
            """Initialise the postion of the particle."""
            theta = 2 * np.pi * rn()
            x = int((self.R + 2) * np.cos(theta)) + self.center
            y = int((self.R + 2) * np.sin(theta)) + self.center
            return x, y

        def diffusion(x, y):
            """Set a partcle at outer circle and move it as random walk.
            Then, if it contacts the existing cluster, the cluster grows.
            """

            def get_distance_from_center(x, y):
                """Get the distance from the center to the particle position"""
                return np.sqrt((x - self.center)**2 + (y - self.center)**2)

            # increase the step size of RW when it is far from the center.
            #     r: distance from the center to the particle
            r = get_distance_from_center(x, y)

            #     l: step size of the random walk of the particle
            l = int(r - self.R - 2) if int(r - self.R - 2) > 0 else 1

            # Random walk
            p = rn() * 4
            if p < 1:
                x += l
            elif p < 2:
                x -= l
            elif p < 3:
                y += l
            else:
                y -= l

            # if the particle is far from the center, reset the possition.
            r = get_distance_from_center(x, y)
            if r >= 2 * self.R:
                return 2

            # if there is no occupied site near the particle, continue.
            # if judge == 0:
            if not (lattice[x-1, y] == 1 or lattice[x+1, y] == 1 or
                    lattice[x, y-1] == 1 or lattice[x, y+1] == 1):
                return x, y

            # else, the particle is occupied to the DLA cluster.
            lattice[x, y] = 1

            # visualise
            if self.view:
                if self.color:
                    colors = ['#ff0000', '#ff8000', '#ffff00', '#80ff00',
                              '#00ff00', '#00ff80', '#00ffff', '#0080ff',
                              '#0000ff', '#8000ff', '#ff00ff', '#ff0080']
                    len_colors = 12
                    n_samecolor = (self.N / len_colors) + 1
                    color = colors[n / n_samecolor]
                else:
                    color = "black"

                self.c(
                    (2 * x - self.L) * self.rsize + self.margin,
                    (2 * y - self.L) * self.rsize + self.margin,
                    (2 * (x + 1) - self.L) * self.rsize + self.margin - 1,
                    (2 * (y + 1) - self.L) * self.rsize + self.margin - 1,
                    outline=color,
                    fill=color
                )
                self.update()

            # Update R
            self.R = int(r) + 1 if int(r) + 1 > self.R else self.R
            # Update sum_rxr
            self.sum_rxr += r*r
            # Update R_g
            self.R_g.append(np.sqrt(self.sum_rxr/(len(self.R_g)+1.)))
            # Finish the random walk of the particle
            return 0

        n = 0
        while n < self.N:
            x, y = reset_particle_postion()
            while True:
                res = diffusion(x, y)
                # 0: process successfully done
                # 2: restart process
                if res == 0:
                    # increment n
                    n += 1
                    break
                elif res == 2:
                    x, y = reset_particle_postion()
                else:
                    x, y = res
        else:
            if self.view:
                # Save the canvas image
                # filename = "img/" + str(time.time()) + ".eps"
                # self.canvas.postscript(file=filename)
                # print "Save the figure to " + filename

                # Print the time
                self.end_time = time.time()
                t = self.end_time - self.start_time
                print "done; N = %d, time = " % self.N + str(t) + ' (s)'

        self.lattice = lattice
        return self.lattice
