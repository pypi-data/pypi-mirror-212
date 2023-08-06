

class InvalidDomain(Exception):
    """Raised if the domain is invalid."""

class InvalidIpAddress(Exception):
    """Raised if the IP address is invalid."""

class NoIpWhoisInfo(Exception):
    """Raised if no IP Whois was found."""    

class NoDNSRecords(Exception):
    """Raised if no DNS record was found."""

class GracefulInterrupt(EOFError):
	"""Raised during a SIGINT interrupt."""
