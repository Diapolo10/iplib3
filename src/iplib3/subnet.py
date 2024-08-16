"""iplib3's functionality specific to subnetting."""

from __future__ import annotations

from typing import overload

from iplib3.constants.ipv4 import (
    IPV4_MIN_SEGMENT_COUNT,
    IPV4_SEGMENT_BIT_COUNT,
)
from iplib3.constants.subnet import (
    IPV4_MAX_SUBNET_VALUE,
    IPV4_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    SubnetType,
)


class PureSubnetMask:
    """Platform and version-independent base class for subnets."""

    __slots__ = ('_prefix_length',)

    def __init__(self: PureSubnetMask) -> None:
        """Create PureSubnetMask."""
        self._prefix_length: int | None = 0

    def __str__(self: PureSubnetMask) -> str:
        """Str conversion."""
        return str(self.prefix_length)

    def __repr__(self: PureSubnetMask) -> str:
        """Str representation."""
        return f"iplib3.{self.__class__.__name__}('{self}')"

    def __eq__(self: PureSubnetMask, other: object) -> bool:
        """Compare equality."""
        # To accommodate strings and integers
        if self.prefix_length == other or str(self) == other:
            return True

        if isinstance(other, PureSubnetMask):
            return self.prefix_length == other.prefix_length

        return False

    def __ne__(self: PureSubnetMask, other: object) -> bool:
        """Compare inequality."""
        return not self == other

    @property
    def prefix_length(self: PureSubnetMask) -> int | None:
        """
        Negative numbers aren't valid, they are treated as zero.

        TODO: Consider whether negative numbers should raise an exception
        """
        if self._prefix_length is None:
            return None

        return max(0, self._prefix_length)


class SubnetMask(PureSubnetMask):
    """Subnet mask for defining subnets."""

    __slots__ = ('_subnet_type',)

    def __init__(self: SubnetMask,
                 subnet_mask: int | str | None = None,
                 subnet_type: SubnetType = SubnetType.IPV6) -> None:
        """Create SubnetMask."""
        subnet_type = SubnetType(subnet_type)
        super().__init__()

        if isinstance(subnet_mask, str) and '.' in subnet_mask:
            # Only subnets for IPv4 use strings
            subnet_type = SubnetType.IPV4

        self._prefix_length: int | None = self._subnet_to_num(subnet_mask, subnet_type)
        self._subnet_type = subnet_type

    def __repr__(self: SubnetMask) -> str:
        """Str representation."""
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

        subnet_type = SubnetType(subnet_type)

        if subnet_mask is None:
            return None

        if not isinstance(subnet_mask, (int, str)):
            msg = f"Invalid type for subnet value: '{subnet_mask.__class__.__name__}'\nExpected int, string, or None"
            raise TypeError(
                msg,
            )

        if subnet_type == SubnetType.IPV4:
            subnet_mask = SubnetMask._ipv4_subnet_to_num(subnet_mask)

        if subnet_type == SubnetType.IPV6:
            if isinstance(subnet_mask, str):
                if '.' in subnet_mask:
                    msg = "IPv6-subnets don't use a string representation"
                    raise ValueError(msg)
                subnet_mask = int(subnet_mask)
            if not IPV6_MIN_SUBNET_VALUE <= subnet_mask <= IPV6_MAX_SUBNET_VALUE:
                msg = f"Subnet '{subnet_mask}' not in valid range ({IPV6_MIN_SUBNET_VALUE}-{IPV6_MAX_SUBNET_VALUE})"
                raise ValueError(
                    msg,
                )

        return int(subnet_mask)

    @staticmethod
    def _ipv4_subnet_to_num(subnet_mask: int | str) -> int:
        if isinstance(subnet_mask, str):
            if '.' in subnet_mask:
                segments = tuple(int(s) for s in reversed(subnet_mask.split('.')))
                if len(segments) != IPV4_MIN_SEGMENT_COUNT:
                    msg = f"Subnet value not valid; '{subnet_mask}' is not a valid string representation"
                    raise ValueError(
                        msg,
                    )

                segment_sum = sum(s<<(8*idx) for idx, s in enumerate(segments))
                subnet_bits = f'{segment_sum:b}'.rstrip('0')

                if '0' in subnet_bits:
                    msg = f"'{subnet_mask}' is an invalid subnet mask"
                    raise ValueError(msg)

                subnet_mask = len(subnet_bits)

            try:
                subnet_mask = int(subnet_mask)
            except ValueError as err:
                msg = f"Subnet value not valid; '{subnet_mask}' is neither a valid string representation nor an integer"
                raise ValueError(
                    msg,
                ) from err

        if not IPV4_MIN_SUBNET_VALUE <= subnet_mask <= IPV4_MAX_SUBNET_VALUE:
            msg = f"Subnet '{subnet_mask}' not in valid range ({IPV4_MIN_SUBNET_VALUE}-{IPV4_MAX_SUBNET_VALUE})"
            raise ValueError(
                msg,
            )

        return subnet_mask

    @staticmethod
    def _prefix_to_subnet_mask(prefix_length: int, subnet_type: SubnetType) -> str:

        subnet_type = SubnetType(subnet_type)

        if subnet_type == SubnetType.IPV6:
            msg = 'IPv6 does not support string representations of subnet masks'
            raise ValueError(msg)

        if not IPV4_MIN_SUBNET_VALUE <= prefix_length <= IPV4_MAX_SUBNET_VALUE:
            msg = f"Invalid subnet value for IPv4: '{prefix_length}'"
            raise ValueError(msg)

        segments = [0, 0, 0, 0]

        for idx, _ in enumerate(segments):
            segments[idx] = 2 ** max(min(IPV4_SEGMENT_BIT_COUNT, prefix_length), 0) - 1
            prefix_length -= IPV4_SEGMENT_BIT_COUNT
        return '.'.join(map(str, segments))
