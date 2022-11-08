"""Subnet constants"""

from iplib3.constants.ipv6 import (
    IPV6_SEGMENT_BIT_COUNT,
    IPV6_MAX_SEGMENT_COUNT
)
from iplib3.constants.ipv4 import (
    IPV4_SEGMENT_BIT_COUNT,
    IPV4_MAX_SEGMENT_COUNT
)

# Subnet mask constants
IPV4_VALID_SUBNET_SEGMENTS = (0, 128, 192, 224, 240, 248, 252, 254, 255)
IPV4_MIN_SUBNET_VALUE = 0  # Usually 1 is a better choice, 0 is technically valid though
IPV4_MAX_SUBNET_VALUE = IPV4_SEGMENT_BIT_COUNT * IPV4_MAX_SEGMENT_COUNT - 1  # == 31
IPV6_MIN_SUBNET_VALUE = 0  # Unlike in IPV4, this should *always* be valid
IPV6_MAX_SUBNET_VALUE = IPV6_SEGMENT_BIT_COUNT * IPV6_MAX_SEGMENT_COUNT - 1  # == 127
