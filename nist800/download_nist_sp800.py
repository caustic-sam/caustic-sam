import os
import re
import logging


import requests
from bs4 import BeautifulSoup

from requests.exceptions import RequestException

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        logging.info(f"Successfully downloaded: {local_filename}")
        return local_filename
    except RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
        return None

def get_sp800_publications():
    base_url = "https://csrc.nist.gov/publications/sp800"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        publications = []
        for link in soup.find_all('a', href=re.compile(r'/publications/detail/sp/800-')):
            publications.append("https://csrc.nist.gov" + link['href'])
        
        logging.info(f"Found {len(publications)} SP-800 publications")
        return publications
    except RequestException as e:
        logging.error(f"Error fetching SP-800 publications list: {e}")
        return []

def download_publications(publications):
    for pub_url in publications:
        try:
            response = requests.get(pub_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            pdf_link = soup.find('a', href=re.compile(r'\.pdf$'))
            if pdf_link:
                pdf_url = "https://csrc.nist.gov" + pdf_link['href']
                filename = os.path.basename(pdf_url)
                logging.info(f"Attempting to download {filename}...")
                download_file(pdf_url, filename)
            else:
                logging.warning(f"No PDF found for {pub_url}")
        except RequestException as e:
            logging.error(f"Error processing {pub_url}: {e}")

if __name__ == "__main__":
    logging.info("Starting NIST SP-800 publication download script")
    publications = get_sp800_publications()
    if publications:
        download_publications(publications)
    else:
        logging.error("No publications found or error occurred while fetching the list")
    logging.info("Script execution completed")
