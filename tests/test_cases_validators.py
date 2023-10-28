"""Validator test cases."""

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

VALID_IPV4_ADDRESSES_STRICT = [
    '127.0.0.1',
    '1.1.1.1',
    '.'.join('0000'),  # Helps prevent false positives on analysis tools
    '255.255.255.255',
    '192.168.0.1',
    '222.13.7.42',
]

VALID_IPV4_ADDRESSES_LOOSE = [
    '12.123.234.345',
    '1337.1337.1337.1337',
]

INVALID_IPV4_ADDRESSES = [
    'DE.AD.BE.EF',
    '12.23.34.45.56',
    '255,255,255,255',
]

PORT_NUMBERS_VALID = [
    None,
    False,
    True,
    13,
    21,
    22,
    25,
    42,
    80,
    192,
    443,
    554,
    1111,
    3742,
    8080,
    25_565,
]

PORT_NUMBERS_INVALID = [
    22.0,
    '42',
    314159,
    -1,
    0xDEADBEEF,
]

TEST_CASES_PORT_VALIDATOR = [
    (PORT_NUMBERS_VALID[0], True),
    (PORT_NUMBERS_VALID[1], True),
    (PORT_NUMBERS_VALID[2], True),
    (PORT_NUMBERS_VALID[3], True),
    (PORT_NUMBERS_VALID[4], True),
    (PORT_NUMBERS_VALID[5], True),
    (PORT_NUMBERS_VALID[6], True),
    (PORT_NUMBERS_VALID[8], True),
    (PORT_NUMBERS_VALID[9], True),
    (PORT_NUMBERS_VALID[10], True),
    (PORT_NUMBERS_VALID[11], True),
    (PORT_NUMBERS_VALID[13], True),
    (PORT_NUMBERS_VALID[14], True),
    (PORT_NUMBERS_VALID[15], True),
    (PORT_NUMBER_MIN_VALUE - 1, False),
    (PORT_NUMBER_MAX_VALUE + 1, False),
    (PORT_NUMBERS_INVALID[4], False),
    (PORT_NUMBERS_INVALID[0], False),
    (PORT_NUMBERS_INVALID[1], False),
    ([1, 2, 3], False),
]

TEST_CASES_IP_VALIDATOR = [
    (VALID_IPV4_ADDRESSES_STRICT[0], True),
    (0xDE_AD_BE_EF, True),
    ('2606:4700:4700::1111', True),
    (IPV6_MAX_VALUE, True),
]

TEST_CASES_IPV4_VALIDATOR = [
    (VALID_IPV4_ADDRESSES_STRICT[1], True, True),
    (VALID_IPV4_ADDRESSES_STRICT[2], True, True),
    (VALID_IPV4_ADDRESSES_STRICT[3], True, True),
    (f'{VALID_IPV4_ADDRESSES_STRICT[4]}:{PORT_NUMBERS_VALID[14]}', True, True),
    (VALID_IPV4_ADDRESSES_LOOSE[0], True, False),
    (INVALID_IPV4_ADDRESSES[0], True, False),
    (INVALID_IPV4_ADDRESSES[1], False, False),
    (INVALID_IPV4_ADDRESSES[2], True, False),
    ([127, 0, 0, 1], True, False),
    (VALID_IPV4_ADDRESSES_LOOSE[1], True, False),
    (f'{VALID_IPV4_ADDRESSES_STRICT[1]}:{PORT_NUMBERS_INVALID[2]}', True, False),
    (f'{VALID_IPV4_ADDRESSES_STRICT[0]}:notaport', True, False),
    (VALID_IPV4_ADDRESSES_LOOSE[1], False, True),
    (f'{VALID_IPV4_ADDRESSES_LOOSE[1]}:{PORT_NUMBERS_INVALID[2]}', False, True),
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
    ('0:0:0:0:0:0:0:0', True, True),
    ('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF', True, True),
    ('[0:0:0:0:0:0:0:0]:80', True, True),
    (f'[FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF]:{PORT_NUMBER_MAX_VALUE}', True, True),
    ('::12', True, True),
    ('314::', True, True),
    ('2606:4700:4700::1111', True, True),
    ('2606:4700:4700::10000', False, True),
    ('2606:4700:4700::10000', True, False),
    ('2606:4700::4700::1111', True, False),
    ('2606:4700:4700::HACK', True, False),
    ('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:0001', True, False),
    ('2606:4700:4700:1111', True, False),
    ([2606, 4700, 4700, 0, 0, 0, 0, 1111], True, False),
    ('[2606:4700:4700::1111]:notaport', True, False),
    (f'[2606:4700:4700::1111]:{PORT_NUMBERS_INVALID[3]}', True, False),
    (f'[2606:4700:4700::1111]:{PORT_NUMBERS_INVALID[2]}', True, False),
    (IPV6_MIN_VALUE, True, True),
    (IPV6_MAX_VALUE, True, True),
    (IPV6_MIN_VALUE - 1, True, False),
    (IPV6_MAX_VALUE + 1, True, False),
]

TEST_CASES_SUBNET_VALIDATOR = [
    ("255.0.0.0", 'ipv4', True),
    ("255.0.0.0", 'IPV4', True),
    ("255.0.0.0", 'ipv6', False),
    ("255.255.255.128", 'ipv6', False),
    ("255.128.0.0", 'ipv4', True),
    (16, 'ipv6', True),
    ("1.1.1.1", 'ipv4', False),
    ("255.128.192.224", 'ipv4', False),
    ("255.128.128.0", 'ipv4', False),
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
    ({'1': 1}, TypeError),
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
    (f'{VALID_IPV4_ADDRESSES_STRICT[0]}:{PORT_NUMBERS_VALID[14]}', 'ipv4', VALID_IPV4_ADDRESSES_STRICT[0], PORT_NUMBERS_VALID[14], True),
    (f'{VALID_IPV4_ADDRESSES_STRICT[0]}:{PORT_NUMBERS_VALID[14]}', 'IPv4', VALID_IPV4_ADDRESSES_STRICT[0], PORT_NUMBERS_VALID[14], True),
    (f'{VALID_IPV4_ADDRESSES_STRICT[0]}:{PORT_NUMBERS_VALID[14]}', 'IPV4', VALID_IPV4_ADDRESSES_STRICT[0], PORT_NUMBERS_VALID[14], True),
    (f'{VALID_IPV4_ADDRESSES_STRICT[5]}:{PORT_NUMBERS_VALID[8]}', 'ipv4', VALID_IPV4_ADDRESSES_STRICT[5], PORT_NUMBERS_VALID[8], True),
    (VALID_IPV4_ADDRESSES_STRICT[0], 'ipv4', VALID_IPV4_ADDRESSES_STRICT[0], PORT_NUMBERS_VALID[0], True),
    (VALID_IPV4_ADDRESSES_STRICT[5], 'ipv4', VALID_IPV4_ADDRESSES_STRICT[5], PORT_NUMBERS_VALID[0], True),
]

TEST_CASES_PORT_STRIPPER_IPV6 = [
    (f'[2606:4700:4700::1111]:{PORT_NUMBERS_VALID[14]}', 'ipv6', '2606:4700:4700::1111', PORT_NUMBERS_VALID[14], True),
    (f'[2606:4700:4700::1111]:{PORT_NUMBERS_VALID[14]}', 'IPv6', '2606:4700:4700::1111', PORT_NUMBERS_VALID[14], True),
    (f'[2606:4700:4700::1111]:{PORT_NUMBERS_VALID[14]}', 'IPV6', '2606:4700:4700::1111', PORT_NUMBERS_VALID[14], True),
    (f'[::DEAD:BEEF]:{PORT_NUMBERS_VALID[8]}', 'ipv6', '::DEAD:BEEF', PORT_NUMBERS_VALID[8], True),
    ('2606:4700:4700::1111', 'ipv6', '2606:4700:4700::1111', PORT_NUMBERS_VALID[0], True),
    ('::DEAD:BEEF', 'ipv6', '::DEAD:BEEF', PORT_NUMBERS_VALID[0], True),
]
