import os
import requests
from bs4 import BeautifulSoup
import logging

# Configuration
BASE_URL = "https://csrc.nist.gov"
SP_PAGE_URL = BASE_URL + "/publications/sp"
DOWNLOAD_DIR = os.path.expanduser("~/Documents/nist_downloads")
LOG_FILE = os.path.join(DOWNLOAD_DIR, "nist_sp_download.log")

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

def setup_download_dir():
    """Ensures the download directory exists; creates it if not."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    logging.info(f"Download directory is ready: {DOWNLOAD_DIR}")

def fetch_page(url):
    """Fetches and returns the HTML content of a webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def extract_intermediate_links(html):
    """
    Extracts links to SP-series intermediate pages from the main page.
    """
    soup = BeautifulSoup(html, "html.parser")
    intermediate_links = {}

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/pubs/sp/"):
            title = a_tag.get_text(strip=True).replace("/", "_") or "SP_Document"
            full_url = BASE_URL + href
            intermediate_links[title] = full_url

    logging.info(f"Found {len(intermediate_links)} intermediate links.")
    return intermediate_links

def extract_pdf_link(intermediate_page_url):
    """
    Navigates to an intermediate page and extracts the PDF download link.
    """
    html = fetch_page(intermediate_page_url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.lower().endswith(".pdf"):
            if not href.startswith("http"):
                return "https://nvlpubs.nist.gov" + href  # Fix relative URL
            return href
    logging.warning(f"No PDF link found on page: {intermediate_page_url}")
    return None

def download_pdf(title, url):
    """Downloads a PDF and saves it locally."""
    file_path = os.path.join(DOWNLOAD_DIR, f"{title}.pdf")
    try:
        logging.info(f"Downloading: {title} from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info(f"Downloaded successfully: {file_path}")
    except Exception as e:
        logging.error(f"Failed to download {title}: {e}")

def download_all_pdfs():
    """
    Main function: fetches SP-series links, navigates intermediate pages, and downloads PDFs.
    """
    setup_download_dir()
    main_page_html = fetch_page(SP_PAGE_URL)
    if not main_page_html:
        logging.error("Failed to fetch main page. Exiting.")
        return

    intermediate_links = extract_intermediate_links(main_page_html)
    if not intermediate_links:
        logging.warning("No intermediate links found. Exiting.")
        return

    for title, intermediate_url in intermediate_links.items():
        logging.info(f"Processing: {title}")
        pdf_url = extract_pdf_link(intermediate_url)
        if pdf_url:
            download_pdf(title, pdf_url)
        else:
            logging.warning(f"No PDF found for: {title}")

    logging.info("All downloads complete.")

if __name__ == "__main__":
    try:
        download_all_pdfs()
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")