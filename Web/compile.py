from setuptools import setup, Extension

module = Extension('db', sources=['db.c'])

setup(
    name='db',
    version='1.0',
    description='Python C extension example',
    ext_modules=[module]
)