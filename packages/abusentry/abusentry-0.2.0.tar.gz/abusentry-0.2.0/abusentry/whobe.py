#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import random
import json

from . import log_message_format, log_date_format
from .utils import (
    fg_color_codes,
    extract_domains,
    extract_ip_addrs,
    graceful_exit,
    input_multiline
)
from .utils.config import configs
from .utils.fangs import defang, refang
from .utils.dns import get_whois
from .utils.ipaddr import get_ip_whois, is_valid_ip_addr

# Globals
__script_name__ = "whobe"
__version__ = "1.0.0"
__description__ = f"a tool for getting whois info for domain(s) or ip address(es)"
__banner__ = pyfiglet.figlet_format(__script_name__, font="standard")

global_config = configs()
parser, args, unknown_args = None, None, None

# build logging properties
def setup_logging(args):
    """Setup logging.
    
    Args:
        args: command line arguments
        
    Returns:
        None
    """
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level, format=log_message_format % __script_name__, datefmt=log_date_format)
    return
# end setup_logging

# parse arguments
def parse_arguments():
    global parser, args, unknown_args
    
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(prog=__script_name__, description=__description__)
    # primary args
    parser.add_argument("domain", metavar="DOMAIN", nargs="*", help="input domain(s) or ip address(es)")
    # optional args
    parser.add_argument("-i", "--interactive", action="store_true", help="run script in interactive mode", default=global_config.get('interactive') or False)
    parser.add_argument("--json", action="store_true", help="output in json", default=global_config.get('json') or False)
    parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done", default=global_config.get('verbose') or False)
    parser.add_argument("-q", "--quiet", action="store_true", help="explain what is being done", default=global_config.get('quiet') or False)
    parser.add_argument("-u", "--usage", action="store_true", help="output script short usage and exit")
    parser.add_argument("-V", "--version", action="version", help="output version information and exit", version="%(prog)s (version {version})".format(version=__version__))
    
    # compile args
    args, unknown_args = parser.parse_known_args()

    # setup logging
    setup_logging(args)

    return parser, args, unknown_args
# end parse_arguments

# print script header
def print_banner(banner):
    width = max([len(l) for l in banner.splitlines()])
    print(random.choice(fg_color_codes), end="")
    print(banner)
    print(Style.RESET_ALL, end="")
    print('-' * width)
# end print_banner

# interactive mode usage
def interactive_mode(caller):
    # register SIGINT signal handler
    graceful_exit()
    
    # inf prompt
    while True:
        print_banner(__banner__)
        print(f"Interactive Mode: {Fore.GREEN}Enabled{Fore.RESET}")
        print(f"Description: {__description__}")
        print()
        
        # retrieve user inputs, callback allows for per-line handling
        stdin = input_multiline(prompt="> ", callback=None)
        if stdin is None:
            break
        else:
            caller(stdin)
# end interactive_mode

# easier indent text
def indent(n=0, ind='  '):
    text = ind * n
    return text
# end indent

import ipaddress
whois_excludes = ['status']
def print_results(results):
    """Print the results to the terminal."""
    global parser, args, unknown_args
    
    if args.json:
        print(json.dumps([{'query': query, 'is_ipaddr':is_ipaddr, 'whois': whois} \
                for query, is_ipaddr, whois in results]))
        
    else:
        for r in range(len(results)):
            query, is_ipaddr, whois = results[r]
            #logging.debug(query, is_ipaddr, whois)
            
            print(f"> {query}")
            
            if is_ipaddr:
                nets = whois['nets']
                for n in range(len(nets)):
                    net = nets[n]
                    print(indent(1) + f"Network {n+1}:")
                    
                    print(indent(2) + f"Name:      {net['name']}")
                    print(indent(2) + f"CIDR:      {net['cidr']}")
                    print(indent(2) + f"Net Range: {net['range']}")
                    print(indent(2) + f"Location:  {net['country']}")
                    address = net['address'].replace('\n', ' ')
                    print(indent(2) + f"Location:  {address}. {net['city'].title()}, {net['state']} {net['postal_code']}")
                    
                    print(indent(2) + "Emails: ")
                    for email in sorted(net['emails']):
                        print(indent(3) + f"  {email}")
                        
                    if n != len(nets) - 1:
                        print()
                        
            else:
                if whois:
                    for key in whois_excludes:
                        del whois[key]
                        
                key_names = [(key, ' '.join(key.split('_')).title()) for key in list(whois.keys())]
                key_width = max([len(name) for key, name in key_names])
                
                for key, name in key_names:
                    value = whois[key]
                    name = (name + ":").ljust(key_width + 2)
                    
                    print(indent(1) + f"{name}", end="")
                    
                    if type(value) is list:
                        print()
                        if key == 'emails':
                            value.sort()
                            
                        for sub_value in value:
                            print(indent(2) + f"  {sub_value}")
                    else:
                        print(value)
            
            if r != len(results) - 1:
                print()
# end print_results

# main handler
def action(uncleaned):
    if not uncleaned:
        logging.error("No values provided.")
        return None
    elif type(uncleaned) is list:
        uncleaned = '\n'.join(uncleaned)
    else:
        pass
        
    cleaned = refang(uncleaned)
    logging.debug("Refanged input text passed to action.")
    
    values = list(set([*extract_domains(cleaned), *extract_ip_addrs(cleaned)]))
    logging.debug(f"Extracted {len(values)} domains / ip addresses from refanged text.")
    
    results = []
    for value in values:
        is_ipaddr, whois = False, None
        if is_valid_ip_addr(value):
            logging.debug(f"Retrieving IP Whois for {value}.")
            whois = get_ip_whois(value)
            is_ipaddr = True
            
        else:
            logging.debug(f"Retrieving Whois for {value}.")
            whois = get_whois(value)
            
        results.append(
            (value, is_ipaddr, whois),
        )
        
    print_results(results)
# end action

"""
> 35.165.89.122
  [ Owner]: 
  [ Emails]:
  [Registrar          ]: MarkMonitor, Inc.
  [Registration Date  ]: 2022-10-03 22:00:06
  [Registration Expire]: expiration_date

"emails": [
  "abusecomplaints@markmonitor.com",
  "hostmaster@amazon.com",
  "whoisrequest@markmonitor.com"
],
"dnssec": "unsigned",
"name": "Legal Department",
[ Owner]: "Amazon.com, Inc.",
"address": "PO BOX 81226",
"city": "Seattle",
"state": "WA",
"registrant_postal_code": "98108-1226",
"country": "US"

indent = lambda n:"   "*n

emails = whois["emails"]
if not 'emails' in whois or not emails:
    emails = []
elif type(emails) is str:
    emails = [emails]
else:
    pass

print(indent(1) + f"Organization: {whois['org']}")
print(indent(1) + f"Registrar: {whois['registrar']}")
print(indent(1) + "Registration:")
print(indent(2) + f"Created On: {whois['creation_date']}")
print(indent(2) + f"Last Updated: {whois['updated_date'][0] if whois['updated_date'] else 'Unknown'}")
print(indent(2) + f"Expiration: {whois['expiration_date'][0] if whois['expiration_date'] else 'Unknown'}")

print(indent(1) + "Emails:")
for email in emails:
    print(indent(2) + f"- {email}")

print(indent(1) + f"Address: {whois['address']}. {whois['city']}, {whois['state']} {whois['registrant_postal_code']}")
print(indent(1) + "Name Servers:")
for ns in whois['name_servers']:
    print(indent(2) + f"- {ns}")

"""

# main function
def main():
    """Main function."""
    parser, args, unknown_args = parse_arguments()
    
    # abrubt exit args
    if args.usage:
        parser.print_usage()
        exit(0)
        
    # jump into interactive mode, when enabled
    elif args.interactive:
        interactive_mode(action)
        
    # no positional args given
    elif len(args.domain) == 0:
        # logging.error("no domain(s) specified")
        logging.error(f"try '{__script_name__} --help' or '{__script_name__} --usage' for more information")
        exit(1)
        
    # handle positional args
    else:
        action(args.domain)
        
    exit(0)
# end main

# do main
if __name__ == "__main__":
    main()
