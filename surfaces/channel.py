'''
Created on 12 Oct 2016

@author: desouslu
'''

import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Channel:
    
    angle = 30
    slope = 0.25
    centre_x = 5
    centre_y = 5
    centre_z = 5
    radius = 0.5
    depth = 1
    
        
    def __init__(self, slope = None):
    
        if slope != None: 
            self.slope = slope
        
    
    def fun(self, x, y):   
        
        plane = ((self.centre_x - x) * self.slope + self.centre_z) * math.cos(math.radians(self.angle)) + \
                ((self.centre_y - y) * self.slope + self.centre_z) * math.sin(math.radians(self.angle))                    
               
        centre = (x - self.centre_x) / math.sin(math.radians(90 - self.angle)) * \
                 math.sin(math.radians(self.angle))
    
        if  (y - self.centre_y) >= (centre - self.radius) and \
            (y - self.centre_y) <= (centre + self.radius): 
            return plane - self.depth
        else:
            return plane 
    
    
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
        

# Uncomment these lines to test a single pit.    
c = Channel()
c.display()

