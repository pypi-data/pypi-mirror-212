"""
.. include:: ../README.md
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("neuron-image-denoise")
except PackageNotFoundError:
    __version__ = "UNKNOWN"
