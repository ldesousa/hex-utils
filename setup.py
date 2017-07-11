#!/usr/bin/python3
# coding=utf8

from setuptools import setup, find_packages

setup(
    name = "hex-utils",
    version = "0.4",
    packages = find_packages(),#['utils'],
    install_requires=[
        'cycler',
        'numpy',
        'pyparsing',
        'python-dateutil',
        'pytz',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'hasc2gml=hex_utils.hasc2gml:main',
            'hasc2geojson=hex_utils.hasc2geojson:main',
            'asc2hasc=hex_utils.asc2hasc:main',
            'csv2hasc=hex_utils.csv2hasc:main',
            'surface2hasc=hex_utils.surface2hasc:main',
            'surface2asc=hex_utils.surface2asc:main'
        ],
    },

    # metadata for upload to PyPI
    author = "Luís Moreira de Sousa",
    author_email = "luis.de.sousa@protonmail.ch",
    description = "Utilities for ASCII encoded hexagonal rasters (HexASCII)",
    license = "EUPL v1.1",
    keywords = "hexagon hexagonal raster HexASCII",
    url = "https://github.com/ldesousa/hex-utils",   # project home page, if any
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        ],

    # could also include long_description, download_url, classifiers, etc.
)
