#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Encapsulates argument declaration for surface tools.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 19-08-2016

import argparse 

def setBasicArguments():
    
    parser = argparse.ArgumentParser(description='Convert continuous surface into HASC grid.')
    parser.add_argument("-x", "--xmin", dest="xmin", default = 0,
                      type=float, help="leftmost xx coordinate" )
    parser.add_argument("-y", "--ymin", dest="ymin", default = 0,
                      type=float, help="bottom yy coordinate" )
    parser.add_argument("-X", "--xmax", dest="xmax", default = 10,
                      type=float, help="rightmost xx coordinate" )
    parser.add_argument("-Y", "--ymax", dest="ymax", default = 10,
                      type=float, help="top xx coordinate" )
    parser.add_argument("-m", "--module", dest="module", required = True,
                      help="Python module containing the surface function" )
    parser.add_argument("-f", "--function", dest="function", required = True,
                      help="surface function" )
    parser.add_argument("-o", "--output", dest="output", default = "surface.hasc",
                      help="output grid file" )
    return parser