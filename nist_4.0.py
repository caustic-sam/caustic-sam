import os
import httpx
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from datetime import datetime

# Configuration
BASE_URL = "https://csrc.nist.gov"
SP_PAGE_URL = BASE_URL + "/publications/sp"
DOWNLOAD_DIR = os.path.expanduser("~/Documents/nist_downloads_http2")
LOG_FILE = os.path.join(DOWNLOAD_DIR, "nist_sp_download.log")

# Ensure the download directory exists before configuring logging
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

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
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetch_page(url):
    """Fetches and returns the HTML content of a webpage."""
    try:
        with httpx.Client(http2=True, timeout=10) as client:
            response = client.get(url, follow_redirects=True)
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
            return href if href.startswith("http") else "https://nvlpubs.nist.gov" + href
    return None

def download_pdf(client, title, url):
    """Downloads a PDF with retries, timeout, and follow_redirects."""
    file_path = os.path.join(DOWNLOAD_DIR, f"{title}.pdf")
    try:
        with client.stream("GET", url, follow_redirects=True, timeout=20) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            with open(file_path, "wb") as file, tqdm(
                desc=f"Downloading: {title}",
                total=total_size,
                unit="B",
                unit_scale=True
            ) as progress:
                for chunk in response.iter_bytes(128 * 1024):
                    file.write(chunk)
                    progress.update(len(chunk))
        logging.info(f"Downloaded: {file_path}")
    except Exception as e:
        logging.error(f"Failed to download {title}: {e}")

def download_all_pdfs():
    """Main function to fetch links, extract PDFs, and download concurrently."""
    setup_download_dir()
    main_page_html = fetch_page(SP_PAGE_URL)
    if not main_page_html:
        logging.error("Failed to fetch main page. Exiting.")
        return

    intermediate_links = extract_intermediate_links(main_page_html)
    logging.info(f"Found {len(intermediate_links)} intermediate links to process.")

    with ThreadPoolExecutor(max_workers=3) as executor, httpx.Client(http2=True) as client:
        futures = []
        for title, intermediate_url in intermediate_links.items():
            pdf_url = extract_pdf_link(intermediate_url)
            if pdf_url:
                futures.append(executor.submit(download_pdf, client, title, pdf_url))

        for future in as_completed(futures):
            pass

    logging.info("All downloads complete.")

if __name__ == "__main__":
    try:
        download_all_pdfs()
    except KeyboardInterrupt:
        logging.error("Script interrupted by user.")
        print("\nDownload interrupted. Exiting gracefully.")
