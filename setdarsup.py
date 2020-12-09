from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    name="dars_utils", 
    ext_modules = cythonize('dars_utils.pyx'),
    include_dirs=[numpy.get_include()]
)
