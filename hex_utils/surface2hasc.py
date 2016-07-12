#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates an hexagonal ASCII grid [0] by sampling a a given surface.
#
# [0] https://github.com/ldesousa/HexAsciiBNF
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 15-06-2016 

import math
from hex_utils.hasc import HASC


# ----- Main ----- #
def main():
    
    x_start = 0
    y_start = 0
    x_end = 2001
    y_end = 2001
    side = 12.408064788
    moduleName = 'surfaceSimple'
    functionName = 'fun'
    
    # Calculate hexagonal cell geometry
    hexPerp = math.sqrt(3) * side / 2
    
    # Position first hexagon
    hexXLL = x_start + side / 2
    hexYLL = y_start + hexPerp / 2 # this / 2 is a cosmetic option
    
    # Calculate grid span
    hexRows = math.ceil(x_end / (2 * hexPerp)) 
    hexCols = math.ceil(y_end / (3 * side / 2))

    grid = HASC()
    grid.init(hexCols, hexRows, hexXLL, hexYLL, side, "E")
    
    # Dynamically import surface function
    module = __import__(moduleName, globals(), locals(), [functionName])
    function = getattr(module, functionName)
    
    for i in range(grid.ncols):
        for j in range(grid.nrows):
            x, y = grid.getCellCentroidCoords(i, j)
            grid.set(i, j, function(x, y))
        
    grid.save("temp.hasc")
    grid.saveAsGML("temp.hasc.gml")
    print("Created new grid successfully")
    
main()