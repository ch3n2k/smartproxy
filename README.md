smartproxy
==========

smartproxy is a relay socks5 server that only relay the requests whose destination IP is not in China. For other requests, go directly to the destination.

## Usage

1. modify config.py for parent proxy, listening port
2. run smartsocksd.py
