import logging
import ipaddress
import dns.inet
from ipwhois import IPWhois
import requests
from datetime import datetime

from .exceptions import InvalidIpAddress, NoIpWhoisInfo


# check if a given ip addr is a valid ipv4 or ipv6 addr
def is_valid_ip_addr(ipaddr, keys=('ipv4', 'ipv6')):
    
    try:
        # primary validation of ip addr
        ip = ipaddress.ip_address(ipaddr)
        if type(ip) is ipaddress.IPv4Address or type(ip) is ipaddress.IPv6Address:
            return True
            
        # secondary validation of ip addr
        try:
            af = dns.inet.af_for_address(ipaddr)
            return keys[af == dns.inet.AF_INET]
        
        except dns.exception.SyntaxError as e:
            raise InvalidIpAddress(e)
            
    except (ValueError, InvalidIpAddress):
        logging.debug(f"IP address is not valid for {ipaddr}.")

# get ip whois information for a valid ip addr
def get_ip_whois(ipaddr):
    try:
        ipw = IPWhois(ipaddr)
        results = ipw.lookup_rdap()
        
        if not results:
            raise NoIpWhoisInfo
            
        return results
        
    except (ValueError, NoIpWhoisInfo):
        logging.error(f"Failed to retreive IP whois for {ipaddr}")

# check if ip addr is a tor node
def check_ip_for_tor_node(ipaddr, ip='1.1.1.1'):
    if not is_valid_ip_addr(ipaddr):
        return None
        
    res = requests.get(f"https://check.torproject.org/cgi-bin/TorBulkExitList.py?", params={'ip': ip})
    if res.status_code == 200:
        tor_list = [ip for ip in res.text.splitlines() if ip]
        return ipaddr in tor_list
    else:
        return False

# SITE DEPRECATED - https://www.sitelike.org/similar/badips.com/
def get_ip_is_bad(ipaddr):
    if not is_valid_ip_addr(ipaddr):
        return None
        
    res = requests.get(f'https://www.badips.com/get/info/{ipaddr}', timeout=10)
    if res.status_code == 200:
        results = res.json()
        return results
    else:
        return None
