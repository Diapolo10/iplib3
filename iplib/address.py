class IPAddress:

    def __init__(self, value=None):
        self._num = 0
        self._ipv4 = "0.0.0.0"
        self._ipv6 = "::"

        if value is None:
            self._ipv4 = self.num_to_ipv4()
            self._ipv6 = self.num_to_ipv6()


    def num_to_ipv4(self):

        num = self._num

        segments = []
        for _ in range(4):
            num, segment = divmod(num, 0xFF+1)
            segments.append(segment)
        return '.'.join(map(str, segments[::-1]))

    def num_to_ipv6(self):
        """ Todo: toggleable shortening and optionally
        remove one section of zeroes """

        num = self._num
        segments = []
        for _ in range(8):
            num, segment = divmod(num, 0xFFFF+1)
            segments.append(hex(segment).split('x')[1].upper())
        return ':'.join(map(str, segments[::-1]))

    def ipv4_to_num(self) -> int:
        """
        Takes a valid IPv4 address and turns
        it into an equivalent integer value.

        Raises ValueError on invalid IPv4 format.
        """

        segments = list(map(int, self._ipv4.split('.')))[::-1]
        total = 0

        for idx, num in enumerate(segments):
            total += num * 2**(idx * 8)
    
        return total

    def ipv6_to_num(self) -> int:
        """
        Takes a valid IPv6 address and turns
        it into an equivalent integer value.

        Raises ValueError on invalid IPv6 format.
        """

        MAX_SEGMENT_COUNT = 8
        MAX_SEGMENT_VALUE = 0xFFFF

        halves = self._ipv6.split('::')
        segments = []

        if len(halves) == 2: # Address with zero-skip part
            total_length = sum(map(len, halves))
            
            if halves[0]:
                segments.extend(halves[0].split(':'))
            
            segments.extend(['0000' for _ in range(MAX_SEGMENT_COUNT - total_length)])
            
            if halves[1]:
                segments.extend(halves[1].split(':'))

        elif len(halves) == 1: # Full address
            segments.extend(halves[0].split(':'))

        else:
            raise ValueError("Invalid IPv6 address format; only one zero-skip allowed")

        segments = list(map(lambda num: int(num, 16), segments[::-1]))
        total = 0

        if (segment_count := len(segments) > MAX_SEGMENT_COUNT):
            raise ValueError(f"Invalid IPv6 address format; too many segments ({segment_count} > {MAX_SEGMENT_COUNT})")

        if (value := max(segments) > MAX_SEGMENT_VALUE):
            raise ValueError(f"Invalid IPv6 address format; segment max value passed ({value} > {MAX_SEGMENT_VALUE})")

        for idx, num in enumerate(segments):
            total += num * 2**(idx * 16)

        return total
