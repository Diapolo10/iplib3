import pytest
from iplib import IPAddress # pylint: disable=import-error

def test_ipv4():
    assert IPAddress(25601440)._ipv4 == '1.134.165.160'