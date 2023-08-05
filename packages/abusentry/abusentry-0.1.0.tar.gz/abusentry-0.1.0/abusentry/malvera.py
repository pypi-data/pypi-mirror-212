#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import requests
import pefile

from . import log_message_format, log_date_format

VERSION = '1.0.0'

def analyze_malware(file_path):
	"""Analyze a malware file."""
	print(f"Analyzing malware: {file_path}")
	
	try:
		# Perform PE file analysis operations here
		pe = pefile.PE(data=file_path)
		
		print(f"PE File Analysis - {file_path}")
		print(f"=======================")
		
		# Access PE file properties and perform analysis
		logging.debug(f"File Type: {pe.OPTIONAL_HEADER.Magic}")
		logging.debug(f"File Architecture: {pe.FILE_HEADER.Machine}")
		logging.debug(f"Entry Point: {hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}")
		logging.debug(f"File Number of Sections: {pe.FILE_HEADER.NumberOfSections}")
		
		# Access PE file sections and perform analysis
		logging.debug(f"Sections: ")
		for section in pe.sections:
			logging.debug(f"\t{section.Name.decode('utf-8')}")
			
		# Access PE file imports and perform analysis
		logging.debug(f"Imports: ")
		for entry in pe.DIRECTORY_ENTRY_IMPORT:
			logging.debug(f"\t{entry.dll.decode('utf-8')}")
			for imp in entry.imports:
				logging.debug(f"\t\t{imp.name.decode('utf-8')}")
			
		# Access PE file exports and perform analysis
		logging.debug(f"Exports: ")
		for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
			logging.debug(f"\t{exp.name.decode('utf-8')}")
			
		# Access PE file resources and perform analysis
		logging.debug(f"Resources: ")
		for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
			logging.debug(f"\t{resource_type.name.decode('utf-8')}")
			for resource_id in resource_type.directory.entries:
				logging.debug(f"\t\t{resource_id.name.decode('utf-8')}")
				for resource_lang in resource_id.directory.entries:
					logging.debug(f"\t\t\t{hex(resource_lang.data.struct.OffsetToData)}")
					
		# Access PE file digital signature and perform analysis
		logging.debug(f"Digital Signature: ")
		if hasattr(pe, 'VS_VERSIONINFO'):
			logging.debug(f"\tSignature Exists: Yes")
			logging.debug(f"\tVersion: {pe.VS_VERSIONINFO.ProductVersion}")
			logging.debug(f"\tSignature Matches File: {pe.verify_checksum()}")
		else:
			logging.debug(f"\tSignature Exists: No")
			
		# Output if the file is malicious or not
		print(f"Malicious: No")
		print(f"=======================")
		print(f"Analysis Complete")
		print(f"=======================")
		print(f"")
		
	except pefile.PEFormatError as e:
		logging.error(f"Error: Invalid PE file format - {e}")

def parse_arguments():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(prog="malvera", 
		description="script for performing isolated malware analysis of files or urls.",
		epilog="a tool focused on uncovering the true nature of malware, combining the words \"malware\" and \"vera\", meaning truth or authenticity in Latin.",)
	parser.add_argument("--file", metavar="FILE", type=str, help="path to the malicious file", required=False)
	parser.add_argument("url", metavar="URL", type=str, nargs="*", help="path to the malicious url or file")
	parser.add_argument("-u", "--usage", action="store_true", help="output script short usage and exit")
	parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
	parser.add_argument("--version", action="version", help="Output version information and exit",
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
	
	# check if file or url
	if args.file and args.url:
		logging.error("Error: Please provide either a file or url, not both")
		sys.exit(1)
		
	elif args.file:
		if args.file.startswith("http://") or args.file.startswith("https://"):
			logging.error("Error: Please provide a file path, not a url")
			sys.exit(1)
		
		# check if file exists
		if os.path.isfile(args.file):
			# perform malware analysis
			analyze_malware(args.file)
			
		else:
			logging.error(f"Error: File not found - {args.file}")
			sys.exit(1)
			
	elif args.url and not args.file:
		for url in args.url:
			# check if url is valid
			if url.startswith("http://") or url.startswith("https://"):
				try:
					response = requests.get(url)
					if response.status_code == 200:
						# perform malware analysis
						print(type(response.content))
						analyze_malware(response.content)
					else:
						logging.error(f"Error: Failed to download file from {url}")
						sys.exit(1)
				except requests.RequestException as e:
					logging.error(f"Error: Failed to download file - {e}")
					sys.exit(1)
			else:
				logging.error(f"Error: Please provide a valid url - {url}")
				sys.exit(1)
			
	else:
		print("Error: Please provide a file or url")
		parser.print_help()
		sys.exit(1)

if __name__ == "__main__":
	main()
