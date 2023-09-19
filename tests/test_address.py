"""Unit tests for iplib3.address"""

import pytest

from iplib3 import IPAddress, IPv4, IPv6  # pylint: disable=import-error,no-name-in-module
from iplib3.address import (  # pylint: disable=import-error,no-name-in-module
    PureAddress,
)
from iplib3.constants import (  # pylint: disable=import-error,no-name-in-module
    IPV4_LOCALHOST,
    IPV6_LOCALHOST,
    IPV6_MAX_VALUE,
    PORT_NUMBER_MAX_VALUE,
)
from iplib3.constants.port import PORT_NUMBER_MIN_VALUE


def test_pure_address():
    """Test the PureAddress base class"""

    assert PureAddress()
    assert PureAddress(0xDE_AD_BE_EF)
    assert PureAddress(port=80)
    assert PureAddress(IPV4_LOCALHOST, 80)
    assert PureAddress(-42)


def test_pure_address_equality():
    """Test PureAddress equality"""

    address = PureAddress(0xDE_AD_BE_EF)

    assert address == PureAddress(0xDE_AD_BE_EF)
    assert (address == PureAddress(0xDE_AD_BE_EF, 80)) is False
    assert (address == 0xDE_AD_BE_EF) is False
    assert (address == 'cheese') is False


def test_pure_address_inequality():
    """Test PureAddress inequality"""

    address = PureAddress(0xDE_AD_BE_EF)

    assert address != PureAddress(0xC0_01_BA_5E)
    assert address != PureAddress(0xDE_AD_BE_EF, 80)
    assert address != 0xC0_01_BA_5E


def test_pure_address_num():
    """Test PureAddress num property"""

    assert PureAddress().num == 0
    assert PureAddress(0xDE_AD_BE_EF).num == 0xDE_AD_BE_EF
    assert PureAddress(port=80).num == 0
    assert PureAddress(IPV4_LOCALHOST, 80).num == 0x7F_00_00_01
    assert PureAddress(-42).num == 0


def test_pure_address_port():
    """Test PureAddress port property"""

    assert PureAddress().port is None
    assert PureAddress(0xDE_AD_BE_EF).port is None
    assert PureAddress(port=80).port == 80
    assert PureAddress(IPV4_LOCALHOST, 80).port == 80
    assert PureAddress(-42).port is None


def test_pure_address_port_setter():
    """Test PureAddress port setter"""

    address = PureAddress()
    assert address.port is None

    address.port = 80
    assert address.port == 80

    address.port = None
    assert address.port is None

    with pytest.raises(TypeError):
        address.port = 3.14

    with pytest.raises(TypeError):
        address.port = '80'

    with pytest.raises(ValueError):
        address.port = PORT_NUMBER_MAX_VALUE+1

    with pytest.raises(ValueError):
        address.port = PORT_NUMBER_MIN_VALUE-1


def test_pure_address_as_hex():
    """Test PureAddress hex output"""

    assert PureAddress(0xDE_AD_BE_EF).as_hex == '0xDEADBEEF'
    assert PureAddress(0x8B_AD_F0_0D).as_hex == '0x8BADF00D'
    assert PureAddress(0xDE_AD_C0_DE).as_hex == '0xDEADC0DE'


def test_pure_address_num_to_ipv4():
    """Test PureAddress num to IPv4 string conversion"""

    assert PureAddress(IPV4_LOCALHOST).num_to_ipv4() == '127.0.0.1'


def test_pure_address_num_to_ipv6():
    """Test PureAddress num to IPv6 string conversion"""

    assert PureAddress(IPV6_LOCALHOST).num_to_ipv6() == '0:0:0:0:0:0:0:1'
    assert PureAddress(0xDEAD_C0DE_1057_BE17).num_to_ipv6() == '0:0:0:0:DEAD:C0DE:1057:BE17'
    assert PureAddress(0xBADC_0FFE_E0DD_F00D).num_to_ipv6() == '0:0:0:0:BADC:FFE:E0DD:F00D'


def test_pure_address_num_to_ipv6_no_shortening():
    """Test PureAddress num to IPv6 string conversion without shortening"""

    assert PureAddress(IPV6_LOCALHOST).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:0000:0000:0000:0001'
    assert PureAddress(0xDEAD_C0DE_1057_BE17).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:DEAD:C0DE:1057:BE17'
    assert PureAddress(0xBADC_0FFE_E0DD_F00D).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:BADC:0FFE:E0DD:F00D'


def test_pure_address_num_to_ipv6_remove_zeroes():
    """Test PureAddress num to IPv6 string conversion with empty segment removal"""

    assert PureAddress(IPV6_LOCALHOST).num_to_ipv6(remove_zeroes=True) == '::1'
    assert PureAddress(0xDEAD_C0DE_1057_BE17).num_to_ipv6(remove_zeroes=True) == '::DEAD:C0DE:1057:BE17'
    assert PureAddress(0xBADC_0FFE_E0DD_F00D).num_to_ipv6(remove_zeroes=True) == '::BADC:FFE:E0DD:F00D'


def test_pure_address_num_to_ipv6_remove_zeroes_no_shortening():
    """
    Test PureAddress num to IPv6 string conversion without
    shortening but segment removal applied
    """

    assert PureAddress(0xBADC_0FFE_E0DD_F00D).num_to_ipv6(shorten=False, remove_zeroes=True) == '::BADC:0FFE:E0DD:F00D'


def test_ipaddress():
    """Test the IPAddress class"""

    assert IPAddress()
    assert isinstance(IPAddress(IPV4_LOCALHOST), IPAddress)
    assert isinstance(IPAddress('127.0.0.1'), IPv4)
    assert isinstance(IPAddress('::DEAD:BEEF'), IPv6)

    assert isinstance(IPAddress(IPV4_LOCALHOST, 80), IPAddress)
    assert isinstance(IPAddress('127.0.0.1', 80), IPv4)
    assert isinstance(IPAddress('::DEAD:BEEF', 80), IPv6)


def test_ipaddress_equality():
    """Test IPAddress equality"""

    address = IPAddress(IPV4_LOCALHOST)

    assert address == IPAddress(IPV4_LOCALHOST)
    assert address == '127.0.0.1'
    assert address == PureAddress(IPV4_LOCALHOST)


def test_ipaddress_string():
    """Test IPAddress string representation"""

    default = IPAddress()
    ipv4 = IPAddress(IPV4_LOCALHOST)
    ipv6 = IPAddress(0xDEAD_DEAD_BEEF)

    assert str(default) == '127.0.0.1'
    assert str(ipv4) == '127.0.0.1'
    assert str(ipv6) == '0:0:0:0:0:DEAD:DEAD:BEEF'

    assert repr(default) == "iplib3.IPAddress('127.0.0.1')"
    assert repr(ipv4) == "iplib3.IPAddress('127.0.0.1')"
    assert repr(ipv6) == "iplib3.IPAddress('0:0:0:0:0:DEAD:DEAD:BEEF')"

    with pytest.raises(ValueError):
        str(IPAddress(IPV6_MAX_VALUE+1))


def test_ipaddress_as_ipv4():
    """Test the IPAddress IPv4 constructor"""

    default = IPAddress()
    ipv4 = IPAddress('127.0.0.1')
    ipv6 = IPAddress('::DEAD:BEEF')

    assert isinstance(default.as_ipv4, IPv4)
    assert isinstance(ipv4.as_ipv4, IPv4)
    assert isinstance(ipv6.as_ipv4, IPv4)


def test_ipaddress_as_ipv6():
    """Test the IPAddress IPv6 constructor"""

    default = IPAddress()
    ipv4 = IPAddress('127.0.0.1')
    ipv6 = IPAddress('::DEAD:BEEF')

    assert isinstance(default.as_ipv6, IPv6)
    assert isinstance(ipv4.as_ipv6, IPv6)
    assert isinstance(ipv6.as_ipv6, IPv6)


def test_ipv4():
    """Test the IPv4 class"""

    assert IPv4()
    assert IPv4('127.0.0.1')
    assert IPv4('127.0.0.1:80')
    assert IPv4('127.0.0.1', 80)
    assert IPv4('127.0.0.1:80', 8080)
    assert IPv4('127.0.0.1', port_num=80)


def test_ipv4_string():
    """Test IPv4 string representation"""

    assert str(IPv4()) == '127.0.0.1'
    assert str(IPv4('127.0.0.1')) == '127.0.0.1'
    assert str(IPv4('127.0.0.1:80')) == '127.0.0.1:80'
    assert str(IPv4('127.0.0.1', 80)) == '127.0.0.1:80'
    assert str(IPv4('127.0.0.1:80', 8080)) == '127.0.0.1:8080'


def test_ipv4_ipv4_to_num():
    """Test IPv4 to num conversion"""

    assert IPv4()._ipv4_to_num() == IPV4_LOCALHOST
    assert IPv4('127.0.0.1')._ipv4_to_num() == IPV4_LOCALHOST
    assert IPv4('192.168.0.1')._ipv4_to_num() == 0xC0_A8_00_01


def test_ipv6():
    """Test the IPv6 class"""

    assert IPv6()
    assert IPv6('2606:4700:4700::1111')
    assert IPv6('2606:4700:4700::1111', 80)
    assert IPv6('[2606:4700:4700::1111]:80')
    assert IPv6('[2606:4700:4700::1111]:80', 8080)


def test_ipv6_string():
    """Test IPv6 string representation"""

    assert str(IPv6()) == '0:0:0:0:0:0:0:1'
    assert str(IPv6('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPv6('2606:4700:4700::1111', 80)) == '[2606:4700:4700::1111]:80'
    assert str(IPv6('[2606:4700:4700::1111]:80')) == '[2606:4700:4700::1111]:80'
    assert str(IPv6('[2606:4700:4700::1111]:80', 8080)) == '[2606:4700:4700::1111]:8080'
    assert str(IPv6('2606:4700:4700::1111', port_num=80)) == '[2606:4700:4700::1111]:80'


def test_ipv6_ipv6_to_num():
    """Test IPv6 to num conversion"""

    assert IPv6()._ipv6_to_num() == IPV6_LOCALHOST
    assert IPv6('70::')._ipv6_to_num() == 0x70_0000_0000_0000_0000_0000_0000_0000

    with pytest.raises(ValueError):
        # Two zero-skips
        IPv6('::DE::AD')._ipv6_to_num()

    with pytest.raises(ValueError):
        # Invalid hex literal
        IPv6('::H07:AF')._ipv6_to_num()

    with pytest.raises(ValueError):
        # Too many segments
        IPv6('1:1:1:1:1:1:1:1:1')._ipv6_to_num()

    with pytest.raises(ValueError):
        # Segment value too high
        IPv6('::7:FFFFF')._ipv6_to_num()

    with pytest.raises(ValueError):
        # Segment value too low (negative)
        IPv6('::7:-34')._ipv6_to_num()
