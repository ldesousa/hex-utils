#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Creates an hexagonal ASCII raster [0] by sampling a a given surface.
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
import imp
import argparse 
from hex_utils.hasc import HASC
from hex_utils.parserSurface import setBasicArguments


def getArguments():
    
    parser = argparse.ArgumentParser(description='Convert continuous surface into HexASCII raster.')
    parser = setBasicArguments(parser)
    parser.add_argument("-s", "--side", dest="side", default = 1,
                      type=float, help="hexagon side length" )
    return parser.parse_args()


# ----- Main ----- #
def main():
    
    args = getArguments()
    
    raster = HASC()
    raster.initWithExtent(args.side, args.xmin, args.ymin, args.xmax, args.ymax)
    
    #modulePath = args.module.rsplit('/', 1)[0]
    moduleName = args.module.rsplit('/', 1)[1].rsplit('.py', 1)[0]
    
    # Dynamically import surface function
    try:
        # This only works with Python 2 - needs another formulation for Python 3        
        module = imp.load_source(moduleName, args.module)
        function = getattr(module, args.function)
    except(Exception) as ex:
        print("Failed to import module or function: %s" % (ex))
        sys.exit()
    
    for i in range(raster.ncols):
        for j in range(raster.nrows):
            x, y = raster.getCellCentroidCoords(i, j)
            raster.set(i, j, function(x, y))
        
    try:
        raster.save(args.output)
        raster.saveAsGML(args.output + ".gml")
    except (ImportError, IOError) as ex:
        print("Error saving the raster %s: %s" % (args.output, ex))
        sys.exit()
    
    print("Created new raster successfully")
    
main()