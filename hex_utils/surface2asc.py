#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Creates a rectangular ESRI ASCII grid by sampling a a given surface.
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 03-06-2016 

import math
from hex_utils.asc import ASC

# ----- Main ----- #
def main():

	x_start = 0
	y_start = 0
	x_end = 2000
	y_end = 2000
	size = 20
	moduleName = 'surfaces.surfaceGaussian'
	functionName = 'fun'
	
	grid = ASC()
	grid.init(	
		math.trunc((x_end - x_start) / size), 
		math.trunc((y_end - y_start) / size), 
		x_start,
		y_start,
		size, "")
	
	x_start += size / 2
	y_start += size / 2
	
	# Dynamically import surface function
	module = __import__(moduleName, globals(), locals(), [functionName])
	function = getattr(module, functionName)
	
	for i in range(grid.ncols):
		for j in range(grid.nrows):
			grid.set(i, grid.nrows - j - 1, 
				function(x_start + i * size, y_start + j * size))
		
	grid.save("tempGaussian.asc")
	
	print("Created new grid successfully")
	
main()