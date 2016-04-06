# coding=utf8
#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "hex.utils",
    version = "0.1",
    packages = find_packages(include=["hex.utils"]),
    scripts = ['hasc2gml.py'],
    entry_points = {'console_scripts': ['hasc2gml = hex.utils']},

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],

    #package_data = {
        # If any package contains *.txt or *.rst files, include them:
    #    '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
    #    'hello': ['*.msg'],
    #},

    # metadata for upload to PyPI
    author = "Luís Moreira de Sousa",
    author_email = "luis.de.sousa@protonmail.ch",
    description = "Utilities for ASCII encoded hexagonal grids",
    license = "EUPL v1.1",
    keywords = "hexagon hexagonal grid HASC",
    url = "https://github.com/ldesousa/hex.utils",   # project home page, if any
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS"
        ],


    # could also include long_description, download_url, classifiers, etc.
)