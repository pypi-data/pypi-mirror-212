from setuptools import setup, Extension
import numpy

setup(
    ext_modules=[
        Extension(
            'neuron_image_denoise._filter',
            sources=['neuron_image_denoise/_filter.pyx'],
            language='c++',
            include_dirs=[numpy.get_include()],
            library_dirs=[],
            libraries=[],
            extra_compile_args=[],
            extra_link_args=[]
            ),
    ]
)
