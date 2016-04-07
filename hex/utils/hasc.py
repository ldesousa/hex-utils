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
    
    _ncols  = None
    _nrows  = None
    _xll    = None  
    _yll    = None  
    _side   = None
    _angle  = None 
    _nodata = ""
    
    _grid = []
    
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
        self._grid = [ncols][nrows]
    
    
    def __init__(self, filePath):
        
        self._file = open(filePath, 'r')
        self._readHeader()
        self._readValues()
        self._file.close()
    
    
    def _readHeaderLine(self, key, valType, optional = False):
       
        error = False
        line = self._file.readline()
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


    def _readLineValue(self, values): 
        
        for val in values:
                
            self._grid[self._colIdx][self._rowIdx] = float(val)
            
            if self._colIdx >= self._ncols:
                self._colIdx = 0;
                self._rowIdx += 1;
            else:
                self.coldIdx += 1;
                


    def _readValues(self):
        
        self._colIdx = 0
        self._rowIdx = 0
        
        if self._nextLine == None:
            self._nextLine = self._file.readline()
            
        while (self._nextLine):
            self._readLineValues(self._nextLine.split())
            self._nextLine = self._file.readline()
        
        
    def _readHeader(self):
    
        # Mandatory header
        self._ncols  = self._readHeaderLine(self._key_ncols,  type(1))
        self._nrows  = self._readHeaderLine(self._key_nrows,  type(1))
        self._xll    = self._readHeaderLine(self._key_xll,    type(1.0))
        self._yll    = self._readHeaderLine(self._key_yll,    type(1.0))
        self._side   = self._readHeaderLine(self._key_side,   type(1.0))
        # Optional headers
        nextLine = self._file.readline()
        self._nodata = self._readHeaderLine(nextLine, self._key_nodata, type("a"), True)
        if self._nodata != "" :
            nextLine = self._file.readline()
        self._angle  = self._readHeaderLine(nextLine, self._key_angle, type(1.0),  True)
        if self._angle == None :
            self._nextLine = nextLine
        else:
            self._nextLine =  self._file.readline()
    
    
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

        
    