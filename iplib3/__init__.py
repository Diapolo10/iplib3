"""A pathlib-equivalent library for IP addresses"""

from .address import *
from .constants import *
from .subnet import *

__all__ = ('IPAddress', 'IPv4', 'IPv6')
