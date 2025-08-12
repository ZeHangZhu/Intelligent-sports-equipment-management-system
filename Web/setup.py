from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

# extensions = [
#     Extension("datetime", [".pyx"],
#         include_dirs=[...],
#         libraries=[...],
#         library_dirs=[...]),
#     Extension("拓展名", [".pyx"],
#         include_dirs=[...],
#         libraries=[...],
#         library_dirs=[...]),
# ]

"""
name             包的名字
ext_modules      要构建的 Python 扩展的列表
"""
setup(
    ext_modules = cythonize("db.pyx")
)
