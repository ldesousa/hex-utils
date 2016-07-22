'''
Created on 30 May 2016

@author: lads
'''

import numpy as np
from surfaces.pit import Pit


class Hubbert(Pit):

    def fun(self, x, y, checkDist = False):                      
                           
        res =  (self.bottom + self.depth) - (2 * self.depth / \
                ( 1 + np.cosh(self.slope * \
                 (((x - self.x0)/self.widenning)**2 + 
                  ((y - self.y0)/self.widenning)**2)))) 

        # discard if too far from the bottom
        if checkDist and (res - self.bottom) > (self.depth * 0.999):
            return np.Infinity
        else:
            return res
        

# Uncomment these lines to test a single pit.
#g = Hubbert()
#g.widenning = 1
#g.display()
