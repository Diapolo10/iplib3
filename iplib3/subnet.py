"""iplib3's functionality specific to subnetting"""

from typing import Optional, Union, Any

from .constants.ipv4 import (
    IPV4_MIN_SEGMENT_COUNT,
    IPV4_SEGMENT_BIT_COUNT,
)
from .constants.ipv6 import (
    IPV6_NUMBER_BIT_COUNT,
)
from .constants.subnet import (
    IPV4_VALID_SUBNET_SEGMENTS,
    IPV4_MIN_SUBNET_VALUE,
    IPV4_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
)


class PureSubnetMask:
    """
    Platform and version-independent base class for subnets
    """
    __slots__ = ('_prefix_length',)


    def __init__(self):
        self._prefix_length: Optional[int] = 0


    def __str__(self) -> str:
        return str(self.prefix_length)


    def __repr__(self) -> str:
        return f"iplib3.{self.__class__.__name__}('{self}')"


    def __eq__(self, other: Any) -> bool:

        # To accommodate strings and integers
        if self.prefix_length == other or str(self) == other:
            return True

        if isinstance(other, PureSubnetMask):
            print("puresubnetmask")
            return self.prefix_length == other.prefix_length

        return False


    @property
    def prefix_length(self) -> Optional[int]:
        """
        Negative numbers aren't valid,
        they are treated as zero.

        TODO: Consider whether negative numbers should raise an exception
        """

        if self._prefix_length is None:
            return None

        return max(0, self._prefix_length)


class SubnetMask(PureSubnetMask):
    """Subnet mask for defining subnets"""

    __slots__ = ('_subnet_type',)

    def __init__(self, subnet_mask: Union[int, str, None] = None, subnet_type: str = 'ipv6'):
        super().__init__()

        if isinstance(subnet_mask, str) and '.' in subnet_mask:
            # Only subnets for IPv4 use strings
            subnet_type = 'ipv4'

        self._prefix_length: Optional[int] = self._subnet_to_num(subnet_mask, subnet_type)
        self._subnet_type = subnet_type.lower()


    def __repr__(self):
        if self._subnet_type.lower() == 'ipv4' and self._prefix_length is not None:
            return (
                f"iplib3.{self.__class__.__name__}"
                f"('{self._prefix_to_subnet_mask(self._prefix_length, self._subnet_type)}')"
            )
        return super().__repr__()


    @staticmethod
    def _subnet_to_num(subnet_mask: Union[int, str, None], subnet_type: str = 'ipv6') -> Optional[int]:

        if subnet_mask is None:
            return None

        if not isinstance(subnet_mask, (int, str)):
            raise TypeError(
                f"Invalid type for subnet value: '{subnet_mask.__class__.__name__}'\n"
                f"Expected int, string, or None"
            )

        if isinstance(subnet_mask, str):
            if '.' in subnet_mask:
                if subnet_type.lower() == 'ipv6':
                    raise ValueError("IPv6-subnets don't use a string representation")

                segments = list(map(int, subnet_mask.split('.')))[::-1]
                total = 0

                try:
                    for segment in segments:
                        total += {
                            subnet: idx
                            for idx, subnet in enumerate(IPV4_VALID_SUBNET_SEGMENTS)
                        }[segment]
                except KeyError as err:
                    raise ValueError(f"'{segment}' is an invalid value in a subnet mask") from err

                return total

            try:
                subnet_mask = int(subnet_mask)
            except ValueError as err:
                raise ValueError(
                    f"Subnet value not valid; '{subnet_mask}' is neither a valid string representation nor an integer"
                ) from err


        if (subnet_type.lower() == 'ipv4'
            and not IPV4_MIN_SUBNET_VALUE <= subnet_mask <= IPV4_MAX_SUBNET_VALUE):
            raise ValueError(
                f"Subnet '{subnet_mask}' not in valid range "
                f"({IPV4_MIN_SUBNET_VALUE}-{IPV4_MAX_SUBNET_VALUE})"
            )

        if (subnet_type.lower() == 'ipv6'
            and not IPV6_MIN_SUBNET_VALUE <= subnet_mask <= IPV6_MAX_SUBNET_VALUE):
            raise ValueError(
                f"Subnet '{subnet_mask}' not in valid range "
                f"({IPV6_MIN_SUBNET_VALUE}-{IPV6_MAX_SUBNET_VALUE})"
            )

        return subnet_mask


    @staticmethod
    def _prefix_to_subnet_mask(prefix_length: int, subnet_type: str) -> str:

        if subnet_type.lower() == 'ipv6':
            raise ValueError("IPv6 does not support string representations of subnet masks")

        if not IPV4_MIN_SUBNET_VALUE <= prefix_length <= IPV4_MAX_SUBNET_VALUE:
            raise ValueError(f"Invalid subnet value for IPv4: '{prefix_length}'")

        segments = [0, 0, 0, 0]

        for idx, _ in enumerate(segments):
            segments[idx] = 2 ** max(min(IPV4_SEGMENT_BIT_COUNT, prefix_length), 0) - 1
            prefix_length -= IPV4_SEGMENT_BIT_COUNT
        return '.'.join(map(str, segments))


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
        segments = tuple(map(int, subnet.split('.')))
        if len(segments) != IPV4_MIN_SEGMENT_COUNT:
            return False

        # Flag for catching invalid subnets where bits
        # are flipped out of order, eg. 255.128.128.0
        root_found = False
        for segment in segments[:-1]:

            if segment == IPV4_VALID_SUBNET_SEGMENTS[-1] and not root_found:
                continue # Skip preceding 255s

            if (root_found and segment != IPV4_VALID_SUBNET_SEGMENTS[0]
                or segment not in IPV4_VALID_SUBNET_SEGMENTS):
                return False

            root_found = True

        return not (root_found
            and segments[-1] != IPV4_VALID_SUBNET_SEGMENTS[0]
            or not
                IPV4_VALID_SUBNET_SEGMENTS[0]
                <= segments[-1]
                <= IPV4_VALID_SUBNET_SEGMENTS[-1] - 1)

    raise TypeError(
        f"IPv4 subnet cannot be of type '{subnet.__class__.__name__}';"
        f" only strings and integers supported"
    )


def _ipv6_subnet_validator(subnet: int) -> bool: # IPv6 subnets have no string representation
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


def _subnet_validator(subnet: Union[str, int], protocol='ipv4') -> bool:
    """
    Validates a given subnet mask, defaulting to IPv4 protocol
    """

    if isinstance(subnet, str) or protocol.lower() == 'ipv4':
        return _ipv4_subnet_validator(subnet)

    if protocol.lower() == 'ipv6':
        return _ipv6_subnet_validator(subnet)

    raise ValueError("Invalid protocol")
