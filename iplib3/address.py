"""iplib3's functionality specific to addresses"""

from typing import Any, List, Optional, Union

from iplib3.subnet import SubnetMask
from iplib3.constants.address import (
    IPV4_LOCALHOST,
    IPV6_LOCALHOST,
)
from iplib3.constants.port import (
    PORT_NUMBER_MIN_VALUE,
    PORT_NUMBER_MAX_VALUE,
)
from iplib3.constants.ipv4 import (
    IPV4_MAX_SEGMENT_COUNT,
    IPV4_MAX_SEGMENT_VALUE,
    IPV4_MIN_VALUE,
    IPV4_MAX_VALUE,
)
from iplib3.constants.ipv6 import (
    IPV6_NUMBER_BIT_COUNT,
    IPV6_SEGMENT_BIT_COUNT,
    IPV6_MIN_SEGMENT_COUNT,
    IPV6_MAX_SEGMENT_COUNT,
    IPV6_MIN_SEGMENT_VALUE,
    IPV6_MAX_SEGMENT_VALUE,
    IPV6_MAX_VALUE,
)
from iplib3.validators import (
    port_validator
)

__all__ = ('IPAddress', 'IPv4', 'IPv6')


class PureAddress:
    """Bare-bones, independent base class for IP addresses"""

    __slots__ = ('_num', '_port')

    def __init__(self, num: Optional[int] = None, port: Optional[int] = None):
        self._num: int = num if num is not None else 0
        self._port: Optional[int] = port if port_validator(port) else None

    def __eq__(self, other: Any) -> bool:

        if isinstance(other, PureAddress):
            return self.num == other.num and self.port == other.port

        return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return f"iplib3.{self.__class__.__name__}('{self}')"

    def __str__(self) -> str:
        return str(self.num)

    @property
    def num(self) -> int:
        """
        Negative numbers aren't valid,
        they are treated as zero.

        TODO: Consider whether negative numbers should raise an exception
        """

        return max(0, self._num)

    @property
    def port(self) -> Optional[int]:
        """
        Returns the port in the address, or None if no port is specified

        TODO: Consider whether invalid port numbers should raise an exception
        """

        if self._port is None:
            return None

        return min(max(PORT_NUMBER_MIN_VALUE, self._port), PORT_NUMBER_MAX_VALUE)

    @port.setter
    def port(self, value: Optional[int]) -> None:
        """
        Sets a new port value. Value must be a valid integer and within the range of valid ports.

        TODO: Find a way to avoid mutability
        """

        if value is None:
            pass  # OK

        elif not isinstance(value, int):
            raise TypeError(f"Port '{value}' is not a valid integer")
        elif not PORT_NUMBER_MIN_VALUE <= value <= PORT_NUMBER_MAX_VALUE:
            raise ValueError(
                f"Port number '{value}' not in valid range "
                f"({PORT_NUMBER_MIN_VALUE}-{PORT_NUMBER_MAX_VALUE})"
            )

        self._port = value

    @property
    def as_hex(self) -> str:
        """
        Returns a hexadecimal representation of the address
        """

        return f"0x{self.num:0X}"

    def num_to_ipv4(self) -> str:
        """
        A wrapper method for the otherwise equivalent static method
        """

        return self._num_to_ipv4(self.num)

    def num_to_ipv6(self, shorten: bool = True, remove_zeroes: bool = False) -> str:
        """
        A wrapper method for the otherwise equivalent static method
        """

        return self._num_to_ipv6(self.num, shorten, remove_zeroes)

    @staticmethod
    def _num_to_ipv4(num: int) -> str:
        """
        Generates an IPv4 string from an integer
        """

        segments = []
        for _ in range(IPV4_MAX_SEGMENT_COUNT):
            num, segment = divmod(num, IPV4_MAX_SEGMENT_VALUE+1)
            segments.append(segment)
        return '.'.join(str(segment) for segment in segments[::-1])

    @staticmethod
    def _num_to_ipv6(num: int, shorten: bool = True, remove_zeroes: bool = False) -> str:
        """
        Generates an IPv6 string from an integer,
        with optional zero removal and shortening.
        """

        segments = []
        for _ in range(IPV6_MAX_SEGMENT_COUNT):
            num, segment = divmod(num, IPV6_MAX_SEGMENT_VALUE+1)
            segments.append(hex(segment).split('x')[1].upper())

        if remove_zeroes and '0' in segments:

            # Goes over the segments to find the
            # longest strip with nothing but zeroes
            # and replaces it with an empty string.
            # The final str.join will turn to '::'.

            longest = 0
            longest_idx = 0
            current = 0
            current_idx = 0

            for idx, seg in enumerate(segments):

                if seg == '0':

                    if not current:
                        current_idx = idx
                    current += 1

                else:
                    current = 0

                if current > longest:
                    longest = current
                    longest_idx = current_idx

            segments = (
                (
                    segments[:longest_idx]
                    if IPV6_MIN_SEGMENT_COUNT < longest_idx < IPV6_MAX_SEGMENT_COUNT-1
                    else ['']
                )
                + ['']
                + (
                    segments[longest_idx+longest:]
                    if IPV6_MIN_SEGMENT_COUNT < longest_idx+longest < IPV6_MAX_SEGMENT_COUNT
                    else ['']
                  )
            )

        if not shorten:

            # Fills up any segments to full length by
            # adding missing zeroes to the front, if any.

            segments = [
                seg.zfill(IPV6_SEGMENT_BIT_COUNT // IPV6_NUMBER_BIT_COUNT)
                if seg else ''
                for seg in segments
            ]

        return ':'.join(segments[::-1])


class IPAddress(PureAddress):
    """More flexible PureAddress subclass"""

    __slots__ = ('_ipv4', '_ipv6', '_submask')

    def __new__(cls, address: Union[int, str, None] = None, port_num: Optional[int] = None, **kwargs):

        if isinstance(address, str):
            # Only IPv4-addresses have '.', ':' is used in both IPv4 and IPv6
            cls = IPv4 if '.' in address else IPv6

        self = object.__new__(cls)

        self.__init__(address=address, port_num=port_num, **kwargs)
        return self

    def __init__(self, address: Optional[int] = IPV4_LOCALHOST, port_num: Optional[int] = None):
        super().__init__(num=address, port=port_num)
        self._ipv4: Optional[IPv4] = None
        self._ipv6: Optional[IPv6] = None
        self._submask: Optional[SubnetMask] = None

    def __eq__(self, other: Any) -> bool:

        # To accommodate strings
        if str(self) == str(other):
            return True

        return super().__eq__(other)

    def __str__(self) -> str:

        if IPV4_MIN_VALUE <= self.num <= IPV4_MAX_VALUE:
            if self._ipv4 is None:
                self._ipv4 = self.as_ipv4
            return str(self._ipv4)

        if IPV4_MAX_VALUE < self.num <= IPV6_MAX_VALUE:
            if self._ipv6 is None:
                self._ipv6 = self.as_ipv6
            return str(self._ipv6)

        raise ValueError(f"No valid address representation exists for {self.num}")

    @property
    def as_ipv4(self) -> 'IPv4':
        """Creates and returns an IPv4 version of the address, if possible"""

        return IPv4(self.num_to_ipv4(), port_num=self.port)

    @property
    def as_ipv6(self) -> 'IPv6':
        """Creates and returns an IPv6-version of the address"""

        return IPv6(self.num_to_ipv6(), port_num=self.port)


class IPv4(IPAddress):
    """An IPAddress subclass specific to IPv4"""

    __slots__ = ('_address',)

    def __init__(self, address: Optional[str] = None, port_num: Optional[int] = None):

        if address is None:
            address = self._num_to_ipv4(IPV4_LOCALHOST)

        _address, *_port = address.split(':')
        if _port:
            address = _address

            if port_num is None:
                port_num = int(_port[0])

        self._address = address
        super().__init__(address=self._ipv4_to_num(), port_num=port_num)

    def __str__(self) -> str:

        if self.port is not None:
            return f"{self._address}:{self.port}"

        return self._address

    def _ipv4_to_num(self) -> int:
        """
        Takes a valid IPv4 address and turns
        it into an equivalent integer value.

        Raises ValueError on invalid IPv4 format.
        """

        segments = [int(segment) for segment in self._address.split('.')][::-1]
        total = 0

        for idx, num in enumerate(segments):
            total += num * 2**(idx * 8)

        return total


class IPv6(IPAddress):
    """An IPAddress subclass specific to IPv6"""

    __slots__ = ('_address',)

    def __init__(self, address: Optional[str] = None, port_num: Optional[int] = None):

        if address is None:
            address = self._num_to_ipv6(IPV6_LOCALHOST)

        _address, *_port = address.split(']:')

        if _port:

            # Removes the opening square bracket
            address = _address[1:]

            if port_num is None:
                port_num = int(_port[0])

        self._address = address
        super().__init__(address=self._ipv6_to_num(), port_num=port_num)

    def __str__(self) -> str:

        if self.port is not None:
            return f"[{self._address}]:{self.port}"

        return self._address

    def _ipv6_to_num(self) -> int:
        """
        Takes a valid IPv6 address and turns
        it into an equivalent integer value.

        Raises ValueError on invalid IPv6 format.
        """

        halves = self._address.split('::')
        segments = []

        if len(halves) == 2:
            # Address with zero-skip part
            left, right = (half.split(':') for half in halves)
            total_length = len(left) + len(right)

            if halves[0]:
                segments.extend(left)
            else:
                segments.append('0000')

            segments.extend(['0000' for _ in range(IPV6_MAX_SEGMENT_COUNT - total_length)])

            if halves[1]:
                segments.extend(right)
            else:
                segments.append('0000')

        elif len(halves) == 1:
            # Full address
            segments.extend(halves[0].split(':'))

        else:
            raise ValueError("Invalid IPv6 address format; only one zero-skip allowed")

        try:
            processed_segments: List[int] = [
                int(segment, IPV6_SEGMENT_BIT_COUNT) if segment else 0
                for segment in segments[::-1]
            ]
        except ValueError as err:
            raise ValueError("Invalid IPv6 address format; address contains invalid characters") from err

        segment_count = len(processed_segments)
        if IPV6_MAX_SEGMENT_COUNT < segment_count:
            raise ValueError(
                f"Invalid IPv6 address format; too many segments "
                f"({segment_count} > {IPV6_MAX_SEGMENT_COUNT})"
            )

        highest = max(processed_segments)
        if IPV6_MAX_SEGMENT_VALUE < highest:
            raise ValueError(
                f"Invalid IPv6 address format; segment max value "
                f"passed ({highest} > {IPV6_MAX_SEGMENT_VALUE})"
            )

        lowest = min(processed_segments)
        if lowest < IPV6_MIN_SEGMENT_VALUE:
            raise ValueError(
                f"Invalid IPv6 address format; segment min value passed ({lowest} < 0)"
            )

        total = 0
        for idx, num in enumerate(processed_segments):
            total += num * 2**(idx * 16)

        return total
