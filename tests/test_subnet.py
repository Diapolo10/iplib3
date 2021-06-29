"""Unit tests for iplib3.subnet"""

import pytest

from iplib3.subnet import (  # pylint: disable=import-error,no-name-in-module
    SubnetMask,
    PureSubnetMask,
)
from iplib3.constants import (  # pylint: disable=import-error,no-name-in-module
    IPV4_MIN_SUBNET_VALUE,
    IPV4_MAX_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
)


def test_pure_subnet_mask():
    """Test the PureSubnetMask base class"""

    _ = PureSubnetMask()


def test_pure_subnet_mask_prefix_length():
    """Test PureSubnetMask prefix length"""

    subnet = PureSubnetMask()
    another = PureSubnetMask()
    another._prefix_length = None
    assert subnet._prefix_length == IPV4_MIN_SUBNET_VALUE
    assert another._prefix_length is None


def test_pure_subnet_mask_string():
    """Test PureSubnetMask string represesetation"""

    subnet = PureSubnetMask()
    assert str(subnet) == '0'
    assert repr(subnet) == "iplib3.PureSubnetMask('0')"


def test_pure_subnet_mask_equality():
    """Test PureSubnetMask equality"""

    subnet = PureSubnetMask()
    assert subnet == PureSubnetMask()
    assert subnet == IPV4_MIN_SUBNET_VALUE
    assert subnet == '0'


def test_pure_subnet_mask_inequality():
    """Test PureSubnetMask inequality"""

    subnet = PureSubnetMask()
    another = PureSubnetMask()
    another._prefix_length = None
    assert subnet != 3.14
    assert subnet != another


def test_subnet_mask_subnet_type():
    """Test SubnetMask subnet type"""

    assert SubnetMask()._subnet_type == 'ipv6'
    assert SubnetMask('255.255.255.0')._subnet_type == 'ipv4'


def test_subnet_mask_string():
    """Test SubnetMask string representation"""

    assert (
        repr(SubnetMask(24, subnet_type='ipv4'))
        == "iplib3.SubnetMask('255.255.255.0')")
    assert repr(SubnetMask(24)) == "iplib3.SubnetMask('24')"


def test_subnet_mask_subnet_to_num():
    """Test SubnetMask subnet to number converter"""

    assert SubnetMask._subnet_to_num(None) is None
    assert SubnetMask._subnet_to_num(24) == 24
    assert SubnetMask._subnet_to_num('24') == 24
    assert SubnetMask._subnet_to_num(None, subnet_type='ipv4') is None
    assert SubnetMask._subnet_to_num(24, subnet_type='ipv4') == 24
    assert SubnetMask._subnet_to_num('24', subnet_type='ipv4') == 24
    assert SubnetMask._subnet_to_num('255.255.128.0', subnet_type='ipv4') == 17


def test_subnet_mask_subnet_to_num_errors():
    """Test SubnetMask subnet to number converter errors"""

    with pytest.raises(TypeError):
        SubnetMask._subnet_to_num([255, 255, 255, 0])
    with pytest.raises(ValueError):
        SubnetMask._subnet_to_num('255.255.255.0')
    with pytest.raises(ValueError):
        SubnetMask._subnet_to_num('3e2')
    with pytest.raises(ValueError):
        SubnetMask._subnet_to_num(IPV4_MAX_SUBNET_VALUE+1, subnet_type='ipv4')
    with pytest.raises(ValueError):
        SubnetMask._subnet_to_num(IPV6_MAX_SUBNET_VALUE+1)
    with pytest.raises(ValueError):
        SubnetMask._subnet_to_num('255.6.0.0', subnet_type='ipv4')


def test_subnet_mask_prefix_to_subnet_mask():
    """Test SubnetMask number to mask converter"""

    assert (
        SubnetMask._prefix_to_subnet_mask(24, subnet_type='ipv4')
        == '255.255.255.0'
    )


def test_subnet_mask_prefix_to_subnet_mask_errors():
    """Test SubnetMask number to mask converter"""

    with pytest.raises(ValueError):
        SubnetMask._prefix_to_subnet_mask(24, subnet_type='ipv6')
    with pytest.raises(ValueError):
        SubnetMask._prefix_to_subnet_mask(IPV4_MAX_SUBNET_VALUE+1, subnet_type='ipv4')
