"""iplib3's functionality specific to validating things."""

from __future__ import annotations

from enum import IntEnum, auto

from iplib3.constants.ipv4 import (
    IPV4_MAX_SEGMENT_COUNT,
    IPV4_MAX_SEGMENT_VALUE,
    IPV4_MAX_VALUE,
    IPV4_MIN_SEGMENT_COUNT,
    IPV4_MIN_SEGMENT_VALUE,
    IPV4_MIN_VALUE,
)
from iplib3.constants.ipv6 import (
    IPV6_MAX_SEGMENT_COUNT,
    IPV6_MAX_SEGMENT_VALUE,
    IPV6_MAX_VALUE,
    IPV6_MIN_SEGMENT_VALUE,
    IPV6_MIN_VALUE,
    IPV6_NUMBER_BIT_COUNT,
    IPV6_SEGMENT_BIT_COUNT,
)
from iplib3.constants.port import (
    PORT_NUMBER_MAX_VALUE,
    PORT_NUMBER_MIN_VALUE,
)
from iplib3.constants.subnet import (
    IPV4_MAX_SUBNET_VALUE,
    IPV4_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    SubnetType,
)

__all__ = ("ip_validator", "ipv4_validator", "ipv6_validator", "port_validator", "subnet_validator")


class ValidationMode(IntEnum):
    """Detemine the validation strictness."""

    RELAXED = auto()
    STRICT = auto()


def port_validator(port_num: int | None) -> bool:
    """
    Validate an address port.

    None means "no port", and is treated as a valid port value.
    Otherwise the port must be an integer between the minimum and maximum port values, inclusive.

    Strings may be accepted in the future, but are not currently supported.

    The function should not raise an exception, wrong types will simply return False.
    """
    if port_num is None:
        return True

    return isinstance(port_num, int) and PORT_NUMBER_MIN_VALUE <= port_num <= PORT_NUMBER_MAX_VALUE


def ip_validator(address: str | int, validation_mode: ValidationMode = ValidationMode.STRICT) -> bool:
    """
    Validate an IP address of any kind, returning a boolean.

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """
    if ipv4_validator(address, validation_mode):
        return True
    return ipv6_validator(address, validation_mode)


def ipv4_validator(address: str | int, validation_mode: ValidationMode = ValidationMode.STRICT) -> bool:
    """
    Validate an IPv4 address, returning a boolean.

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """
    valid = False

    if isinstance(address, str) and "." in address:
        portless_address, _, valid = _port_stripper(address, protocol=SubnetType.IPV4, validation_mode=validation_mode)

        if valid:
            valid = _ipv4_address_validator(portless_address, validation_mode=validation_mode)

    if isinstance(address, int):
        valid = IPV4_MIN_VALUE <= address <= IPV4_MAX_VALUE

    return valid


def ipv6_validator(address: str | int, validation_mode: ValidationMode = ValidationMode.STRICT) -> bool:
    """
    Validate an IPv6 address, returning a boolean.

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """
    valid = False

    if isinstance(address, str):
        portless_address, _, valid = _port_stripper(address, protocol=SubnetType.IPV6, validation_mode=validation_mode)

        if not valid:
            return valid

        valid = _ipv6_address_validator(portless_address, validation_mode=validation_mode)

    if isinstance(address, int):
        valid = IPV6_MIN_VALUE <= address <= IPV6_MAX_VALUE

    return valid


def subnet_validator(subnet: str | int, protocol: SubnetType = SubnetType.IPV4) -> bool:
    """
    Validate a given subnet mask, defaulting to IPv4 protocol.

    Strings will be validated as IPv4 regardless of the protocol toggle
    as IPv6 subnets have no valid string representation.
    """
    protocol = SubnetType(protocol)

    valid = False

    if protocol == SubnetType.IPV4:
        valid = _ipv4_subnet_validator(subnet)

    elif protocol == SubnetType.IPV6 and isinstance(subnet, int):
        valid = _ipv6_subnet_validator(subnet)

    return valid


def _ipv4_subnet_validator(subnet: str | int) -> bool:
    """
    Validate an IPv4-compliant subnet mask.

    The function uses the IPv4-standard to
    validate a subnet, including all values.

    Types other than strings or integers
    *will raise a TypeError* with the name
    of the used type.
    """
    if isinstance(subnet, str):
        segments = tuple(int(s) for s in reversed(subnet.split(".")))
        if len(segments) != IPV4_MIN_SEGMENT_COUNT:
            return False

        segment_sum = sum(s << (8 * idx) for idx, s in enumerate(segments))
        subnet_bits = f"{segment_sum:b}".rstrip("0")

        if "0" in subnet_bits:
            return False

        subnet = len(subnet_bits)

    if isinstance(subnet, int):
        return IPV4_MIN_SUBNET_VALUE <= subnet <= IPV4_MAX_SUBNET_VALUE

    msg = f"IPv4 subnet cannot be of type '{subnet.__class__.__name__}'; only strings and integers supported"
    raise TypeError(
        msg,
    )


def _ipv6_subnet_validator(subnet: int) -> bool:  # IPv6 subnets have no string representation
    """
    Validate an IPv6-compliant subnet mask.

    The IPv6-standard has no string
    representation for subnests, so
    only integers need to be handled.

    Non-integer types will raise a ValueError
    with the name of the used type.
    """
    if isinstance(subnet, int):
        return IPV6_MIN_SUBNET_VALUE <= subnet <= IPV6_MAX_SUBNET_VALUE and subnet % IPV6_NUMBER_BIT_COUNT == 0

    msg = f"IPv6 subnet cannot be of type '{subnet.__class__.__name__}', it must be an integer"
    raise TypeError(msg)


def _port_stripper(
    address: str, protocol: SubnetType = SubnetType.IPV4, validation_mode: ValidationMode = ValidationMode.STRICT
) -> tuple[str, int | None, bool]:
    """
    Extract the port number from IP addresses, if any.

    Returns a tuple with the portless address, the port (or None),
    and validation information as a boolean.
    """
    protocol = SubnetType(protocol)

    valid = True
    port_num = None
    port_separator = None

    if protocol == SubnetType.IPV4:
        port_separator = ":"
    if protocol == SubnetType.IPV6:
        port_separator = "]:"

    # Try split on closing bracket and port separator
    address, *port = address.strip().split(port_separator)
    if port and valid:
        if protocol == SubnetType.IPV6:
            # Get rid of the opening bracket that contained the address (eg. [::12:34]:8080 -> ::12:34)
            address = address[1:]

        # Is port number a valid integer?
        try:
            port_num = int(port[0])
        except ValueError:
            valid = False

        if validation_mode == ValidationMode.STRICT and valid:
            valid = port_validator(port_num)

    return address, port_num, valid


def _ipv4_address_validator(address: str, validation_mode: ValidationMode = ValidationMode.STRICT) -> bool:
    """Validate the address part of an IPv4 address."""
    valid = True

    try:
        segments = [int(segment) for segment in address.split(".")]
    except ValueError:
        # IPv4 address was not made of valid integers
        return False

    if not IPV4_MIN_SEGMENT_COUNT <= len(segments) <= IPV4_MAX_SEGMENT_COUNT:
        # Invalid number of segments
        valid = False

    elif validation_mode == ValidationMode.STRICT:
        for seg in segments:
            if not IPV4_MIN_SEGMENT_VALUE <= seg <= IPV4_MAX_SEGMENT_VALUE:
                # Segment value was too high or too low to be strictly valid
                valid = False
                break

    return valid


def _ipv6_address_validator(address: str, validation_mode: ValidationMode = ValidationMode.STRICT) -> bool:
    """Validate the address part of an IPv6 address."""
    address = address.strip()
    valid = True
    segments: list[str] = []
    empty_segment = f"{IPV6_MIN_SEGMENT_VALUE:0{IPV6_NUMBER_BIT_COUNT}}"
    skips = address.count("::")

    if skips > 1:
        # More than one, illegal zero-skip
        valid = False

    elif skips == 1:
        # One, legal zero-skip
        left, *_, right = address.split("::")

        left_segments = left.split(":")
        right_segments = right.split(":")
        total_segments = len(left_segments) + len(right_segments)

        segments.extend(left_segments if left else [empty_segment])
        segments.extend(empty_segment for _ in range(IPV6_MAX_SEGMENT_COUNT - total_segments))
        segments.extend(right_segments if right else [empty_segment])

    else:
        # No zero-skip, full address
        segments = address.split(":")

    try:
        processed_segments: list[int] = [int(segment, IPV6_SEGMENT_BIT_COUNT) if segment else 0 for segment in segments]
    except ValueError:
        # IPv6 address was not made of valid hexadecimal numbers
        return False

    if len(processed_segments) != IPV6_MAX_SEGMENT_COUNT:
        valid = False

    if validation_mode == ValidationMode.STRICT and valid:
        valid = all(IPV6_MIN_SEGMENT_VALUE <= seg <= IPV6_MAX_SEGMENT_VALUE for seg in processed_segments)

    return valid
