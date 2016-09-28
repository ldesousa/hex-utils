#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates a synthetic surface with Gaussian pits.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 30-05-2016

from surfaces.surfaceBase import Surface
from surfaces.pitGaussian import Gaussian

gauss = Surface()
        
gauss.p1  = Gaussian( 270,  250, 8.2052, gauss.depth, gauss.slope, gauss.widenning)
gauss.p2  = Gaussian( 270,  730, 8.5342, gauss.depth, gauss.slope, gauss.widenning)
gauss.p3  = Gaussian( 270, 1230, 8.8676, gauss.depth, gauss.slope, gauss.widenning)
gauss.p4  = Gaussian( 270, 1730, 9.2032, gauss.depth, gauss.slope, gauss.widenning)
    
gauss.p5  = Gaussian( 770,  250, 7.9552, gauss.depth, gauss.slope, gauss.widenning)
gauss.p6  = Gaussian( 770,  730, 8.2866, gauss.depth, gauss.slope, gauss.widenning)
gauss.p7  = Gaussian( 770, 1230, 8.6176, gauss.depth, gauss.slope, gauss.widenning)
gauss.p8  = Gaussian( 770, 1730, 8.9509, gauss.depth, gauss.slope, gauss.widenning)
    
gauss.p9  = Gaussian(1270,  250, 7.7052, gauss.depth, gauss.slope, gauss.widenning)
gauss.p10 = Gaussian(1270,  730, 8.0366, gauss.depth, gauss.slope, gauss.widenning)
gauss.p11 = Gaussian(1270, 1230, 8.3699, gauss.depth, gauss.slope, gauss.widenning)
gauss.p12 = Gaussian(1270, 1730, 8.7009, gauss.depth, gauss.slope, gauss.widenning)
    
gauss.p13 = Gaussian(1770,  250, 7.4552, gauss.depth, gauss.slope, gauss.widenning)
gauss.p14 = Gaussian(1770,  730, 7.7883, gauss.depth, gauss.slope, gauss.widenning)
gauss.p15 = Gaussian(1770, 1230, 8.1216, gauss.depth, gauss.slope, gauss.widenning)
gauss.p16 = Gaussian(1770, 1730, 8.4509, gauss.depth, gauss.slope, gauss.widenning)

def fun(x, y):
    return gauss.fun(x, y)

# Uncomment this lines for auto-plotting
# gauss.plot()

