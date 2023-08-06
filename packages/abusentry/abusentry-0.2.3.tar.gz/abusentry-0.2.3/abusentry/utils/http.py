import logging
import requests
import urllib3
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
from datetime import datetime

from .dns import get_dns_records


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ACCEPTED_CONTENT_TYPES = ["text/html", "text/xml", "application/json"]
# Usable user agents
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/%s Firefox/77.0' % datetime.now().strftime('%Y%m%d'),
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/%s Firefox/77.0' % datetime.now().strftime('%Y%m%d'),
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
# Default user agent randomly selected from available user-agents
DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"

# Default headers for requests
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': DEFAULT_USER_AGENT,
}

# Common names used for identifying content
CONTENT_NAMES = ["Content", "Page", "Website", "URL", "Resource", "File", "Document", "Image", "Video", "Audio", "Post", "Article", "Blog", "Feed"]

# Common states used for identifying content being down
CONTENT_STATES = ["Down", "Removed", "Deleted", "Not Found", "Unavailable", "Not Available", "Unreachable", "Not Found", "Unavailable"]

# Combine names and states to create down identifiers
CONTENT_DOWN_IDENTIFIERS = [f'{name} {state}' for state in CONTENT_STATES for name in CONTENT_NAMES]


def get_random_user_agent(user_agents=None):
    if not user_agents:
        user_agents = DEFAULT_USER_AGENT
        
    return random.choice(user_agents)
# end get_random_user_agent

def filter_headers(headers, keys=None):
    """
    Filters the headers to only include the given header keys.

    Args:
        headers (dict): The headers to filter.
        keys (list|tuple): The keys to filter for.

    Returns:
        dict: The filtered headers.
    """
    if keys is None:
        return headers
        
    filtered = {}
    for header, value in headers.items():
        for response_header in keys:
            if header.lower() in response_header.lower() or \
                response_header.lower() in header.lower():
                filtered[header] = value
                
    return filtered
# end filter_headers

def get_tls_version(raw_version):
    """
    Given the raw.version, return the HTTP version as decimal string.

    Args:
        version (int): HTTP TLS version.

    Returns:
        str: 1.0, 1.1, 1.2, 1.3, 2.0, etc.
    """
    splits = list(str(raw_version))
    splits.insert(1, '.')
    version = ''.join(splits)
    return version
# end get_tls_version

def get_http_version(raw_version):
    tls_version = get_tls_version(raw_version)
    return f'HTTP/{tls_version}'
# end get_http_version

def check_content_is_dead(response, content_identifiers=None):
    if not content_identifiers:
        content_identifiers = CONTENT_DOWN_IDENTIFIERS
        
    # check page content for signs indicating actually down
    #textual_down = any([name in response.text for name in content_identifiers])
    textual_down = any([re.search(name, response.text, re.I|re.M) for name in content_identifiers])

    down_status = False
    message = None
    if 400 <= response.status_code < 500:
        down_status = True
        
        if not textual_down:
            message = 'Caution: Page content didn\'t align 100% with status code.'
            
    elif 200 <= response.status_code < 300:
        down_status = False
        if textual_down:
            message = 'Page contents indicated content was taken down / removed.'
            down_status = True

    else:
        message = 'Error: Unhandled status codes in <function: check_content_is_dead>'
        
    return down_status, message
# end check_content_is_dead

def extract_html_meta_redirects(soup):
    """Check HTML for meta redirect"""
    redirect = None

    meta_refresh_tag = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if meta_refresh_tag:
        meta_redirect = meta_refresh_tag['content'].split(';url=')[1].strip()

    return redirect
# end extract_html_meta_redirects

def extract_javascript_redirects(soup):
    """Check HTML for JavaScript redirect"""
    redirect = None

    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        if script_tag.string:
            if 'location.href' in script_tag.string:
                href_split = script_tag.string.split('location.href=')
                if len(href_split) > 1:
                    redirect = href_split[1].strip(';"\'')
    return redirect
# end extract_javascript_redirects

def extract_client_side_redirects(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    # Check if the response has a meta or JavaScript redirect
    meta_redirect = extract_html_meta_redirects(soup)
    js_redirect = extract_javascript_redirects(soup)
    redirect_type, redirect = None, None

    # HTML Meta Redirects
    if meta_redirect:
        redirect_type, redirect = 'HTML Meta', meta_redirect

    # JavaScript Redirects
    # TODO: Need to re-evaluate the value that is extracted and look into false positives.
    elif js_redirect:
        #redirect_type, redirect = 'JavaScript', js_redirect
        pass

    # Do nothing
    else:
        pass

    return redirect_type, redirect
# end extract_client_side_redirects

def build_full_url(url, next_url):
    if not next_url:
        next_url = None
    elif next_url.startswith('http'):
        pass
    else:
        next_url = urljoin(url, next_url)
        
    return next_url 
# end build_full_url

def get_analyzed_request(url):
    redirect_chains = []
    current_url = url
    
    session = requests.Session()
    session.allow_redirects = False
    
    while current_url:
        # extract domain from url for dns lookup
        domain = urlparse(current_url).netloc
        
        # inherit records from a matching domain in redirect chain
        dns_records = None
        for d in redirect_chains:
            if d['domain'] == domain:
                logging.debug(f"Assuming DNS records from prior request for {domain}.")
                dns_records = d['dns_records']
                
        # retrieve latest records
        if not dns_records:
            dns_records = get_dns_records(domain)
            
        result = {
            'url': current_url,
            'domain': domain,
            'dns_records': dns_records,
            'response': None,
            'javascript_redirect': None,
            'meta_redirect': None,
            'error': False,
        }
        
        if not dns_records:
            result['error'] = 'No DNS Records'
            
        try:
            
            # request headers with spoofed user-agent
            headers = {
                **DEFAULT_REQUEST_HEADERS,
                'User-Agent': get_random_user_agent(), # spoof user-agent on each turn
            }
            
            # Make the request
            response = session.get(current_url, headers=headers, allow_redirects=False, stream=True)
            
            # extract domain from url for dns lookup
            domain = urlparse(current_url).netloc
            
            # inherit records from a matching domain in redirect chain
            dns_records = None
            for d in redirect_chains:
                if d['domain'] == domain:
                    logging.debug(f"Assuming DNS records from prior request for {domain}.")
                    dns_records = d['dns_records']
                    
            # retrieve latest records
            if not dns_records:
                dns_records = get_dns_records(domain)
                
            # Check if the response has a meta or JavaScript redirect
            client_redirect_type, client_redirect =  extract_client_side_redirects(response.text)
            
            # Store the redirect chain and DNS records
            result['response' ] = response
            result['client_redirect'] = client_redirect
            result['client_redirect_type'] = client_redirect_type
            
        except (requests.exceptions.RequestException) as e:
            logging.error(f"An error occurred while fetching URL: {current_url}")
            result['error'] = e
            
        # add result to redirect chain    
        redirect_chains.append(result)
        
        if not result['error']:
            # Check for relative and absolute redirects
            if response.is_redirect:
                next_url = response.headers['Location']
                current_url = build_full_url(response.url, next_url)
                
            else:
                if client_redirect:
                    current_url = build_full_url(current_url, client_redirect)
                else:
                    current_url = None
                    
        # bail when we've run into an issue
        else:
            break
    return redirect_chains
# end get_analyzed_request
