'''
Created on 21 July 2016

@author: lads
'''

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from pit import Pit


class Gaussian(Pit):

    slope = 0.25
    widenning = 2
    

    def fun(self, x, y):                      
        
        return 2.5 * self.peakValue / np.sqrt(2*np.pi) * \
            np.exp(-(((x - self.peakPoint)/self.widenning)**2/2)-(((y - self.peakPoint)/self.widenning)**2/2))

    
g = Gaussian()
g.display()
