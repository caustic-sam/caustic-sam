# pylint: disable=W1514
# pylint: disable=C0114
# pylint: disable=C0116

# Importing the required libraries
import json  # This library is used to work with JSON files (read, write, etc.)

import requests  # This library helps us make HTTP requests to fetch web pages
from bs4 import BeautifulSoup  # This library helps us parse HTML and extract data

# Function to load configuration data from a JSON file
# The config file contains the websites and their HTML structure to guide the scraping
def load_config(config_file='cyber_news_config.json'):
    with open(config_file, 'r') as file:  # Open the config file for reading
        return json.load(file)  # Load the JSON data and return it as a Python dictionary

# Function to fetch HTML content from a URL
def fetch_html(url):
    try:
        # Make an HTTP GET request to the given URL
        response = requests.get(url, timeout=10)
        # Raise an error if the request failed (e.g., server not found, 404 error, etc.)
        response.raise_for_status()
        # Return the HTML content of the page
        return response.text
    except requests.RequestException as e:
        # Print the error message if something goes wrong
        print(f"Error fetching {url}: {e}")
        return None  # Return None if there's an error

# Function to parse the articles from the HTML content based on the configuration
# The config tells us which tags and classes contain the article titles and links
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
            title = title_tag.a.get_text(strip=True)  # Get the text inside the title tag
            link = title_tag.a['href']  # Get the link from the href attribute of the <a> tag
            # Add the title and link to our list of articles
            articles.append({'title': title, 'link': link})
    
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
    with open(filename, 'w') as file:  # Open the file in write mode
        json.dump(data, file, indent=4)  # Write the data into the file with indentation for readability
    print(f"Data saved to {filename}")  # Print a message when the data is successfully saved

# Main entry point for the script
def main():
    config = load_config()  # Load the config file with website details
    scraped_data = scrape_news(config)  # Scrape the news articles
    save_to_json(scraped_data)  # Save the scraped articles to a JSON file

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()  # Call the main function
