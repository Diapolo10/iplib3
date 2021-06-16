# iplib3
 A `pathlib.Path` equivalent for IP addresses.

<!-- Badge chain start -->
 [![Version](https://img.shields.io/pypi/v/iplib3)](https://pypi.org/project/iplib3/) ![Build Status](https://github.com/diapolo10/iplib3/workflows/iplib3%20CI/badge.svg) [![License](https://img.shields.io/github/license/diapolo10/iplib3)](https://opensource.org/licenses/MIT) [![Coverage Status](https://coveralls.io/repos/github/Diapolo10/iplib3/badge.svg?branch=main?logo=coveralls)](https://coveralls.io/github/Diapolo10/iplib3?branch=main)  
 [![Dependencies](https://img.shields.io/librariesio/github/diapolo10/iplib3)](https://libraries.io/github/Diapolo10/iplib3) [![CodeFactor](https://www.codefactor.io/repository/github/diapolo10/iplib3/badge?logo=codefactor)](https://www.codefactor.io/repository/github/diapolo10/iplib3) [![Rating](https://img.shields.io/librariesio/sourcerank/pypi/iplib3)](https://libraries.io/github/Diapolo10/iplib3/sourcerank) ![Python versions](https://img.shields.io/pypi/pyversions/iplib3?logo=python)  
 ![Downloads](https://img.shields.io/pypi/dm/iplib3?logo=pypi) ![Wheel](https://img.shields.io/pypi/wheel/iplib3?logo=pypi) ![Repository size](https://img.shields.io/github/repo-size/diapolo10/iplib3?logo=github) ![Code size](https://img.shields.io/github/languages/code-size/diapolo10/iplib3?logo=github)  
 ![Lines of code](https://img.shields.io/tokei/lines/github/diapolo10/iplib3?logo=github) ![File count](https://img.shields.io/github/directory-file-count/diapolo10/iplib3?logo=github) ![Last commit](https://img.shields.io/github/last-commit/diapolo10/iplib3?logo=github)
<!-- Badge chain end -->

This module was heavily inspired by the built-in `pathlib` module to provide a similiar, flexible interface for IP addresses. `iplib3` can effortlessly convert between IPv4, IPv6, raw numbers and hex values and it can also verify IP address syntax. It can recognise optional port numbers and store them separately from the main address. The `iplib.IPAddress` class works like `pathlib.Path` in that it accepts both IPv4 and IPv6 addresses, returning an object representing whichever format was used. The module also uses some unit tests, and these will be added more over time as functionality grows and becomes more set in stone.

The module is currently lacking in long-term vision as I used it as a practice project, but there are some plans to further flesh it out. It could incorporate URL support in the future and may be extended with `requests` integration.

This project is not affiliated with `iplib`, the naming similarity is merely a coincidence.

## Requirements

`iplib3` requires Python version 3.6 and above. It could be back-ported to 3.5 or for even earlier versions with relatively little change, but the maintainer doesn't see a good reason to focus on earlier versions. This module does not support Python 2.

## Installation

To install `iplib3`, use the package manager [`pip`](https://pip.pypa.io/en/stable/).

For Windows:

```sh
py -3 -m pip install iplib3
```

For Unix/Linux:

```sh
pip3 install iplib3
```

For other platforms, you may try:

```sh
pip install iplib3
```

## Basic Use

The module mainly provides a single class, `iplib3.IPAddress`, which can be used to initialise IP address objects of any supported type. However, it is possible to use the provided `iplib3.IPv4` and `iplib3.IPv6` classes directly if needed.

The primary class has the advantage that it also supports raw numbers; you can initialise it with any positive integer in addition to stringified addresses, and since you can directly convert between the two sub-classes at any time you can use all functionality with just `iplib3.IPAddress`. Since `iplib3.IPv4` and `iplib3.IPv6` are subclasses of `iplib3.IPAddress`, you can use `isinstance` to recognise any of the three types.

###IP Address

In `iplib3`, *IPAddress* is a single class to initialise IP address objects of any supported type. *IPAddress* by default initialise IP Addresses of IPv4 type.

######Example:
```python
from iplib3 import IPAddress, IPv6
address = IPAddress('222.173.190.239')
print(address) 

```
######Output:
```
222.173.190.239
```

###Port Number
In `iplib3`, *port* is used to specify port number to IP address.

######Example:
```python
print(address.port) 
```
######Output:
```
None
```
As *port* is not assigned a number, it shows results as *None*.

######Example:
```python
address.port = 80
print(address) 
```
######Output:
```
222.173.190.239:80
```
IP Address is shown along with the specified port number.

###Printable Representation of IP Address
*repr()* function returns a printable representation of the IP Address.

######Example:
```python
print(repr(address))
```
######Output:
```
iplib3.IPv4('222.173.190.239:80')
```
### IP Address IPv6
In `iplib3`, declare IP Address for IPv6 using `.as_ipv6`. By using `.as_ipv6`, convert IP Address from IPv4 to IPv6. 

######Example:
```python
ipv6_address = address.as_ipv6
print(ipv6_address)
```
######Output:
```
[0:0:0:0:0:0:DEAD:BEEF]:80
```
### IP Address IPv6 with Port Number

In `iplib3`, *port* is used to specify port number to IP address for IPv6.

######Example:
```python
ipv6_address.port = None
print(ipv6_address)
```
######Output:
```
0:0:0:0:0:0:DEAD:BEEF
```
###Printable Representation of IP Address IPv6
*repr()* function returns a printable representation of the IP Address for IPv6.

######Example:
```python
print(repr(ipv6_address))
```
######Output:
```
iplib3.IPv6('0:0:0:0:0:0:DEAD:BEEF')
```
###Different Formats of IP Address IPv6
IP Address of IPv6 exists in different formats.

######Example:
```python
foo = IPv6('[::1337:1337:1337:1337]:25565')
bar = IPv6('::1337:1337:1337:1337', 25565)
baz = IPv6('::1337:1337:1337:1337', port_num=25565)
print(f"Addresses are {'equal' if foo == bar == baz else 'not equal'}")
print(baz)
```
######Output:
```
Addresses are equal
[::1337:1337:1337:1337]:25565
```
###Convert IP Address IPv6 to IPv4
In `iplib3`, convert IP Address of IPv6 to IPv4 using `.as_ipv4`.
######Example:
```python
baz=baz.as_ipv4
print(baz)
print(repr(baz))
```
######Output:
```
19.55.19.55:25565
iplib3.IPv4('19.55.19.55:25565')
```
In `iplib3`, subsequent conversions of IPv4 and IPv6 are not the same.
######Example:
```python
print(baz.as_ipv4.as_ipv6 == baz)
```
######Output:
```
False
```
###Update Port Number
To update an existing port number of an IP Address, specify a new port number using *port_num*.
######Example:
```python
spam = IPv6('[::1337:1337:1337:1337]:80', port_num=25565)
print(spam) 
```
######Output:
```
[::1337:1337:1337:1337]:25565
```

###Convert IP Address to Hexa values
In `iplib3`, convert IP Address to hexa values using `.hex`.
######Example:
```python
print(address.hex) 
```

######Output:
```
0xDEADBEEF
```
###Convert IP Address to Numbers
In `iplib3`, convert IP Address to numbers using `.num`.
######Example:
```python
print(address.num) 
```

######Output:
```
3735928559
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
This project is licensed under an [MIT](./LICENSE) license.
