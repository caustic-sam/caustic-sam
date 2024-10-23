# pylint: disable=W1514
# pylint: disable=C0114
# pylint: disable=C0116

import json
from bs4 import BeautifulSoup
import requests




# Load configuration from the provided JSON file
def load_config(config_path='cyber_news_config.json'):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config['sources']
    except FileNotFoundError:
        print(f"Error: The config file '{config_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{config_path}'.")
        return []

# Generic function to scrape stories from various websites
def get_stories_from_site(url, headline_tag, headline_class, container_class=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    stories = []

    if container_class:
        containers = soup.find_all('div', class_=container_class)[:3]
    else:
        containers = soup.find_all(headline_tag, class_=headline_class)[:3]

    for container in containers:
        title_tag = container.find(headline_tag, class_=headline_class)

        if not title_tag:
            title_tag = container.find('a')

        title = title_tag.get_text().strip() if title_tag else "No Title Found"
        link_tag = container.find('a', href=True)

        if link_tag:
            link = link_tag['href']
            stories.append(f"Title: {title}\nLink: {link}")
        else:
            print(f"Warning: No link found for story '{title}' from {url}")

    return stories

# Aggregate stories from all sources
def aggregate_stories(config_path='cyber_news_config.json'):
    print("Fetching stories from various sources...")

    all_stories = []
    sources = load_config(config_path)

    for source in sources:
        url = source['url']
        headline_tag = source['headline_tag']
        headline_class = source['headline_class']
        container_class = source.get('container_class')

        print(f"Scraping {url}...")

        site_stories = get_stories_from_site(url, headline_tag, headline_class, container_class)

        if not site_stories:
            print(f"Warning: No stories found for {url}")

        all_stories += site_stories

    return all_stories

# Main function to display aggregated stories
if __name__ == "__main__":
    top_stories = aggregate_stories()

    print("\nTop Cybersecurity Stories:\n")
    for story in top_stories:
        print(story)
        print("-" * 80)
