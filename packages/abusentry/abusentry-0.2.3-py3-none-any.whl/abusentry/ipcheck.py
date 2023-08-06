#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import random
import json
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network, summarize_address_range

from . import log_message_format, log_date_format
from .utils import (
    fg_color_codes,
    extract_ip_addrs,
    extract_ipv4,
    extract_ipv6,
    graceful_exit,
    input_multiline,
)
from .utils.fangs import defang, refang
from .utils.dns import get_dns_records
from .utils.ipaddr import get_ip_whois, check_ip_for_tor_node
from .utils.config import configs

# Globals
__script_name__ = "ipcheck"
__version__ = "1.0.0"
__description__ = f"a tool for retrieving ip info a ip address(es)"
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
    """Parse command line arguments."""
    global parser, args, unknown_args
    
    parser = argparse.ArgumentParser(prog=__script_name__, description=__description__)
    # primary args
    parser.add_argument("ipaddr", metavar="IPADDR", nargs="*", help="input ip address(es)")
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

def print_results(results):
    """Print the results to the terminal."""
    global parser, args, unknown_args
    
    if args.json:
        print(json.dumps([{'ipaddr': ipaddr, 'records': [{'type': record_type, 'value': answer} \
                for record_type, answer in records], 'whois': whois} \
                    for ipaddr, records, whois, tor_node in results]))
        
    else:
        for r in range(len(results)):
            ipaddr, records, whois, tor_node = results[r]
            
            rtpad = max([*[len(rt) for rt, a in records], len('TOR NODE')]) + 5
            
            print(f"> {ipaddr}")
            if len(records) == 0:
                print(indent(1) + f"[{ 'ERR'.ljust(rtpad) }] No records found.")
                continue
                
            for record_type, answer in records:
                print(indent(1) + f"[{ record_type.ljust(rtpad) }]: {answer}")
                
            print(indent(1) + f"[{ 'TOR NODES'.ljust(rtpad) }]: {'ACTIVE' if tor_node else 'NO ACTIVE'}")
            
            # this whois info will get updated to provide way more advanced output
            print(indent(1) + f"[{ 'NETWORK INFO'.ljust(rtpad) }]:")
            
            nets = whois['nets']
            for n in range(len(nets)):
                net = nets[n]
                print(indent(2) + f"Network {n+1}:")
                
                print(indent(3) + f"Name:      {net['name']}")
                print(indent(3) + f"CIDR:      {net['cidr']}")
                print(indent(3) + f"Net Range: {net['range']}")
                print(indent(3) + f"Location:  {net['country']}")
                address = net['address'].replace('\n', ' ')
                print(indent(3) + f"Location:  {address}. {net['city'].title()}, {net['state']} {net['postal_code']}")
                
                print(indent(3) + "Emails: ")
                for email in sorted(net['emails']):
                    print(indent(4) + f"  {email}")
                    
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
    
    ipaddrs = extract_ip_addrs(cleaned) # ipv4/ipv6
    logging.debug(f"Extracted {len(ipaddrs)} ip address(es) from refanged text.")
    
    results = []
    for ipaddr in ipaddrs:
        logging.debug(f"Retrieving IP info for {ipaddr}.")
        
        records = get_dns_records(ipaddr)
        ip_whois = get_ip_whois(ipaddr)
        tor_node = check_ip_for_tor_node(ipaddr)
        
        results.append(
            (ipaddr, records, ip_whois, tor_node),
        )
        
    print_results(results)
    return
# end action

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
    elif len(args.ipaddr) == 0:
        # logging.error("no ip address(es) specified")
        logging.error(f"try '{__script_name__} --help' or '{__script_name__} --usage' for more information")
        exit(1)
        
    # handle positional args
    else:
        action(args.ipaddr)
        
    exit(0)

# do main
if __name__ == "__main__":
    main()
