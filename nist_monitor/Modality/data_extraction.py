import logging
import httpx
from bs4 import BeautifulSoup
from config import BASE_URL

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

def fetch_summary(intermediate_page_url):
    """Fetches the summary text from the SP intermediate page."""
    html = fetch_page(intermediate_page_url)
    if not html:
        return "N/A"
    soup = BeautifulSoup(html, "html.parser")
    summary_tag = soup.find("meta", {"name": "description"})
    return summary_tag["content"] if summary_tag else "No summary available."