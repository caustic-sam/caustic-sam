import logging
from utils import setup_logging
from downloader import download_all_pdfs

if __name__ == "__main__":
    setup_logging()
    try:
        download_all_pdfs()
    except KeyboardInterrupt:
        logging.error("Script interrupted by user.")
        print("\nDownload interrupted. Exiting gracefully.")