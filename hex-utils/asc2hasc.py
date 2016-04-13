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
from asc import ASC
from hasc import HASC

def wrongUsage():
    
    print("This programme requires two arguments:\n" +
          " - path to an input ESRI ASCII file \n" +
          " - path to the output HASC file \n" + 
          "Usage example: \n"
          "   asc2hasc /path/to/input.asc /path/to/output.hasc")
    sys.exit()

# This method is the same as in other command line utils
def processArguments(args):
    
    global inputFile
    global outputFile
    
    if len(args) < 3:
        wrongUsage() 
    else:
        inputFile = str(args[1])
        outputFile = str(args[2])

# ------------ Main ------------ #

processArguments(sys.argv)

esriGrid = ASC()
esriGrid.loadFromFile(inputFile)

esriArea = math.pow(esriGrid.size, 2)

# Comment here the logic to get to this hexagon cell size
hexSide = math.sqrt(2 * esriArea / (3 * math.sqrt(3)))
hexPerp = math.sqrt(3) * hexSide / 2

hexRows = math.ceil((esriGrid.nrows * esriGrid.size) / (2 * hexPerp)) 
hexCols = math.ceil((esriGrid.ncols * esriGrid.size) / (3 * hexSide / 2))

print("Calcs:" + 
      "\nesriArea: " + str(esriArea) + 
      "\nhexSide: " + str(hexSide) +
      "\nhexPerp: " + str(hexPerp) +
      "\nhexRows: " + str(hexRows) +
      "\nhexCols: " + str(hexCols))

hexGrid = HASC()
hexGrid.init(hexCols, hexRows, esriGrid.xll, esriGrid.yll, hexSide, esriGrid.nodata)

for j in range(hexGrid.nrows):
    for i in range(hexGrid.ncols):
        x = esriGrid.xll + i * 3 * hexSide / 2
        y = esriGrid.yll + j * 2 * hexPerp + (j % 2) * hexPerp
        hexGrid.set(i, j, esriGrid.getNearestNeighbour(x, y))
        
# This must be evolved into HASC save
hexGrid.saveAsGML("new.gml")

hexGrid.save(outputFile)
        
print ("Done!")


