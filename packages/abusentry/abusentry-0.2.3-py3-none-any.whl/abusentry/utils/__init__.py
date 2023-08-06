import logging
from colorama import Fore, Back, Style
import re
from os import system, name
import signal

from .exceptions import GracefulInterrupt


__all__ = [
    'fg_color_codes', 'bg_color_codes',
    'RE_URL', 'RE_DOMAIN', 'RE_EMAIL_ADDR', 'RE_IPV4_ADDR', 'RE_IPV6_ADDR',
    'extract_urls', 'extract_domains', 'extract_emails', 'extract_ipv4', 'extract_ipv6',
    'clear',
    'graceful_exit',
    'input_multiline',
    'GracefulInterruptHandler',
]

logger = logging.getLogger(__name__)

# non-transparent, dark, and light colors
fg_color_codes = [v for k, v in Fore.__dict__.items() if not 'BLACK' in k or 'WHITE' in k or 'RESET' in k]
bg_color_codes = [v for k, v in Back.__dict__.items() if not 'BLACK' in k or 'WHITE' in k or 'RESET' in k]


# text extracts
RE_URL = re.compile(r"(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])", re.I|re.M)
RE_DOMAIN = re.compile(r"((((?!-))[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63})\b", re.I|re.M)
RE_EMAIL_ADDR = re.compile(r"([a-zA-Z0-9._-]+@((((?!-))[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}))", re.I|re.M)
RE_IPV4_ADDR = re.compile(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", re.I|re.M)
RE_IPV6_ADDR = re.compile(r"(?<![:.\w])(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}(?![:.\w])", re.I|re.M)

def _extract(texts, pattern, unique=False):
    if type(texts) is str:
        texts = [texts]
    
    results = []
    for text in texts:
        for value in pattern.findall(text):
            # skip any empty values or objects
            if not value:
                continue
            # use first item if type list or tuple
            elif type(value) in [list, tuple]:
                value = value[0]
                
            results.append(value)
            
    if unique:
        results = list(set(results))
        
    return results

def extract_urls(text, unique=False):
    """Extracts URLs from a given text."""
    return _extract(text, RE_URL, unique=unique)

def extract_domains(text, unique=False):
    """Extracts domains from a given text."""
    return _extract(text, RE_DOMAIN, unique=unique)

def extract_emails(text, unique=False):
    """Extracts emails from a given text."""
    return _extract(text, RE_EMAIL, unique=unique)


def extract_ip_addrs(text, unique=False):
    """Extracts IPv4/6 addresses from a given text."""
    
    values = [*extract_ipv4(text), *extract_ipv6(text),]
    if unique:
        values = list(set(values))
        
    return values

def extract_ipv4(text, unique=False):
    """Extracts IPv4 addresses from a given text."""
    values = _extract(text, RE_IPV4_ADDR, unique=unique)
    if unique:
        values = list(set(values))
    return values

def extract_ipv6(text, unique=False):
    """Extracts IPv6 addresses from a given text."""
    values = _extract(text, RE_IPV6_ADDR, unique=unique)
    if unique:
        values = list(set(values))
    return values


# clear terminal using shell command
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
        
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# capture safeexit on CTRL+c
def graceful_exit():
    # callback function called when SIGINT is received
    def handler(signal_received, frame):
        # Handle any cleanup here
        logger.info("Exiting...")
        exit(0)
        
    # register handler for signal
    signal.signal(signal.SIGINT, handler)

# allow from multi-line inputs, with optional per-line callbacks
def input_multiline(prompt='', callback=None, *args, **kwargs):
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    
    while True:
        try:
            line = input(prompt)
            
            if not callback is None:
                _ = callback(line, *args, **kwargs)
                
            contents.append(line)
            
        # catch Ctrl-D or Ctrl-Z
        except EOFError:
            return None
            
    return '\n'.join(contents)


class GracefulInterruptHandler(object):
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig
        
    def __enter__(self):
        self.interrupted = False
        self.released = False
        self.original_handler = signal.getsignal(self.sig)
        
        def handler(signum, frame):
            self.release()
            self.interrupted = True
            
        signal.signal(self.sig, handler)
        return self
        
    def __exit__(self, type, value, tb):
        self.release()
        
    def release(self):
        if self.released:
            return False
            
        signal.signal(self.sig, self.original_handler)
        self.released = True
        return True
