#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import requests
import random

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
__script_name__ = "unshorten"
__version__ = "1.0.0"
__description__ = f"a tool to unshorten shortened url(s)"
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
    parser.add_argument("url", metavar="URL", nargs="*", help="shortened url(s)")
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
        data = json.dumps([{'query': url, 'result': unshortened} for url, unshortened in results])
        print(data)
    else:
        for r in range(len(results)):
            url, unshortened = results[r]
            print(f"> {url}")
            print(f">> {unshortened}")
            
            if r != len(results) - 1:
                print()
            
def get_unshortened_url(url):
    """Get unshortened URL."""
    
    logging.debug(f"Unshortening URL: {url}")
    
    result = None
    try:
        response = requests.get(f"https://unshorten.me/s/{url}")
        if response.status_code == 200:
            result = response.text
            
    except Exception as e:
        logging.error(f"Error unshortening URL: {url}")
        logging.error(e)
    
    return result
# end action

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
    
    results = []
    for url in urls:
        unshortened = get_unshortened_url(url)
        results.append(
            (url, unshortened),
        )
        
    print_results(results)
# end action

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
    elif len(args.url) == 0:
        # logging.error("no domain(s) specified")
        logging.error(f"try '{__script_name__} --help' or '{__script_name__} --usage' for more information")
        exit(1)
        
    # handle positional args
    else:
        action(args.url)
        
    exit(0)
# end main

# do main
if __name__ == "__main__":
    main()
