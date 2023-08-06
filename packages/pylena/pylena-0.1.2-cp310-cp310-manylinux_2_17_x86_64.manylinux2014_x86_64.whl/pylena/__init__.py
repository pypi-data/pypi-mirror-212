"""
Base
"""

__all__ = ["check_type", "check_numpy_array", "morpho", "scribo", "__version__"]

from . import morpho as morpho
from . import scribo as scribo
from .utils import *
from ._version import __version__
