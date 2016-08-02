#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates an hexagonal ASCII grid [0] by sampling a a given surface.
# Usage examples:
# surface2hasc -x 0 -y 0 -X 2001 -Y 2001 -s 12.4080647880 -m surfaces.surfaceGaussian -f fun -o output.hasc
# surface2hasc -x 0 -y 0 -X 2001 -Y 2001 -s 13.2191028998 -m surfaces.surfaceGaussian -f fun -o output.hasc
#
# [0] https://github.com/ldesousa/HexAsciiBNF
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 15-06-2016 

import math
import argparse
from hex_utils.hasc import HASC

def setArguments():
    
    parser = argparse.ArgumentParser(description='Convert continuous surface into HASC grid.')
    parser.add_argument("-x", "--xmin", dest="xmin", default = 0,
                      type=float, help="leftmost xx coordinate" )
    parser.add_argument("-y", "--ymin", dest="ymin", default = 0,
                      type=float, help="bottom yy coordinate" )
    parser.add_argument("-X", "--xmax", dest="xmax", default = 10,
                      type=float, help="rightmost xx coordinate" )
    parser.add_argument("-Y", "--ymax", dest="ymax", default = 10,
                      type=float, help="top xx coordinate" )
    parser.add_argument("-s", "--side", dest="side", default = 1,
                      type=float, help="hexagon side length" )
    parser.add_argument("-m", "--module", dest="module", required = True,
                      help="Python module containing the surface function" )
    parser.add_argument("-f", "--function", dest="function", required = True,
                      help="surface function" )
    parser.add_argument("-o", "--output", dest="output", default = "surface.hasc",
                      help="output HASC file" )
    return parser

# ----- Main ----- #
def main():
    
    args = setArguments().parse_args()
    
    # Calculate hexagonal cell geometry
    hexPerp = math.sqrt(3) * args.side / 2
    
    # Position first hexagon
    hexXLL = args.xmin + args.side / 2
    hexYLL = args.ymin + hexPerp / 2 # this / 2 is a cosmetic option
    
    # Calculate grid span
    hexRows = math.ceil(args.xmax / (2 * hexPerp)) 
    hexCols = math.ceil(args.ymax / (3 * args.side / 2))

    grid = HASC()
    grid.init(hexCols, hexRows, hexXLL, hexYLL, args.side, "9999")
    
    # Dynamically import surface function
    module = __import__(args.module, globals(), locals(), [args.function])
    function = getattr(module, args.function)
    
    for i in range(grid.ncols):
        for j in range(grid.nrows):
            x, y = grid.getCellCentroidCoords(i, j)
            grid.set(i, j, function(x, y))
        
    grid.save(args.output)
    grid.saveAsGML(args.output + ".gml")
    print("Created new grid successfully")
    
main()