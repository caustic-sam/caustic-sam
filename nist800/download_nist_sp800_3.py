import requests
from bs4 import BeautifulSoup
import re
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_sp800_publications():
    url = "https://csrc.nist.gov/publications/sp800"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        logging.info(f"Attempting to fetch SP 800 publications list from {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        publications = []
        
        # Find the link to the SP 800 publications page
        sp800_link = soup.find('a', id='quick-link-sp-800-lg')
        if sp800_link:
            sp800_url = "https://csrc.nist.gov" + sp800_link['href']
            logging.info(f"Fetching SP 800 publications from: {sp800_url}")
            sp800_response = requests.get(sp800_url, headers=headers)
            sp800_response.raise_for_status()
            sp800_soup = BeautifulSoup(sp800_response.content, 'html.parser')
            
            # Extract publication numbers from the SP 800 page
            for link in sp800_soup.find_all('a', href=re.compile(r'/publications/detail/sp/800-')):
                pub_number = re.search(r'800-(\d+)', link['href'])
                if pub_number:
                    publications.append(pub_number.group(1))
        
        logging.info(f"Found {len(publications)} SP-800 publications")
        return publications
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching SP-800 publications list: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error in get_sp800_publications: {e}")
        return []

def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        logging.info(f"Successfully downloaded: {local_filename}")
        return local_filename
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
        return None

def download_sp800_publications():
    publications = get_sp800_publications()
    if not publications:
        logging.error("No publications found to download.")
        return

    base_url = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-"
    
    for pub_number in publications:
        url = f"{base_url}{pub_number}.pdf"
        filename = f"NIST.SP.800-{pub_number}.pdf"
        
        logging.info(f"Attempting to download {filename}")
        result = download_file(url, filename)
        
        if result is None:
            logging.warning(f"Publication 800-{pub_number} not found or error occurred")
        else:
            # Check if the file is actually a PDF (size > 1000 bytes as a simple heuristic)
            if os.path.getsize(filename) > 1000:
                logging.info(f"Successfully downloaded {filename}")
            else:
                logging.warning(f"{filename} downloaded but may not be a valid PDF. Removing file.")
                os.remove(filename)

if __name__ == "__main__":
    logging.info("Starting NIST SP-800 publication download script")
    download_sp800_publications()
    logging.info("Script execution completed")
