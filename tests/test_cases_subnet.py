from iplib3.constants import (
    IPV4_MAX_SUBNET_VALUE,
    IPV4_MIN_SUBNET_VALUE,
    IPV6_MAX_SUBNET_VALUE,
)
from iplib3.subnet import PureSubnetMask, SubnetMask

TEST_CASES_PURE_SUBNET_MASK_PREFIX_LENGTH = [
    (PureSubnetMask(), None),
    (PureSubnetMask(), IPV4_MIN_SUBNET_VALUE),
]

TEST_CASES_PURE_SUBNET_MASK_STRING = [
    (PureSubnetMask(), '0', 'str'),
    (PureSubnetMask(), "iplib3.PureSubnetMask('0')", 'repr'),
]

TEST_CASES_PURE_SUBNET_MASK_EQUALITY = [
    (PureSubnetMask(), PureSubnetMask()),
    (PureSubnetMask(), IPV4_MIN_SUBNET_VALUE),
    (PureSubnetMask(), '0'),
]

TEST_CASES_PURE_SUBNET_MASK_INEQUALITY = [
    (PureSubnetMask(), PureSubnetMask()),
    (PureSubnetMask(), 3.14),
    (PureSubnetMask(), IPV4_MIN_SUBNET_VALUE),
]

TEST_CASES_SUBNET_MASK_SUBNET_TYPE = [
    (SubnetMask(), 'ipv6'),
    (SubnetMask('255.255.255.0'), 'ipv4'),
]

TEST_CASES_SUBNET_MASK_STRING = [
    (SubnetMask(24, subnet_type='ipv4'), "iplib3.SubnetMask('255.255.255.0')"),
    (SubnetMask(24), "iplib3.SubnetMask('24')"),
]

TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM = [
    (None, 'ipv6', None),
    (24, 'ipv6', 24),
    ('24', 'ipv6', 24),
    (None, 'ipv4', None),
    (24, 'ipv4', 24),
    ('24', 'ipv4', 24),
    ('255.255.128.0', 'ipv4', 17),
]

TEST_CASES_SUBNET_MASK_SUBNET_TO_NUM_ERRORS = [
    ([255, 255, 255, 0], 'ipv6', TypeError, "Invalid type for subnet value: "),
    ('255.255.255.0', 'ipv6', ValueError, "IPv6-subnets don't use a string representation"),
    ('3e2', 'ipv6', ValueError,  "Subnet value not valid; "),
    (IPV4_MAX_SUBNET_VALUE + 1, 'ipv4', ValueError, "Subnet '"),
    (IPV6_MAX_SUBNET_VALUE + 1, 'ipv6', ValueError, "Subnet '"),
    ('255.6.0.0', 'ipv4', ValueError, " is an invalid value in a subnet mask"),
]

TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK = [
    (24, 'ipv4', '255.255.255.0'),
]

TEST_CASES_SUBNET_MASK_PREFIX_TO_SUBNET_MASK_ERRORS = [
    (24, 'ipv6', ValueError, "IPv6 does not support string representations of subnet masks"),
    (IPV4_MAX_SUBNET_VALUE + 1, 'ipv4', ValueError, "Invalid subnet value for IPv4: "),
]
