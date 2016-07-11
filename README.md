Utilities for ASCII Hexagonal grids
=====================================


Copyright
-------------------------------------------------------------------------------

Copyright (c) 2016 Luís Moreira de Sousa. All rights reserved. 
Any use of this document constitutes full acceptance of all terms of the 
document licence.


Description
-------------------------------------------------------------------------------

This project aims to deliver a series of tools to facilitate the manipulation and usage of hexagonal raster grids. These tools rely on the Hexagonal [ASCII file format](https://github.com/ldesousa/HexAsciiBNF) (or HASC for short) for the physical storage of hexagonal rasters.

 - **hasc2gml** - from an input HASC file creates a GML file with a vector feature for each hexagonal cell. Simplifies the display of hexagonal rasters in common desktop GIS software.
 
 - **asc2hasc** - creates an HASC file from an input ESRI ASCII grid. It can either preserve cell area or approximate spatial resolution.
 
 - **surface2hasc** - creates an HASC file from a continuous surface function (still in development).
 
This tool suite can be installed from the [PyPi repository](https://pypi.python.org/pypi/hex-utils).

Future work includes the development of a Graphical User Interface (GUI) for these tools on QGIS, making the usage of hexagonal grids even simpler.


Licence
-------------------------------------------------------------------------------

This suite of programmes is released under the EUPL 1.1 licence. For further 
details please consult the LICENCE file.
