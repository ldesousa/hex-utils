'''
Created on 21 Jul 2016

@author: lads
'''

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Pit:
    
    peakValue = 5
    peakPoint = 5
    
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
    

