"""Unit tests for iplib3.subnet."""

import pytest

from iplib3.constants.subnet import SubnetType
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


def test_pure_subnet_mask() -> None:
    """Test the PureSubnetMask base class."""
    _ = PureSubnetMask()


@pytest.mark.parametrize(
    ("subnet", "prefix_length"),
    TEST_CASES_PURE_SUBNET_MASK_PREFIX_LENGTH,
)
def test_pure_subnet_mask_prefix_length(subnet: PureSubnetMask, prefix_length: int | None) -> None:
    """Test PureSubnetMask prefix length."""
    subnet._prefix_length = prefix_length
    assert subnet._prefix_length == prefix_length


@pytest.mark.parametrize(
    ("subnet", "excepted_output", "representation"),
    TEST_CASES_PURE_SUBNET_MASK_STRING,
)
def test_pure_subnet_mask_string(subnet: PureSubnetMask, excepted_output: str, representation: str) -> None:
    """Test PureSubnetMask string representation."""
    if representation == "str":
        assert str(subnet) == excepted_output
    elif representation == "repr":
        assert repr(subnet) == excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_PURE_SUBNET_MASK_EQUALITY,
)
def test_pure_subnet_mask_equality(subnet: PureSubnetMask, excepted_output: PureSubnetMask) -> None:
    """Test PureSubnetMask equality."""
    assert subnet == excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_PURE_SUBNET_MASK_INEQUALITY,
)
def test_pure_subnet_mask_inequality(subnet: PureSubnetMask, excepted_output: PureSubnetMask) -> None:
    """Test PureSubnetMask inequality."""
    subnet._prefix_length = None
    assert subnet != excepted_output


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_SUBNET_MASK_SUBNET_TYPE,
)
def test_subnet_mask_subnet_type(subnet: SubnetMask, excepted_output: str) -> None:
    """Test SubnetMask subnet type."""
    assert subnet._subnet_type == excepted_output


@pytest.mark.parametrize(
    ("subnet", "error", "error_message"),
    TEST_CASES_SUBNET_MASK_SUBNET_LENGTH,
)
def test_subnet_mask_subnet_length(subnet: str | int, error: type[Exception], error_message: str) -> None:
    """Test SubnetMask subnet length."""
    with pytest.raises(error, match=error_message):
        SubnetMask._ipv4_subnet_to_num(subnet)


@pytest.mark.parametrize(
    ("subnet", "excepted_output"),
    TEST_CASES_SUBNET_MASK_STRING,
)
def test_subnet_mask_string(subnet: SubnetMask, excepted_output: str) -> None:
    """Test SubnetMask string representation."""
    assert repr(subnet) == excepted_output


@pytest.mark.parametrize(
    ("subnet_mask", "subnet_type", "excepted_output"),
    TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM,
)
def test_subnet_mask_subnet_to_num(
    subnet_mask: str | int | None, subnet_type: SubnetType, excepted_output: int | None
) -> None:
    """Test SubnetMask subnet to number converter."""
    assert SubnetMask._subnet_to_num(subnet_mask=subnet_mask, subnet_type=subnet_type) == excepted_output


@pytest.mark.parametrize(
    ("subnet_mask", "subnet_type", "error", "match_message"),
    TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM_ERRORS,
)
def test_subnet_mask_subnet_to_num_errors(
    subnet_mask: None, subnet_type: SubnetType, error: type[Exception], match_message: str
) -> None:
    """Test SubnetMask subnet to number converter errors."""
    with pytest.raises(error, match=match_message):
        SubnetMask._subnet_to_num(subnet_mask=subnet_mask, subnet_type=subnet_type)


@pytest.mark.parametrize(
    ("prefix_length", "subnet_type", "excepted_output"),
    TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK,
)
def test_subnet_mask_prefix_to_subnet_mask(prefix_length: int, subnet_type: SubnetType, excepted_output: str) -> None:
    """Test SubnetMask number to mask converter."""
    assert SubnetMask._prefix_to_subnet_mask(prefix_length=prefix_length, subnet_type=subnet_type) == excepted_output


@pytest.mark.parametrize(
    ("prefix_length", "subnet_type", "error", "match_message"),
    TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK_ERRORS,
)
def test_subnet_mask_prefix_to_subnet_mask_errors(
    prefix_length: int, subnet_type: SubnetType, error: type[Exception], match_message: str
) -> None:
    """Test SubnetMask number to mask converter."""
    with pytest.raises(error, match=match_message):
        SubnetMask._prefix_to_subnet_mask(prefix_length=prefix_length, subnet_type=subnet_type)
