import pytest

from iplib3 import ( # pylint: disable=import-error,no-name-in-module
    IPAddress, IPv4, IPv6
)
from iplib3.address import ( # pylint: disable=import-error,no-name-in-module
    _ipv4_validator, _ipv6_validator,
    _port_validator, _subnet_validator,
    _ipv4_subnet_validator, _ipv6_subnet_validator,

    IPV4_SEGMENT_BIT_COUNT, IPV6_SEGMENT_BIT_COUNT,
    IPV4_MIN_SEGMENT_COUNT, IPV6_MIN_SEGMENT_COUNT,
    IPV4_MAX_SEGMENT_COUNT, IPV6_MAX_SEGMENT_COUNT,
    IPV4_MIN_SEGMENT_VALUE, IPV6_MIN_SEGMENT_VALUE,
    IPV4_MAX_SEGMENT_VALUE, IPV6_MAX_SEGMENT_VALUE,
    IPV4_MIN_SUBNET_VALUE,  IPV6_MIN_SUBNET_VALUE,
    IPV4_MAX_SUBNET_VALUE,  IPV6_MAX_SUBNET_VALUE,
    IPV4_MIN_VALUE,         IPV6_MIN_VALUE,
    IPV4_MAX_VALUE,         IPV6_MAX_VALUE,

    PORT_NUMBER_MIN_VALUE, PORT_NUMBER_MAX_VALUE,
)

def test_ipv4():
    assert str(IPAddress(25601440).as_ipv4) == '1.134.165.160'
    assert str(IPAddress('192.168.1.1')) == '192.168.1.1'
    assert str(IPv4('192.168.1.1')) == '192.168.1.1'
    assert str(IPAddress('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPv4('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPAddress(0xDEADBEEF).as_ipv4) == '222.173.190.239'
    assert str(IPAddress(0xDEADBEEF, port_num=80).as_ipv4) == '222.173.190.239:80'


def test_ipv4_port_initialisation():

    foo = IPv4('222.173.190.239:80')
    bar = IPv4('222.173.190.239', 80) # pylint: disable=too-many-function-args
    baz = IPv4('222.173.190.239', port_num=80)
    spam = IPv4('222.173.190.239:25565', port_num=80) # Argument-given ports should be preferred

    assert foo == bar == baz == spam
    assert str(baz) == '222.173.190.239:80'


def test_ipv6():
    assert str(IPAddress(25601440).as_ipv6) == '0:0:0:0:0:0:186:A5A0'
    assert str(IPAddress('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPv6('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPAddress('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPv6('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPAddress(0xDEADBEEF).as_ipv6) == '0:0:0:0:0:0:DEAD:BEEF'


def test_ipv6_full():
    assert IPAddress(25601440).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:0000:0000:0186:A5A0'


def test_ipv6_remove_zeroes():
    assert IPAddress(25601440).num_to_ipv6(remove_zeroes=True) == '::186:A5A0'
    assert IPAddress(0xDEADBEEF).num_to_ipv6(remove_zeroes=True) == '::DEAD:BEEF'


def test_ipv6_port_initialisation():

    foo = IPv6('[::1337:1337:1337:1337]:25565')
    bar = IPv6('::1337:1337:1337:1337', 25565) # pylint: disable=too-many-function-args
    baz = IPv6('::1337:1337:1337:1337', port_num=25565)
    spam = IPv6('[::1337:1337:1337:1337]:80', port_num=25565) # Argument-given ports should be preferred

    assert foo == bar == baz == spam
    assert str(baz) == '[::1337:1337:1337:1337]:25565'


def test_chaining():
    assert str(IPAddress(25601440).as_ipv6.as_ipv4) == '1.134.165.160'


def test_hex_output():

    base = IPAddress(0xDEADBEEF)
    v4 = base.as_ipv4
    v6 = base.as_ipv6

    assert base.as_hex == '0xDEADBEEF'
    assert v4.as_hex   == '0xDEADBEEF'
    assert v6.as_hex   == '0xDEADBEEF'


def test_ipv4_validator():
    assert _ipv4_validator('1.1.1.1') is True
    assert _ipv4_validator('0.0.0.0') is True
    assert _ipv4_validator('255.255.255.255') is True

    assert _ipv4_validator('192.168.0.1:8080') is True
    assert _ipv4_validator('12.123.234.345') is False
    assert _ipv4_validator('FF.FF.FF.FF') is False
    assert _ipv4_validator('1.1.1.1:314159') is False
    assert _ipv4_validator('12.23.34.45.56') is False
    assert _ipv4_validator('12.23.34.45.56', strict=False) is False

    assert _ipv4_validator('1337.1337.1337.1337') is False
    assert _ipv4_validator('1337.1337.1337.1337:314159') is False
    assert _ipv4_validator('1337.1337.1337.1337', strict=False) is True
    assert _ipv4_validator('1337.1337.1337.1337:314159', strict=False) is True

    assert _ipv4_validator(25601440) is True
    assert _ipv4_validator(0xDEADBEEF) is True
    assert _ipv4_validator(25601440, strict=False) is True
    assert _ipv4_validator(0xDEADBEEF, strict=False) is True


def test_ipv6_validator():
    assert _ipv6_validator('0:0:0:0:0:0:0:0') is True
    assert _ipv6_validator('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF') is True
    assert _ipv6_validator('[0:0:0:0:0:0:0:0]:80') is True
    assert _ipv6_validator('[FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF]:65535') is True
    assert _ipv6_validator('::12') is True
    assert _ipv6_validator('314::') is True
    assert _ipv6_validator('2606:4700:4700::1111') is True


def test_port_validator():
    assert _port_validator(None) is True
    assert _port_validator(False) is True
    assert _port_validator(True) is True
    assert _port_validator(13) is True
    assert _port_validator(21) is True
    assert _port_validator(22) is True
    assert _port_validator(25) is True
    assert _port_validator(80) is True
    assert _port_validator(104) is True
    assert _port_validator(192) is True
    assert _port_validator(443) is True
    assert _port_validator(554) is True
    assert _port_validator(3724) is True
    assert _port_validator(8080) is True
    assert _port_validator(25565) is True

    assert _port_validator(PORT_NUMBER_MIN_VALUE-1) is False
    assert _port_validator(PORT_NUMBER_MAX_VALUE+1) is False
    assert _port_validator(0xDEADBEEF) is False
    assert _port_validator("Hello, world!") is False
    assert _port_validator([3, 1, 4]) is False


def test_ipv4_subnet_validator():
    assert _ipv4_subnet_validator("255.0.0.0") is True
    assert _ipv4_subnet_validator("255.255.0.0") is True
    assert _ipv4_subnet_validator("255.255.128.0") is True
    assert _ipv4_subnet_validator("255.255.255.0") is True
    assert _ipv4_subnet_validator("255.255.255.128") is True
    assert _ipv4_subnet_validator("255.255.255.192") is True
    assert _ipv4_subnet_validator("255.255.255.224") is True
    assert _ipv4_subnet_validator("255.255.255.240") is True
    assert _ipv4_subnet_validator("255.255.255.248") is True
    assert _ipv4_subnet_validator("255.255.255.252") is True
    assert _ipv4_subnet_validator("255.255.255.254") is True
    assert _ipv4_subnet_validator("255.255.255.255") is False

    assert _ipv4_subnet_validator("255.128.128.0") is False
    assert _ipv4_subnet_validator("256.256.256.0") is False
    assert _ipv4_subnet_validator("128.0.0.1") is False

    for subnet in range(IPV4_MIN_SUBNET_VALUE, IPV4_MAX_SUBNET_VALUE+1):
        assert _ipv4_subnet_validator(subnet) is True

    assert _ipv4_subnet_validator(IPV4_MAX_SUBNET_VALUE+1) is False
    assert _ipv4_subnet_validator(IPV4_MIN_SUBNET_VALUE-1) is False

    with pytest.raises(TypeError) as e_info: # pylint: disable=unused-variable
        _ipv4_subnet_validator([255, 255, 255, 0])


def test_ipv6_subnet_validator():

    for subnet in range(IPV6_MIN_SUBNET_VALUE, IPV6_MAX_SUBNET_VALUE+1):
        assert _ipv6_subnet_validator(subnet) is True

    assert _ipv6_subnet_validator(IPV6_MAX_SUBNET_VALUE+1) is False
    assert _ipv6_subnet_validator(IPV6_MIN_SUBNET_VALUE-1) is False

    with pytest.raises(TypeError) as e_info: # pylint: disable=unused-variable
        _ipv6_subnet_validator("Hello, world!")

def test_subnet_validator():
    assert _subnet_validator("255.0.0.0", protocol='ipv4') is True
    assert _subnet_validator("255.0.0.0", protocol='IPV4') is True
    assert _subnet_validator("255.0.0.0", protocol='ipv6') is True
    assert _subnet_validator('255.255.255.128', protocol='ipv6') is True
    assert _subnet_validator("255.128.0.0", protocol='ipv4') is True
    assert _subnet_validator("1.1.1.1", protocol='ipv4') is False
    assert _subnet_validator("255.128.192.224", protocol='ipv4') is False
    assert _subnet_validator("255.128.128.0", protocol='ipv4') is False



