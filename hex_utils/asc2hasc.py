#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Transforms rectangular ESRI ASCCI grids into ASCII encoded cartographic 
# hexagonal grids (HASC) [0]. The resulting hexagonal grid is created with a
# spatial resolution similar to the input rectangular grid. The values of the
# resulting hexagonal grid are computed using a simple nearest-neighbour or
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
                      type=float, help="cell area of the output grid" )
    parser.add_argument("-r", "--resolution", action='store_true',
                      help = "preserve original spatial resolution")
    parser.add_argument("-m", "--method", default="mq",
                      help = "Interpolation method: mq - Multiquadratic, nn - Nearest Neighbour")
    parser.add_argument("-i", "--input", dest="inputFile", required = True,
                      help="input ESRI ASCII grid file" )
    parser.add_argument("-o", "--output", dest="outputFile", default = "out.hasc",
                      help="output HexASCII grid file" )
    
    return parser.parse_args()


# ------------ Main ------------ #
def main():
    
    args = setArguments()
    
    esriGrid = ASC()
    try:
        esriGrid.loadFromFile(args.inputFile)
    except (ValueError, IOError) as ex:
        print("Error loading the grid %s: %s" % (args.inputFile, ex))
        sys.exit()
    
    esriArea = math.pow(esriGrid.size, 2)
    hexArea = 0
    
    # Preserve spatial resolution: increase cell area.
    if (args.resolution): 
        hexArea = esriArea * RES_FACTOR
    # Use area provided.
    elif (args.area > 0):
        hexArea = args.area
    # Preserve cell area: used the same as the original grid.
    else:
        hexArea = esriArea
    
    # Calculate hexagonal cell geometry as function of area
    hexSide = math.sqrt(2 * hexArea / (3 * math.sqrt(3)))
    hexPerp = math.sqrt(3) * hexSide / 2
    
    # Calculate grid span
    hexRows = math.ceil((esriGrid.nrows * esriGrid.size) / (2 * hexPerp)) 
    hexCols = math.ceil((esriGrid.ncols * esriGrid.size) / (3 * hexSide / 2))
    
        
    # Position first hexagon
    # yy position tries to minimise the area of square cells outside the HASC grid
    hexXLL = esriGrid.xll + hexSide / 2
    hexYLL = (esriGrid.yll + esriGrid.nrows * esriGrid.size) - \
        hexRows * 2 * hexPerp + hexPerp
    
    print("Geometries:" + 
          "\n Input square cell area : " + str(esriArea) + 
          "\n Hexagon cell area      : " + str(hexArea)  +
          "\n Hexagon side length    : " + str(hexSide)  +
          "\n Hexagon perpendicular  : " + str(hexPerp)  +
          "\n Num rows in hasc grid  : " + str(hexRows)  +
          "\n Num cols in hasc grid  : " + str(hexCols))
    
    print("\nConverting ...")
    
    hexGrid = HASC()
    hexGrid.init(hexCols, hexRows, hexXLL, hexYLL, hexSide, esriGrid.nodata)
    
    if(args.method == Method.MULTIQUADRATIC):
        interpol = esriGrid.getNearestNeighbour
    else:
        interpol = esriGrid.interpolMultiquadratic    
    
    for j in range(hexGrid.nrows):
        for i in range(hexGrid.ncols):
            x, y = hexGrid.getCellCentroidCoords(i, j)
            hexGrid.set(i, j, interpol(x, y))
    
    hexGrid.save(args.outputFile)
            
    print ("Finished successfully.")
    
main()    
