# iplib3
 A `pathlib.Path` equivalent for IP addresses.

This module was heavily inspired by the built-in `pathlib` module to provide a similiar, flexible interface for IP addresses. `iplib3` can effortlessly convert between IPV4, IPV6, raw numbers and hex values and it can also verify IP address syntax. It can recognise optional port numbers and store them separately from the main address. The `iplib.IPAddress` class works like `pathlib.Path` in that it accepts both IPV4 and IPV6 addresses, returning an object representing whichever format was used. The module also uses some unit tests, and these will be added more over time as functionality grows and becomes more set in stone.

The module is currently lacking in long-term vision as I used it as a practice project, but there are some plans to further flesh it out. It could incorporate URL support in the future and may be extended with `requests` integration.

This project is not affiliated with `iplib`, the naming similarity is merely a coincidence.
