"""Unit tests for iplib3.subnet."""

import pytest

from iplib3.subnet import (
    PureSubnetMask,
    SubnetMask,
)
from tests.test_cases_subnet import (
    TEST_CASES_PURE_SUBNET_MASK_EQUALITY,
    TEST_CASES_PURE_SUBNET_MASK_INEQUALITY,
    TEST_CASES_PURE_SUBNET_MASK_PREFIX_LENGTH,
    TEST_CASES_PURE_SUBNET_MASK_STRING,
    TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK,
    TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK_ERRORS,
    TEST_CASES_SUBNET_MASK_STRING,
    TEST_CASES_SUBNET_MASK_SUBNET_LENGTH,
    TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM,
    TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM_ERRORS,
    TEST_CASES_SUBNET_MASK_SUBNET_TYPE,
)


def test_pure_subnet_mask():
    """Test the PureSubnetMask base class."""
    _ = PureSubnetMask()


@pytest.mark.parametrize(
    ("subnet", "prefix_length"),
    TEST_CASES_PURE_SUBNET_MASK_PREFIX_LENGTH,
)
def test_pure_subnet_mask_prefix_length(subnet, prefix_length):
    """Test PureSubnetMask prefix length."""
    subnet._prefix_length = prefix_length  # noqa: SLF001
    assert subnet._prefix_length == prefix_length  # noqa: SLF001


@pytest.mark.parametrize(
    ("subnet", "excepted_output", "representation"),
    TEST_CASES_PURE_SUBNET_MASK_STRING,
)
def test_pure_subnet_mask_string(subnet, excepted_output, representation):
    """Test PureSubnetMask string representation."""
    if representation == "str":
        assert str(subnet) == excepted_output
    elif representation == "repr":
        assert repr(subnet) == excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_PURE_SUBNET_MASK_EQUALITY,
)
def test_pure_subnet_mask_equality(subnet, excepted_output):
    """Test PureSubnetMask equality."""
    assert subnet == excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_PURE_SUBNET_MASK_INEQUALITY,
)
def test_pure_subnet_mask_inequality(subnet, excepted_output):
    """Test PureSubnetMask inequality."""
    subnet._prefix_length = None  # noqa: SLF001
    assert subnet != excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_SUBNET_MASK_SUBNET_TYPE,
)
def test_subnet_mask_subnet_type(subnet, excepted_output):
    """Test SubnetMask subnet type."""
    assert subnet._subnet_type == excepted_output  # noqa: SLF001


@pytest.mark.parametrize(
    ("subnet", "error", "error_message"),
    TEST_CASES_SUBNET_MASK_SUBNET_LENGTH,
)
def test_subnet_mask_subnet_length(subnet, error, error_message):
    """Test SubnetMask subnet length."""
    with pytest.raises(error, match=error_message):
        SubnetMask._ipv4_subnet_to_num(subnet)  # noqa: SLF001


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_SUBNET_MASK_STRING,
)
def test_subnet_mask_string(subnet, excepted_output):
    """Test SubnetMask string representation."""
    assert repr(subnet) == excepted_output


@pytest.mark.parametrize(
    ("subnet_mask", "subnet_type", "excepted_output"),
    TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM,
)
def test_subnet_mask_subnet_to_num(subnet_mask, subnet_type, excepted_output):
    """Test SubnetMask subnet to number converter."""
    assert SubnetMask._subnet_to_num(subnet_mask=subnet_mask, subnet_type=subnet_type) == excepted_output  # noqa: SLF001


@pytest.mark.parametrize(
    ("subnet_mask", "subnet_type", "error", "match_message"),
    TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM_ERRORS,
)
def test_subnet_mask_subnet_to_num_errors(subnet_mask, subnet_type, error, match_message):
    """Test SubnetMask subnet to number converter errors."""
    with pytest.raises(error, match=match_message):
        SubnetMask._subnet_to_num(subnet_mask=subnet_mask, subnet_type=subnet_type)  # noqa: SLF001


@pytest.mark.parametrize(
    ("prefix_length", "subnet_type", "excepted_output"),
    TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK,
)
def test_subnet_mask_prefix_to_subnet_mask(prefix_length, subnet_type, excepted_output):
    """Test SubnetMask number to mask converter."""
    assert SubnetMask._prefix_to_subnet_mask(prefix_length=prefix_length, subnet_type=subnet_type) == excepted_output  # noqa: SLF001


@pytest.mark.parametrize(
    ("prefix_length", "subnet_type", "error", "match_message"),
    TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK_ERRORS,
)
def test_subnet_mask_prefix_to_subnet_mask_errors(prefix_length, subnet_type, error, match_message):
    """Test SubnetMask number to mask converter."""
    with pytest.raises(error, match=match_message):
        SubnetMask._prefix_to_subnet_mask(prefix_length=prefix_length, subnet_type=subnet_type)  # noqa: SLF001
