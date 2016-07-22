'''
Created on 21 Jul 2016

@author: lads
'''

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Pit:
    
    bottom = 5
    depth = 5
    x0 = 5
    y0 = 5
    slope = 0.25
    widenning = 1
    
        
    def __init__(self, x0 = None, y0 = None, bottom = None, depth = None, 
                        slope = None, widenning = None):
    
        if x0 != None: 
            self.x0 = x0
        if y0 != None: 
            self.y0 = y0
        if bottom != None: 
            self.bottom = bottom
        if depth != None: 
            self.depth = depth
        if slope != None: 
            self.slope = slope
        if widenning != None: 
            self.widenning = widenning
            
    
    def fun(self, x, y):                      
    
        return x**2 + y**2
    
    
    def display(self):    
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = y = np.arange(0, 10, 0.1)
        X, Y = np.meshgrid(x, y)
        zs = np.array([self.fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)
        
        ax.plot_wireframe(X, Y, Z)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Height')
        
        plt.show()
    

