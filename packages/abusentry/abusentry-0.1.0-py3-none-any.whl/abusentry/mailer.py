#!/usr/bin/env python3

import logging
import argparse
import pyfiglet
from colorama import Fore, Back, Style
import random

from . import log_message_format, log_date_format, fg_colors, bg_colors
from .utils import clear, input_multiline, graceful_exit

__script_name__ = "mailer"
__version__ = "1.0.0"
__description__ = ""
__banner__ = pyfiglet.figlet_format(__script_name__, font="larry3d")

"""
from html.parser import HTMLParser
from urllib.parse import unquote

text = re.sub(r'=[\n\r]([ \t]+)?', '', text) '=\n' => ''
# https://stackoverflow.com/questions/2774471/what-is-c2-a0-in-mime-encoded-quoted-printable-text
text = re.sub(r'=([A-Z0-9]{2})', '%\g<1>', text) # '=3D' => '%3D'
for match in list(set(re.findall(r'%[A-Z0-9]{2}', text))):
        #text = re.sub(match, h.unescape(match), text)
        text = re.sub(match, unquote(match), text) # '%3D' => '='

# https://stackoverflow.com/questions/43824650/encoding-issue-decode-quoted-printable-string-in-python
import quopri
mystring = '=C3=A9'
decoded_string = quopri.decodestring(mystring).decode('utf-8', 'ignore')
for m in list(set(re.findall(r'(=[A-Z0-9]{2})', decoded_string))):
	mm = re.sub(r'=([A-Z0-9]{2})', '%\g<1>', m)
        if mm != '=':
            value = unquote(mm)
	    if value:
	    	decoded_string = re.sub(m, value, decoded_string)

#print(decoded_string.decode('utf-8'))
"""

def setup_logging(args):
	"""Setup logging.
	
	Args:
		args: command line arguments
		
	Returns:
		None
	"""
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(level=logging_level, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
	return

def parse_arguments():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(prog=__script_name__, description=__description__)
	# primary args
	parser.add_argument("input", metavar="INPUT", nargs="*", help="input text to parse")
	# optional args
	parser.add_argument("-i", "--interactive", action="store_true", help="run script in interactive mode")
	# common args
	parser.add_argument("-u", "--usage", action="store_true", help="output script short usage and exit")
	parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
	parser.add_argument("--version", action="version", help="output version information and exit", version="%(prog)s (version {version})".format(version=__version__))
	# compile args
	args, unknown_args = parser.parse_known_args()

	# setup logging
	setup_logging(args)

	# check for input text
	if not args.interactive and not args.input:
		logging.error("no input text provided")
		logging.error("try '{prog} --help' or '{prog} --usage' for more information".format(prog=parser.prog))
		exit(1)

	return parser, args, unknown_args

def print_banner():
	width = max([len(l) for l in __banner__.splitlines()])
	print(random.choice(colors), end="")
	print(__banner__)
	print(Style.RESET_ALL, end="")
	print('-' * width)

def print_results(text):
	pass

def interactive_mode():
	# register SIGINT signal handler
	graceful_exit()
	
	# inf prompt
	while True:
		print_banner()
		print(f"Description: {__description__}")
		print(f"Interactive Mode: {Fore.GREEN}Enabled{Fore.RESET}")
		print()
		
		if input_multiline(prompt="> ") is None:
			break

def main():
	"""Main function."""
	parser, args = parse_arguments()

	# print short usage and exit
	if args.usage:
		parser.print_usage()
		exit(0)
	
	if args.interactive:
		clear()
		print_banner()

	# jump into interactive mode if enabled
	if args.interactive:
		interactive_mode()
		exit(0)

	# handle no input text provided
	if not args.input:
		logging.error("no input text provided")
		logging.error("try '{prog} --help' or '{prog} --usage' for more information".format(prog=parser.prog))
		exit(1)


if __name__ == "__main__":
	main()
