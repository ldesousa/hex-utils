Utilities for Hexagonal ASCII grids
===============================================================================


Copyright
-------------------------------------------------------------------------------

Copyright (c) 2016 Luís Moreira de Sousa. All rights reserved. 
Any use of this document constitutes full acceptance of all terms of the 
document licence.


Description
-------------------------------------------------------------------------------

This project aims to deliver a series of tools to facilitate the manipulation 
and usage of hexagonal raster grids. These tools rely on the 
[Hexagonal ASCII file format](https://github.com/ldesousa/HexAsciiBNF) 
(or HASC for short) for the physical storage of hexagonal rasters.

 - **hasc2gml** - from an input HASC file creates a GML file with a vector feature for each hexagonal cell. Simplifies the display of hexagonal rasters in common desktop GIS software.
 
 - **asc2hasc** - creates an HASC file from an input ESRI ASCII grid. It can either preserve cell area or approximate spatial resolution.
 
 - **surface2hasc** - creates an HASC file from a continuous surface function.
 
 - **surface2asc** - creates an ESRI ASCII file from a continuous surface function.
 
Future work includes the development of a Graphical User Interface (GUI) for 
these tools on QGIS, making the usage of hexagonal grids even simpler.


This tool suite can be installed from the [PyPi repository](https://pypi.python.org/pypi/hex-utils).




Installation Requirements
-------------------------------------------------------------------------------

The `hasc2gml` script requires the Python GDAL library; the `asc2hasc` script 
requires the `scipy` library. At this moment there are no functional universal 
Python packages available for these libraries. Therefore system specific 
packages are required in these cases. On Debian based systems they can be 
installed with the following command:

`sudo apt install python3-gdal python3-scipy` 

The Python package manager is required to install dependencies; on Debian based 
systems it can be obtained like:

`sudo apt install python3-pip`

Installing from PyPi
-------------------------------------------------------------------------------

The easiest way to install `hex-utils` is through the universal package 
available from the Python Package Index (PyPi); an example again on Debian 
based systems:

`sudo pip3 install hex-utils`

Installing from GitHub
-------------------------------------------------------------------------------

Start by cloning the repository to your system:

`git clone git@github.com:ldesousa/hex-utils.git`

Change to the new folder:

`cd hex-utils.git`

It is possible to install directly from the `master` branch, but it is more 
advisable to use of the [tagged releases](https://github.com/ldesousa/hex-utils/releases), 
*e.g.*:

`git checkout tags/v2.2`

Then install the scripts system wide:

`sudo python3 setup.py install`

Finally, install the remaining dependencies:

`sudo pip3 install -r requirements.txt`

Licence
-------------------------------------------------------------------------------

This suite of programmes is released under the [EUPL 1.1 licence](https://joinup.ec.europa.eu/community/eupl/og_page/introduction-eupl-licence). 
For full details please consult the LICENCE file.
