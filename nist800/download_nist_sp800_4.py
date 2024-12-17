import re
import requests
from bs4 import BeautifulSoup

def extract_nist_links_with_logging(url):
    try:
        print(f"Fetching the webpage: {url}")

        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        print(f"HTTP request successful. Status Code: {response.status_code}")

        html_content = response.text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all anchor tags with href attributes
        links = [a['href'] for a in soup.find_all('a', href=True)]
        print(f"Total <a> tags with href found: {len(links)}")

        # Regex pattern for NIST Special Publication links
        pattern = r"https://nvlpubs\.nist\.gov/nistpubs/Legacy/SP/nistspecialpublication800-\d+\.pdf"
        print(f"Regex pattern: {pattern}")

        # Filter links based on the pattern
        matched_links = [link for link in links if re.fullmatch(pattern, link)]

        if matched_links:
            print(f"Total matched links: {len(matched_links)}")
        else:
            print("No links matched the pattern. Possible reasons:")
            print("- The webpage doesn't contain the expected links.")
            print("- The regex pattern is incorrect or too restrictive.")
            print("- The webpage's HTML structure has changed.")

        return matched_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Replace with the actual URL of the webpage you are scraping
    url = "https://example.com"  
    matching_links = extract_nist_links_with_logging(url)

    print("\nMatched Links:")
    if matching_links:
        for link in matching_links:
            print(link)
    else:
        print("No links were extracted.")