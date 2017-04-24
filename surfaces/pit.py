#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
#
# Base class for pits.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 21-07-2016

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from surfaces.surface import Surface


class Pit(Surface):
    
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

    

