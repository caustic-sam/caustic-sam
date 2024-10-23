import requests
import json

# List of URLs to scrape
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
]

# Function to fetch the HTML of a website
def fetch_html(url):
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise an error if the request fails
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to save the HTML content to a JSON file
def save_to_json(data, filename="website_data.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def main():
    html_data = {}
    
    for url in urls:
        html_content = fetch_html(url)
        if html_content:
            # Store the HTML content in a dictionary
            html_data[url] = html_content
        else:
            html_data[url] = "Failed to fetch HTML"
    
    # Save the HTML content to a JSON file
    save_to_json(html_data)

if __name__ == "__main__":
    main()
