#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Base class for synthetic surfaces inspired in the EAT2 test.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 30-05-2016

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource

class Surface:

    oo = 9.2676
    y_top = 9.1208
    xn = 8.2776
    yn = 10.1108
    dx = (xn - oo) / 1980.0
    dy = -((yn - y_top) / 1980.0) 
    
    depth = 1.3
    slope = 5
    widenning = 300
    
    # The pit functions
    p1  = None
    p2  = None
    p3  = None
    p4  = None
    
    p5  = None
    p6  = None
    p7  = None
    p8  = None
    
    p9  = None
    p10 = None
    p11 = None
    p12 = None
    
    p13 = None
    p14 = None
    p15 = None
    p16 = None
    
    
    #def __init__(self):
     
    
    def fun(self, x, y):

        z = []
        
        z.append(self.p1.fun(x, y,  True))
        z.append(self.p2.fun(x, y,  True))
        z.append(self.p3.fun(x, y,  True))
        z.append(self.p4.fun(x, y,  True))
        
        z.append(self.p5.fun(x, y,  True))
        z.append(self.p6.fun(x, y,  True))
        z.append(self.p7.fun(x, y,  True))
        z.append(self.p8.fun(x, y,  True))
            
        z.append(self.p9.fun(x, y,  True))
        z.append(self.p10.fun(x, y,  True))
        z.append(self.p11.fun(x, y,  True))
        z.append(self.p12.fun(x, y,  True))
            
        z.append(self.p13.fun(x, y,  True))
        z.append(self.p14.fun(x, y,  True))
        z.append(self.p15.fun(x, y,  True))
        z.append(self.p16.fun(x, y,  True))
            
        z.append(self.oo + ((x - 10) * self.dx) - ((y - 10) * self.dy))
        
        z.sort()
        return z[0]


    def plot(self):
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = y = np.arange(0, 2000, 5)
        X, Y = np.meshgrid(x, y)
        zs = np.array([self.fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)
        
        ls = LightSource(270, 45)
        # To use a custom hillshading mode, override the built-in shading and pass
        # in the rgb colors of the shaded surface calculated from "shade".
        rgb = ls.shade(Z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
        
        ax.plot_surface(X, Y, Z, facecolors=rgb)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Height')
        
        plt.show()

    
        