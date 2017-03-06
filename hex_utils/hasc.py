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
from hex_utils.grid import Grid

class HASC (Grid):
    
    _key_ncols  = "ncols"
    _key_nrows  = "nrows"
    _key_xll    = "xll"
    _key_yll    = "yll"
    _key_side   = "side"
    _key_nodata = "no_data"
    _key_angle  = "angle"
     
    _side    = 0
    _angle   = None  
    _hexPerp = 0
    
    _angle_rd = 0
    
    @property
    def side(self):
        return self._side
    
    @property
    def angle(self):
        return self._angle
    
    @property
    def hexPerp(self):
        return self._hexPerp

    
    def _set_side(self, side):
                
        if (side <= 0):
            raise ValueError('Invalid cell side')
        self._side = side

   
    def init(self, ncols, nrows, xll, yll, side, nodata = "", angle = None):
        
        Grid.init(self, ncols, nrows, xll, yll, nodata)  
        self._set_side( side)
        self._angle    = angle 
        self._angle_rd = math.radians(angle)
        self._hexPerp  = math.sqrt(3) * self._side / 2
        
    
    def initWithExtent(self, side, xll, yll, xtr, ytr, nodata = "", angle = None):
        
        # Calculate hexagonal cell geometry
        self._side = side
        self._hexPerp = math.sqrt(3) * self._side / 2
        
        # Calculate grid span
        self._set_nrows(math.ceil((ytr - yll) / (2 * self._hexPerp))) 
        self._set_ncols(math.ceil((xtr - xll) / (3 * self._side / 2) + (self._side / 2)))
        
        # Position first hexagon
        # yy position tries to minimise the area of square cells outside the given extent
        self._xll = xll + self._side / 2
        self._xll = ytr - self._nrows * 2 * self._hexPerp + self._hexPerp
        
        self._nodata = nodata
        self._angle = angle
        self._angle_rd = math.radians(angle)
        self._grid = [[None for x in range(self._nrows)] for y in range(self._ncols)]
    
    
    def cellArea(self):
        
        return self._side * self.hexPerp * 3
    
        
    def _loadHeader(self):
    
        # Mandatory header
        ncols = self._loadHeaderLine(self._file.readline(), self._key_ncols,  type(1))
        nrows = self._loadHeaderLine(self._file.readline(), self._key_nrows,  type(1))
        xll   = self._loadHeaderLine(self._file.readline(), self._key_xll,    type(1.0))
        yll   = self._loadHeaderLine(self._file.readline(), self._key_yll,    type(1.0))
        side  = self._loadHeaderLine(self._file.readline(), self._key_side,   type(1.0))
        # Optional headers
        self._nextLine = self._file.readline()
        nodata = self._loadHeaderLine(self._nextLine, self._key_nodata, type("a"), True)
        if nodata != "" :
            self._nextLine = self._file.readline()
        angle = self._loadHeaderLine(self._nextLine, self._key_angle, type(1.0),  True)
        if angle != None :
            self._nextLine =  self._file.readline()
            
        self.init(ncols, nrows, xll, yll, side, nodata, angle)
    
    
    def _saveHeader(self, f):
           
        f.write(self._key_ncols + "\t" + str(self._ncols) + "\n")
        f.write(self._key_nrows + "\t" + str(self._nrows) + "\n")
        f.write(self._key_xll + "\t" + str(self._xll) + "\n")
        f.write(self._key_yll + "\t" + str(self._yll) + "\n")
        f.write(self._key_side + "\t" + str(self._side) + "\n")
        if self._nodata != "" :
            f.write(self._key_nodata + "\t" + str(self._nodata) + "\n") 
        if self._angle != None :
            f.write(self._key_angle + "\t" + str(self._angle) + "\n") 
     
     
    def getCellCentroidCoords(self, i, j):
        
        return self.rotatePoint(self._getUnrotatedCellCentroidCoords(i, j))
    
    
    def _getUnrotatedCellCentroidCoords(self, i, j):    
        
        x = self._xll + i * 3 * self._side / 2
        y = self._yll + (self._nrows - 1 - j) * 2 * self._hexPerp + (i % 2) * self._hexPerp
        
        return (x, y)
            
    
    def saveAsGML(self, outputFilePath):
        
        try:
            from osgeo import ogr
        except ImportError:
            raise ImportError(""" ERROR: Could not find the GDAL/OGR Python library. 
                       On Debian based systems you can install it with this command:
                       apt install python-gdal""") 
        
        driver = ogr.GetDriverByName("GML")
        outSource = driver.CreateDataSource(
            outputFilePath, 
            ["XSISCHEMAURI=http://schemas.opengis.net/gml/2.1.2/feature.xsd"])
        outLayer = outSource.CreateLayer("output", None, ogr.wkbUnknown)
    
        newField = ogr.FieldDefn("value", ogr.OFTReal)
        outLayer.GetLayerDefn().AddFieldDefn(newField)
    
        for j in range(self._nrows):
            for i in range(self._ncols):
                    
                cellVertexes = self.getCellVertexes(i, j)
                    
                polygon = ogr.CreateGeometryFromWkt("POLYGON ((" +
                    str(cellVertexes[0][0]) + " " + str(cellVertexes[0][1]) + ", " +
                    str(cellVertexes[1][0]) + " " + str(cellVertexes[1][1]) + ", " +
                    str(cellVertexes[2][0]) + " " + str(cellVertexes[2][1]) + ", " +
                    str(cellVertexes[3][0]) + " " + str(cellVertexes[3][1]) + ", " +
                    str(cellVertexes[4][0]) + " " + str(cellVertexes[4][1]) + ", " +
                    str(cellVertexes[5][0]) + " " + str(cellVertexes[5][1]) + ", " +
                    str(cellVertexes[0][0]) + " " + str(cellVertexes[0][1]) + "))")
                
                outFeature = ogr.Feature(feature_def=outLayer.GetLayerDefn())
                outFeature.SetGeometryDirectly(polygon)
                outFeature.SetField("value", str(self._grid[i][self._nrows - j - 1]))
                outLayer.CreateFeature(outFeature)
             
    
    def saveAsGeoJSON(self, outputFilePath):
           
        try:
            from geojson import Feature, Polygon, FeatureCollection, dump
        except ImportError:
            raise ImportError(""" ERROR: Could not find the GeoJSON Python library.""")
        
        collection = FeatureCollection([])
        
        for j in range(self._nrows):
            for i in range(self._ncols):
                
                cellVertexes = self.getCellVertexes(i, j)
                
                collection.features.append(
                    Feature(
                        geometry = Polygon([[
                            cellVertexes[0],  
                            cellVertexes[1], 
                            cellVertexes[2], 
                            cellVertexes[3],                 
                            cellVertexes[4],
                            cellVertexes[5], 
                            cellVertexes[0]
                           ]]), 
                        properties = {"value": str(self._grid[i][j])}))
        
        with open(outputFilePath, 'w') as fp:
            dump(collection, fp)
            
            
    def getCellVertexes(self, i, j):
        """
         Edge coordinates of an hexagon centered in (x,y) having a side of d:
        
                   [x-d/2, y+sqrt(3)*d/2]   [x+d/2, y+sqrt(3)*d/2] 
        
          [x-d, y]                                                 [x+d, y]
        
                   [x-d/2, y-sqrt(3)*d/2]   [x+d/2, y-sqrt(3)*d/2]
        """
        
        # Using unrotated centroid coordinates to avoid an extra computation
        x,y = self._getUnrotatedCellCentroidCoords(i, j)
        
        return [
            self.rotatePoint(x - self._side,      y                 ),  
            self.rotatePoint(x - self._side / 2,  y - self._hexPerp ), 
            self.rotatePoint(x + self._side / 2,  y - self._hexPerp ), 
            self.rotatePoint(x + self._side,      y                 ),                 
            self.rotatePoint(x + self._side / 2,  y + self._hexPerp ),
            self.rotatePoint(x - self._side / 2,  y + self._hexPerp ), 
            ]
        
        
    def rotatePoint(self, pointX, pointY):
        """
        Rotates a point relative to the mesh origin by the angle specified in the angle property.
        Uses the angle formed between the segment linked the point or interest to the origin and
        the parallel intersection the origin. This angle is called beta in the code.
        """    
        if(self.angle == 0 or self.angle == None):
            return(pointX, pointY)
        
              
        # 1. Compute the segment length
        length = math.sqrt((pointX - self.xll) ** 2 + (pointY - self.yll) ** 2)
        # 2. Compute beta
        beta = math.acos((pointX - self.xll) / length) 
        if(pointY < self.yll):
            beta = math.pi * 2 - beta
           
        # 3. Compute offsets
        offsetX = math.cos(beta) * length - math.cos(self._angle_rd + beta) * length
        offsetY = math.sin(self._angle_rd + beta) * length - math.sin(beta) * length 
        return (pointX - offsetX, pointY + offsetY)
                