#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Abstract class for rasters.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 08-04-2016  

import math, sys

class Raster:
    
    _ncols  = 0
    _nrows  = 0
    _xll    = 0  
    _yll    = 0  
    _nodata = ""

    _mesh = None
    
    _file = None
    _nextLine = None 
    
    _value_min = sys.float_info.max
    _value_max = sys.float_info.min
    
    @property
    def ncols(self):
        return self._ncols
    
    @property
    def nrows(self):
        return self._nrows
    
    @property
    def xll(self):
        return self._xll
    
    @property
    def yll(self):
        return self._yll
    
    @property
    def nodata(self):
        return self._nodata
    
    @property
    def min(self):
        return self._value_min
    
    @property
    def max(self):
        return self._value_max
    
    
    def _set_ncols(self, ncols):
        
        if (ncols <= 0):
            raise ValueError('Invalid number of columns')
        self._ncols = ncols
    
    
    def _set_nrows(self, nrows):
        
        if (nrows <= 0):
            raise ValueError('Invalid number of rows')
        self._nrows = nrows
        
            
    def init(self, ncols, nrows, xll, yll, nodata = ""):
         
        self._set_ncols(ncols)
        self._set_nrows(nrows)
        self._xll     = xll  
        self._yll     = yll  
        self._nodata  = nodata
        self._mesh    = [[None for x in range(self._nrows)] for y in range(self._ncols)]
    
    
    def loadFromFile(self, filePath):
        
        self._file = open(filePath, 'r')
        self._loadHeader()
        self._loadValues()
        self._file.close()
        
        
    def _checkRasterBounds(self, i, j):
        
        if i < 0 or i >= self._ncols or j < 0 or  j >= self._nrows:
            raise IndexError("Raster index [" + str(i) + "][" + str(j) + "] out of bounds. " + 
                             "nCols: " + str(self._ncols) + " nRows: " + str(self._nrows))
   
        
    def get(self, i, j):
        
        self._checkRasterBounds(i, j)
        return self._mesh[i][j]    
        
        
    def set(self, i, j, val):
        
        self._checkRasterBounds(i, j)
        self._mesh[i][j] = val
        if self._value_max < val:
            self._value_max = val
        elif self._value_min > val:
            self._value_min = val
    
    
    def _loadHeaderLine(self, line, key, valType, optional = False):
       
        error = False
        elements = line.split()
        
        if len(elements) < 2:
            if not optional:
                print ("Error, malformed file. " + 
                       "Could not read " + key + " header line.")
            return None
        
        token = elements[0]
        value = elements[1]
        
        if token.upper() != key.upper():
            if not optional:
                print ("Error, malformed file. " + 
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


    def _loadLineValues(self, values): 
        
        for val in values:
                
            try:
                #self._mesh[self._colIdx][self._rowIdx] = float(val)
                self.set(self._colIdx, self._rowIdx, float(val))
            except IndexError as ex:
                raise IndexError(
                    "Accessing cell matrix out of boundaries: [" + 
                    str(self._colIdx) + ", " + str(self._rowIdx) + "]. " + 
                    "Expected something in the range [0.." + 
                    str(self._ncols - 1) + ", 0.." + str(self._nrows - 1) + "]")
            
            self._colIdx += 1
            if self._colIdx >= self._ncols:
                self._colIdx = 0
                self._rowIdx += 1               
                

    def _loadValues(self):
        
        self._colIdx = 0
        self._rowIdx = 0
        
        self._mesh = [[None for x in range(self._nrows)] for y in range(self._ncols)]
        
        if self._nextLine == None:
            self._nextLine = self._file.readline()
            
        while (self._nextLine):
            self._loadLineValues(self._nextLine.split())
            self._nextLine = self._file.readline()
            
    
    def _saveHeader(self, f):
        raise NotImplementedError("Please Implement this method")
            
    def save(self, outputFile):
        
        f = open(outputFile,"w")
        
        self._saveHeader(f)
            
        for j in range(self._nrows):
            
            line = ""
            for i in range(self._ncols):
                if (self._mesh[i][j] is None or math.isnan(self._mesh[i][j])):
                    line += str(self._nodata) + " "
                else:
                    line += str(self._mesh[i][j]) + " "
            f.write(line + "\n")        
            