import pytest
from iplib3 import IPAddress, IPv4, IPv6, _ipv4_validator, _ipv6_validator # pylint: disable=import-error

def test_ipv4():
    assert str(IPAddress(25601440).as_ipv4) == '1.134.165.160'
    assert str(IPAddress('192.168.1.1')) == '192.168.1.1'
    assert str(IPv4('192.168.1.1')) == '192.168.1.1'
    assert str(IPAddress('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPv4('1.1.1.1:8080')) == '1.1.1.1:8080'

def test_ipv6():
    assert str(IPAddress(25601440).as_ipv6) == '0:0:0:0:0:0:186:A5A0'
    assert str(IPAddress('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPv6('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPAddress('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPv6('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'

def test_ipv6_full():
    assert IPAddress(25601440).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:0000:0000:0186:A5A0'

def test_ipv6_remove_zeroes():
    assert IPAddress(25601440).num_to_ipv6(remove_zeroes=True) == '::186:A5A0'

def test_chaining():
    assert str(IPAddress(25601440).as_ipv6.as_ipv4) == '1.134.165.160'

def test_ipv4_validator():
    assert _ipv4_validator('1.1.1.1') is True
    assert _ipv4_validator('0.0.0.0') is True
    assert _ipv4_validator('255.255.255.255') is True
    assert _ipv4_validator('192.168.0.1:8080') is True
    assert _ipv4_validator('12.123.234.345') is False
    assert _ipv4_validator('FF.FF.FF.FF') is False
    assert _ipv4_validator('1.1.1.1:314159') is False
    assert _ipv4_validator('12.23.34.45.56') is False
    assert _ipv4_validator('1337.1337.1337.1337', strict=False) is True
    assert _ipv4_validator('1337.1337.1337.1337:314159', strict=False) is True

def test_ipv6_validator():
    assert _ipv6_validator('0:0:0:0:0:0:0:0') is True
    assert _ipv6_validator('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF') is True
    assert _ipv6_validator('[0:0:0:0:0:0:0:0]:80') is True
    assert _ipv6_validator('[FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF]:65535') is True
    assert _ipv6_validator('::12') is True
    assert _ipv6_validator('314::') is True
    assert _ipv6_validator('2606:4700:4700::1111') is True
