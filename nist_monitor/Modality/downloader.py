import os
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import httpx
import random

from config import DOWNLOAD_DIR, SP_PAGE_URL, LIMIT_DOWNLOADS
from utils import setup_download_dir, log_to_excel
from data_extraction import fetch_page, extract_intermediate_links, extract_pdf_link, fetch_summary

def download_pdf(client, title, url, intermediate_url):
    """Downloads a PDF with retries, logs size, time, and summary."""
    file_path = os.path.join(DOWNLOAD_DIR, f"{title}.pdf")
    start_time = time.time()
    size_mb = 0
    summary = fetch_summary(intermediate_url)  # Fetch the summary before downloading

    try:
        with client.stream("GET", url, follow_redirects=True, timeout=20) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            size_mb = total_size / (1024 * 1024)  # Convert to MB

            with open(file_path, "wb") as file, tqdm(
                desc=f"Downloading: {title}",
                total=total_size,
                unit="B",
                unit_scale=True
            ) as progress:
                for chunk in response.iter_bytes(128 * 1024):
                    file.write(chunk)
                    progress.update(len(chunk))

        time_taken = time.time() - start_time
        logging.info(f"Downloaded: {file_path} ({size_mb:.2f} MB in {time_taken:.2f}s)")
        log_to_excel(title, "Success", size_mb, time_taken, summary)

    except Exception as e:
        time_taken = time.time() - start_time
        logging.error(f"Failed to download {title}: {e}")
        log_to_excel(title, "Failed", size_mb, time_taken, summary)

def download_all_pdfs():
    """Main function to fetch links, extract PDFs, and download concurrently."""
    setup_download_dir()
    main_page_html = fetch_page(SP_PAGE_URL)
    if not main_page_html:
        logging.error("Failed to fetch main page. Exiting.")
        return

    intermediate_links = extract_intermediate_links(main_page_html)
    logging.info(f"Found {len(intermediate_links)} intermediate links to process.")

    if LIMIT_DOWNLOADS:
        all_titles = list(intermediate_links.keys())
        # Randomly pick 5 titles from the available links
        selected_titles = random.sample(all_titles, min(5, len(all_titles)))
        intermediate_links = {title: intermediate_links[title] for title in selected_titles}
        logging.info(f"LIMIT_DOWNLOADS is True. Only these 5 documents will be downloaded: {', '.join(selected_titles)}")

    logging.info(f"Processing {len(intermediate_links)} documents after applying the limit.")

    with ThreadPoolExecutor(max_workers=3) as executor, httpx.Client(http2=True) as client:
        futures = []
        for title, intermediate_url in intermediate_links.items():
            pdf_url = extract_pdf_link(intermediate_url)
            if pdf_url:
                futures.append(executor.submit(download_pdf, client, title, pdf_url, intermediate_url))

        for future in as_completed(futures):
            pass

    logging.info("All downloads complete.")