#!/usr/bin/env python3

import json
import logging
import argparse
from time import sleep
from urllib.parse import urlencode
import pyfiglet
from colorama import Fore, Back, Style
import requests
import random
import vt

from . import log_message_format, log_date_format
from .utils import (
    fg_color_codes,
    extract_urls,
    graceful_exit,
    input_multiline,
)
from .utils.fangs import defang, refang
from .utils.config import configs


# Globals
__script_name__ = "virustotal"
__version__ = "1.0.0"
__description__ = f"a tool to check url(s) against virustotal"
__epilog__ = "For more information, visit https://github.com/xransum/abusentry"
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
    parser.add_argument("url", metavar="URL", nargs="*", help="input URL(s)")
    # optional args
    parser.add_argument("--apikey", choices=["add", "remove", "list"], help="virustotal api key")
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
        print(json.dumps(results, indent=4))
    else:
        for url, scan in results:
            print(f"> {url}")
            # VT: <url> - 0 hits
            # VT: <url> - 54 hits (34 Malicious, 20 Suspicious) - 10 Malware, 5 Phishing, 2 Malicious, 1 Suspicious, 1 Unrated
            
            one_line_results = [f"VT: https://www.virustotal.com/gui/url/{scan.id.split('-')[1]}"]
            malicious_hits = [(k, v) for k, v in scan.results.items() if v['category'] == 'malicious']
            suspicious_hits = [(k, v) for k, v in scan.results.items() if v['category'] == 'suspicious']
            hits_categories = list(set([v['category'] for _, v in [*malicious_hits, *suspicious_hits]]))
            hits_count = len(malicious_hits)+len(suspicious_hits)
            hit_types = list(set([v['result'].capitalize() for _, v in [*malicious_hits, *suspicious_hits]]))
            
            one_line_results.append(f' - {hits_count} hits')
            if hits_count > 0:
                types_segs = []
                
                if malicious_hits:
                    types_segs.append(f'{len(malicious_hits)} Malicious')
                    
                if suspicious_hits:
                    types_segs.append(f'{len(suspicious_hits)} Suspicious')
                    
                one_line_results.append(f' ({", ".join(types_segs)})')
                one_line_results.append(f' - {", ".join(hit_types)}')
                
            print(''.join(one_line_results))
            
            for category in hits_categories:
                logging.debug(f'    {category.capitalize()} Hits:')
                for k, v in scan.results.items():
                    if v['category'] == category:
                        logging.debug(f'        {k}: {v["result"]}')
                        
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
    
    urls = extract_urls(cleaned)
    logging.debug(f"Extracted {len(urls)} url(s) from refanged text.")
    
    with vt.Client(global_config.get('virustotal_api_key')) as client:
        results = []
        for url in urls:
            scan = client.scan_url(url, wait_for_completion=True)
            results.append(
                (url, scan),
            )
            
    print_results(results)
# end action

def apikey_handle(args):
    """Handle the apikey argument."""
    
    if args.apikey == "add":
        if global_config.get('virustotal_api_key'):
            print("An API key already exists. Remove it first, use '--apikey remove'.")
        else:
            api_key = input("Enter the API key: ")
            global_config.set('virustotal_api_key', api_key)
            print("API key added.")
        
    elif args.apikey == "remove":
        if global_config.get('virustotal_api_key'):
            global_config.set('virustotal_api_key', None)
            print("API key removed.")
        else:
            print("No API key exists.")
        
    elif args.apikey == "list":
        if global_config.get('virustotal_api_key'):
            print("API key exists.")
        else:
            print("No API key exists.")
    else:
        print("Invalid argument.")
        
    return
# end apikey_handle

# main function
def main():
    """Main function."""
    parser, args, unknown_args = parse_arguments()
    
    # abrubt exit args
    if args.usage:
        parser.print_usage()
        exit(0)
    
    if args.apikey:
        apikey_handle(args)
        
    # jump into interactive mode, when enabled
    elif args.interactive:
        interactive_mode(action)
        
    # no positional args given
    elif len(args.url) == 0:
        # logging.error("no ip address(es) specified")
        logging.error(f"try '{__script_name__} --help' or '{__script_name__} --usage' for more information")
        exit(1)
        
    # handle positional args
    else:
        action(args.url)
        
    exit(0)

# do main
if __name__ == "__main__":
    main()
