#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates a synthetic surface with Hubbertian pits.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 30-05-2016

from surfaces.surfaceBase import Surface
from surfaces.pitHubbert import Hubbert

hubbert = Surface()

hubbert.widenning = 350

hubbert.p1  = Hubbert( 270,  250, 8.2052, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p2  = Hubbert( 270,  730, 8.5342, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p3  = Hubbert( 270, 1230, 8.8676, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p4  = Hubbert( 270, 1730, 9.2032, hubbert.depth, hubbert.slope, hubbert.widenning)
    
hubbert.p5  = Hubbert( 770,  250, 7.9552, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p6  = Hubbert( 770,  730, 8.2866, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p7  = Hubbert( 770, 1230, 8.6176, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p8  = Hubbert( 770, 1730, 8.9509, hubbert.depth, hubbert.slope, hubbert.widenning)
    
hubbert.p9  = Hubbert(1270,  250, 7.7052, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p10 = Hubbert(1270,  730, 8.0366, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p11 = Hubbert(1270, 1230, 8.3699, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p12 = Hubbert(1270, 1730, 8.7009, hubbert.depth, hubbert.slope, hubbert.widenning)
    
hubbert.p13 = Hubbert(1770,  250, 7.4552, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p14 = Hubbert(1770,  730, 7.7883, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p15 = Hubbert(1770, 1230, 8.1216, hubbert.depth, hubbert.slope, hubbert.widenning)
hubbert.p16 = Hubbert(1770, 1730, 8.4509, hubbert.depth, hubbert.slope, hubbert.widenning)
    
def fun(x, y):
    return hubbert.fun(x, y)

# Uncomment these lines for auto-plotting
# hubbert.plot()
