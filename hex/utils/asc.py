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

from grid import Grid

class ASC (Grid):

    _key_ncols  = "ncols"
    _key_nrows  = "nrows"
    _key_xll    = "xllcorner"
    _key_yll    = "yllcorner"
    _key_size   = "cellsize"
    _key_nodata = "NODATA_value"
  
    _size   = 0    
    
    def __init(self, ncols, nrows, xll, yll, size, nodata = ""):
        
        self._ncols  = ncols
        self._nrows  = nrows
        self._xll    = xll  
        self._yll    = yll  
        self._size   = size
        self._nodata = nodata
        self._grid = [[None for x in range(self._ncols)] for x in range(self._nrows)]
    
    
    def __init__(self, filePath):
        
        self._file = open(filePath, 'r')
        self._loadHeader()
        self._loadValues()
        self._file.close()
     
    
         
    def _loadHeader(self):
    
        # Mandatory header
        self._ncols  = self._loadHeaderLine(self._file.readline(), self._key_ncols,  type(1))
        self._nrows  = self._loadHeaderLine(self._file.readline(), self._key_nrows,  type(1))
        self._xll    = self._loadHeaderLine(self._file.readline(), self._key_xll,    type(1.0))
        self._yll    = self._loadHeaderLine(self._file.readline(), self._key_yll,    type(1.0))
        self._size   = self._loadHeaderLine(self._file.readline(), self._key_size,   type(1.0))
        # Optional headers
        self._nextLine = self._file.readline()
        self._nodata = self._loadHeaderLine(self._nextLine, self._key_nodata, type("a"), True)
        if self._nodata != "" :
            self._nextLine = self._file.readline()
  
        
    