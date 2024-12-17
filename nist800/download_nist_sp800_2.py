import os
import re
import logging

import requests
from bs4 import BeautifulSoup

from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

def get_sp800_publications():
    base_url = "https://csrc.nist.gov/publications/sp800"
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content length: {len(response.content)}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        publications = []
        for link in soup.find_all('a', href=re.compile(r'/publications/detail/sp/800-')):
            publications.append("https://csrc.nist.gov" + link['href'])
        
        logging.info(f"Found {len(publications)} SP-800 publications")
        if len(publications) == 0:
            logging.warning(f"HTML content: {soup.prettify()[:500]}...")  # Log first 500 characters of HTML
        return publications
    except RequestException as e:
        logging.error(f"Error fetching SP-800 publications list: {e}")
        return []

if __name__ == "__main__":
    logging.info("Starting NIST SP-800 publication download script")
    publications = get_sp800_publications()
    if publications:
        logging.info(f"First few publications: {publications[:5]}")
    else:
        logging.error("No publications found or error occurred while fetching the list")
    logging.info("Script execution completed")
