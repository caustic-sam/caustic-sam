import os
import requests
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pandas as pd
from datetime import datetime

# Configuration
BASE_URL = "https://csrc.nist.gov"
SP_PAGE_URL = BASE_URL + "/publications/sp"
DOWNLOAD_DIR = os.path.expanduser("~/Documents/nist_downloads")
LOG_FILE = os.path.join(DOWNLOAD_DIR, "nist_sp_download.log")
EXCEL_FILE = os.path.join(DOWNLOAD_DIR, "download_log.xlsx")

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

# Setup global list to track downloads
download_records = []

def setup_download_dir():
    """Ensures the download directory exists."""
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
    """Extracts links to SP-series intermediate pages."""
    soup = BeautifulSoup(html, "html.parser")
    intermediate_links = {}
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/pubs/sp/"):
            title = a_tag.get_text(strip=True).replace("/", "_") or "SP_Document"
            intermediate_links[title] = BASE_URL + href
    return intermediate_links

def extract_pdf_link(intermediate_page_url):
    """Navigates to an intermediate page and extracts the PDF download link."""
    html = fetch_page(intermediate_page_url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.lower().endswith(".pdf"):
            if not href.startswith("http"):
                return "https://nvlpubs.nist.gov" + href
            return href
    return None

def download_pdf(title, url):
    """Downloads a PDF and saves it locally."""
    file_path = os.path.join(DOWNLOAD_DIR, f"{title}.pdf")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        download_time = datetime.now().strftime("%H:%M:%S")
        download_records.append({"Title": title, "Time": download_time})
        logging.info(f"Downloaded: {file_path}")
    except Exception as e:
        logging.error(f"Failed to download {title}: {e}")

def save_download_log():
    """Saves download records to an Excel file."""
    df = pd.DataFrame(download_records)
    df.to_excel(EXCEL_FILE, index=False)
    logging.info(f"Download log saved to: {EXCEL_FILE}")

def download_all_pdfs():
    """Main function to fetch links, extract PDFs, and download concurrently."""
    setup_download_dir()
    main_page_html = fetch_page(SP_PAGE_URL)
    if not main_page_html:
        logging.error("Failed to fetch main page. Exiting.")
        return

    intermediate_links = extract_intermediate_links(main_page_html)
    if not intermediate_links:
        logging.warning("No intermediate links found. Exiting.")
        return

    # Progress bar setup
    progress_bar = tqdm(total=len(intermediate_links), desc="Processing Documents", ncols=80)

    # Threaded downloads
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for title, intermediate_url in intermediate_links.items():
            futures.append(executor.submit(process_and_download, title, intermediate_url))
        
        for future in as_completed(futures):
            progress_bar.update(1)
    progress_bar.close()

    save_download_log()
    logging.info("All downloads complete.")

def process_and_download(title, intermediate_url):
    """Processes an intermediate page and downloads the PDF."""
    logging.info(f"Processing: {title}")
    pdf_url = extract_pdf_link(intermediate_url)
    if pdf_url:
        download_pdf(title, pdf_url)
    else:
        logging.warning(f"No PDF found for: {title}")

if __name__ == "__main__":
    try:
        download_all_pdfs()
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")