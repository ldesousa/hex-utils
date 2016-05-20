#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Transforms rectangular ESRI ASCCI grids into ASCII encoded cartographic 
# hexagonal grids (HASC) [0]. The resulting hexagonal grid is created with a
# spatial resolution similar to the input rectangular grid. The values of the
# resulting hexagonal grid are computed using a simple nearest-neighbour 
# algorithm.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 
#
# [0] https://github.com/ldesousa/HexAsciiBNF

import sys
import math
from hex_utils.asc import ASC
from hex_utils.hasc import HASC

RES_FACTOR = 1.134

def wrongUsage():
    
    print("\nThis programme requires three arguments:\n" +
          " - conversion mode \n" +
          " - path to an input ESRI ASCII file \n" +
          " - path to the output HASC file \n\n" + 
          "The conversion can be of two types: \n" +
          " -a : preserve cell area  \n" +
          " -r : preserve spatial resolution \n\n" +
          "Usage example: \n"
          "   asc2hasc -r /path/to/input.asc /path/to/output.hasc\n")
    sys.exit()

# This method is the same as in other command line utils
def processArguments(args):
    
    global inputFile
    global outputFile
    
    if len(args) < 4 or (str(args[1]) != '-r' and str(args[1]) != '-a'):
        wrongUsage() 
    else:
        inputFile = str(args[2])
        outputFile = str(args[3])

# ------------ Main ------------ #
def main():
    
    processArguments(sys.argv)
    
    esriGrid = ASC()
    esriGrid.loadFromFile(inputFile)
    
    esriArea = math.pow(esriGrid.size, 2)
    hexArea = 0
    
    # Preserve spatial resolution: increase cell area.
    if (sys.argv[1] == '-r'): 
        hexArea = esriArea * RES_FACTOR
    # Preserve cell area: used the same as the original grid.
    else:
        hexArea = esriArea
    
    # Calculate hexagonal cell geometry as function of area
    hexSide = math.sqrt(2 * hexArea / (3 * math.sqrt(3)))
    hexPerp = math.sqrt(3) * hexSide / 2
    
    # Position first hexagon
    hexXLL = esriGrid.xll + hexSide / 2
    hexYLL = esriGrid.yll + hexPerp / 2 # this / 2 is a cosmetic option
    
    # Calculate grid span
    hexRows = math.ceil((esriGrid.nrows * esriGrid.size) / (2 * hexPerp)) 
    hexCols = math.ceil((esriGrid.ncols * esriGrid.size) / (3 * hexSide / 2))
    
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
    
    for j in range(hexGrid.nrows):
        for i in range(hexGrid.ncols):
            x = hexXLL + i * 3 * hexSide / 2
            y = hexYLL + (hexRows - 1 - j) * 2 * hexPerp + (i % 2) * hexPerp
    
            hexGrid.set(i, j, esriGrid.getNearestNeighbour(x, y))
    
    hexGrid.save(outputFile)
            
    print ("Finished successfully.")
    
main()    
