from abc import ABCMeta, abstractmethod
from typing import Optional, Union, Any

from .constants.ipv4 import (
    IPV4_MAX_SEGMENT_COUNT,
    IPV4_MAX_SEGMENT_VALUE,
)
from .constants.subnet import (
    IPV4_VALID_SUBNET_SEGMENTS,
    IPV4_MIN_SUBNET_VALUE,
    IPV4_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
)


class PureSubnetMask(metaclass=ABCMeta):
    """
    Abstract base class for subnets
    """
    __slots__ = ('_prefix_length',)


    @abstractmethod
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
        
        if not isinstance(other, PureSubnetMask):
            return False
        
        if not self.prefix_length == other.prefix_length:
            return False

        return True


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
    __slots__ = ('_subnet_type',)

    def __init__(self, subnet_mask: Union[int, str, None] = None, subnet_type: str = 'ipv6'):

        if isinstance(subnet_mask, str) and '.' in subnet_mask:
            # Only subnets for IPv4 use strings
            subnet_type = 'ipv4'

        self._prefix_length: Optional[int] = self._subnet_to_num(subnet_mask, subnet_type)
        self._subnet_type = subnet_type


    def __repr__(self):
        if self._subnet_type.lower() == 'ipv4' and self._prefix_length is not None:
            return f"iplib3.{self.__class__.__name__}({self._prefix_to_subnet_mask(self._prefix_length, self._subnet_type)})"
        return super().__repr__()


    @staticmethod
    def _subnet_to_num(subnet_mask: Union[int, str, None], subnet_type: str = 'ipv6') -> Optional[int]:

        if subnet_mask is None:
            return None

        if not isinstance(subnet_mask, (int, str)):
            raise TypeError(f"Invalid type for subnet value: '{subnet_mask.__class__.__name__}'\nExpected int, string or None")

        if isinstance(subnet_mask, str):
            if '.' in subnet_mask:
                if subnet_type.lower() == 'ipv6':
                    raise ValueError("IPv6-subnets don't use a string representation")

                segments = list(map(int, subnet_mask.split('.')))[::-1]
                total = 0

                for idx, num in enumerate(segments):
                    total += num * 2**(idx * 8)

                return total

            try:
                subnet_mask = int(subnet_mask)
            except ValueError:
                raise ValueError(f"Subnet value not valid; '{subnet_mask}' is neither a valid string representation nor an integer")


        if subnet_type.lower() == 'ipv4' and not IPV4_MIN_SUBNET_VALUE <= subnet_mask <= IPV4_MAX_SUBNET_VALUE:
            raise ValueError(f"Subnet '{subnet_mask}' not in valid range ({IPV4_MIN_SUBNET_VALUE}-{IPV4_MAX_SUBNET_VALUE})")

        if subnet_type.lower() == 'ipv6' and not IPV6_MIN_SUBNET_VALUE <= subnet_mask <= IPV6_MAX_SUBNET_VALUE:
            raise ValueError(f"Subnet '{subnet_mask}' not in valid range ({IPV6_MIN_SUBNET_VALUE}-{IPV6_MAX_SUBNET_VALUE})")

        return subnet_mask


    @staticmethod
    def _prefix_to_subnet_mask(prefix_length: int, subnet_type: str) -> str:

        if subnet_type.lower() == 'ipv6':
            raise ValueError("IPv6 does not support string representations of subnet masks")

        if not IPV4_MIN_SUBNET_VALUE <= prefix_length <= IPV4_MAX_SUBNET_VALUE:
            raise ValueError(f"Invalid subnet value for IPv4: '{prefix_length}'")

        segments = []
        for _ in range(IPV4_MAX_SEGMENT_COUNT):
            prefix_length, segment = divmod(prefix_length, IPV4_MAX_SEGMENT_VALUE+1)
            segments.append(segment)
        return '.'.join(map(str, segments[::-1]))