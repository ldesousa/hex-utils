#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Class for HASC grid - an ASCII encoded cartographic hexagonal grid [0]. 
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 
#
# [0] https://github.com/ldesousa/HexAsciiBNF

import math
from osgeo import ogr

from grid import Grid

class HASC (Grid):
    
    _key_ncols  = "ncols"
    _key_nrows  = "nrows"
    _key_xll    = "xll"
    _key_yll    = "yll"
    _key_side   = "side"
    _key_nodata = "no_data"
    _key_angle  = "angle"
     
    _side   = 0
    _angle  = None  
    
   
    def init(self, ncols, nrows, xll, yll, side, nodata = "", angle = None):
        Grid.init(self, ncols, nrows, xll, yll, nodata)  
        self._side   = side
        self._angle  = angle 
        
        
    def set(self, i, j, val):
        
        if i >= 0 and i < self._ncols and j >= 0 and  j < self._nrows:
            self._grid[i][j] = val
        else:
            raise IndexError("Grid index [" + str(i) + "][" + str(j) + "] out of bounds. " + 
                             "nCols: " + str(self._ncols) + " nRows: " + str(self._nrows))
    
        
    def _loadHeader(self):
    
        # Mandatory header
        self._ncols  = self._loadHeaderLine(self._file.readline(), self._key_ncols,  type(1))
        self._nrows  = self._loadHeaderLine(self._file.readline(), self._key_nrows,  type(1))
        self._xll    = self._loadHeaderLine(self._file.readline(), self._key_xll,    type(1.0))
        self._yll    = self._loadHeaderLine(self._file.readline(), self._key_yll,    type(1.0))
        self._side   = self._loadHeaderLine(self._file.readline(), self._key_side,   type(1.0))
        # Optional headers
        self._nextLine = self._file.readline()
        self._nodata = self._loadHeaderLine(self._nextLine, self._key_nodata, type("a"), True)
        if self._nodata != "" :
            self._nextLine = self._file.readline()
        self._angle  = self._loadHeaderLine(self._nextLine, self._key_angle, type(1.0),  True)
        if self._angle != None :
            self._nextLine =  self._file.readline()
    
    def saveAsGML(self, outputFilePath):
    
        
        driver = ogr.GetDriverByName("GML")
        outSource = driver.CreateDataSource(
            outputFilePath, 
            ["XSISCHEMAURI=http://schemas.opengis.net/gml/2.1.2/feature.xsd"])
        outLayer = outSource.CreateLayer("output", None, ogr.wkbUnknown)
    
        newField = ogr.FieldDefn("value", ogr.OFTReal)
        outLayer.GetLayerDefn().AddFieldDefn(newField)
    
        # The perpendicular distance from cell center to cell edge
        perp = math.sqrt(3) * self._side / 2
        
        # Edge coordinates of an hexagon centered in (x,y) and a side of d:
        #
        #           [x-d/2, y+sqrt(3)*d/2]   [x+d/2, y+sqrt(3)*d/2] 
        #
        #  [x-d, y]                                                 [x+d, y]
        #
        #           [x-d/2, y-sqrt(3)*d/2]   [x+d/2, y-sqrt(3)*d/2]
    
        for j in range(0, self._nrows):
            for i in range(0, self._ncols):
                x = self._xll + i * 3 * self._side / 2
                y = self._yll + j * 2 * perp
                if (i % 2) != 0:
                    y += perp
                    
                polygon = ogr.CreateGeometryFromWkt("POLYGON ((" +
                    str(x - self._side)     + " " +  str(y)        + ", " +
                    str(x - self._side / 2) + " " +  str(y - perp) + ", " +
                    str(x + self._side / 2) + " " +  str(y - perp) + ", " +
                    str(x + self._side)     + " " +  str(y)        + ", " +
                    str(x + self._side / 2) + " " +  str(y + perp) + ", " +
                    str(x - self._side / 2) + " " +  str(y + perp) + ", " +
                    str(x - self._side)     + " " +  str(y)       + "))")
                
                outFeature = ogr.Feature(feature_def=outLayer.GetLayerDefn())
                outFeature.SetGeometryDirectly(polygon)
                outFeature.SetField("value", self._grid[i][j])
                outLayer.CreateFeature(outFeature)
    
    