# -*- coding: utf-8 -*-
#! anaconda create -n CLPU python=3.5 && conda activate CLPU && pip install .
"""
This is the setup file for pythonic CLPU utilities.

project             standardized modules for often used python functions at CLPU
acronym             pyCLPU
created on          2022-01-01 00:00:00

@author             Micha (MEmx), CLPU, Villamayor, Spain
@moderator          Eduardo, CLPU, Villamayor, Spain
@updator            Diego (MEmx), CLPU, Villamayor, Spain
            
@contact            mehret@clpu.es

interpreter         python > 3.5
version control     git
url                 https://git.clpu.es/mehret/pyclpu

requires explicitely {
 - setuptools
 - glob
}

execute installation via {
  > pip install .
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/MODULE.py))
  sys.path.append(os.path.abspath(root))
  import MODULE
  from importlib import reload 
  reload(MODULE)
}

"""

# credits to https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

from setuptools import setup

import glob

# read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(\
    name="pyclpu",\
    description='CLPU Utilities',\
    long_description = long_description,\
    long_description_content_type='text/markdown',\
    author='Michael Ehret',\
    author_email='mehret@clpu.es',\
    url='https://git.clpu.es/mehret/pyclpu',\
    license='MIT',\
    packages=['pyclpu'],
    scripts=glob.glob("pyclpu/*.py"),
    install_requires=[\
        'numpy','scipy','opencv-python','cython','pillow',\
        'matplotlib',\
    ],\
    # and build in modules cython, importlib.reload, inspect.getsourcefile, glob, math, opencv, pillow, os, sys, time
    classifiers=[\
        'Development Status :: 1 - Planning',\
        'Intended Audience :: Science/Research',\
        'Programming Language :: Python :: 3.5',\
    ],\
)