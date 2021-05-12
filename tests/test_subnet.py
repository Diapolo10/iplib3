import pytest

from iplib3.subnet import ( # pylint: disable=import-error,no-name-in-module
    SubnetMask,
    PureSubnetMask,
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


def test_pure_subnet_mask():
    """Test the PureSubnetMask base class"""
    
    # Override the abstract methods to enable testing
    PureSubnetMask.__abstractmethods__ = set()

    @dataclass
    class Dummy(PureSubnetMask):
        pass

    subnet = Dummy()
    another = Dummy()
    another._prefix_length = None
    assert subnet.prefix_length == 0
    assert another.prefix_length is None
    
    assert str(subnet) == '0'
    assert repr(subnet) == "iplib3.PureSubnetMask('0')"

    assert subnet == Dummy()
    assert subnet == 0
    assert subnet == '0'

    assert (subnet == 3.14) is False
    assert (subnet == another) is False


def test_subnet_mask():
    assert SubnetMask()._subnet_type == 'ipv6'
    assert SubnetMask('255.255.255.0')._subnet_type == 'ipv4'

    assert (
        repr(SubnetMask(24, subnet_type='ipv4'))
        == "iplib3.SubnetMask('255.255.255.0')")
    assert repr(SubnetMask(24)) == "iplib3.SubnetMask('24')"

    assert SubnetMask._subnet_to_num(None) is None
    assert SubnetMask._subnet_to_num(24) == 24
    assert SubnetMask._subnet_to_num('24') == 24
    assert SubnetMask._subnet_to_num(None, subnet_type='ipv4') is None
    assert SubnetMask._subnet_to_num(24, subnet_type='ipv4') == 24
    assert SubnetMask._subnet_to_num('24', subnet_type='ipv4') == 24
    assert SubnetMask._subnet_to_num('255.255.128.0', subnet_type='ipv4') == 17

    with pytest.raises(TypeError) as e_info: # pylint: disable=unused-variable
        SubnetMask._subnet_to_num([255, 255, 255, 0])
    with pytest.raises(ValueError) as e_info: # pylint: disable=unused-variable
        SubnetMask._subnet_to_num('255.255.255.0')
    with pytest.raises(ValueError) as e_info: # pylint: disable=unused-variable
        SubnetMask._subnet_to_num('3e2')
    with pytest.raises(ValueError) as e_info: # pylint: disable=unused-variable
        SubnetMask._subnet_to_num(IPV4_MAX_SUBNET_VALUE+1, subnet_type='ipv4')
    with pytest.raises(ValueError) as e_info: # pylint: disable=unused-variable
        SubnetMask._subnet_to_num(IPV6_MAX_SUBNET_VALUE+1)

    assert (
        SubnetMask._prefix_to_subnet_mask(24, subnet_type='ipv4')
        == '255.255.255.0'
    )

    with pytest.raises(ValueError) as e_info: # pylint: disable=unused-variable
        SubnetMask._prefix_to_subnet_mask(24, subnet_type='ipv6')
    with pytest.raises(ValueError) as e_info: # pylint: disable=unused-variable
        SubnetMask._prefix_to_subnet_mask(IPV4_MAX_SUBNET_VALUE+1, subnet_type='ipv4')
