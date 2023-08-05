#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import random
import os

from . import log_message_format, log_date_format
from .utils import (
    fg_color_codes,
)
from .utils.config import configs

# Globals
__script_name__ = "abusentry"
__version__ = "1.0.0"
__description__ = f"helper script for the abusentry toolkit"
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
    # optional args
    parser.add_argument("--list", action="store_true", help="list available tools")
    parser.add_argument("--update", action="store_true", help="check for updates")
    parser.add_argument("--uninstall", action="store_true", help="uninstall abusentry")
    parser.add_argument("--force", action="store_true", help="force action")
    parser.add_argument("--configs", action="store_true", help="configure abusentry")
    
    # common args
    parser.add_argument("-u", "--usage", action="store_true", help="output script short usage and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
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

def get_pip_cmd():
    """Get pip command."""
    # when pip3 is not installed, use python3 -m pip
    PIP_CMD = "pip3"
    if not os.system(PIP_CMD):
        PIP_CMD = "python3 -m pip"
    return PIP_CMD
# end get_pip_cmd

def update(args):
    """Update script."""
    print("Updating abusentry...")
    PIP_CMD = get_pip_cmd()
    UPDATE_CMD = f"{PIP_CMD} install --upgrade abusentry"
    os.system(UPDATE_CMD)
    return
# end update

def uninstall(args):
    """Uninstall script."""
    print("Uninstalling abusentry...")
    PIP_CMD = get_pip_cmd()
    UNINSTALL_CMD = f"{PIP_CMD} uninstall abusentry"
    if args.force:
        UNINSTALL_CMD += " -y"
        
    os.system(UNINSTALL_CMD)
    return
# end uninstall

scripts = [
    "abusentry",
    "dnscheck",
    "ipcheck",
    "sniper",
    "whobe",
    "urlscan",
    "virustotal",
    "unshorten",
]

def get_exec_path(cmd):
    """Get location of executable."""
    return os.popen(f"which {cmd}").read().strip()
# end get_exec_path

def list_tools(args):
    """List available tools."""
    print("Tools available:")
    
    for script in scripts:
        path = get_exec_path(script)
        
        text = f"  - {script}"
        if not path:
            text += " (not installed)"
        
        if __script_name__ in script:
            text += " (this script)"
            
        print(text)
    return
# end list_tools

def handle_configs(unknown_args):
    subparser = argparse.ArgumentParser(prog="abusentry:configs", description="global configs")
    subparser.add_argument("key", choices=["interactive", "verbose", "json", "quiet", "urlscan-apikey", "virustotal-apikey",], help="config key")
    # on,off, or api key
    subparser.add_argument("value", choices=["on", "off"], help="config value")
    subargs = subparser.parse_args(unknown_args)
    
    print(f"Setting {subargs.key} to {subargs.value}...")
    
    if subargs.key in ["interactive", "verbose", "json", "quiet"]:
        if subargs.value not in ["on", "off"]:
            print("Invalid value, must be on or off")
            subparser.print_help()
            exit(1)
        else:
            if subargs.value == "on":
                subargs.value = True
            elif subargs.value == "off":
                subargs.value = False
            else:
                print("Invalid value, must be on or off")
                subparser.print_help()
                exit(1)
                
            global_config.set(subargs.key, subargs.value)
# end handle_configs

# main function
def main():
    """Main function."""
    parser, args, unknown_args = parse_arguments()
    
    # abrubt exit args
    if args.usage:
        parser.print_usage()
        exit(0)
    
    if args.update:
        print_banner(__banner__)
        update(args)
        
    if args.uninstall:
        print_banner(__banner__)
        uninstall(args)
        
    if args.list:
        print_banner(__banner__)
        list_tools(args)
        
    if args.configs:
        handle_configs(unknown_args)
        
    # exit if no args
    if not any([v for k, v in args.__dict__.items() ]):
        parser.print_help()
        
    exit(0)
# end main

# do main
if __name__ == "__main__":
    main()
