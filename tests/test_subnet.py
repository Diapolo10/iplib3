import pytest

from iplib3.subnet import ( # pylint: disable=import-error,no-name-in-module
    _subnet_validator,
    _ipv4_subnet_validator,
    _ipv6_subnet_validator,
)
from iplib3.constants import ( # pylint: disable=import-error,no-name-in-module
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
    assert _ipv4_subnet_validator("255.128") is False
    assert _ipv4_subnet_validator("255.255.255.255.128") is False


    for subnet in range(IPV4_MIN_SUBNET_VALUE, IPV4_MAX_SUBNET_VALUE+1):
        assert _ipv4_subnet_validator(subnet) is True

    assert _ipv4_subnet_validator(IPV4_MAX_SUBNET_VALUE+1) is False
    assert _ipv4_subnet_validator(IPV4_MIN_SUBNET_VALUE-1) is False

    with pytest.raises(TypeError) as e_info: # pylint: disable=unused-variable
        _ipv4_subnet_validator([255, 255, 255, 0])


def test_ipv6_subnet_validator():

    for subnet in range(IPV6_MIN_SUBNET_VALUE, IPV6_MAX_SUBNET_VALUE+1, 4):
        assert _ipv6_subnet_validator(subnet) is True

    assert _ipv6_subnet_validator(IPV6_MAX_SUBNET_VALUE+1) is False
    assert _ipv6_subnet_validator(IPV6_MIN_SUBNET_VALUE-1) is False
    assert _ipv6_subnet_validator(17) is False

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