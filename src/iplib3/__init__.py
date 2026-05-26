"""A pathlib-equivalent library for IP addresses."""

import importlib.metadata

from iplib3.address import *
from iplib3.subnet import *
from iplib3.validators import *

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ("IPAddress", "IPv4", "IPv6", "port_validator")
