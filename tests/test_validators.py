"""Unit tests for iplib3.validators."""

import pytest

from iplib3.constants.subnet import SubnetType
from iplib3.validators import (
    ValidationMode,
    _ipv4_subnet_validator,
    _ipv6_subnet_validator,
    _port_stripper,
    ip_validator,
    ipv4_validator,
    ipv6_validator,
    port_validator,
    subnet_validator,
)
from tests.test_cases_validators import (
    TEST_CASES_IP_VALIDATOR,
    TEST_CASES_IPV4_SUBNET_VALIDATOR,
    TEST_CASES_IPV4_SUBNET_VALIDATOR_ERRORS,
    TEST_CASES_IPV4_VALIDATOR,
    TEST_CASES_IPV6_SUBNET_VALIDATOR,
    TEST_CASES_IPV6_SUBNET_VALIDATOR_ERRORS,
    TEST_CASES_IPV6_VALIDATOR,
    TEST_CASES_PORT_STRIPPER_IPV4,
    TEST_CASES_PORT_STRIPPER_IPV6,
    TEST_CASES_PORT_VALIDATOR,
    TEST_CASES_SUBNET_VALIDATOR,
)


@pytest.mark.parametrize(
    ("port_num", "excepted_output"),
    TEST_CASES_PORT_VALIDATOR,
)
def test_port_validator(port_num: int | None, *, excepted_output: bool) -> None:
    """Test the port validator with None."""
    assert port_validator(port_num=port_num) is excepted_output


@pytest.mark.parametrize(
    ("address", "excepted_output"),
    TEST_CASES_IP_VALIDATOR,
)
def test_ip_validator(address: str, *, excepted_output: bool) -> None:
    """Test the generic IP address validator."""
    assert ip_validator(address=address) is excepted_output


@pytest.mark.parametrize(
    ("address", "validation_mode", "excepted_output"),
    TEST_CASES_IPV4_VALIDATOR,
)
def test_ipv4_validator(address: str, validation_mode: ValidationMode, *, excepted_output: bool) -> None:
    """Test IPv4 validator."""
    assert ipv4_validator(address=address, validation_mode=validation_mode) is excepted_output


@pytest.mark.parametrize(
    ("address", "validation_mode", "excepted_output"),
    TEST_CASES_IPV6_VALIDATOR,
)
def test_ipv6_validator(address: str, validation_mode: ValidationMode, *, excepted_output: bool) -> None:
    """Test IPv6 validator."""
    assert ipv6_validator(address=address, validation_mode=validation_mode) is excepted_output


@pytest.mark.parametrize(
    ("subnet", "protocol", "excepted_output"),
    TEST_CASES_SUBNET_VALIDATOR,
)
def test_subnet_validator(subnet: str | int, protocol: SubnetType, *, excepted_output: bool) -> None:
    """Test subnet validator."""
    assert subnet_validator(subnet=subnet, protocol=protocol) is excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_IPV4_SUBNET_VALIDATOR,
)
def test_ipv4_subnet_validator(subnet: str, *, excepted_output: bool) -> None:
    """Test IPv4 subnet validator."""
    assert _ipv4_subnet_validator(subnet=subnet) is excepted_output


@pytest.mark.parametrize(
    ("subnet", "error"),
    TEST_CASES_IPV4_SUBNET_VALIDATOR_ERRORS,
)
def test_ipv4_subnet_validator_errors(subnet: str, error: type[Exception]) -> None:
    """Test the IPv4 subnet validator using invalid types."""
    with pytest.raises(error):
        _ipv4_subnet_validator(subnet=subnet)


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_IPV6_SUBNET_VALIDATOR,
)
def test_ipv6_subnet_validator(subnet: int, *, excepted_output: bool) -> None:
    """Test IPv6 subnet validator."""
    assert _ipv6_subnet_validator(subnet=subnet) == excepted_output


@pytest.mark.parametrize(
    ("subnet", "error"),
    TEST_CASES_IPV6_SUBNET_VALIDATOR_ERRORS,
)
def test_ipv6_subnet_validator_errors(subnet: int, error: type[Exception]) -> None:
    """Test the IPv6 subnet validator using invalid types."""
    with pytest.raises(error):
        _ipv6_subnet_validator(subnet=subnet)


@pytest.mark.parametrize(
    ("address", "protocol", "excepted_address", "excepted_port", "excepted_valid"),
    TEST_CASES_PORT_STRIPPER_IPV4,
)
def test_port_stripper_ipv4(
    address: str, protocol: SubnetType, excepted_address: str, excepted_port: int, *, excepted_valid: bool
) -> None:
    """Test the port stripper with IPv4."""
    address, port, valid = _port_stripper(address=address, protocol=protocol)
    assert address == excepted_address
    assert port == excepted_port
    assert valid is excepted_valid


@pytest.mark.parametrize(
    ("address", "protocol", "excepted_address", "excepted_port", "excepted_valid"),
    TEST_CASES_PORT_STRIPPER_IPV6,
)
def test_port_stripper_ipv6(
    address: str, protocol: SubnetType, excepted_address: str, excepted_port: int, *, excepted_valid: bool
) -> None:
    """Test the port stripper with IPv6."""
    address, port, valid = _port_stripper(address=address, protocol=protocol)
    assert address == excepted_address
    assert port == excepted_port
    assert valid is excepted_valid


def test_port_stripper_invalid_protocol() -> None:
    """Test the port stripper for using invalid protocol."""
    with pytest.raises(ValueError, match="Invalid subnet type"):
        _port_stripper("127.0.0.1:8080", protocol="IPv9")  # type: ignore[arg-type]
