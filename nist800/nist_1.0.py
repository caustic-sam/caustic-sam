import os
import shutil
import requests
from bs4 import BeautifulSoup
import hashlib
import time

BASE_URL = "https://csrc.nist.gov"
TARGET_URL = BASE_URL + "/publications/final-pubs"
HOME_DIR = os.path.expanduser("~/Documents/nist_downloads")
HASH_FILE = os.path.join(HOME_DIR, "hashes.txt")
INTERVAL = 86400  # Daily interval

def setup_download_dir():
    """Set up or clear the download directory."""
    if os.path.exists(HOME_DIR):
        shutil.rmtree(HOME_DIR)  # Remove existing directory
    os.makedirs(HOME_DIR)  # Create fresh directory
    print(f"Download directory is ready: {HOME_DIR}")

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_documents(html):
    soup = BeautifulSoup(html, "html.parser")
    documents = {}
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/publications/"):
            full_url = BASE_URL + href
            title = link.get_text(strip=True).replace("/", "_")  # Sanitize filename
            documents[title] = full_url
    return documents

def download_file(url, title):
    response = requests.get(url)
    response.raise_for_status()
    file_path = os.path.join(HOME_DIR, f"{title}.pdf")
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"Downloaded: {file_path}")

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, "r") as file:
        return dict(line.strip().split(" ", 1) for line in file)

def save_hashes(hashes):
    with open(HASH_FILE, "w") as file:
        for title, hash_val in hashes.items():
            file.write(f"{title} {hash_val}\n")

def get_hash(content):
    return hashlib.md5(content).hexdigest()

def monitor_documents():
    setup_download_dir()
    old_hashes = load_hashes()
    html = fetch_page(TARGET_URL)
    documents = parse_documents(html)
    updated_hashes = {}

    for title, url in documents.items():
        print(f"Checking: {title}")
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        current_hash = get_hash(content)
        updated_hashes[title] = current_hash

        if title not in old_hashes or old_hashes[title] != current_hash:
            print(f"New/Updated document: {title}")
            download_file(url, title)

    save_hashes(updated_hashes)
    print("Monitoring complete. Next check in 24 hours.")

if __name__ == "__main__":
    while True:
        try:
            monitor_documents()
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL)