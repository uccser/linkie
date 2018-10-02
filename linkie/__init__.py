# flake8: noqa
import logging
from .linkie import Linkie


logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = '1.3.0'
