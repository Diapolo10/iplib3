"""Unit tests for iplib3.address."""

import pytest
from tests.test_cases_address import (
    TEST_CASES_IPADDRESS,
    TEST_CASES_IPADDRESS_AS_IPV4,
    TEST_CASES_IPADDRESS_AS_IPV6,
    TEST_CASES_IPADDRESS_EQUALITY,
    TEST_CASES_IPADDRESS_REPR,
    TEST_CASES_IPADDRESS_STRING,
    TEST_CASES_IPV4,
    TEST_CASES_IPV4_IPV4_TO_NUM,
    TEST_CASES_IPV4_STRING,
    TEST_CASES_IPV6,
    TEST_CASES_IPV6_IPV6_TO_NUM,
    TEST_CASES_IPV6_IPV6_TO_NUM_ERRORS,
    TEST_CASES_IPV6_STRING,
    TEST_CASES_PURE_ADDRESS,
    TEST_CASES_PURE_ADDRESS_AS_HEX,
    TEST_CASES_PURE_ADDRESS_EQUALITY,
    TEST_CASES_PURE_ADDRESS_INEQUALITY,
    TEST_CASES_PURE_ADDRESS_NUM,
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV4,
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6,
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6_NO_SHORTENING,
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6_REMOVE_ZEROS,
    TEST_CASES_PURE_ADDRESS_PORT,
    TEST_CASES_PURE_ADDRESS_PORT_SETTER_ERROR,
)

from iplib3 import IPAddress
from iplib3.address import IPv6, PureAddress
from iplib3.constants import IPV6_MAX_VALUE


@pytest.mark.parametrize(
    "pure_address",
    TEST_CASES_PURE_ADDRESS,
)
def test_pure_address(pure_address):
    """Test the PureAddress base class."""
    assert pure_address


@pytest.mark.parametrize(
    ("address", "input_address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_EQUALITY,
)
def test_pure_address_equality(address, input_address, excepted_output):
    """Test PureAddress equality."""
    output = address == input_address
    assert output is excepted_output


@pytest.mark.parametrize(
    ("first_address", "second_address"),
    TEST_CASES_PURE_ADDRESS_INEQUALITY,
)
def test_pure_address_inequality(first_address, second_address):
    """Test PureAddress inequality."""
    assert first_address != second_address


@pytest.mark.parametrize(
    ("address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_NUM,
)
def test_pure_address_num(address, excepted_output):
    """Test PureAddress num property."""
    assert address.num == excepted_output


@pytest.mark.parametrize(
    ("address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_PORT,
)
def test_pure_address_port(address, excepted_output):
    """Test PureAddress port property."""
    assert address.port == excepted_output


def test_pure_address_port_setter():
    """Test PureAddress port setter."""
    address = PureAddress()
    assert address.port is None

    address.port = 80
    assert address.port == 80  # noqa: PLR2004

    address.port = None
    assert address.port is None


@pytest.mark.parametrize(
    ("value", "error", "match_message"),
    TEST_CASES_PURE_ADDRESS_PORT_SETTER_ERROR,
)
def test_pure_address_port_setter_error(value, error, match_message):
    """Test pure address port errors."""
    address = PureAddress()
    with pytest.raises(error, match=match_message):
        address.port = value


@pytest.mark.parametrize(
    ("pure_address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_AS_HEX,
)
def test_pure_address_as_hex(pure_address, excepted_output):
    """Test PureAddress hex output."""
    assert pure_address.as_hex == excepted_output


@pytest.mark.parametrize(
    ("pure_address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV4,
)
def test_pure_address_num_to_ipv4(pure_address, excepted_output):
    """Test PureAddress num to IPv4 string conversion."""
    assert pure_address.num_to_ipv4() == excepted_output


@pytest.mark.parametrize(
    ("pure_address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6,
)
def test_pure_address_num_to_ipv6(pure_address, excepted_output):
    """Test PureAddress num to IPv6 string conversion."""
    assert pure_address.num_to_ipv6() == excepted_output


@pytest.mark.parametrize(
    ("pure_address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6_NO_SHORTENING,
)
def test_pure_address_num_to_ipv6_no_shortening(pure_address, excepted_output):
    """Test PureAddress num to IPv6 string conversion without shortening."""
    assert pure_address.num_to_ipv6(shorten=False) == excepted_output


@pytest.mark.parametrize(
    ("pure_address", "excepted_output"),
    TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6_REMOVE_ZEROS,
)
def test_pure_address_num_to_ipv6_remove_zeroes(pure_address, excepted_output):
    """Test PureAddress num to IPv6 string conversion with empty segment removal."""
    assert pure_address.num_to_ipv6(remove_zeroes=True) == excepted_output


def test_pure_address_num_to_ipv6_remove_zeroes_no_shortening():
    """Test PureAddress num to IPv6 string conversion without shortening but segment removal applied."""
    assert PureAddress(0xBADC_0FFE_E0DD_F00D).num_to_ipv6(shorten=False, remove_zeroes=True) == '::BADC:0FFE:E0DD:F00D'


@pytest.mark.parametrize(
    ("ip_address", "excepted_instance"),
    TEST_CASES_IPADDRESS,
)
def test_ipaddress(ip_address, excepted_instance):
    """Test the IPAddress class."""
    assert isinstance(ip_address, excepted_instance)


@pytest.mark.parametrize(
    ("ip_address", "excepted_output"),
    TEST_CASES_IPADDRESS_EQUALITY,
)
def test_ipaddress_equality(ip_address, excepted_output):
    """Test IPAddress equality."""
    assert ip_address == excepted_output


@pytest.mark.parametrize(
    ("ip_address", "excepted_output"),
    TEST_CASES_IPADDRESS_STRING,
)
def test_ipaddress_string(ip_address, excepted_output):
    """Test IPAddress string representation."""
    assert str(ip_address) == excepted_output


def test_ipaddress_string_error():
    """Test string form errors."""
    with pytest.raises(ValueError, match="No valid address representation exists"):
        str(IPAddress(IPV6_MAX_VALUE + 1))


@pytest.mark.parametrize(
    ("ip_address", "excepted_output"),
    TEST_CASES_IPADDRESS_REPR,
)
def test_ipaddress_repr(ip_address, excepted_output):
    """Test IP address representation."""
    assert repr(ip_address) == excepted_output


@pytest.mark.parametrize(
    ("ip_address", "excepted_instance"),
    TEST_CASES_IPADDRESS_AS_IPV4,
)
def test_ipaddress_as_ipv4(ip_address, excepted_instance):
    """Test the IPAddress IPv4 constructor."""
    assert isinstance(ip_address.as_ipv4, excepted_instance)


@pytest.mark.parametrize(
    ("ip_address", "excepted_instance"),
    TEST_CASES_IPADDRESS_AS_IPV6,
)
def test_ipaddress_as_ipv6(ip_address, excepted_instance):
    """Test the IPAddress IPv6 constructor."""
    assert isinstance(ip_address.as_ipv6, excepted_instance)


@pytest.mark.parametrize(
    "input_ipv4", TEST_CASES_IPV4,
)
def test_ipv4(input_ipv4):
    """Test the IPv4 class."""
    assert input_ipv4


@pytest.mark.parametrize(
    ("input_ipv4", "excepted_output"),
    TEST_CASES_IPV4_STRING,
)
def test_ipv4_string(input_ipv4, excepted_output):
    """Test IPv4 string representation."""
    assert str(input_ipv4) == excepted_output


@pytest.mark.parametrize(
    ("input_ipv4", "excepted_output"),
    TEST_CASES_IPV4_IPV4_TO_NUM,
)
def test_ipv4_ipv4_to_num(input_ipv4, excepted_output):
    """Test IPv4 to num conversion."""
    assert input_ipv4._ipv4_to_num() == excepted_output  # noqa: SLF001


@pytest.mark.parametrize(
    "input_ipv6", TEST_CASES_IPV6,
)
def test_ipv6(input_ipv6):
    """Test the IPv6 class."""
    assert input_ipv6


@pytest.mark.parametrize(
    ("input_ipv6", "excepted_output"),
    TEST_CASES_IPV6_STRING,
)
def test_ipv6_string(input_ipv6, excepted_output):
    """Test IPv6 string representation."""
    assert str(input_ipv6) == excepted_output


@pytest.mark.parametrize(
    ("input_ipv6", "excepted_output"),
    TEST_CASES_IPV6_IPV6_TO_NUM,
)
def test_ipv6_ipv6_to_num(input_ipv6, excepted_output):
    """Test IPv6 to num conversion."""
    assert IPv6(input_ipv6)._ipv6_to_num() == excepted_output  # noqa: SLF001


@pytest.mark.parametrize(
    ("input_ipv6", "error", "match_message"),
    TEST_CASES_IPV6_IPV6_TO_NUM_ERRORS,
)
def test_ipv6_ipv6_to_num_errors(input_ipv6, error, match_message):
    """Test errors converting IPv6 into number."""
    with pytest.raises(error, match=match_message):
        IPv6(input_ipv6)._ipv6_to_num()  # noqa: SLF001
