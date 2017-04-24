#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Encapsulates argument declaration for surface tools.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 24-04-2017


def addExtentArguments(parser):
    
    parser.add_argument("-x", "--xmin", dest="xmin", default = 0,
                      type=float, help="leftmost xx coordinate" )
    parser.add_argument("-y", "--ymin", dest="ymin", default = 0,
                      type=float, help="bottom yy coordinate" )
    parser.add_argument("-X", "--xmax", dest="xmax", default = 10,
                      type=float, help="rightmost xx coordinate" )
    parser.add_argument("-Y", "--ymax", dest="ymax", default = 10,
                      type=float, help="top xx coordinate" )
    return parser