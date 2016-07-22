'''
Created on 21 July 2016

@author: lads
'''

import numpy as np
from surfaces.pit import Pit

class Gaussian(Pit):
    
    def fun(self, x, y, checkDist = False):                      
        
        res =  (self.bottom + self.depth) - \
            2.5 * (self.depth) / np.sqrt(2*np.pi) * \
            np.exp(-(((x - self.x0)/self.widenning)**2/2) \
                   -(((y - self.y0)/self.widenning)**2/2))
            
        # discard if too far from the bottom
        if checkDist and (res - self.bottom) > (self.depth * 0.999):
            return np.Infinity
        else:
            return res

# Uncomment these lines to test a single pit.    
#g = Gaussian()
#g.widenning = 2
#g.display()
