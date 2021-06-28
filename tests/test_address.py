"""Unit tests for iplib3.address"""

import pytest

from iplib3 import (  # pylint: disable=import-error,no-name-in-module
    IPAddress, IPv4, IPv6
)
from iplib3.address import (  # pylint: disable=import-error,no-name-in-module
    PureAddress,
)
from iplib3.constants import (  # pylint: disable=import-error,no-name-in-module
    IPV6_MAX_VALUE,
    PORT_NUMBER_MAX_VALUE,
)


def test_ipv4():
    """Unit tests for IPv4"""

    assert str(IPAddress(25601440).as_ipv4) == '1.134.165.160'
    assert str(IPAddress('192.168.1.1')) == '192.168.1.1'
    assert str(IPv4('192.168.1.1')) == '192.168.1.1'
    assert str(IPAddress('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPv4('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPAddress(0xDEADBEEF).as_ipv4) == '222.173.190.239'
    assert str(IPAddress(0xDEADBEEF, port_num=80).as_ipv4) == '222.173.190.239:80'
    assert str(IPv4()) == '127.0.0.1'

    address = IPAddress(0xDEADBEEF)
    assert address == IPAddress(0xDEADBEEF)
    assert (address == IPAddress(0xDEADBEEF, port_num=8080)) is False
    assert address != IPAddress(0x1057B317)
    assert address != "Hello, world!"


def test_ipv4_port_initialisation():
    """Unit tests for IPv4 port number initialisation"""

    first = IPv4('222.173.190.239:80')
    second = IPv4('222.173.190.239', 80)  # pylint: disable=too-many-function-args
    third = IPv4('222.173.190.239', port_num=80)
    fourth = IPv4('222.173.190.239:25565', port_num=80)  # Argument-given ports should be preferred

    assert first == second == third == fourth
    assert str(third) == '222.173.190.239:80'

    first.port = 42
    assert first.port == 42
    first.port = None
    assert first.port is None

    with pytest.raises(TypeError):
        first.port = "1337"

    with pytest.raises(ValueError):
        first.port = PORT_NUMBER_MAX_VALUE+1


def test_ipv6():
    """Unit tests for IPv6"""

    assert str(IPAddress(25601440).as_ipv6) == '0:0:0:0:0:0:186:A5A0'
    assert str(IPAddress('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPv6('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPAddress('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPv6('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPAddress(0xDEADBEEF).as_ipv6) == '0:0:0:0:0:0:DEAD:BEEF'
    assert str(IPv6()) == '0:0:0:0:0:0:0:1'


def test_ipv6_full():
    """Test full-sized IPv6 string representation"""

    assert (
        IPAddress(25601440).num_to_ipv6(shorten=False)
        == '0000:0000:0000:0000:0000:0000:0186:A5A0'
    )


def test_ipv6_remove_zeroes():
    """Test IPv6 shortening"""

    assert IPAddress(25601440).num_to_ipv6(remove_zeroes=True) == '::186:A5A0'
    assert IPAddress(0xDEADBEEF).num_to_ipv6(remove_zeroes=True) == '::DEAD:BEEF'


def test_ipv6_port_initialisation():
    """Test IPv6 port number initialisation"""

    first = IPv6('[::1337:1337:1337:1337]:25565')
    second = IPv6('::1337:1337:1337:1337', 25565)  # pylint: disable=too-many-function-args
    third = IPv6('::1337:1337:1337:1337', port_num=25565)
    fourth = IPv6('[::1337:1337:1337:1337]:80', port_num=25565)

    assert first == second == third == fourth
    assert str(third) == '[::1337:1337:1337:1337]:25565'


def test_chaining():
    """Test chaining conversions between the IPAddress types"""

    assert str(IPAddress(25601440).as_ipv6.as_ipv4) == '1.134.165.160'


def test_hex_output():
    """Test hex number output"""

    base = IPAddress(0xDEADBEEF)
    four = base.as_ipv4
    six = base.as_ipv6

    assert base.as_hex == '0xDEADBEEF'
    assert four.as_hex == '0xDEADBEEF'
    assert six.as_hex == '0xDEADBEEF'


def test_pure_address():
    """Test the PureAddress base class"""

    assert PureAddress()
    assert PureAddress(0xDE_AD_BE_EF)
    assert PureAddress(port=80)
    assert PureAddress(0x7F_00_00_01, 80)


def test_ipaddress():
    """Test the IPAddress class"""

    instance = IPAddress()
    instance2 = IPAddress(0xDEAD_DEAD_BEEF)

    assert repr(IPAddress()) == "iplib3.IPAddress('127.0.0.1')"
    assert str(instance) == '127.0.0.1'
    assert str(instance) == '127.0.0.1'
    assert str(instance2) == '0:0:0:0:0:DEAD:DEAD:BEEF'
    assert str(instance2) == '0:0:0:0:0:DEAD:DEAD:BEEF'

    rigged = IPAddress(IPV6_MAX_VALUE+1)
    # rigged.num.func.setter = (lambda self, x: setattr(self._num, x))
    # rigged.num = IPV6_MAX_VALUE+1

    with pytest.raises(ValueError):
        str(rigged)


def test_ipv6_to_num():
    """Test leftover functionality on IPv6"""

    assert IPv6('70::')._ipv6_to_num()
    with pytest.raises(ValueError):
        IPv6('12::34::')._ipv6_to_num()
    with pytest.raises(ValueError):
        IPv6('::H07:AF')._ipv6_to_num()
    with pytest.raises(ValueError):
        IPv6('1:1:1:1:1:1:1:1:1')._ipv6_to_num()
    with pytest.raises(ValueError):
        IPv6('::7:FFFFF')._ipv6_to_num()
    with pytest.raises(ValueError):
        IPv6('::7:-34')._ipv6_to_num()
