"""iplib3's functionality specific to addresses"""

from abc import ABCMeta, abstractmethod
from typing import Any, List, Tuple, Optional, Union

from .constants.address import (
    IPV4_LOCALHOST,
    IPV6_LOCALHOST,
)
from .constants.port import (
    PORT_NUMBER_MIN_VALUE,
    PORT_NUMBER_MAX_VALUE,
)
from .constants.ipv4 import (
    IPV4_SEGMENT_BIT_COUNT,
    IPV4_MIN_SEGMENT_COUNT,
    IPV4_MAX_SEGMENT_COUNT,
    IPV4_MIN_SEGMENT_VALUE,
    IPV4_MAX_SEGMENT_VALUE,
    IPV4_MIN_VALUE,
    IPV4_MAX_VALUE,
)
from .constants.ipv6 import (
    IPV6_NUMBER_BIT_COUNT,
    IPV6_SEGMENT_BIT_COUNT,
    IPV6_MIN_SEGMENT_COUNT,
    IPV6_MAX_SEGMENT_COUNT,
    IPV6_MIN_SEGMENT_VALUE,
    IPV6_MAX_SEGMENT_VALUE,
    IPV6_MIN_VALUE,
    IPV6_MAX_VALUE,
)
from .constants.subnet import (
    IPV4_VALID_SUBNET_SEGMENTS,
    IPV4_MIN_SUBNET_VALUE,
    IPV4_MAX_SUBNET_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
)

__all__ = ('IPAddress', 'IPv4', 'IPv6')


# Note; all functions with leading underscores are considered
# not to be part of the public interface. They may receive
# sudden changes, they may be moved, and they may even be
# completely deleted in the future. Please don't rely on them
# outside the library. If proven useful and working, some of
# them may eventually make their way into the public interface
# in which case the leading underscores will be removed.
# - L


def _port_validator(port_num: Optional[int]) -> bool:
    """
    Validates an address port

    None means "no port", and is treated as a valid port value.
    Otherwise the port must be an integer between the minimum and maximum port values, inclusive.

    Strings may be accepted in the future, but are not currently supported.

    The function should not raise an exception, wrong types will simply return False.
    """

    if port_num is None:
        pass # OK
        
    elif not isinstance(port_num, int):
        return False
    elif not PORT_NUMBER_MIN_VALUE <= port_num <= PORT_NUMBER_MAX_VALUE:
        return False
    
    return True


def _ipv4_validator(address: Union[str, int], strict: bool = True) -> bool:
    """
    Validates an IPv4 address, returning a boolean.

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """

    if isinstance(address, str):

        if '.' not in address:
            return False

        address, *port = address.split(':')
        if port: # Handles ports separately to keep the rest of the code intact
            try:
                port_num = int(port[0])
            except ValueError:
                # Port number wasn't a valid integer
                return False

            if strict:
                if not PORT_NUMBER_MIN_VALUE <= port_num <= PORT_NUMBER_MAX_VALUE: # 2**16
                    # Port number was too high or too low to be strictly valid
                    return False

        try:
            segments = list(map(int, address.split('.')))
        except ValueError:
            # IPv4 address was not made of valid integers
            return False

        if len(segments) != IPV4_MAX_SEGMENT_COUNT:
            # Invalid number of segments
            return False

        if strict:
            for seg in segments:
                if not IPV4_MIN_SEGMENT_VALUE <= seg <= IPV4_MAX_SEGMENT_VALUE:
                    # Segment value was too high or too low to be strictly valid
                    return False

        return True

    elif isinstance(address, int):
        return IPV4_MIN_VALUE <= address <= IPV4_MAX_VALUE

    return False


def _ipv6_validator(address: Union[str, int], strict: bool = True) -> bool:
    """
    Validates an IPv6 address, returning a boolean.

    Under strict mode ensures that the numerical values
    don't exceed legal bounds, otherwise focuses on form.
    """

    if isinstance(address, str):

        address, *port = address.split(']:') # Try split on closing bracket and port separator
        if port:
            address = address[1:] # Gets rid of the opening bracket that contained the address
            try:
                port_num = int(port[0])
            except ValueError:
                # Port number wasn't a valid integer
                return False

            if strict:
                if not PORT_NUMBER_MIN_VALUE <= port_num <= PORT_NUMBER_MAX_VALUE: # 2**16
                    # Port number was too high or too low to be strictly valid
                    return False

        halves = address.split('::')
        segments = []

        if len(halves) == 2:
            # Address with zero-skip part
            left, right = map(lambda x: x.split(':'), halves)
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
            # More than one zero-skip
            return False

        try:
            processed_segments: List[int] = list(map(
                lambda x: int(x, IPV6_SEGMENT_BIT_COUNT) if x else 0,
                segments
            ))
        except ValueError:
            # IPv6 address was not made of valid hexadecimal numbers
            return False

        if len(processed_segments) != IPV6_MAX_SEGMENT_COUNT:
            # Invalid number of segments
            return False

        if strict:
            for seg in processed_segments:
                if not IPV6_MIN_SEGMENT_VALUE <= seg <= IPV6_MAX_SEGMENT_VALUE:
                    # Segment value was too high or too low to be strictly valid
                    return False

        return True

    elif isinstance(address, int):
        return IPV6_MIN_VALUE <= address <= IPV6_MAX_VALUE

    return False


def _ip_validator(address: Union[str, int], strict: bool = True):
    if _ipv4_validator(address, strict):
        return True
    return _ipv6_validator(address, strict)


class PureAddress(metaclass=ABCMeta):
    """Abstract base class for IP addresses"""

    __slots__ = ('_num', '_port')


    @abstractmethod
    def __init__(self):
        self._num: int = 0
        self._port: Optional[int] = None


    def __eq__(self, other: Any) -> bool:

        # To accommodate strings
        if str(self) == str(other):
            return True
        
        if not isinstance(other, PureAddress):
            return False
        
        if not self.num == other.num and self.port == other.port:
            return False

        return True


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
            pass # OK
        
        elif not isinstance(value, int):
            raise TypeError(f"Port '{value}' is not a valid integer")
        elif not PORT_NUMBER_MIN_VALUE <= value <= PORT_NUMBER_MAX_VALUE:
            raise ValueError(f"Port number '{value}' not in valid range ({PORT_NUMBER_MIN_VALUE}-{PORT_NUMBER_MAX_VALUE})")
        
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

        TODO: toggleable shortening and optionally
              remove one section of zeroes
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
        return '.'.join(map(str, segments[::-1]))


    @staticmethod
    def _num_to_ipv6(num: int, shorten: bool, remove_zeroes: bool) -> str:
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
    __slots__ = ('_ipv4', '_ipv6', '_submask')

    def __new__(cls, address: Union[int, str, None] = None, *args, **kwargs):

        if isinstance(address, str):
            # Only IPv4-addresses have '.', ':' is used in both IPv4 and IPv6
            cls = IPv4 if '.' in address else IPv6

        self = object.__new__(cls)

        self.__init__(address, *args, **kwargs)
        return self


    def __init__(self, address_num=IPV4_LOCALHOST, port_num=None):
        self._num = address_num if address_num is not None else 0
        self._port = port_num if _port_validator(port_num) else None
        self._ipv4 = None
        self._ipv6 = None
        self._submask = None


    def __repr__(self) -> str:
        return f"iplib3.{self.__class__.__name__}('{self}')"


    def __str__(self) -> str:
        
        if IPV4_MIN_VALUE <= self.num <= IPV4_MAX_VALUE:
            if self._ipv4 is None:
                self._ipv4 = self.as_ipv4
            return str(self._ipv4)

        elif IPV4_MAX_VALUE < self.num <= IPV6_MAX_VALUE:
            if self._ipv6 is None:
                self._ipv6 = self.as_ipv6
            return str(self._ipv6)
        
        else:
            raise ValueError(f"No valid address representation exists for {self.num}")


    @property
    def as_ipv4(self) -> 'IPv4':
        return IPv4(self.num_to_ipv4(), port_num=self.port)


    @property
    def as_ipv6(self) -> 'IPv6':
        return IPv6(self.num_to_ipv6(), port_num=self.port)


class IPv4(IPAddress):
    __slots__ = ('_address',)

    def __init__(self, address: str, port_num: Optional[int] = None):
        
        self._port = port_num

        _address, *_port = address.split(':')
        if _port:
            address = _address

            if port_num is None:
                self._port = int(_port[0])

        self._address = address
        self._num = self._ipv4_to_num()


    def __str__(self) -> str:
        if self.port is not None:
            return f"{self._address}:{self.port}"
        else:
            return self._address


    def _ipv4_to_num(self) -> int:
        """
        Takes a valid IPv4 address and turns
        it into an equivalent integer value.

        Raises ValueError on invalid IPv4 format.
        """

        segments = list(map(int, self._address.split('.')))[::-1]
        total = 0

        for idx, num in enumerate(segments):
            total += num * 2**(idx * 8)
    
        return total


class IPv6(IPAddress):
    __slots__ = ('_address',)

    def __init__(self, address: str, port_num: Optional[int] = None):

        self._port = port_num

        _address, *_port = address.split(']:')
        if _port:
            address = _address[1:] # Removes the opening square bracket

            if port_num is None:
                self._port = int(_port[0])

        self._address = address
        self._num = self._ipv6_to_num()


    def __str__(self) -> str:
        if self.port is not None:
            return f"[{self._address}]:{self.port}"
        else:
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
            left, right = map(lambda x: x.split(':'), halves)
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
            processed_segments: List[int] = list(map(lambda num: int(num, 16) if num != '' else 0, segments[::-1]))
        except ValueError:
            raise ValueError(f"Invalid IPv6 address format; address contains invalid characters")

        segment_count = len(processed_segments)
        if IPV6_MAX_SEGMENT_COUNT < segment_count:
            raise ValueError(f"Invalid IPv6 address format; too many segments ({segment_count} > {IPV6_MAX_SEGMENT_COUNT})")

        highest = max(processed_segments)
        if IPV6_MAX_SEGMENT_VALUE < highest:
            raise ValueError(f"Invalid IPv6 address format; segment max value passed ({highest} > {IPV6_MAX_SEGMENT_VALUE})")

        lowest = min(processed_segments)
        if lowest < IPV6_MIN_SEGMENT_VALUE:
            raise ValueError(f"Invalid IPv6 address format; segment min value passed ({lowest} < 0)")
        
        total = 0
        for idx, num in enumerate(processed_segments):
            total += num * 2**(idx * 16)

        return total