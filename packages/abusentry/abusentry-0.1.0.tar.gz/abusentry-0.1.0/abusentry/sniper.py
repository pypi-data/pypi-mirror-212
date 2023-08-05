#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import random
import json
from inspect import isclass
from urllib.parse import urlparse, urlunparse, urljoin

from . import log_message_format, log_date_format
from .utils import (
    fg_color_codes,
    extract_ip_addrs,
    extract_urls,
    graceful_exit,
    input_multiline,
)
from .utils.fangs import defang, refang
from .utils.dns import get_dns_records
from .utils.ipaddr import get_ip_whois, check_ip_for_tor_node
from .utils.http import (
    get_analyzed_request,
    get_http_version,
    filter_headers,
    check_content_is_dead,
)
from .utils.config import configs


# Globals
__script_name__ = "sniper"
__version__ = "1.0.0"
__description__ = f"a tool checking url(s) content status and aliveness integrity"
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
        # The response object requires some major cleaning to not accidently
        # return any PAI/PII/Illegal content. Though, should be gucci since request
        # is a stream, content is never downloaded unless we want it to be.
        data = []
        for url, request_chain in results:
            obj = {'url': url, 'results': []}
            for request in request_chain:
                res = {}
                # clean all values and 
                for key, value in request['response'].__dict__.copy().items():
                    # stringify any value that is a class
                    if isclass(value):
                        value = str(value)
                    
                    # removing leading "_" for some keys like "_content"
                    if key.startswith('_'):
                        key = key[1:]
                        
                    res[key] = value
                
                # double verify the original response is nuked
                del request['response']
                
                # create a copy of the result and add the 
                # cleaned request.Response.
                obbj = request.copy()
                obbj['response'] = res
                
        # stringy data
        data_str = json.dumps([{'url': url, 'results': request_chain} for url, request_chain in results])
        print(data_str)
    else:
        for r in range(len(results)):
            url, request_chain = results[r]
            
            print(f"> {url}")
            
            for r in range(len(request_chain)):
                request = request_chain[r]
                response = request['response']
                
                # determine if redirected and by how
                redirected = False
                redirect_type = None
                
                # anything not the last item has to be a redirect
                if r != len(request_chain) - 1:
                    redirected = True
                    
                    # Determine type of redirect
                    client_side_redirect = request['client_redirect']
                    if bool(client_side_redirect):
                        redirect_type = request['client_redirect_type']

                    else:
                        # don't need this, server-side redirects are known by status codes
                        #redirect_type = 'Server-side'
                        pass
                    
                # don't double print queried URL
                if r != 0:
                    if redirected:
                        print(f">> Redirect: {request['url']}")
                    else:
                        print(f">> {request['url']}")
                
                # do nothing we already printed it
                else:
                    pass
                
                # make http version pretty like curl
                http_version = get_http_version(response.raw.version)
                
                print(f"   {http_version} - {response.status_code} - {response.reason}", end="")
                if redirected:
                    print(f" ({redirect_type})")
                else:
                    print()
                        
                
                # filter for only necessary headers
                # TODO: Allow passing of custom args for header fields like [-x "Host: abcde"]
                headers = filter_headers(response.headers, keys=[])
                
                # print headers
                for key, value in headers.items():
                    print(f"   {key}: {value}")
                
                # print the results of whether the response text is down or not
                print()
                if r == len(request_chain) - 1:
                    down_status, message = check_content_is_dead(response)
                    
                    # set the text accordingly
                    status_text = ''
                    if down_status == True:
                        status_text = f"{Fore.GREEN}Down{Fore.RESET}"
                    elif down_status == False:
                        status_text = f"{Fore.RED}Alive{Fore.RESET}"
                    else:
                        status_text = f"{Fore.BLUE}Unknown{Fore.RESET}"
                    
                    # print status
                    print(f"   Content status: {status_text}")
                    if message:
                        print(f"   ** {message} **")
                        
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
    
    urls = extract_urls(cleaned)
    logging.debug(f"Extracted {len(urls)} url(s) from refanged text.")
    
    results = []
    for url in urls:
        redirect_chains = get_analyzed_request(url)
        results.append(
            (url, redirect_chains),
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
