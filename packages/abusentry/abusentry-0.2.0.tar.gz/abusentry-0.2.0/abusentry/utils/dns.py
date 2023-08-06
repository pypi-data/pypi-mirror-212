import logging
import ipaddress
import dns.inet
import dns.name
import dns.resolver
import dns.query
import dns.update
import dns.tsig
import dns.tsigkeyring
import dns.rdatatype
import whois
from datetime import timedelta
from inspect import isclass

Timeout = dns.resolver.Timeout

from .ipaddr import is_valid_ip_addr
from .exceptions import NoDNSRecords
from .exceptions import (
    InvalidIpAddress,
)

logger = logging.getLogger(__name__)

DEFAULT_NAMESERVERS = [
    "1.1.1.1", "1.0.0.1",  # Cloudflare
    "8.8.8.8", "8.8.4.4",  # Google
    "9.9.9.9", "149.112.112.112",  # Quad9
    "208.67.222.222", "208.67.220.220",  # OpenDNS
    "8.26.56.26", "8.20.247.20",  # Comodo Secure
    "185.225.168.168", "185.228.169.168",  # CleanBrowsing
    "76.76.19.19", "76.223.122.150",  # Alternate
    "176.103.130.130", "176.103.130.131",  # AdGuard
    "64.6.64.6", "64.6.65.6",  # Verisign
]

DEFAULT_RECORD_TYPES = ["A", "AAAA", "MX", "CNAME", "PTR"]

# check if a given string is a valid record type
def is_valid_record_type(record_type):
    try:
        rdtype = dns.rdatatype.from_text(record_type)
        return rdtype is not None
        
    except dns.rdatatype.UnknownRdatatype:
        logger.error(f"Invalid DNS Record Type: {record_type}")
        return False
# end is_valid_record_type

# get record for a given DNS record type
def get_dns_record(domain, record_type, nameservers=DEFAULT_NAMESERVERS):
    
    # ensure record type string is uppercased
    record_type = record_type.upper()
    
    # check if valid record type is provided
    if not is_valid_record_type(record_type):
        return None
    
    # configure DNS resolver with default name servers
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = nameservers
    resolver.search = []
    
    try:
        # Retrieve DNS records for the domain
        records = resolver.resolve(domain, record_type)  # Example: A record
        
        # raise empty results
        if not records:
            raise NoDNSRecords
        
        logger.debug(f"Resolved {len(records)} {record_type} for {domain}.")
        # Process and return the DNS records
        return [(record.rdtype.name, record.to_text()) for record in records]
        
    except (dns.exception.SyntaxError, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, NoDNSRecords) as e:
        logger.debug(f"No {record_type} record(s) found for {domain}.")
# end get_dns_record

# get reverse dns record for a given ip addr
def get_rdns_record(ipaddr):
    
    # check if ip addr is valid ipv4 or ipv6
    if not is_valid_ip_addr(ipaddr):
        return None
    
    try:
        record = dns.reversename.from_address(ipaddr)
        # raise empty results
        if not record:
            raise InvalidDNSRecord
            
        # Process and return the DNS records
        return [('PTR', record.to_text())]
        
    except (dns.exception.SyntaxError, dns.resolver.NXDOMAIN, NoDNSRecords):
        logger.error(f"No PTR record(s) found for {ipaddr}.")
# end get_rdns_record

# get records for multiple DNS record types, as [(record_type, resolved_to), ...]
def get_dns_records(domain, record_types=DEFAULT_RECORD_TYPES):
    
    logger.debug(f"Fetching DNS records for {domain} - {str(record_types)}.")
    
    records = []
    for record_type in record_types:
        record_type = record_type.upper()
        
        if record_type == 'PTR' and is_valid_ip_addr(domain):
            answers = get_rdns_record(domain)
        else:
            answers = get_dns_record(domain, record_type)
            
        if answers:
            records.extend(answers)
            
    logger.debug(f"Retrieved {len(records)} record(s) for {domain}.")
    return records
# end get_dns_records

# get whois information for a domain
def get_whois(domain):
    w = None
    try:
        w = whois.whois(domain)
        if not w['domain']:
            w = None
    except Exception as e:
        logging.debug(f"Failed to retreive whois data for {domain}")
        logging.debug(str(e))
        
    return w
# end get_whois

# DEPRECATED
def parse_name(fqdn, origin=None):
    """
    Parse a fully qualified domain name into a relative name
    and an origin zone. Please note that the origin return value will
    have a trailing dot.

    :param fqdn: fully qualified domain name (str)
    :param origin: origin zone (optional, str)
    :return: origin, relative name (both dns.name.Name)
    """
    fqdn = dns.name.from_text(fqdn)
    if origin is None:
        origin = dns.resolver.zone_for_name(fqdn)
        rel_name = fqdn.relativize(origin)
    else:
        origin = dns.name.from_text(origin)
        rel_name = fqdn - origin
    return origin, rel_name
# end parse_name

# DEPRECATED
def query_domain(qname, rdtype, origin=None):
    """
    Query the domain for a specific record type.
    :param qname: domain name to query (str)
    :param rdtype: record type to query (str)
    :param origin: origin zone (optional, str)
    :return: list of tuples (record type, record value)
    """
    origin, name = parse_name(qname, origin)
    fqdn = name + origin
    assert fqdn.is_absolute()
    origin_str = str(origin)

    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [*NAMESERVERS, ]
    resolver.search = []
    
    result = []
    try:
        answer = resolver.resolve(fqdn, rdtype)
        result = sorted(list(set([(r.rdtype.name, r.to_text())
                for r in answer if r.to_text()])), key=lambda r: r[-1])
        logger.debug("Query: %s Answer: %s" % (fqdn.to_text(), result))
    except (dns.resolver.Timeout, dns.resolver.NoNameservers):
        # Raised when there is a timeout or no available nameservers
        logger.debug("Timeout when querying for name '%s' in zone '%s' with rdtype '%s'." % (
                       name, origin, rdtype))
    except dns.resolver.NoAnswer:
        # Raised when there is no answer (no record)
        logger.debug("No answer when querying for name '%s' in zone '%s' with rdtype '%s'." % (
                       name, origin, rdtype))
    except dns.resolver.NXDOMAIN:
        # Raised when there is no such domain
        # If we are looking for a PTR record, we can try to resolve the IP address to a name
        if rdtype == 'PTR' and check_ip(fqdn.to_text()):
            return [query_reverse_dns(fqdn.to_text())]
        logger.debug("No such domain '%s' in zone '%s' with rdtype '%s'." % (
                          name, origin, rdtype))
    else:
        # Raised when there is an answer
        logger.debug("Answer for name '%s' in zone '%s' with rdtype '%s'." % (
                         name, origin, rdtype))
        return result
# end query_domain
