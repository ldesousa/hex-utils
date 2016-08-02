#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates a rectangular ESRI ASCII grid by sampling a a given surface.
# Usage example:
# surface2asc -x 0 -y 0 -X 2000 -Y 2000 -s 20 -m surfaces.surfaceGaussian -f fun -o output.asc
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 03-06-2016 

import math
import argparse
from hex_utils.asc import ASC

def setArguments():
	
	parser = argparse.ArgumentParser(description='Convert continuous surface into ESRI ASCII grid.')
	parser.add_argument("-x", "--xmin", dest="xmin", default = 0,
	                  type=float, help="leftmost xx coordinate" )
	parser.add_argument("-y", "--ymin", dest="ymin", default = 0,
	                  type=float, help="bottom yy coordinate" )
	parser.add_argument("-X", "--xmax", dest="xmax", default = 10,
	                  type=float, help="rightmost xx coordinate" )
	parser.add_argument("-Y", "--ymax", dest="ymax", default = 10,
	                  type=float, help="top xx coordinate" )
	parser.add_argument("-s", "--size", dest="size", default = 1,
	                  type=float, help="cell size (width and height)" )
	parser.add_argument("-m", "--module", dest="module", required = True,
	                  help="Python module containing the surface function" )
	parser.add_argument("-f", "--function", dest="function", required = True,
	                  help="surface function" )
	parser.add_argument("-o", "--output", dest="output", default = "surface.asc",
	                  help="output ASC file" )
	return parser


# ----- Main ----- #
def main():
	
	args = setArguments().parse_args()
	
	grid = ASC()
	grid.init(	
		math.trunc((args.xmax - args.xmin) / args.size), 
		math.trunc((args.ymax - args.ymin) / args.size), 
		args.xmin,
		args.ymin,
		args.size, "")
	
	args.xmin += args.size / 2
	args.ymin += args.size / 2
	
	# Dynamically import surface function
	module = __import__(args.module, globals(), locals(), [args.function])
	function = getattr(module, args.function)
	
	for i in range(grid.ncols):
		for j in range(grid.nrows):
			grid.set(i, grid.nrows - j - 1, 
				function(args.xmin + i * args.size, args.ymin + j * args.size))
		
	grid.save(args.output)
	
	print("Created new grid successfully")
	
main()