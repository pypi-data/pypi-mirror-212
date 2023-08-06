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
from .utils.fangs import defang, refang
from .utils.dns import get_dns_records
from .utils.config import configs

# Globals
__script_name__ = "dnscheck"
__version__ = "1.0.0"
__description__ = f"a tool for retrieve dns records for a domain(s)"
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
    parser.add_argument("domain", metavar="DOMAIN", nargs="*", help="input domain(s)")
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

def print_results(results):
    """Print the results to the terminal."""
    global parser, args, unknown_args
    
    if args.json:
        print(json.dumps([{'domain': domain, 'records': [{'type': record_type, 'value': answer} \
                for record_type, answer in records]} \
                    for domain, records in results]))
        
    else:
        for r in range(len(results)):
            domain, records = results[r]
            rtpad = max([len(rt) for rt, a in records])
            
            print(f"> {domain}")
            if len(records) == 0:
                print(f"[{ 'ERR'.ljust(rtpad) }] No records found.")
                continue
                
            for record_type, answer in records:
                print(f"[{ record_type.ljust(rtpad) }]: {answer}")
                
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
    
    domains = extract_domains(cleaned)
    if domains:
        logging.debug(f"Extracted {len(domains)} domains(s) from refanged text.")
    else:
        domains = extract_ip_addrs(cleaned) # ipv4/ipv6
        if domains:
            logging.debug(f"Extracted {len(domains)} ip address(es) from refanged text.")
            
    results = []
    for domain in domains:
        logging.debug(f"Retrieving DNS records for {domain}.")
        
        records = get_dns_records(domain)
        results.append(
            (domain, records),
        )
        
    print_results(results)
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
