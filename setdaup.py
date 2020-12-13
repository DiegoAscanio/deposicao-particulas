from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    name="da_utils", 
    ext_modules = cythonize('da_utils.pyx'),
    include_dirs=[numpy.get_include()]
)
