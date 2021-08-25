# IPLib3

A `pathlib.Path`-equivalent for IP addresses.

|              |   |
|--------------|---|
| PyPI         | ![Python versions](https://img.shields.io/pypi/pyversions/iplib3?logo=python) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/iplib3) ![Wheel](https://img.shields.io/pypi/wheel/iplib3?logo=pypi) ![Downloads](https://img.shields.io/pypi/dm/iplib3?logo=pypi) [![Version](https://img.shields.io/pypi/v/iplib3)](https://pypi.org/project/iplib3/) |
| Tests (main) | [![codecov](https://codecov.io/gh/Diapolo10/iplib3/branch/main/graph/badge.svg?token=JUWGSVLIF3)](https://codecov.io/gh/Diapolo10/iplib3) ![Unit tests](https://github.com/diapolo10/iplib3/workflows/Unit%20tests/badge.svg) ![Pylint](https://github.com/diapolo10/iplib3/workflows/Pylint/badge.svg) ![Flake8](https://github.com/diapolo10/iplib3/workflows/Flake8/badge.svg) ![Deploy to PyPI](https://github.com/diapolo10/iplib3/workflows/Deploy%20to%20PyPI/badge.svg) |
| Tests (nightly) | [![codecov](https://codecov.io/gh/Diapolo10/iplib3/branch/nightly/graph/badge.svg?token=JUWGSVLIF3)](https://codecov.io/gh/Diapolo10/iplib3/branch/nightly) ![Unit tests](https://github.com/diapolo10/iplib3/workflows/Unit%20tests/badge.svg?branch=nightly) ![Pylint](https://github.com/diapolo10/iplib3/workflows/Pylint/badge.svg?branch=nightly) ![Flake8](https://github.com/diapolo10/iplib3/workflows/Flake8/badge.svg?branch=nightly) ![Deploy to PyPI](https://github.com/diapolo10/iplib3/workflows/Deploy%20to%20PyPI/badge.svg?branch=nightly) |
| Docs         | [![Documentation Status](https://readthedocs.org/projects/iplib3/badge/?version=latest)](https://iplib3.readthedocs.io/en/latest/?badge=latest) |
| Activity     | ![GitHub contributors](https://img.shields.io/github/contributors/diapolo10/iplib3) ![Last commit](https://img.shields.io/github/last-commit/diapolo10/iplib3?logo=github) ![GitHub all releases](https://img.shields.io/github/downloads/diapolo10/iplib3/total?logo=github) ![GitHub issues](https://img.shields.io/github/issues/diapolo10/iplib3) ![GitHub closed issues](https://img.shields.io/github/issues-closed/diapolo10/iplib3) ![GitHub pull requests](https://img.shields.io/github/issues-pr/diapolo10/iplib3) ![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/diapolo10/iplib3) |
| QA           | [![CodeFactor](https://www.codefactor.io/repository/github/diapolo10/iplib3/badge?logo=codefactor)](https://www.codefactor.io/repository/github/diapolo10/iplib3) [![Rating](https://img.shields.io/librariesio/sourcerank/pypi/iplib3)](https://libraries.io/github/Diapolo10/iplib3/sourcerank) |
| Other        | [![License](https://img.shields.io/github/license/diapolo10/iplib3)](https://opensource.org/licenses/MIT) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDiapolo10%2Fiplib3.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FDiapolo10%2Fiplib3?ref=badge_shield) [![Requirements Status](https://requires.io/github/Diapolo10/iplib3/requirements.svg?branch=nightly)](https://requires.io/github/Diapolo10/iplib3/requirements/?branch=nightly) ![Repository size](https://img.shields.io/github/repo-size/diapolo10/iplib3?logo=github) ![Code size](https://img.shields.io/github/languages/code-size/diapolo10/iplib3?logo=github) ![Lines of code](https://img.shields.io/tokei/lines/github/diapolo10/iplib3?logo=github) |

This module was heavily inspired by the built-in `pathlib` module to provide a similar, flexible interface for IP addresses. `iplib3` can effortlessly convert between IPv4, IPv6, raw numbers and hex values and it can also verify IP address syntax. It can recognise optional port numbers and store them separately from the main address. The `iplib.IPAddress` class works like `pathlib.Path` in that it accepts both IPv4 and IPv6 addresses, returning an object representing whichever format was used. The module also uses some unit tests, and these will be added more over time as functionality grows and becomes more set in stone.

The module is currently lacking in long-term vision as I used it as a practice project, but there are some plans to further flesh it out. It could incorporate URL support in the future and may be extended with `requests` integration.

This project is not affiliated with `iplib`, the naming similarity is merely a coincidence.


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDiapolo10%2Fiplib3.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FDiapolo10%2Fiplib3?ref=badge_large)

## Installation

`iplib3` will work with Python versions 3.6 and above. It could be back-ported to 3.5 or for even earlier versions with relatively little change, but the maintainer doesn't see a good reason to focus on earlier versions.

This module will not support Python 2.

Use the package manager [`pip`](https://pip.pypa.io/en/stable/) to install `iplib3`.

On Windows:

```sh
py -m pip install iplib3
```

On most Unix-like platforms:

```sh
pip3 install iplib3
```

On other platforms, you may try:

```sh
pip install iplib3
```

The library is distributed as wheels and source distributions, and the source distributions use Poetry as the build back-end instead of `setuptools`.

## Usage

The module mainly provides a single class, `iplib3.IPAddress`, which can be used to initialise IP address objects of any supported type. However, it is possible to use the provided `iplib3.IPv4` and `iplib3.IPv6` classes directly if needed.

The primary class has the advantage that it also supports raw numbers; you can initialise it with any positive integer in addition to stringified addresses, and since you can directly convert between the two sub-classes at any time you can use all functionality with just `iplib3.IPAddress`. Since `iplib3.IPv4` and `iplib3.IPv6` are subclasses of `iplib3.IPAddress`, you can use `isinstance` to recognise any of the three types.

Some basic usage examples:

```python
from iplib3 import IPAddress, IPv6

address = IPAddress('222.173.190.239')
print(address) # 222.173.190.239

print(address.port) # None, because we never specified one
address.port = 80
print(address) # 222.173.190.239:80

print(repr(address)) # iplib3.IPv4('222.173.190.239:80')


ipv6_address = address.as_ipv6
print(ipv6_address) # [0:0:0:0:0:0:DEAD:BEEF]:80
ipv6_address.port = None
print(ipv6_address) # 0:0:0:0:0:0:DEAD:BEEF

print(repr(ipv6_address)) # iplib3.IPv6('0:0:0:0:0:0:DEAD:BEEF')

foo = IPv6('[::1337:1337:1337:1337]:25565')
bar = IPv6('::1337:1337:1337:1337', 25565)
baz = IPv6('::1337:1337:1337:1337', port_num=25565)

print(f"Addresses are {'equal' if foo == bar == baz else 'not equal'}")
print(baz) # [::1337:1337:1337:1337]:25565

print(baz.as_ipv4.as_ipv6 == baz)

# If the string contains a port number and you also provide a port separately,
# then the separately provided port takes precedence
spam = IPv6('[::1337:1337:1337:1337]:80', port_num=25565)
print(spam) # [::1337:1337:1337:1337]:25565

print(address.hex) # 0xDEADBEEF
print(address.num) # 3735928559
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under an [MIT license](./LICENSE).

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDiapolo10%2Fiplib3.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FDiapolo10%2Fiplib3?ref=badge_large)
