#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates an hexagonal ASCII grid [0] by sampling a a given surface.
# Usage examples:
# surface2hasc -x 0 -y 0 -X 2001 -Y 2001 -s 12.4080647880 -m surfaces.eat2Gaussian -f fun -o output.hasc
# surface2hasc -x 0 -y 0 -X 2001 -Y 2001 -s 13.2191028998 -m surfaces.eat2Gaussian -f fun -o output.hasc
#
# [0] https://github.com/ldesousa/HexAsciiBNF
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 15-06-2016 

import sys
import math
from hex_utils.hasc import HASC
from hex_utils.surfaceParser import setBasicArguments


def getArguments():
    
    parser = setBasicArguments()
    parser.add_argument("-s", "--side", dest="side", default = 1,
                      type=float, help="hexagon side length" )
    return parser.parse_args()


# ----- Main ----- #
def main():
    
    args = getArguments()
    
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
        
    try:
        grid.save(args.output)
        grid.saveAsGML(args.output + ".gml")
    except (ImportError, IOError) as ex:
        print("Error saving the grid %s: %s" % (args.output, ex))
        sys.exit()
    
    print("Created new grid successfully")
    
main()