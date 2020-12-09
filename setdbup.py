from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    name="db_utils", 
    ext_modules = cythonize('db_utils.pyx'),
    include_dirs=[numpy.get_include()]
)
