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