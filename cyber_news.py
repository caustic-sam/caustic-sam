# pylint: disable=W1514
# pylint: disable=C0114
# pylint: disable=C0116
# pylint: disable=C0411

import requests  # For making HTTP requests to fetch web pages
from bs4 import BeautifulSoup  # For parsing HTML and extracting data
import json  # For working with JSON files (read, write, etc.)

# Function to load configuration data from a JSON file
def load_config(config_file='cyber_news_config.json'):
    try:
        with open(config_file, 'r') as file:  # Open the config file for reading
            config = json.load(file)  # Load the JSON data
            if "sources" not in config:
                raise KeyError("'sources' key is missing in the configuration file")
            return config  # Return the loaded configuration
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return None
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.")
        return None

# Function to fetch HTML content from a URL with a User-Agent header
def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Added User-Agent header
        response.raise_for_status()
        return response.text  # Return the HTML content of the page
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to parse the articles from the HTML content based on the configuration
def parse_articles(html, config):
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML using BeautifulSoup
    articles = []  # Initialize an empty list to store the article information
    
    # Find all article tags based on the config (e.g., <h2> or <article>)
    for article_tag in soup.find_all(config['article_tag'], class_=config['article_class']):
        # Find the title tag inside the article (e.g., <h2> or <a>)
        title_tag = article_tag.find(config['title_tag'], class_=config['title_class'])
        
        # If we find the title tag and it contains a link
        if title_tag and title_tag.a:
            # Extract the title text and the link URL
            title = title_tag.a.get_text(strip=True)
            link = title_tag.a['href']
            articles.append({'title': title, 'link': link})  # Add the title and link to our list of articles
    
    return articles  # Return the list of articles found

# Main function to scrape news from all websites
def scrape_news(config):
    all_articles = {}  # Dictionary to store articles from all websites
    
    # Loop through each website listed in the config
    for site, site_config in config['sources'].items():
        print(f"Scraping {site}...")  # Print a message to show progress
        html = fetch_html(site)  # Fetch the HTML content from the website
        if html:
            # Parse the articles for the current website and store them
            articles = parse_articles(html, site_config)
            all_articles[site] = articles  # Add articles to our dictionary
    
    return all_articles  # Return the dictionary containing all articles

# Function to save the scraped data into a JSON file
def save_to_json(data, filename='scraped_news.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

# Main entry point for the script
def main():
    config = load_config()  # Load the config file with website details
    if config:  # Proceed only if the configuration was successfully loaded
        scraped_data = scrape_news(config)  # Scrape the news articles
        save_to_json(scraped_data)  # Save the scraped articles to a JSON file

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()  # Call the main function
