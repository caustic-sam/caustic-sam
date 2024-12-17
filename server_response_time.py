import time
import requests

url = "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf"  # Example file

start_time = time.time()
response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

downloaded = 0
for chunk in response.iter_content(chunk_size=8192):
    downloaded += len(chunk)
end_time = time.time()

elapsed = end_time - start_time
speed = downloaded / elapsed / 1024 / 1024  # Convert to MB/s
print(f"Downloaded {total_size / 1024 / 1024:.2f} MB in {elapsed:.2f} seconds ({speed:.2f} MB/s)")