# iplib3
 A `pathlib.Path` equivalent for IP addresses.

This module was heavily inspired by the built-in `pathlib` module to provide a similiar, flexible interface for IP addresses. `iplib3` can effortlessly convert between IPv4, IPv6, raw numbers and hex values and it can also verify IP address syntax. It can recognise optional port numbers and store them separately from the main address. The `iplib.IPAddress` class works like `pathlib.Path` in that it accepts both IPv4 and IPv6 addresses, returning an object representing whichever format was used. The module also uses some unit tests, and these will be added more over time as functionality grows and becomes more set in stone.

The module is currently lacking in long-term vision as I used it as a practice project, but there are some plans to further flesh it out. It could incorporate URL support in the future and may be extended with `requests` integration.

This project is not affiliated with `iplib`, the naming similarity is merely a coincidence.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `iplib3`.

```sh
pip install iplib3
```

## Usage

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
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
This project is licensed under an [MIT](./LICENSE) license.