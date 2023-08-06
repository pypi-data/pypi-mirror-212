#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import random
import urllib.parse
import base64
import re

from . import log_message_format, log_date_format
from .utils import (
    fg_color_codes,
    graceful_exit,
    input_multiline
)
from .utils.config import configs
from .utils.fangs import defang, refang

# Globals
__script_name__ = "decode"
__version__ = "1.0.0"
__description__ = f"a tool for decoding text"
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
    # TODO: Fix below action choices, it breaks interactive mode.
    parser.add_argument("action", metavar="ACTION", choices=["proofpoint", "url", "safelinks", "unshorten", "base64", "cisco", "unfurl"], help="Choose the action to perform")
    parser.add_argument("text", metavar="TEXT", nargs="*", help="input text")
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

def proofpoint_decoder(result):
    # Implement your ProofPoint decoder logic here
    decoded_text = result  # Placeholder
    return decoded_text

def url_decoder(result):
    # Implement your URL decoder logic here
    decoded_url = urllib.parse.unquote(result)
    return decoded_url

def office_safelinks_decoder(result):
    # Implement your Office SafeLinks decoder logic here
    decoded_url = encoded_url  #result
    return decoded_url

def url_unshortener(result):
    # Implement your URL unshortener logic here
    unshortened_url = result  # Placeholder
    return unshortened_url

def base64_decoder(result):
    # Implement your Base64 decoder logic here
    decoded_text = urllib.b64decode(result).decode('utf-8')
    return decoded_text

def cisco_password7_decoder(result):
    # Implement your Cisco Password 7 decoder logic here
    decoded_password = result  # Placeholder
    return decoded_password

def unfurl_url(result):
    # Implement your URL unfurling logic here
    unfurled_data = result  # Placeholder
    return unfurled_data
    

HEADINGS = {
    'url': 'URL Decoder',
    'proofpoint': 'ProofPoint Decoder',
    'safelinks': 'SafeLinks Decoder',
    'unshorten': 'URL Unshorten Decoder',
    'base64': 'Base64 Decoder',
    'cisco': 'Cisco Password 7 Decoder',
    'unfurl': 'Unfurl Decoder',
}

def print_results(results):
    """Print the results to the terminal."""
    
    global parser, args, unknown_args
    
    for r in range(len(results)):
        uncleaned, result = results[r]
        
        heading = HEADINGS.get(args.action)
        print(f"- {heading} {'-'.rjust(40 - len(heading), '-')}")
        print(result)
        
        if r != len(results) - 1:
            print()
        else:
            print("-"*50)
# end print_results

# main handler
def action(uncleaned):
    if not uncleaned:
        logging.error("No values provided.")
        return None
    elif type(uncleaned) is not list:
        uncleaned = [uncleaned]
    else:
        pass
        
    global parser, args, unknown_args
    
    results = []
    for unclean in uncleaned:
        # we refang twice as some reports could have been defanged
        # twice when being sent to hosting owner.
        cleaned = refang(unclean).strip()
        
        result = None
        if args.action == 'proofpoint':
            result = proofpoint_decoder(cleaned)
        elif args.action == 'url':
            result = url_decoder(cleaned)
        elif args.action == 'safelinks':
            result = office_safelinks_decoder(cleaned)
        elif args.action == 'unshorten':
            result = url_unshortener(cleaned)
        elif args.action == 'base64':
            result = base64_decoder(cleaned)
        elif args.action == 'cisco':
            result = cisco_password7_decoder(cleaned)
        elif args.action == 'unfurl':
            result = unfurl_url(cleaned)
        else:
            pass
            
        results.append(
            (unclean, result),
        )
        
    print_results(results)
# end action

# main function
def main():
    """Main function."""
    parser, args, unknown_args = parse_arguments()
    
    logging.warning("This script is unfinished, we apologize for the inconvenience...")
    
    # abrubt exit args
    if args.usage:
        parser.print_usage()
        exit(0)
        
    # jump into interactive mode, when enabled
    elif args.interactive:
        interactive_mode(action)
        
    # no positional args given
    elif len(args.text) == 0:
        # logging.error("no text specified")
        logging.error(f"try '{__script_name__} --help' or '{__script_name__} --usage' for more information")
        exit(1)
        
    # handle positional args
    else:
        action(args.text)
        
    exit(0)
# end main

# do main
if __name__ == "__main__":
    main()
