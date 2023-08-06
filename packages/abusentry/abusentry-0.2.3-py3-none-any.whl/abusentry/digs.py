#!/usr/bin/env python3

import logging
import argparse
import signal
import re
import random
import pyfiglet
from colorama import Fore, Back, Style

from . import log_message_format, log_date_format, fg_colors, bg_colors
from .utils import clear, input_multiline, graceful_exit
from .resolver import DEFAULT_RECORD_TYPES, dns_resolve, check_rdtype, validate_record_types


__script_name__ = 'dig'
__version__ = '1.0.0'
__description__ = "Simple domain or IP address lookup of DNS records."
__banner__ = pyfiglet.figlet_format(__script_name__, font='larry3d')


def setup_logging(args):
	"""Setup logging.
	
	Args:
		args: command line arguments
		
	Returns:
		None
	"""
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(level=logging_level, format=log_message_format, datefmt=log_date_format)
	return

def parse_arguments():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(prog=__script_name__, description=__description__)
	# primary args
	parser.add_argument("domains", metavar="DOMAIN", nargs="*", type=str, help="domain/ip address dns lookup")
	# optional args
	parser.add_argument("-t", "--type", metavar="RDTYPE", type=str, help="specific DNS record type")
	parser.add_argument("-i", "--interactive", action="store_true", help="run script in interactive mode")
	# common args
	parser.add_argument("-u", "--usage", action="store_true", help="output script short usage and exit")
	parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
	parser.add_argument("-V", "--version", action="version", help="output version information and exit", version="%(prog)s (version {version})".format(version=__version__))
	# compile args
	args, unknown_args = parser.parse_known_args()

	# setup logging
	setup_logging(args)
	
	return parser, args, unknown_args

def print_banner():
	width = max([len(l) for l in __banner__.splitlines()])
	print(random.choice(fg_colors), end="")
	print(__banner__)
	print(Style.RESET_ALL, end="")
	print('-' * width)

def print_results(domain, record_type, answers):
	"""Print the DNS records for a given domain and record type."""
	rtpad = max([len(r) for r in record_type])

	print(f"> {domain}")
	if len(answers) == 0:
		print(f"[{ 'ERR'.ljust(rtpad) }] No records found.")
	else:
		for rdtype, answer in answers:
			print(f"[{rdtype.ljust(rtpad)}]: {answer}")

def handle_domain(domain, record_types):
	# remove any leading whitespace or trailing newlines
	domain = domain.strip()
	
	# do nothing on empty values
	if not domain:
		return None
		
	# Parse domain argument in case it's a full URL
	if '://' in domain or '/' in domain:
		logging.debug(f"Extracting domain from URL: {url}")
		domain = domain.split('//', 1)[-1].split('/', 1)[0]
		
	logging.debug(f"Domain: {domain}")
	answers = dns_resolve(domain, rdtypes=record_types)
	print_results(domain, record_types, answers)

def handle_domains(domains, record_types):
	# since some shells don't fully interpret new lines when pasting
	domains_list = []
	if type(domains) is str:
		domains_list = [d for d in domains.strip().splitlines()]
		
	# same as above comment, but instead handling all items as such
	elif type(domains) is list:
		for domain in domains:
			for d in domain.strip().splitlines():
				if not d:
					continue
				domains_list.append(d)
				
	# no reason to get here
	else:
		pass
		
	# remove all empty values
	domains_list = [d for d in domains_list if d]
	for domain in domains_list:
		handle_domain(domain, record_types=record_types)

def interactive_mode(record_types):
	# register SIGINT signal handler
	graceful_exit()
	
	# inf prompt
	while True:
		print_banner()
		print(f"Description: {__description__}")
		print(f"Interactive Mode: {Fore.GREEN}Enabled{Fore.RESET}")
		print()
		
		if input_multiline(prompt="Input: ", callback=handle_domains, record_types=record_types) is None:
			break

def main():
	"""Main function."""
	parser, args, unknown_args = parse_arguments()
	
	# print short usage and exit
	if args.usage:
		parser.print_usage()
		exit(0)
	
	# Ensure proper record types are provided
	record_types = validate_record_types(args.type)
	if not record_types:
		record_types = DEFAULT_RECORD_TYPES

	# handle interactive mode
	if args.interactive:
		interactive_mode(record_types=record_types)

	# handle no domains specified outside of interactive mode
	elif len(args.domains) <= 0:
		logging.debug("no domain(s) specified")
		logging.info(f"try '{__script_name__} --help' or '{__script_name__} --usage' for more information")
		parser.print_usage()
		exit(1)

	# handle as cli args
	else:
		handle_domains(args.domains, record_types=record_types)
		
	exit(0)


if __name__ == "__main__":
	main()

