

"""
[] 
    "https://krebsonsecurity.com/",
    "https://thehackernews.com/",
    "https://www.darkreading.com/",
    "https://www.bleepingcomputer.com/",
    "https://www.cyberscoop.com/",
    "https://www.securityweek.com/",
    "https://www.scmagazine.com/",
    "https://threatpost.com/",
    "https://www.wired.com/category/security/",
    "https://www.zdnet.com/topic/security/",
    "https://securityboulevard.com/",
    "https://arstechnica.com/security/",
    "https://www.infosecurity-magazine.com/",
    "https://www.reddit.com/r/cybersecurity/",
    "https://isc.sans.edu/",
    "https://nakedsecurity.sophos.com/",
    "https://portswigger.net/daily-swig",
    "https://www.welivesecurity.com/",
    "https://blog.malwarebytes.com/"
] """

import requests
import os

# Create the directory if it doesn't exist
os.makedirs('./dump', exist_ok=True)

# Function to fetch HTML content from a URL
def fetch_html(url):
    try:
        # Make an HTTP GET request to the given URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error if the request failed
        
        # Save the HTML to a file in the ./dump directory
        filename = os.path.join('./dump', url.split('//')[1].replace('/', '_') + ".html")
        with open(filename, 'w') as file:
            file.write(response.text)
        
        print(f"Saved HTML for {url} to {filename}")
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Example use case
urls = [
    "https://krebsonsecurity.com/",
    "https://thehackernews.com/",
    "https://www.darkreading.com/",
    "https://www.bleepingcomputer.com/",
    "https://www.cyberscoop.com/",
    "https://www.securityweek.com/",
    "https://www.scmagazine.com/",
    "https://threatpost.com/",
    "https://www.wired.com/category/security/",
    "https://www.zdnet.com/topic/security/",
    "https://securityboulevard.com/",
    "https://arstechnica.com/security/",
    "https://www.infosecurity-magazine.com/",
    "https://www.reddit.com/r/cybersecurity/",
    "https://isc.sans.edu/",
    "https://nakedsecurity.sophos.com/",
    "https://portswigger.net/daily-swig",
    "https://www.welivesecurity.com/",
    "https://blog.malwarebytes.com/"
    # Add more URLs from your config if necessary
]

for url in urls:
    fetch_html(url)
