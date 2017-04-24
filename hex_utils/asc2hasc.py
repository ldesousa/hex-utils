#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Transforms rectangular ESRI ASCII grids into ASCII encoded cartographic 
# hexagonal rasters (HASC) [0]. The resulting hexagonal grid is created with a
# spatial resolution similar to the input rectangular grid. The values of the
# resulting hexagonal mesh are computed using a simple nearest-neighbour or
# a multi-quadratic interpolation.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 
#
# [0] https://github.com/ldesousa/HexAsciiBNF

import sys
import math
from hex_utils.asc import ASC
from hex_utils.hasc import HASC
import argparse 
from enum import Enum  

RES_FACTOR = 1.134   

class Method(Enum):
    MULTIQUADRATIC = 'mq',
    NEAREST_NEIGHBOUR = 'nn' 



def setArguments():
    
    parser = argparse.ArgumentParser(description='Converts an ESRI ASCII grid into an HexASCII (HASC) grid.')
    parser.add_argument("-a", "--area", dest="area", default = 0,
                      type=float, help="cell area of the output mesh" )
    parser.add_argument("-r", "--resolution", action='store_true',
                      help = "preserve original spatial resolution")
    parser.add_argument("-m", "--method", default="mq",
                      help = "Interpolation method: mq - Multiquadratic, nn - Nearest Neighbour")
    parser.add_argument("-i", "--input", dest="inputFile", required = True,
                      help="input ESRI ASCII raster file" )
    parser.add_argument("-o", "--output", dest="outputFile", default = "out.hasc",
                      help="output HexASCII raster file" )
    
    return parser.parse_args()


# ------------ Main ------------ #
def main():
    
    args = setArguments()
    
    esriGrid = ASC()
    try:
        esriGrid.loadFromFile(args.inputFile)
    except (ValueError, IOError) as ex:
        print("Error loading the raster %s: %s" % (args.inputFile, ex))
        sys.exit()
    
    esriArea = math.pow(esriGrid.size, 2)
    hexArea = 0
    
    # Preserve spatial resolution: increase cell area.
    if (args.resolution): 
        hexArea = esriArea * RES_FACTOR
    # Use area provided.
    elif (args.area > 0):
        hexArea = args.area
    # Preserve cell area: used the same as the original raster.
    else:
        hexArea = esriArea
    
    # Calculate hexagonal cell geometry as function of area
    hexSide = math.sqrt(2 * hexArea / (3 * math.sqrt(3)))
    hexPerp = math.sqrt(3) * hexSide / 2
    
    # Calculate mesh span
    hexRows = math.ceil((esriGrid.nrows * esriGrid.size) / (2 * hexPerp)) 
    hexCols = math.ceil((esriGrid.ncols * esriGrid.size) / (3 * hexSide / 2))
    
        
    # Position first hexagon
    # yy position tries to minimise the area of square cells outside the HASC mesh
    hexXLL = esriGrid.xll + hexSide / 2
    hexYLL = (esriGrid.yll + esriGrid.nrows * esriGrid.size) - \
        hexRows * 2 * hexPerp + hexPerp
    
    print("Geometries:" + 
          "\n Input square cell area    : " + str(esriArea) + 
          "\n Hexagon cell area         : " + str(hexArea)  +
          "\n Hexagon side length       : " + str(hexSide)  +
          "\n Hexagon perpendicular     : " + str(hexPerp)  +
          "\n Num rows in HexASCII mesh : " + str(hexRows)  +
          "\n Num cols in HexASCII mesh : " + str(hexCols))
    
    print("\nConverting ...")
    
    hexRaster = HASC()
    hexRaster.init(hexCols, hexRows, hexXLL, hexYLL, hexSide, esriGrid.nodata)
    
    if(args.method == Method.MULTIQUADRATIC):
        interpol = esriGrid.getNearestNeighbour
    else:
        interpol = esriGrid.interpolMultiquadratic    
    
    for j in range(hexRaster.nrows):
        for i in range(hexRaster.ncols):
            x, y = hexRaster.getCellCentroidCoords(i, j)
            hexRaster.set(i, j, interpol(x, y))
    
    hexRaster.save(args.outputFile)
            
    print ("Finished successfully.")
    
main()    
