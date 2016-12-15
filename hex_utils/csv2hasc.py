#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates an hexagonal ASCII grid [0] from CSV file with a set of point samples.
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


def getArguments():

    parser = argparse.ArgumentParser(description='Creates an HASC raster from a CSV file with a set of point samples.')
    parser.add_argument("-x", "--xmin", dest="xmin", default = 0,
                      type=float, help="leftmost xx coordinate" )
    parser.add_argument("-y", "--ymin", dest="ymin", default = 0,
                      type=float, help="bottom yy coordinate" )
    parser.add_argument("-X", "--xmax", dest="xmax", default = 10,
                      type=float, help="rightmost xx coordinate" )
    parser.add_argument("-Y", "--ymax", dest="ymax", default = 10,
                      type=float, help="top xx coordinate" )
    parser.add_argument("-s", "--side", dest="side", default = 0.62, # area ~ 1
                      type=float, help="hexagon cell side length" )
    parser.add_argument("-i", "--input", dest="input", required = True,
                      help="input CSV file" )
    parser.add_argument("-o", "--output", dest="output", default = "output.hasc",
                      help="output HASC file" )
    return parser.parse_args()


# ----- Main ----- #
def main():
    
    neighbours = 4
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
    d,i = tree.query(numpy.array([5,5]),4)    
    
    hexGrid = HASC()
    hexGrid.initWithExtent(args.side, args.xmin, args.ymin, args.xmax, args.ymax)
    
    print("Geometries:" + 
          "\n Hexagon cell area      : " + str(hexGrid.cellArea())  +
          "\n Hexagon side length    : " + str(hexGrid.side)  +
          "\n Hexagon perpendicular  : " + str(hexGrid.hexPerp)  +
          "\n Num rows in hasc grid  : " + str(hexGrid.nrows)  +
          "\n Num cols in hasc grid  : " + str(hexGrid.ncols))
    
    x, y = hexGrid.getCellCentroidCoords(6, 6)
    d, ind = tree.query(numpy.array([x, y]),neighbours + 1) 
    
    for j in range(hexGrid.nrows):
        for i in range(hexGrid.ncols):
            
            xx = []
            yy = []
            vals = []
            x, y = hexGrid.getCellCentroidCoords(i, j)
            d, ind = tree.query(numpy.array([x, y]),neighbours)  
            
            for n in range(neighbours):
                xx.append(tree.data[ind[n]][0])
                yy.append(tree.data[ind[n]][1])
                vals.append(values[ind[n]])
                
            f = interpolate.Rbf(xx, yy, vals, epsilon=epsilon)
            hexGrid.set(i, j, f(x,y))
            
    hexGrid.save(args.output)        
    hexGrid.saveAsGeoJSON(args.output + ".json") 
    hexGrid.saveAsGML(args.output + ".gml")
            
            
main()            
            
            
              
                                