"""Unit tests for iplib3.validators"""

import pytest

from iplib3.constants import (  # pylint: disable=import-error,no-name-in-module
    IPV4_MAX_SUBNET_VALUE,
    IPV4_MAX_VALUE,
    IPV4_MIN_SUBNET_VALUE,
    IPV4_MIN_VALUE,
    IPV6_MAX_SUBNET_VALUE,
    IPV6_MAX_VALUE,
    IPV6_MIN_SUBNET_VALUE,
    IPV6_MIN_VALUE,
    PORT_NUMBER_MAX_VALUE,
    PORT_NUMBER_MIN_VALUE,
)
from iplib3.validators import (  # pylint: disable=import-error,no-name-in-module
    _ipv4_subnet_validator,
    _ipv6_subnet_validator,
    _port_stripper,
    ip_validator,
    ipv4_validator,
    ipv6_validator,
    port_validator,
    subnet_validator,
)


def test_port_validator_none():
    """Test the port validator with None"""

    assert port_validator(None) is True


def test_port_validator_bool():
    """Test the port validator with None"""

    assert port_validator(False) is True
    assert port_validator(True) is True


def test_port_validator_valid_nums():
    """Test the port validator with valid numbers"""

    assert port_validator(13) is True
    assert port_validator(21) is True
    assert port_validator(22) is True
    assert port_validator(25) is True
    assert port_validator(80) is True
    assert port_validator(104) is True
    assert port_validator(192) is True
    assert port_validator(443) is True
    assert port_validator(554) is True
    assert port_validator(3724) is True
    assert port_validator(8080) is True
    assert port_validator(25565) is True


def test_port_validator_invalid_nums():
    """Test the port validator with invalid numbers"""

    assert port_validator(PORT_NUMBER_MIN_VALUE-1) is False
    assert port_validator(PORT_NUMBER_MAX_VALUE+1) is False
    assert port_validator(0xDEADBEEF) is False


def test_port_validator_invalid_types():
    """Test the port validator using invalid/unsupported types"""

    assert port_validator(22.0) is False
    assert port_validator("42") is False
    assert port_validator([3, 1, 4]) is False


def test_ip_validator():
    """Test the generic IP address validator"""

    assert ip_validator('128.0.0.1') is True
    assert ip_validator(0xDE_AD_BE_EF) is True
    assert ip_validator('2606:4700:4700::1111') is True
    assert ip_validator(IPV6_MAX_VALUE) is True


def test_ipv4_validator_valid_address():
    """Test the IPv4 address validator using valid addresses"""

    assert ipv4_validator('1.1.1.1') is True
    assert ipv4_validator('0.0.0.0') is True  # noqa: S104
    assert ipv4_validator('255.255.255.255') is True
    assert ipv4_validator('192.168.0.1:8080') is True


def test_ipv4_validator_invalid_address():
    """Test the IPv4 address validator using invalid addresses"""

    assert ipv4_validator('12.123.234.345') is False
    assert ipv4_validator('DE.AD.BE.EF') is False
    assert ipv4_validator('12.23.34.45.56') is False
    assert ipv4_validator('12.23.34.45.56', strict=False) is False
    assert ipv4_validator('255,255,255,255') is False
    assert ipv4_validator([127, 0, 0, 1]) is False
    assert ipv4_validator('1337.1337.1337.1337') is False


def test_ipv4_validator_invalid_port():
    """Test the IPv4 address validator using invalid ports"""

    assert ipv4_validator('1.1.1.1:314159') is False
    assert ipv4_validator('128.0.0.1:notaport') is False


def test_ipv4_validator_no_strict():
    """Test the IPv4 address validator with strict mode disabled"""

    assert ipv4_validator('1337.1337.1337.1337', strict=False) is True
    assert ipv4_validator('1337.1337.1337.1337:314159', strict=False) is True


def test_ipv4_validator_valid_number():
    """Test the IPv4 address validator using numbers"""

    assert ipv4_validator(25601440) is True
    assert ipv4_validator(0xDEADBEEF) is True
    assert ipv4_validator(25601440, strict=False) is True
    assert ipv4_validator(0xDEADBEEF, strict=False) is True
    assert ipv4_validator(IPV4_MIN_VALUE) is True
    assert ipv4_validator(IPV4_MAX_VALUE) is True


def test_ipv4_validator_invalid_number():
    """Test the IPv4 address validator using invalid numbers"""

    assert ipv4_validator(IPV4_MIN_VALUE-1) is False
    assert ipv4_validator(IPV4_MAX_VALUE+1) is False
    assert ipv4_validator(256014.40) is False


def test_ipv6_validator_valid_address():
    """Test the IPv6 address validator using valid addresses"""

    assert ipv6_validator('0:0:0:0:0:0:0:0') is True
    assert ipv6_validator('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF') is True
    assert ipv6_validator('[0:0:0:0:0:0:0:0]:80') is True
    assert ipv6_validator('[FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF]:65535') is True
    assert ipv6_validator('::12') is True
    assert ipv6_validator('314::') is True
    assert ipv6_validator('2606:4700:4700::1111') is True
    assert ipv6_validator('2606:4700:4700::10000', strict=False) is True


def test_ipv6_validator_invalid_address():
    """Test the IPv6 address validator using invalid addresses"""

    assert ipv6_validator('2606:4700:4700::10000') is False
    assert ipv6_validator('2606:4700::4700::1111') is False
    assert ipv6_validator('2606:4700:4700::HACK') is False
    assert ipv6_validator('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:0001') is False
    assert ipv6_validator('2606:4700:4700:1111') is False
    assert ipv6_validator([2606, 4700, 4700, 0, 0, 0, 0, 1111]) is False


def test_ipv6_validator_invalid_port():
    """Test the IPv6 address validator using invalid ports"""

    assert ipv6_validator('[2606:4700:4700::1111]:notaport') is False
    assert ipv6_validator('[2606:4700:4700::1111]:-1') is False
    assert ipv6_validator('[2606:4700:4700::1111]:314159') is False


def test_ipv6_validator_valid_number():
    """Test the IPv6 address validator using numbers"""

    assert ipv6_validator(IPV6_MIN_VALUE) is True
    assert ipv6_validator(IPV6_MAX_VALUE) is True


def test_ipv6_validator_invalid_number():
    """Test the IPv6 addreess validator using invalid numbers"""

    assert ipv6_validator(IPV6_MIN_VALUE-1) is False
    assert ipv6_validator(IPV6_MAX_VALUE+1) is False


def test_subnet_validator_valid_subnet():
    """Test the general subnet validator using valid subnets"""

    assert subnet_validator("255.0.0.0", protocol='ipv4') is True
    assert subnet_validator("255.0.0.0", protocol='IPV4') is True
    assert subnet_validator("255.0.0.0", protocol='ipv6') is True
    assert subnet_validator("255.255.255.128", protocol='ipv6') is True
    assert subnet_validator("255.128.0.0", protocol='ipv4') is True
    assert subnet_validator(16, protocol='ipv6') is True


def test_subnet_validator_invalid_subnet():
    """Test the general subnet validator using invalid subnets"""

    assert subnet_validator("1.1.1.1", protocol='ipv4') is False
    assert subnet_validator("255.128.192.224", protocol='ipv4') is False
    assert subnet_validator("255.128.128.0", protocol='ipv4') is False
    assert subnet_validator(24, protocol='ipv8') is False


def test_ipv4_subnet_validator_valid_subnet_string():
    """Test the IPv4 subnet validator using valid subnet strings"""

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


def test_ipv4_subnet_validator_invalid_subnet_string():
    """Test the IPv4 subnet validator using invalid subnet strings"""

    assert _ipv4_subnet_validator("255.255.255.255") is False
    assert _ipv4_subnet_validator("255.128.128.0") is False
    assert _ipv4_subnet_validator("256.256.256.0") is False
    assert _ipv4_subnet_validator("128.0.0.1") is False
    assert _ipv4_subnet_validator("255.128") is False
    assert _ipv4_subnet_validator("255.255.255.255.128") is False


def test_ipv4_subnet_validator_valid_subnet_number():
    """Test the IPv4 subnet validator using valid subnet numbers"""

    for subnet in range(IPV4_MIN_SUBNET_VALUE, IPV4_MAX_SUBNET_VALUE+1):
        assert _ipv4_subnet_validator(subnet) is True


def test_ipv4_subnet_validator_invalid_subnet_number():
    """Test the IPv4 subnet validator using invalid subnet numbers"""

    assert _ipv4_subnet_validator(IPV4_MAX_SUBNET_VALUE+1) is False
    assert _ipv4_subnet_validator(IPV4_MIN_SUBNET_VALUE-1) is False


def test_ipv4_subnet_validator_invalid_type():
    """Test the IPv4 subnet validator using invalid types"""

    with pytest.raises(TypeError):
        _ipv4_subnet_validator([255, 255, 255, 0])


def test_ipv6_subnet_validator_valid_subnet_number():
    """Test the IPv6 subnet validator using valid subnet numbers"""

    for subnet in range(IPV6_MIN_SUBNET_VALUE, IPV6_MAX_SUBNET_VALUE+1, 4):
        assert _ipv6_subnet_validator(subnet) is True


def test_ipv6_subnet_validator_invalid_subnet_number():
    """Test the IPv6 subnet validator using invalid subnet numbers"""

    assert _ipv6_subnet_validator(IPV6_MAX_SUBNET_VALUE+1) is False
    assert _ipv6_subnet_validator(IPV6_MIN_SUBNET_VALUE-1) is False
    assert _ipv6_subnet_validator(17) is False


def test_ipv6_subnet_validator_invalid_type():
    """Test the IPv6 subnet validator using invalid types"""

    with pytest.raises(TypeError):
        _ipv6_subnet_validator("255.255.255.0")

    with pytest.raises(TypeError):
        _ipv6_subnet_validator("::DEAD:BEEF")


def test_port_stripper_ipv4():
    """Test the port stripper with IPv4"""

    address, port, valid = _port_stripper("127.0.0.1:8080", protocol='ipv4')
    assert address == '127.0.0.1'
    assert port == 8080
    assert valid
    address, port, valid = _port_stripper("127.0.0.1:8080", protocol='IPv4')
    assert address == '127.0.0.1'
    assert port == 8080
    assert valid
    address, port, valid = _port_stripper("127.0.0.1:8080", protocol='IPV4')
    assert address == '127.0.0.1'
    assert port == 8080
    assert valid
    address, port, valid = _port_stripper("222.13.7.42:80", protocol='ipv4')
    assert address == '222.13.7.42'
    assert port == 80
    assert valid


def test_port_stripper_ipv4_no_port():
    """Test the port stripper with IPv4 without port"""

    address, port, valid = _port_stripper("127.0.0.1", protocol='ipv4')
    assert address == '127.0.0.1'
    assert port is None
    assert valid
    address, port, valid = _port_stripper("222.13.7.42", protocol='ipv4')
    assert address == '222.13.7.42'
    assert port is None
    assert valid


def test_port_stripper_ipv6():
    """Test the port stripper with IPv6"""

    address, port, valid = _port_stripper("[2606:4700:4700::1111]:8080", protocol='ipv6')
    assert address == '2606:4700:4700::1111'
    assert port == 8080
    assert valid
    address, port, valid = _port_stripper("[2606:4700:4700::1111]:8080", protocol='IPv6')
    assert address == '2606:4700:4700::1111'
    assert port == 8080
    assert valid
    address, port, valid = _port_stripper("[2606:4700:4700::1111]:8080", protocol='IPV6')
    assert address == '2606:4700:4700::1111'
    assert port == 8080
    assert valid
    address, port, valid = _port_stripper("[::DEAD:BEEF]:80", protocol='ipv6')
    assert address == '::DEAD:BEEF'
    assert port == 80
    assert valid


def test_port_stripper_ipv6_no_port():
    """Test the port stripper with IPv6 without port"""

    address, port, valid = _port_stripper("2606:4700:4700::1111", protocol='ipv6')
    assert address == '2606:4700:4700::1111'
    assert port is None
    assert valid
    address, port, valid = _port_stripper("::DEAD:BEEF", protocol='ipv6')
    assert address == '::DEAD:BEEF'
    assert port is None
    assert valid


def test_port_stripper_invalid_protocol():
    """Test the port stripper for using invalid protocol"""

    _, _, valid = _port_stripper("127.0.0.1:8080", protocol='IPv9')
    assert valid is False
