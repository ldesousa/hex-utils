#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
#
# Base class for synthetic surfaces.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 13-10-2016

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource

class Surface:
    
    ax = None
    X = None
    Y = None
    Z = None
    
    def fun(self, x, y):
        return 0
    
    
    def setUp(self, wire=False):
        
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        if wire:
            x = y = np.arange(0, 10, 0.1)
        else:
            x = y = np.arange(0, 2000, 5)
        self.X, self.Y = np.meshgrid(x, y)
        zs = np.array([self.fun(x,y) for x,y in zip(np.ravel(self.X), np.ravel(self.Y))])
        self.Z = zs.reshape(self.X.shape)
    
    
    def setLabels(self):
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Height')
    
    
    def plotRainbow(self):
        
        self.setUp()
        
        ls = LightSource(270, 45)
        # To use a custom hillshading mode, override the built-in shading and pass
        # in the rgb colors of the shaded surface calculated from "shade".
        rgb = ls.shade(self.Z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
        
        self.ax.plot_surface(self.X, self.Y, self.Z, facecolors=rgb)
        
        self.setLabels()
        plt.show()
     
    
    def plotWireFrame(self):  
          
        self.setUp(True)
        self.ax.plot_wireframe(self.X, self.Y, self.Z)
        self.setLabels()
        plt.show()    
        