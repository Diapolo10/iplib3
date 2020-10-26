import pytest
from iplib import IPAddress # pylint: disable=import-error

def test_ipv4():
    assert str(IPAddress(25601440).as_ipv4) == '1.134.165.160'
    assert str(IPAddress('192.168.1.1')) == '192.168.1.1'

def test_ipv6():
    assert str(IPAddress(25601440).as_ipv6) == '0:0:0:0:0:0:186:A5A0'

def test_ipv6_full():
    assert IPAddress(25601440).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:0000:0000:0186:A5A0'

def test_ipv6_remove_zeroes():
    assert IPAddress(25601440).num_to_ipv6(remove_zeroes=True) == '::186:A5A0'

def test_chaining():
    assert str(IPAddress(25601440).as_ipv6.as_ipv4) == '1.134.165.160'
