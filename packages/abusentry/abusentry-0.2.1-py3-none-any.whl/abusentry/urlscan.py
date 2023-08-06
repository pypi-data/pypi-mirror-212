#!/usr/bin/env python3

import os
import argparse
import json
import requests
import logging
from urllib.parse import urlparse
from utils import log_message_format, log_date_format, ApiKey

VERSION = '1.0.0'
API_URL = 'https://urlscan.io/api/v1'
API_KEY_FILE = os.path.join(os.path.expanduser('~'), '.urlscan_api_key')

def uri_validator(x):
	try:
		result = urlparse(x)
		return all([result.scheme, result.netloc])
	except:
		return False

def get_scan(url, api_key):
	headers = {'API-Key': api_key, 'Content-Type': 'application/json'}
	data = {"url": url, "visibility": "private"}
	res = requests.post(f'{API_URL}/scan/', headers=headers, data=json.dumps(data))
	results = res.json()

	if 'message' in results:
		logging.error("%s - %s" % (results['message'], results['description']))
		return None

	scan_url = results['api']
	scan = None
	while True:
		res = requests.get(scan_url, headers=headers)
		if res.status_code == 200:
			scan = res.json()
			break

	return scan["result"]

def parse_arguments():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(prog="urlscan", description="Perform URL analysis using the urlscan.io API",)
	parser.add_argument("url", metavar="URL", nargs="*", help="URL(s) to scan")
	parser.add_argument("-k", "--keys", nargs="?", help="manage API keys", choices=["get", "add", "remove"], default=None)
	parser.add_argument("-u", "--usage", action="store_true", help="output script short usage and exit")
	parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
	parser.add_argument("--version", action="version", help="output version information and exit",
						version="%(prog)s (version {version})".format(version=VERSION))
	args = parser.parse_args()
	return parser, args

def main():
	"""Main function."""
	parser, args = parse_arguments()
	
	# print short usage and exit
	if args.usage:
		parser.print_usage()
		exit(0)
	
	# configure logging
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(format=log_message_format, datefmt=log_date_format, level=logging_level)
	
	# Set API key
	api_key = ApiKey(API_KEY_FILE, 'URLSCAN_API_KEY')
	
	# Manage API keys
	if args.keys:
		if args.keys == "add":
			logging.info("Adding API key...")
			# Add API key to environment variable
			if len(args.url) != 1:
				logging.error("You must specify exactly one API key to add")
				exit(1)
				
			api_key.add(args.url[0])
			print("API key added")
			exit(0)
		elif args.keys == "remove":
			logging.info("Removing API key...")
			# Remove API key from environment variable
			api_key.remove()
			print("API key removed")
			exit(0)
		elif args.keys == "get":
			logging.info("Getting API keys...")
			# Get API keys from environment variable
			if not api_key.get():
				logging.error("No API keys found")
				exit(1)
				
			print( api_key.get() )
			exit(0)
			
	# Get URL to scan
	if not args.url:
		parser.print_help()
		exit()
		
	# Check if URL is valid
	for url in args.url:
		if not uri_validator(url):
			logging.error("Invalid URL: %s" % url)
			exit(1)
			
	# Get scan results
	for u in range(len(args.url)):
		url = args.url[u]
		if len(args.url) > 1:
			print("URL: %s" % url)
			
		scan = get_scan(url, API_KEY)
		if not scan:
			logging.error("Failed to get scan results for %s" % url)
			exit(1)
			
		# Print scan results
		print("SS: %s" % scan['page']['url'])
		print()

if __name__ == "__main__":
	main()
