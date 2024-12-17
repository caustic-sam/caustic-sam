import os

# Configuration
LIMIT_DOWNLOADS = True  # Set True for only 5 random downloads, False for all
BASE_URL = "https://csrc.nist.gov"
SP_PAGE_URL = f"{BASE_URL}/publications/sp"
DOWNLOAD_DIR = os.path.expanduser("~/Documents/nist_downloads_http2")
LOG_FILE = os.path.join(DOWNLOAD_DIR, "nist_sp_download.log")
EXCEL_FILE = os.path.join(DOWNLOAD_DIR, "download_log.xlsx")

# Ensure the download directory exists before configuring logging
os.makedirs(DOWNLOAD_DIR, exist_ok=True)