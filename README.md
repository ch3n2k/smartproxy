smartproxy
==========

smartproxy is a relay socks5 server that only relay the requests whose destination IP is not in China. For other requests, go directly to the destination.

Usage

modify config.py for parent proxy, listening port
run smartsocksd.py
