"""iplib3's functionality specific to validating things"""

from typing import List, Optional, Tuple, Union

from iplib3.constants.port import (
    PORT_NUMBER_MIN_VALUE,
    PORT_NUMBER_MAX_VALUE,
)
from iplib3.constants.ipv4 import (
    IPV4_MAX_SEGMENT_COUNT,
    IPV4_MIN_SEGMENT_COUNT,
    IPV4_MIN_SEGMENT_VALUE,
    IPV4_MAX_SEGMENT_VALUE,
    IPV4_MIN_VALUE,
    IPV4_MAX_VALUE,
)
from iplib3.constants.ipv6 import (
    IPV6_NUMBER_BIT_COUNT,
    IPV6_SEGMENT_BIT_COUNT,
    IPV6_MAX_SEGMENT_COUNT,
    IPV6_MIN_SEGMENT_VALUE,
    IPV6_MAX_SEGMENT_VALUE,
    IPV6_MIN_VALUE,
    IPV6_MAX_VALUE,
)
from iplib3.constants.subnet import (
    IPV4_VALID_SUBNET_SEGMENTS,
    IPV4_MIN_SUBNET_VALUE,
    IPV4_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
)

__all__ = ('port_validator', 'ip_validator', 'ipv4_validator', 'ipv6_validator', 'subnet_validator')


def port_validator(port_num: Optional[int]) -> bool:
    """
    Validates an address port

    None means "no port", and is treated as a valid port value.
    Otherwise the port must be an integer between the minimum and maximum port values, inclusive.

    Strings may be accepted in the future, but are not currently supported.

    The function should not raise an exception, wrong types will simply return False.
    """

    if port_num is None:
        return True

    return (
        isinstance(port_num, int)
        and PORT_NUMBER_MIN_VALUE <= port_num <= PORT_NUMBER_MAX_VALUE
    )


def ip_validator(address: Union[str, int], strict: bool = True) -> bool:
    """
    Validates an IP address of any kind, returning a boolean

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """

    if ipv4_validator(address, strict):
        return True
    return ipv6_validator(address, strict)


def ipv4_validator(address: Union[str, int], strict: bool = True) -> bool:
    """
    Validates an IPv4 address, returning a boolean

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """

    valid = False

    if isinstance(address, str) and '.' in address:

        portless_address, _, valid = _port_stripper(address, protocol='ipv4', strict=strict)

        if valid:
            valid = _ipv4_address_validator(portless_address, strict=strict)

    if isinstance(address, int):
        valid = IPV4_MIN_VALUE <= address <= IPV4_MAX_VALUE

    return valid


def ipv6_validator(address: Union[str, int], strict: bool = True) -> bool:
    """
    Validates an IPv6 address, returning a boolean

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """

    valid = False

    if isinstance(address, str):

        portless_address, _, valid = _port_stripper(address, protocol='ipv6', strict=strict)

        if not valid:
            return valid

        valid = _ipv6_address_validator(portless_address, strict=strict)

    if isinstance(address, int):
        valid = IPV6_MIN_VALUE <= address <= IPV6_MAX_VALUE

    return valid


def subnet_validator(subnet: Union[str, int], protocol='ipv4') -> bool:
    """
    Validates a given subnet mask, defaulting to IPv4 protocol

    Strings will be validated as IPv4 regardless of the protocol toggle
    as IPv6 subnets have no valid string representation.
    """

    valid = False

    if isinstance(subnet, str) or protocol.lower() == 'ipv4':
        valid = _ipv4_subnet_validator(subnet)

    elif protocol.lower() == 'ipv6':
        valid = _ipv6_subnet_validator(subnet)

    return valid


def _ipv4_subnet_validator(subnet: Union[str, int]) -> bool:
    """
    Validates an IPv4-compliant subnet mask

    The function uses the IPv4-standard to
    validate a subnet, including all values.

    Types other than strings or integers
    *will raise a TypeError* with the name
    of the used type.
    """

    if isinstance(subnet, int):
        return IPV4_MIN_SUBNET_VALUE <= subnet <= IPV4_MAX_SUBNET_VALUE

    if isinstance(subnet, str):
        segments = tuple(int(s) for s in subnet.split('.'))
        if len(segments) != IPV4_MIN_SEGMENT_COUNT:
            return False

        # Flag for catching invalid subnets where bits
        # are flipped out of order, eg. 255.128.128.0
        root_found = False
        for segment in segments[:-1]:

            if segment == IPV4_VALID_SUBNET_SEGMENTS[-1] and not root_found:
                continue  # Skip preceding 255s

            if root_found and segment != IPV4_VALID_SUBNET_SEGMENTS[0]:
                return False

            if segment not in IPV4_VALID_SUBNET_SEGMENTS:
                return False

            root_found = True

        return not (
            root_found
            and segments[-1] != IPV4_VALID_SUBNET_SEGMENTS[0]
            or not
            IPV4_VALID_SUBNET_SEGMENTS[0]
            <= segments[-1]
            <= IPV4_VALID_SUBNET_SEGMENTS[-1] - 1
        )

    raise TypeError(
        f"IPv4 subnet cannot be of type '{subnet.__class__.__name__}';"
        f" only strings and integers supported"
    )


def _ipv6_subnet_validator(subnet: int) -> bool:  # IPv6 subnets have no string representation
    """
    Validates an IPv6-compliant subnet mask

    The IPv6-standard has no string
    representation for subnests, so
    only integers need to be handled.

    Non-integer types will raise a ValueError
    with the name of the used type.
    """

    if isinstance(subnet, int):
        return (
            IPV6_MIN_SUBNET_VALUE <= subnet <= IPV6_MAX_SUBNET_VALUE
            and isinstance(subnet, int)
            and subnet % IPV6_NUMBER_BIT_COUNT == 0
        )

    raise TypeError(f"IPv6 subnet cannot be of type '{subnet.__class__.__name__}', it must be an integer")


def _port_stripper(address: str, protocol: str = 'ipv4', strict: bool = True) -> Tuple[str, Optional[int], bool]:
    """
    Extracts the port number from IP addresses, if any

    Returns a tuple with the portless address, the port (or None),
    and validation information as a boolean.
    """

    valid = True
    port_num = None
    port_separator = None

    if protocol.lower() == 'ipv4':
        port_separator = ':'
    elif protocol.lower() == 'ipv6':
        port_separator = ']:'
    else:
        valid = False

    # Try split on closing bracket and port separator
    address, *port = address.strip().split(port_separator)
    if port and valid:

        if protocol.lower() == 'ipv6':
            # Get rid of the opening bracket that contained the address (eg. [::12:34]:8080 -> ::12:34)
            address = address[1:]

        # Is port number a valid integer?
        try:
            port_num = int(port[0])
        except ValueError:
            valid = False

        if strict and valid:
            valid = port_validator(port_num)

    return address, port_num, valid


def _ipv4_address_validator(address: str, strict: bool = True) -> bool:
    """Validates the address part of an IPv4 address"""

    valid = True

    try:
        segments = [int(segment) for segment in address.split('.')]
    except ValueError:
        # IPv4 address was not made of valid integers
        valid = False

    else:
        if not IPV4_MIN_SEGMENT_COUNT <= len(segments) <= IPV4_MAX_SEGMENT_COUNT:
            # Invalid number of segments
            valid = False

        elif strict:
            for seg in segments:
                if not IPV4_MIN_SEGMENT_VALUE <= seg <= IPV4_MAX_SEGMENT_VALUE:
                    # Segment value was too high or too low to be strictly valid
                    valid = False
                    break

    return valid


def _ipv6_address_validator(address: str, strict: bool = True) -> bool:
    """Validates the address part of an IPv6 address"""

    valid = True
    segments = []
    empty_segment = f'{IPV6_MIN_SEGMENT_VALUE}' * IPV6_NUMBER_BIT_COUNT

    # Split on zero-skip, if any
    try:
        left, *extra, right = address.strip().split('::')
    except ValueError:
        # No zero-skip, full address
        segments.extend(address.split(':'))
    else:

        if not extra:
            # One, legal zero-skip
            left_segments = left.split(':')
            right_segments = right.split(':')
            total_segments = len(left_segments) + len(right_segments)

            if left:
                segments.extend(left_segments)
            else:
                segments.append(empty_segment)

            segments.extend(empty_segment for _ in range(IPV6_MAX_SEGMENT_COUNT - total_segments))

            if right:
                segments.extend(right_segments)
            else:
                segments.append(empty_segment)

        else:
            # More than one, illegal zero-skip
            valid = False

    try:
        processed_segments: List[int] = [
            int(segment, IPV6_SEGMENT_BIT_COUNT) if segment else 0
            for segment in segments
        ]
    except ValueError:
        # IPv6 address was not made of valid hexadecimal numbers
        valid = False
    else:

        if len(processed_segments) != IPV6_MAX_SEGMENT_COUNT:
            valid = False

        if strict and valid:
            valid = all(
                IPV6_MIN_SEGMENT_VALUE <= seg <= IPV6_MAX_SEGMENT_VALUE
                for seg in processed_segments
            )

    return valid
