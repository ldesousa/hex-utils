#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016-2017 - Luís Moreira de Sousa
# Licenced under EUPL 1.1. Please consult the LICENCE file for details.
#
# Creates a rectangular ESRI ASCII grid by sampling a a given surface.
# Usage example:
# surface2asc -x 0 -y 0 -X 2000 -Y 2000 -s 20 -m surfaces.eat2Gaussian -f fun -o output.asc
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 03-06-2016 

import sys
import math
import argparse 
from hex_utils.asc import ASC
from hex_utils.parserSurface import setBasicArguments


def getArguments():

	parser = argparse.ArgumentParser(description='Convert continuous surface into ESRI ASCII raster.')
	parser = setBasicArguments(parser)
	parser.add_argument("-s", "--size", dest="size", default = 1,
						type=float, help="cell size (width and height)" )
	return parser.parse_args()


# ----- Main ----- #
def main():
	
	args = getArguments()
	
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
	
	try:	
		grid.save(args.output)
	except IOError as ex:
		print("Error saving the raster %s: %s" % (args.output, ex))
		sys.exit()

	print("Created new ASCII grid successfully")
	
main()