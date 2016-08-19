#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Class for the ESRI ASCII grid format [0]. 
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 
#
# [0] http://resources.esri.com/help/9.3/arcgisengine/java/GP_ToolRef/spatial_analyst_tools/esri_ascii_raster_format.htm

import math
from hex_utils.grid import Grid

class ASC (Grid):

    _key_ncols  = "ncols"
    _key_nrows  = "nrows"
    _key_xll    = "xllcorner"
    _key_yll    = "yllcorner"
    _key_size   = "cellsize"
    _key_nodata = "NODATA_value"
  
    _size   = 0
       
    @property
    def size(self):
        return self._size
    
    
    def _set_size(self, size):
                
        if (size <= 0):
            raise ValueError('Invalid cell size')
        self._size = size
        
    
    def init(self, ncols, nrows, xll, yll, size, nodata = ""):
        
        Grid.init(self, ncols, nrows, xll, yll, nodata)
        self._set_size(size)
        
        
    def getNearestNeighbour(self, x, y):
        
        if x < self._xll:
            x = self._xll
            
        if x > self._xll + self._size * (self._ncols - 1):
            x = self._xll + self._size * (self._ncols - 1)
        
        if y < self._yll:
            y = self._yll
            
        if y > self._yll + self._size * (self._nrows - 1):
            y = self._yll + self._size * (self._nrows - 1)
            
        i = math.trunc((x - self._xll) / self._size)
        j = self._nrows - 1 - math.trunc((y - self._yll) / self._size)
 
        try:
            return self._grid[i][j]
        except IndexError:
            raise IndexError("Wrong indexes in nearest neighbour:" + 
                "i: " + str(i) + " j: " + str(j) + " x: " + str(x) + " y: " + str(y))
    
    
    def _loadHeader(self):
    
        # Mandatory header
        self._set_ncols(self._loadHeaderLine(self._file.readline(), self._key_ncols,  type(1)))
        self._set_nrows(self._loadHeaderLine(self._file.readline(), self._key_nrows,  type(1)))
        self._xll     = self._loadHeaderLine(self._file.readline(), self._key_xll,    type(1.0))
        self._yll     = self._loadHeaderLine(self._file.readline(), self._key_yll,    type(1.0))
        self._set_size( self._loadHeaderLine(self._file.readline(), self._key_size,   type(1.0)))
        # Optional headers
        self._nextLine = self._file.readline()
        self._nodata = self._loadHeaderLine(self._nextLine, self._key_nodata, type("a"), True)
        if self._nodata != "" :
            self._nextLine = self._file.readline()
  
    
    def _saveHeader(self, f):
           
        f.write(self._key_ncols + "\t" + str(self._ncols) + "\n")
        f.write(self._key_nrows + "\t" + str(self._nrows) + "\n")
        f.write(self._key_xll   + "\t" + str(self._xll)   + "\n")
        f.write(self._key_yll   + "\t" + str(self._yll)   + "\n")
        f.write(self._key_size  + "\t" + str(self._size)  + "\n")
        if self._nodata != "" :
            f.write(self._key_nodata + "\t" + str(self._nodata) + "\n")   
    