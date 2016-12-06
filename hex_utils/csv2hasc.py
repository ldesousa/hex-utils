#
# Creates an hexagonal ASCII grid [0] from a set of point samples.
# Usage examples:
#
# [0] https://github.com/ldesousa/HexAsciiBNF
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 06-12-2016 

# import sys
# import math
import csv
import numpy
from scipy import spatial
from scipy import interpolate
from hex_utils.hasc import HASC

area = 1
xll = 0
yll = 0
xtr = 10
ytr = 10

neighbours = 4
epsilon = 100

coords_list = []
values_list = []

with open('../data/samples.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    
    for row in spamreader:
        # print (', '.join(row))
        # print (row[0])
        raw = str(row[0]).split(',')
        coords_list.append([float(raw[0]), float(raw[1])])
        values_list.append(float(raw[2]))
                             
coords = numpy.array(coords_list)
values = numpy.array(values_list)
 
# print(coords)
# print(values)  

tree = spatial.KDTree(coords)
d,i = tree.query(numpy.array([5,5]),4)    
# print(tree.data[i[0]])                          
# print(tree.data[i[1]])
# print(tree.data[i[2]])
# print(tree.data[i[3]])
# print(values[i[3]])
# print(i[3])

hexGrid = HASC()
hexGrid.initWithExtent(area, xll, yll, xtr, ytr)

print("Geometries:" + 
      "\n Hexagon cell area      : " + str(area)  +
      "\n Hexagon side length    : " + str(hexGrid.side)  +
      "\n Hexagon perpendicular  : " + str(hexGrid.hexPerp)  +
      "\n Num rows in hasc grid  : " + str(hexGrid.nrows)  +
      "\n Num cols in hasc grid  : " + str(hexGrid.ncols))


x, y = hexGrid.getCellCentroidCoords(6, 6)
d, ind = tree.query(numpy.array([x, y]),neighbours + 1) 
print("Coords: " + str(x) + ", " + str(y))
print("Indexes:")
print(ind)
print(tree.data[ind[0]])
print(tree.data[ind[1]])
print(tree.data[ind[2]])
print(tree.data[ind[3]])
print(tree.data[ind[4]])

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
#         newVal = float(f(x,y))
#         print ("New value: " + str(newVal))
#         hexGrid.set(i, j, newVal)
        
hexGrid.save("../data/samples.hasc")        
hexGrid.saveAsGeoJSON("../data/samples.hasc.json") 
hexGrid.saveAsGML("../data/samples.hasc.gml")
        
        
        
        
        
          
                            