'''
Created on 12 Oct 2016

@author: desouslu
'''

import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from surfaces.surface import Surface

class Channel(Surface):
    
    angle = 30
    slope = 0.014893617021
    centre_x = 5
    centre_y = 5
    centre_z = 5
    radius = 0.15
    depth = 0.3
    length = 7
    weir_height = 0.15
    weir_lenght = 0.1
    
        
    def __init__(self, slope = None):
    
        if slope != None: 
            self.slope = slope
        
    
    def fun(self, x, y):   
        
        plane = ((self.centre_x - x) * self.slope + self.centre_z) * math.cos(math.radians(self.angle)) + \
                ((self.centre_y - y) * self.slope + self.centre_z) * math.sin(math.radians(self.angle))                    
               
        centre = (x - self.centre_x) / math.sin(math.radians(90 - self.angle)) * \
                 math.sin(math.radians(self.angle))
                 
        dist_centre = math.sqrt((x - self.centre_x)**2 + (y - self.centre_y)**2)
    
        if  (y - self.centre_y) >= (centre - self.radius) and \
            (y - self.centre_y) <= (centre + self.radius): 
            if y > self.centre_y and \
               dist_centre > (self.length / 2) and \
               dist_centre < (self.length / 2 + self.weir_lenght):
                    return plane - self.depth + self.weir_height
            else:
                return plane - self.depth
        else:
            return plane 
      
      
c = Channel()      
c.plotWireFrame()
        
def fun(x, y):
    return c.fun(x, y)
        
    



