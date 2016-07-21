'''
Created on 30 May 2016

@author: lads
'''

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from pit import Pit


class Hubbert(Pit):

    slope = 0.25
    widenning = 0.5


    def fun(self, x, y):                      
                           
        return self.peakValue - (2 * self.peakValue / ( 1 + self.widenning * np.cosh( \
                        self.slope * (((x - self.peakPoint))**2 + ((y - self.peakPoint))**2)))) 


g = Hubbert()
g.display()
