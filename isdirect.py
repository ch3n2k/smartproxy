#!/usr/bin/env python

import sys
import socket
import bisect

def ip2int(ip):
    return reduce(lambda x,y: x*256+y, [int(x) for x in ip.split('.')])

def init_geolite():
    import urllib2
    import zipfile
    import StringIO
    buf = StringIO.StringIO(urllib2.urlopen("http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip").read())
    geolite_begin = []
    geolite_end = []
    for line in zipfile.ZipFile(buf).open('GeoIPCountryWhois.csv').readlines():
        ip_begin, ip_end, int_begin, int_end, code = line.strip().split(',')[0:5] 
        if code == '"CN"':
            geolite_begin.append(int(int_begin[1:-1]))
            geolite_end.append(int(int_end[1:-1]))
    for ip_begin, ip_end in internal_ip:
        ipb = ip2int(ip_begin)
        ipe = ip2int(ip_end)
        i = bisect.bisect(geolite_begin, ipb)
        geolite_begin.insert(i, ipb)
        geolite_end.insert(i, ipe)
    return (geolite_begin, geolite_end)

def ischina(ip_int):
    if geolite:
        i = bisect.bisect_right(geolite[0], ip_int) -1
        if i == 0 or ip_int > geolite[1][i]:
            return False
        else:
            return True
    else:
        return False

def isdirect(hostname):
    hostname = hostname.strip()
    try:
        ip = socket.gethostbyname(hostname)
    except Exception, e:
        ip = "0.0.0.0"
    ip_int = ip2int(ip)
    try:
        is_china = ischina(ip_int)
    except Exception, e:
        is_china = False

    return  is_china and \
            (ip_int not in blacklist_ip) and \
            (not any([hostname.endswith(i) for i in blacklist_domain])) \
            or \
            (any([hostname.endswith(i) for i in whitelist_domain]))

#bad IPs returned by domestic DNS servers
blacklist_ip =[ip2int(ip) for ip in ['0.0.0.0',
    '4.36.66.178', '8.7.198.45', '37.61.54.158', '46.82.174.68',
    '59.24.3.173', '60.191.124.236', '64.33.88.161', '64.33.99.47',
    '64.66.163.251', '65.104.202.252', '65.160.219.113', '66.45.252.237',
    '72.14.205.99', '72.14.205.104', '74.125.39.113', '74.125.127.102',
    '74.125.155.102', '78.16.49.15', '93.46.8.89', '128.121.126.139',
    '159.106.121.75', '169.132.13.103', '180.168.41.175', '192.67.198.6',
    '202.106.1.2', '202.181.7.85', '203.98.7.65', '203.161.230.171',
    '207.12.88.98', '208.56.31.43', '209.36.73.33', '209.85.229.138',
    '209.145.54.50', '209.220.30.174', '211.94.66.147', '213.169.251.35',
    '216.221.188.182', '216.234.179.13', '243.185.187.30', '243.185.187.39',
    '255.255.255.255', '74.125.39.102'
    ]]
#domains hijacked
blacklist_domain = ['skype.com', 'youtube.com']
#private IP ranges
internal_ip = [("127.0.0.0", "127.255.255.255"), ("192.168.0.0", "192.168.255.255"), ("172.16.0.0", "172.31.255.255"), ("10.0.0.0", "10.255.255.255")]
#private domain names
whitelist_domain = ['local', 'localhost' ]

geolite = init_geolite()

if __name__ == "__main__":
    while 1:
        line=sys.stdin.readline()
        if line == "":
            break
        print("OK" if isdirect(line) else "ERR")
        sys.stdout.flush()
