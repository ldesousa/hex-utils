#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Abstract class for raster grids.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 08-04-2016 

class Grid:
    
    _ncols  = 0
    _nrows  = 0
    _xll    = 0  
    _yll    = 0  
    _nodata = ""

    _grid = None
    
    _file = None
    _nextLine = None 
    
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
    
    
    
    def init(self, ncols, nrows, xll, yll, nodata = ""):
        
        self._ncols  = ncols
        self._nrows  = nrows
        self._xll    = xll  
        self._yll    = yll  
        self._nodata = nodata
        self._grid = [[None for x in range(self._nrows)] for y in range(self._ncols)]
    
    
    def loadFromFile(self, filePath):
        
        self._file = open(filePath, 'r')
        self._loadHeader()
        self._loadValues()
        self._file.close()
        
    
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
                self._grid[self._colIdx][self._rowIdx] = float(val)
            except IndexError as ex:
                raise IndexError(
                    "Accessing cell matrix out of boundaries: [" + 
                    str(self._colIdx) + ", " + str(self._rowIdx) + "]. " + 
                    "Expected something in the range [0.." + 
                    str(self._ncols - 1) + ", 0.." + str(self._nrows - 1) + "]")
            
            self._colIdx += 1;
            if self._colIdx >= self._ncols:
                self._colIdx = 0;
                self._rowIdx += 1;               
                

    def _loadValues(self):
        
        self._colIdx = 0
        self._rowIdx = 0
        
        self._grid = [[None for x in range(self._nrows)] for y in range(self._ncols)]
        
        if self._nextLine == None:
            self._nextLine = self._file.readline()
            
        while (self._nextLine):
            self._loadLineValues(self._nextLine.split())
            self._nextLine = self._file.readline()
            
            