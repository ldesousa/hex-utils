'''
Created on 21 July 2016

@author: lads
'''

import numpy as np
from pit import Pit

class Gaussian(Pit):
    
    def fun(self, x, y):                      
        
        return (self.bottom + self.depth) - \
            2.5 * (self.bottom + self.depth) / np.sqrt(2*np.pi) * \
            np.exp(-(((x - self.x0)/self.widenning)**2/2) \
                   -(((y - self.y0)/self.widenning)**2/2))

    
g = Gaussian()
g.widenning = 2
g.display()
