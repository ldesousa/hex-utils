#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
#
# Gaussian pit.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 21-07-2016

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
# g = Gaussian()
# g.widenning = 2
# g.plotWireFrame()
