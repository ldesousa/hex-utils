#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Class an HASC grid - an ASCII encoded cartographic hexagonal grid [0]. 
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 
#
# [0] https://github.com/ldesousa/HexAsciiBNF

import math
from osgeo import ogr

class HASC:
    
    _key_ncols  = "ncols"
    _key_nrows  = "nrows"
    _key_xll    = "xll"
    _key_yll    = "yll"
    _key_side   = "side"
    _key_nodata = "no_data"
    _key_angle  = "angle"
    
    _ncols  = 0
    _nrows  = 0
    _xll    = 0  
    _yll    = 0  
    _side   = 0
    _angle  = None 
    _nodata = ""
    
    _grid = None
    
    _file = None
    _nextLine = None  
    
    def __init(self, ncols, nrows, xll, yll, side, nodata = "", angle = None):
        
        self._ncols  = ncols
        self._nrows  = nrows
        self._xll    = xll  
        self._yll    = yll  
        self._side   = side
        self._angle  = angle 
        self._nodata = nodata
        self._grid = [[None for x in range(self._ncols)] for x in range(self._nrows)]
    
    
    def __init__(self, filePath):
        
        self._file = open(filePath, 'r')
        self._loadHeader()
        self._loadValues()
        self._file.close()
    
    
    def _loadHeaderLine(self, line, key, valType, optional = False):
       
        error = False
        token = line.split()[0]
        value = line.split()[1]
        
        if token.upper() != key.upper():
            if not optional:
                print ("Error, not an hexagonal ASCII raster file. " + 
                    "Expected " + key + " but read " + token)
            return None
        
        if type(1) == valType:
            try:
                return int(value)
            except Exception:
                error = True
        
        elif type(1.0) == valType:
            try:
                return float(value)
            except Exception:
                error = True
                
        else:
            return value
            
        if error:    
            print ("Error converting the string '" + value + "' into " + valType)
            return None
        
        
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


    def _loadLineValues(self, values): 
        
        for val in values:
                
            self._grid[self._colIdx][self._rowIdx] = float(val)
            
            self._colIdx += 1;
            if self._colIdx >= self._ncols:
                self._colIdx = 0;
                self._rowIdx += 1;               
                


    def _loadValues(self):
        
        self._colIdx = 0
        self._rowIdx = 0
        
        self._grid = [[None for x in range(self._ncols)] for x in range(self._nrows)]
        
        if self._nextLine == None:
            self._nextLine = self._file.readline()
            
        while (self._nextLine):
            self._loadLineValues(self._nextLine.split())
            self._nextLine = self._file.readline()
    
    
    def createOutputGML(self, outputFilePath):
        
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

        
    