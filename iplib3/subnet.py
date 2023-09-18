"""iplib3's functionality specific to subnetting"""

from __future__ import annotations

from enum import Enum
from typing import overload

from iplib3.constants.ipv4 import (
    IPV4_SEGMENT_BIT_COUNT,
)
from iplib3.constants.subnet import (
    IPV4_MAX_SUBNET_VALUE,
    IPV4_MIN_SUBNET_VALUE,
    IPV4_VALID_SUBNET_SEGMENTS,
    IPV6_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
)


class SubnetType(str, Enum):
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'

    @classmethod
    def _missing_(cls: SubnetType, value: str) -> SubnetType:
        for member in cls:
            if member.value == value.lower():
                return member
        return None


class PureSubnetMask:
    """
    Platform and version-independent base class for subnets
    """
    __slots__ = ('_prefix_length',)

    def __init__(self: PureSubnetMask) -> None:
        self._prefix_length: int | None = 0

    def __str__(self: PureSubnetMask) -> str:
        return str(self.prefix_length)

    def __repr__(self: PureSubnetMask) -> str:
        return f"iplib3.{self.__class__.__name__}('{self}')"

    def __eq__(self: PureSubnetMask, other: object) -> bool:

        # To accommodate strings and integers
        if self.prefix_length == other or str(self) == other:
            return True

        if isinstance(other, PureSubnetMask):
            return self.prefix_length == other.prefix_length

        return False

    def __ne__(self: PureSubnetMask, other: object) -> bool:
        return not self == other

    @property
    def prefix_length(self: PureSubnetMask) -> int | None:
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

    def __init__(self: SubnetMask, subnet_mask: int | str | None = None, subnet_type: SubnetType = SubnetType.IPV6) -> None:
        super().__init__()

        if isinstance(subnet_mask, str) and '.' in subnet_mask:
            # Only subnets for IPv4 use strings
            subnet_type = SubnetType.IPV4

        self._prefix_length: int | None = self._subnet_to_num(subnet_mask, subnet_type)
        self._subnet_type = subnet_type

    def __repr__(self: SubnetMask) -> str:
        if self._subnet_type == SubnetType.IPV4 and self._prefix_length is not None:
            return (
                f"iplib3.{self.__class__.__name__}"
                f"('{self._prefix_to_subnet_mask(self._prefix_length, self._subnet_type)}')"
            )
        return super().__repr__()

    @overload
    @staticmethod
    def _subnet_to_num(subnet_mask: None, subnet_type: SubnetType) -> None:
        ...

    @overload
    @staticmethod
    def _subnet_to_num(subnet_mask: int | str, subnet_type: SubnetType) -> int:
        ...

    @staticmethod
    def _subnet_to_num(subnet_mask: int | str | None, subnet_type: SubnetType = SubnetType.IPV6) -> int | None:

        if subnet_mask is None:
            return None

        if not isinstance(subnet_mask, (int, str)):
            raise TypeError(
                f"Invalid type for subnet value: '{subnet_mask.__class__.__name__}'\n"
                f"Expected int, string, or None",
            )

        if isinstance(subnet_mask, str):
            if '.' in subnet_mask:
                if subnet_type == SubnetType.IPV6:
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
                    f"Subnet value not valid; '{subnet_mask}' is neither a valid string representation nor an integer",
                ) from err

        if subnet_type == SubnetType.IPV4 and not IPV4_MIN_SUBNET_VALUE <= subnet_mask <= IPV4_MAX_SUBNET_VALUE:
            raise ValueError(
                f"Subnet '{subnet_mask}' not in valid range "
                f"({IPV4_MIN_SUBNET_VALUE}-{IPV4_MAX_SUBNET_VALUE})",
            )

        if subnet_type == SubnetType.IPV6 and not IPV6_MIN_SUBNET_VALUE <= subnet_mask <= IPV6_MAX_SUBNET_VALUE:
            raise ValueError(
                f"Subnet '{subnet_mask}' not in valid range "
                f"({IPV6_MIN_SUBNET_VALUE}-{IPV6_MAX_SUBNET_VALUE})",
            )

        return subnet_mask

    @staticmethod
    def _prefix_to_subnet_mask(prefix_length: int, subnet_type: SubnetType) -> str:

        if subnet_type == SubnetType.IPV6:
            raise ValueError("IPv6 does not support string representations of subnet masks")

        if not IPV4_MIN_SUBNET_VALUE <= prefix_length <= IPV4_MAX_SUBNET_VALUE:
            raise ValueError(f"Invalid subnet value for IPv4: '{prefix_length}'")

        segments = [0, 0, 0, 0]

        for idx, _ in enumerate(segments):
            segments[idx] = 2 ** max(min(IPV4_SEGMENT_BIT_COUNT, prefix_length), 0) - 1
            prefix_length -= IPV4_SEGMENT_BIT_COUNT
        return '.'.join(map(str, segments))
