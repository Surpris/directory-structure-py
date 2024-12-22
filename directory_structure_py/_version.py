"""_version.py
version information
"""

from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = 'unknown'

__all__ = ['__version__']
