"""Subnet constants."""

from __future__ import annotations

from enum import Enum

from iplib3.constants.ipv4 import IPV4_MAX_SEGMENT_COUNT, IPV4_SEGMENT_BIT_COUNT
from iplib3.constants.ipv6 import IPV6_MAX_SEGMENT_COUNT, IPV6_SEGMENT_BIT_COUNT

# Subnet mask constants
IPV4_VALID_SUBNET_SEGMENTS = (0, 128, 192, 224, 240, 248, 252, 254, 255)
IPV4_MIN_SUBNET_VALUE = 0  # Usually 1 is a better choice, 0 is technically valid though
IPV4_MAX_SUBNET_VALUE = IPV4_SEGMENT_BIT_COUNT * IPV4_MAX_SEGMENT_COUNT - 1  # == 31
IPV6_MIN_SUBNET_VALUE = 0  # Unlike in IPv4, this should *always* be valid
IPV6_MAX_SUBNET_VALUE = IPV6_SEGMENT_BIT_COUNT * IPV6_MAX_SEGMENT_COUNT - 1  # == 127


class SubnetType(str, Enum):
    """Subnet type."""

    IPV4 = "ipv4"
    IPV6 = "ipv6"

    @classmethod
    def _missing_(cls: type[SubnetType], value: object) -> SubnetType:
        for member in cls:
            if isinstance(value, str) and member.value == value.lower():
                return member

        msg = "Invalid subnet type"
        raise ValueError(msg)
