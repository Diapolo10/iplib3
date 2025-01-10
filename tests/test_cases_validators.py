"""Test cases for validators."""

from iplib3.constants import (
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

TEST_CASES_PORT_VALIDATOR = [
    (None, True),
    (False, True),
    (True, True),
    (13, True),
    (21, True),
    (22, True),
    (25, True),
    (80, True),
    (192, True),
    (443, True),
    (554, True),
    (3724, True),
    (8080, True),
    (25_565, True),
    (PORT_NUMBER_MIN_VALUE - 1, False),
    (PORT_NUMBER_MAX_VALUE + 1, False),
    (0xDEADBEEF, False),
    (22.0, False),
    ("42", False),
    ([1, 2, 3], False),
]

TEST_CASES_IP_VALIDATOR = [
    ("128.0.0.1", True),
    (0xDE_AD_BE_EF, True),
    ("2606:4700:4700::1111", True),
    (IPV6_MAX_VALUE, True),
]

TEST_CASES_IPV4_VALIDATOR = [
    ("1.1.1.1", True, True),
    ("0.0.0.0", True, True),  #  noqa: S104
    ("255.255.255.255", True, True),
    ("192.168.0.1:8080", True, True),
    ("12.123.234.345", True, False),
    ("DE.AD.BE.EF", True, False),
    ("12.23.34.45.56", False, False),
    ("255,255,255,255", True, False),
    ([127, 0, 0, 1], True, False),
    ("1337.1337.1337.1337", True, False),
    ("1.1.1.1:314159", True, False),
    ("128.0.0.1:notaport", True, False),
    ("1337.1337.1337.1337", False, True),
    ("1337.1337.1337.1337:314159", False, True),
    (25601440, True, True),
    (0xDEADBEEF, True, True),
    (25601440, False, True),
    (0xDEADBEEF, False, True),
    (IPV4_MIN_VALUE, True, True),
    (IPV4_MAX_VALUE, True, True),
    (IPV4_MIN_VALUE - 1, True, False),
    (IPV4_MAX_VALUE + 1, True, False),
    (256014.40, True, False),
]

TEST_CASES_IPV6_VALIDATOR = [
    ("0:0:0:0:0:0:0:0", True, True),
    ("FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF", True, True),
    ("[0:0:0:0:0:0:0:0]:80", True, True),
    ("[FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF]:65535", True, True),
    ("::12", True, True),
    ("314::", True, True),
    ("2606:4700:4700::1111", True, True),
    ("2606:4700:4700::10000", False, True),
    ("2606:4700:4700::10000", True, False),
    ("2606:4700::4700::1111", True, False),
    ("2606:4700:4700::HACK", True, False),
    ("FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:0001", True, False),
    ("2606:4700:4700:1111", True, False),
    ([2606, 4700, 4700, 0, 0, 0, 0, 1111], True, False),
    ("[2606:4700:4700::1111]:notaport", True, False),
    ("[2606:4700:4700::1111]:-1", True, False),
    ("[2606:4700:4700::1111]:314159", True, False),
    (IPV6_MIN_VALUE, True, True),
    (IPV6_MAX_VALUE, True, True),
    (IPV6_MIN_VALUE - 1, True, False),
    (IPV6_MAX_VALUE + 1, True, False),
]

TEST_CASES_SUBNET_VALIDATOR = [
    ("255.0.0.0", "ipv4", True),
    ("255.0.0.0", "IPV4", True),
    ("255.0.0.0", "ipv6", False),
    ("255.255.255.128", "ipv6", False),
    ("255.128.0.0", "ipv4", True),
    (16, "ipv6", True),
    ("1.1.1.1", "ipv4", False),
    ("255.128.192.224", "ipv4", False),
    ("255.128.128.0", "ipv4", False),
]

TEST_CASES_IPV4_SUBNET_VALIDATOR = [
    ("255.0.0.0", True),
    ("255.255.0.0", True),
    ("255.255.128.0", True),
    ("255.255.255.0", True),
    ("255.255.255.128", True),
    ("255.255.255.192", True),
    ("255.255.255.224", True),
    ("255.255.255.240", True),
    ("255.255.255.248", True),
    ("255.255.255.252", True),
    ("255.255.255.254", True),
    ("255.255.255.255", False),
    ("255.128.128.0", False),
    ("256.256.256.0", False),
    ("128.0.0.1", False),
    ("255.128", False),
    ("255.255.255.255.128", False),
    (0, True),
    (1, True),
    (30, True),
    (31, True),
    (IPV4_MAX_SUBNET_VALUE + 1, False),
    (IPV4_MIN_SUBNET_VALUE - 1, False),
]

TEST_CASES_IPV4_SUBNET_VALIDATOR_ERRORS = [
    ([1, 2, 3, 4], TypeError),
    ({"1": 1}, TypeError),
]

TEST_CASES_IPV6_SUBNET_VALIDATOR = [
    (0, True),
    (4, True),
    (8, True),
    (12, True),
    (IPV6_MAX_SUBNET_VALUE + 1, False),
    (IPV6_MIN_SUBNET_VALUE - 1, False),
    (17, False),
]

TEST_CASES_IPV6_SUBNET_VALIDATOR_ERRORS = [
    ("255.255.255.0", TypeError),
    ("::DEAD:BEEF", TypeError),
    ([1, 2, 3], TypeError),
]

TEST_CASES_PORT_STRIPPER_IPV4 = [
    ("127.0.0.1:8080", "ipv4", "127.0.0.1", 8080, True),
    ("127.0.0.1:8080", "IPv4", "127.0.0.1", 8080, True),
    ("127.0.0.1:8080", "IPV4", "127.0.0.1", 8080, True),
    ("222.13.7.42:80", "ipv4", "222.13.7.42", 80, True),
    ("127.0.0.1", "ipv4", "127.0.0.1", None, True),
    ("222.13.7.42", "ipv4", "222.13.7.42", None, True),
]

TEST_CASES_PORT_STRIPPER_IPV6 = [
    ("[2606:4700:4700::1111]:8080", "ipv6", "2606:4700:4700::1111", 8080, True),
    ("[2606:4700:4700::1111]:8080", "IPv6", "2606:4700:4700::1111", 8080, True),
    ("[2606:4700:4700::1111]:8080", "IPV6", "2606:4700:4700::1111", 8080, True),
    ("[::DEAD:BEEF]:80", "ipv6", "::DEAD:BEEF", 80, True),
    ("2606:4700:4700::1111", "ipv6", "2606:4700:4700::1111", None, True),
    ("::DEAD:BEEF", "ipv6", "::DEAD:BEEF", None, True),
]
