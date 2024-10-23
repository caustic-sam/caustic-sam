import requests
from bs4 import BeautifulSoup

# Define a function to get top three stories from each site
def get_krebs_on_security():
    url = 'https://krebsonsecurity.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    stories = []
    for item in soup.find_all('h2', class_='entry-title')[:3]:
        title = item.get_text()
        link = item.find('a')['href']
        stories.append(f"Title: {title}\nLink: {link}")
    return stories

def get_hacker_news():
    url = 'https://thehackernews.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    stories = []
    for item in soup.find_all('h2', class_='home-title')[:3]:
        title = item.get_text()
        link = item.find('a')['href']
        stories.append(f"Title: {title}\nLink: {link}")
    return stories

def get_dark_reading():
    url = 'https://www.darkreading.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    stories = []
    for item in soup.find_all('h3', class_='article-title')[:3]:
        title = item.get_text()
        link = item.find('a')['href']
        stories.append(f"Title: {title}\nLink: {link}")
    return stories

def get_security_week():
    url = 'https://www.securityweek.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    stories = []
    for item in soup.find_all('h2', class_='title')[:3]:
        title = item.get_text()
        link = item.find('a')['href']
        stories.append(f"Title: {title}\nLink: {link}")
    return stories

# You can define more functions for other websites following the same pattern
# Adding more functions like `get_bleeping_computer`, `get_cyberscoop`, etc.

# Aggregating all stories
def aggregate_stories():
    print("Fetching stories from various sources...")
    
    all_stories = []

    # Add stories from each website to the list
    all_stories += get_krebs_on_security()
    all_stories += get_hacker_news()
    all_stories += get_dark_reading()
    all_stories += get_security_week()

    # More sites can be added as functions are created
    # For now, we'll return the stories as a combined list

    return all_stories

# Main function to display the aggregated stories
if __name__ == "__main__":
    top_stories = aggregate_stories()

    # Printing all the top stories
    print("\nTop Cybersecurity Stories:\n")
    for story in top_stories:
        print(story)
        print("-" * 80)
