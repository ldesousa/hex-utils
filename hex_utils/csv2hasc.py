#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Creates an hexagonal ASCII raster [0] from CSV file with a set of point samples.
# Values in the new raster are interpolated using the multiquadratic method.
# It assumes the CSV file to be organised into three columns, with xx, yy 
# coordinates and values in succession, as:
# xx1;yy1;value1;
# xx2;yy2;value2;
# Also assumes no headers to be present.
# 
# Usage example:
# csv2hasc -x 0 -y 0 -X 10 -Y 10 -s 0.62 -i input.csv -o output.hasc
#
# [0] https://github.com/ldesousa/HexAsciiBNF
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 06-12-2016 

import csv
import numpy
import argparse 
from scipy import spatial
from scipy import interpolate
from hex_utils.hasc import HASC
from hex_utils.parserExtent import addExtentArguments


def getArguments():

    parser = argparse.ArgumentParser(description=
        '''Creates an HASC raster from a CSV file with a set of point samples.
           Values in the new raster are interpolated using the multiquadratic method.
           It assumes the CSV file has no headers and is organised into three columns, 
           with xx, yy coordinates and values in succession, as:
           xx1;yy1;value1;
           xx2;yy2;value2;''')
    parser = addExtentArguments(parser)
    parser.add_argument("-s", "--side", dest="side", default = 0.62, # area ~ 1
                      type=float, help="hexagon cell side length" )
    parser.add_argument("-i", "--input", dest="input", required = True,
                      help="input CSV file" )
    parser.add_argument("-o", "--output", dest="output", default = "output.hasc",
                      help="output HASC file" )
    return parser.parse_args()


# ----- Main ----- #
def main():
    
    neighbours = 5
    tolerance = 0.1
    epsilon = 100
    
    coords_list = []
    values_list = []
    
    args = getArguments()
    
    with open(args.input, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
        for row in spamreader:
            raw = str(row[0]).split(',')
            coords_list.append([float(raw[0]), float(raw[1])])
            values_list.append(float(raw[2]))
                                 
    coords = numpy.array(coords_list)
    values = numpy.array(values_list)
    tree = spatial.KDTree(coords)
    # Set maximum and minimum admissable values
    max_value = values.max() + (values.max() - values.min()) * tolerance
    min_value = values.min() - (values.max() - values.min()) * tolerance
      
    hexRaster = HASC()
    hexRaster.initWithExtent(args.side, args.xmin, args.ymin, args.xmax, args.ymax)
    
    print("Geometries:" + 
          "\n Hexagon cell area     : " + str(hexRaster.cellArea())  +
          "\n Hexagon side length   : " + str(hexRaster.side)  +
          "\n Hexagon perpendicular : " + str(hexRaster.hexPerp)  +
          "\n Num rows in HASC mesh : " + str(hexRaster.nrows)  +
          "\n Num cols in hasc mesh : " + str(hexRaster.ncols))
    
    for j in range(hexRaster.nrows):
        for i in range(hexRaster.ncols):
            
            xx = []
            yy = []
            vals = []
            x, y = hexRaster.getCellCentroidCoords(i, j)
            d, ind = tree.query(numpy.array([x, y]),neighbours)  
            
            for n in range(neighbours):
                xx.append(tree.data[ind[n]][0])
                yy.append(tree.data[ind[n]][1])
                vals.append(values[ind[n]])
                
            f = interpolate.Rbf(xx, yy, vals, epsilon=epsilon)
            new_value = f(x,y)
            if new_value < min_value:
                hexRaster.set(i, j, min_value)
            elif new_value > max_value:
                hexRaster.set(i, j, max_value)
            else:
                hexRaster.set(i, j, new_value)
            
    hexRaster.save(args.output)        
    hexRaster.saveAsGeoJSON(args.output + ".json") 
    hexRaster.saveAsGML(args.output + ".gml")
            
    print("\nSuccessfully created new HexASCII raster.")        
            
main()            
            
            
              
                                