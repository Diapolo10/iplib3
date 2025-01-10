"""Test cases for addresses."""

from iplib3 import IPAddress, IPv4, IPv6
from iplib3.address import PureAddress
from iplib3.constants import (
    IPV4_LOCALHOST,
    IPV6_LOCALHOST,
    PORT_NUMBER_MAX_VALUE,
)
from iplib3.constants.port import PORT_NUMBER_MIN_VALUE

TEST_CASES_PURE_ADDRESS = [
    PureAddress(),
    PureAddress(0xDE_AD_BE_EF),
    PureAddress(port=80),
    PureAddress(IPV4_LOCALHOST, 80),
    PureAddress(-42),
]

TEST_CASES_PURE_ADDRESS_EQUALITY = [
    (PureAddress(0xDE_AD_BE_EF), PureAddress(0xDE_AD_BE_EF), True),
    (PureAddress(0xDE_AD_BE_EF), PureAddress(0xDE_AD_BE_EF, 80), False),
    (PureAddress(0xDE_AD_BE_EF), 0xDE_AD_BE_EF, False),
    (PureAddress(0xDE_AD_BE_EF), "cheese", False),
]

TEST_CASES_PURE_ADDRESS_INEQUALITY = [
    (PureAddress(0xDE_AD_BE_EF), PureAddress(0xC0_01_BA_5E)),
    (PureAddress(0xDE_AD_BE_EF), PureAddress(0xDE_AD_BE_EF, 80)),
    (PureAddress(0xDE_AD_BE_EF), 0xC0_01_BA_5E),
]

TEST_CASES_PURE_ADDRESS_NUM = [
    (PureAddress(), 0),
    (PureAddress(0xDE_AD_BE_EF), 0xDE_AD_BE_EF),
    (PureAddress(port=80), 0),
    (PureAddress(IPV4_LOCALHOST, 80), 0x7F_00_00_01),
    (PureAddress(-42), 0),
]

TEST_CASES_PURE_ADDRESS_PORT = [
    (PureAddress(), None),
    (PureAddress(0xDE_AD_BE_EF), None),
    (PureAddress(port=80), 80),
    (PureAddress(IPV4_LOCALHOST, 80), 80),
    (PureAddress(-42), None),
]

TEST_CASES_PURE_ADDRESS_PORT_SETTER_ERROR = [
    (3.14, TypeError, "Port "),
    ("80", TypeError, "Port "),
    (PORT_NUMBER_MAX_VALUE + 1, ValueError, "Port number "),
    (PORT_NUMBER_MIN_VALUE - 1, ValueError, "Port number "),
]

TEST_CASES_PURE_ADDRESS_AS_HEX = [
    (PureAddress(0xDE_AD_BE_EF), "0xDEADBEEF"),
    (PureAddress(0x8B_AD_F0_0D), "0x8BADF00D"),
    (PureAddress(0xDE_AD_C0_DE), "0xDEADC0DE"),
]

TEST_CASES_PURE_ADDRESS_NUM_TO_IPV4 = [
    (PureAddress(IPV4_LOCALHOST), "127.0.0.1"),
]

TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6 = [
    (PureAddress(IPV6_LOCALHOST), "0:0:0:0:0:0:0:1"),
    (PureAddress(0xDEAD_C0DE_1057_BE17), "0:0:0:0:DEAD:C0DE:1057:BE17"),
    (PureAddress(0xBADC_0FFE_E0DD_F00D), "0:0:0:0:BADC:FFE:E0DD:F00D"),
]

TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6_NO_SHORTENING = [
    (PureAddress(IPV6_LOCALHOST), "0000:0000:0000:0000:0000:0000:0000:0001"),
    (PureAddress(0xDEAD_C0DE_1057_BE17), "0000:0000:0000:0000:DEAD:C0DE:1057:BE17"),
    (PureAddress(0xBADC_0FFE_E0DD_F00D), "0000:0000:0000:0000:BADC:0FFE:E0DD:F00D"),
]

TEST_CASES_PURE_ADDRESS_NUM_TO_IPV6_REMOVE_ZEROS = [
    (PureAddress(IPV6_LOCALHOST), "::1"),
    (PureAddress(0xDEAD_C0DE_1057_BE17), "::DEAD:C0DE:1057:BE17"),
    (PureAddress(0xBADC_0FFE_E0DD_F00D), "::BADC:FFE:E0DD:F00D"),
]

TEST_CASES_IPADDRESS = [
    (IPAddress(), IPAddress),
    (IPAddress(IPV4_LOCALHOST), IPAddress),
    (IPAddress("127.0.0.1"), IPv4),  # type: ignore[arg-type]
    (IPAddress("::DEAD:BEEF"), IPv6),  # type: ignore[arg-type]
    (IPAddress(IPV4_LOCALHOST, 80), IPAddress),
    (IPAddress("127.0.0.1", 80), IPv4),  # type: ignore[arg-type]
    (IPAddress("::DEAD:BEEF", 80), IPv6),  # type: ignore[arg-type]
]

TEST_CASES_IPADDRESS_EQUALITY = [
    (IPAddress(IPV4_LOCALHOST), IPAddress(IPV4_LOCALHOST)),
    (IPAddress(IPV4_LOCALHOST), "127.0.0.1"),
    (IPAddress(IPV4_LOCALHOST), PureAddress(IPV4_LOCALHOST)),
]

TEST_CASES_IPADDRESS_STRING = [
    (IPAddress(), "127.0.0.1"),
    (IPAddress(IPV4_LOCALHOST), "127.0.0.1"),
    (IPAddress(0xDEAD_DEAD_BEEF), "0:0:0:0:0:DEAD:DEAD:BEEF"),
]

TEST_CASES_IPADDRESS_REPR = [
    (IPAddress(), "iplib3.IPAddress('127.0.0.1')"),
    (IPAddress(IPV4_LOCALHOST), "iplib3.IPAddress('127.0.0.1')"),
    (IPAddress(0xDEAD_DEAD_BEEF), "iplib3.IPAddress('0:0:0:0:0:DEAD:DEAD:BEEF')"),
]

TEST_CASES_IPADDRESS_AS_IPV4 = [
    (IPAddress(), IPv4),
    (IPAddress("127.0.0.1"), IPv4),  # type: ignore[arg-type]
    (IPAddress("::DEAD:BEEF"), IPv4),  # type: ignore[arg-type]
]

TEST_CASES_IPADDRESS_AS_IPV6 = [
    (IPAddress(), IPv6),
    (IPAddress("127.0.0.1"), IPv6),  # type: ignore[arg-type]
    (IPAddress("::DEAD:BEEF"), IPv6),  # type: ignore[arg-type]
]

TEST_CASES_IPV4 = [
    IPv4(),
    IPv4("127.0.0.1"),
    IPv4("127.0.0.1:80"),
    IPv4("127.0.0.1", 80),
    IPv4("127.0.0.1:80", 8080),
    IPv4("127.0.0.1", port_num=80),
]

TEST_CASES_IPV4_STRING = [
    (IPv4(), "127.0.0.1"),
    (IPv4("127.0.0.1"), "127.0.0.1"),
    (IPv4("127.0.0.1:80"), "127.0.0.1:80"),
    (IPv4("127.0.0.1", 80), "127.0.0.1:80"),
    (IPv4("127.0.0.1:80", 8080), "127.0.0.1:8080"),
]

TEST_CASES_IPV4_IPV4_TO_NUM = [
    (IPv4(), IPV4_LOCALHOST),
    (IPv4("127.0.0.1"), IPV4_LOCALHOST),
    (IPv4("192.168.0.1"), 0xC0_A8_00_01),
]

TEST_CASES_IPV6 = [
    IPv6(),
    IPv6("2606:4700:4700::1111"),
    IPv6("2606:4700:4700::1111", 80),
    IPv6("[2606:4700:4700::1111]:80"),
    IPv6("[2606:4700:4700::1111]:80", 8080),
]

TEST_CASES_IPV6_STRING = [
    (IPv6(), "0:0:0:0:0:0:0:1"),
    (IPv6("2606:4700:4700::1111"), "2606:4700:4700::1111"),
    (IPv6("2606:4700:4700::1111", 80), "[2606:4700:4700::1111]:80"),
    (IPv6("[2606:4700:4700::1111]:80"), "[2606:4700:4700::1111]:80"),
    (IPv6("[2606:4700:4700::1111]:80", 8080), "[2606:4700:4700::1111]:8080"),
    (IPv6("2606:4700:4700::1111", port_num=80), "[2606:4700:4700::1111]:80"),
]

TEST_CASES_IPV6_IPV6_TO_NUM = [
    (None, IPV6_LOCALHOST),
    ("70::", 0x70_0000_0000_0000_0000_0000_0000_0000),
]

TEST_CASES_IPV6_IPV6_TO_NUM_ERRORS = [
    # Two zero-skips
    ("::DE::AD", ValueError, "Invalid IPv6 address format; only one zero-skip allowed"),
    # Invalid hex literal
    ("::H07:AF", ValueError, "Invalid IPv6 address format; address contains invalid characters"),
    # Too many segments
    ("1:1:1:1:1:1:1:1:1", ValueError, "Invalid IPv6 address format; too many segments "),
    # Segment value too high
    ("::7:FFFFF", ValueError, "Invalid IPv6 address format; segment max value "),
    # Segment value too low (negative)
    ("::7:-34", ValueError, "Invalid IPv6 address format; segment min value "),
]
