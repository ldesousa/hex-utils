#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Encapsulates argument declaration for surface tools.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 19-08-2016

from hex_utils.parserExtent import addExtentArguments

def setBasicArguments(parser):
    
    parser = addExtentArguments(parser)
    parser.add_argument("-m", "--module", dest="module", required = True,
                      help="Python module containing the surface function" )
    parser.add_argument("-f", "--function", dest="function", required = True,
                      help="surface function" )
    parser.add_argument("-o", "--output", dest="output", default = "surface.hasc",
                      help="output raster file" )
    return parser