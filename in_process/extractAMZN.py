import json
import time
from datetime import datetime

import requests

class HansardScraper:
    """A scraper for retrieving parliamentary debates from the UK Hansard API."""
    
    def __init__(self):
        self.api_url = "https://hansard.parliament.uk/api/"
        self.headers = {
            'User-Agent': 'Research Bot (Educational Purpose)',
            'Accept': 'application/json'
        }
    
    def get_daily_debates(self, date):
        """Get all debates for a specific date"""
        formatted_date = date.strftime("%Y-%m-%d")
        endpoint = f"{self.api_url}sittings?date={formatted_date}"
        
        print(f"\nTrying to fetch debates from: {endpoint}")
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_debate_content(self, debate_id):
        """Get content of a specific debate"""
        time.sleep(1)  # Polite delay
        endpoint = f"{self.api_url}debate/{debate_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching debate {debate_id}: {e}")
            return None

def test_scraper():
    scraper = HansardScraper()
    
    # Test with today's date
    test_date = datetime.now()
    print(f"Testing scraper for date: {test_date.strftime('%Y-%m-%d')}")
    
    # Get debates for the day
    daily_debates = scraper.get_daily_debates(test_date)
    
    if not daily_debates:
        print("No debates found. Trying yesterday...")
        test_date = datetime.now().replace(day=datetime.now().day - 1)
        daily_debates = scraper.get_daily_debates(test_date)
    
    if daily_debates:
        print("\nFound sittings for this date!")
        
        # Print first level of data to see structure
        print("\nDebate Structure:")
        print(json.dumps(daily_debates[0] if daily_debates else {}, indent=2)[:500])
        
        # Try to get one full debate
        for sitting in daily_debates:
            for debate in sitting.get('Debates', [])[:1]:  # Just get first debate
                debate_id = debate.get('Id')
                print(f"\nFetching full content for debate ID: {debate_id}")
                
                full_debate = scraper.get_debate_content(debate_id)
                if full_debate:
                    print("\nSuccessfully retrieved debate content!")
                    print("\nDebate Title:", full_debate.get('Title'))
                    print("Date:", full_debate.get('Date'))
                    print("Number of speeches:", len(full_debate.get('Speeches', [])))
                    
                    # Print first speech if available
                    speeches = full_debate.get('Speeches', [])
                    if speeches:
                        print("\nFirst speech sample:")
                        print("Speaker:", speeches[0].get('MemberName'))
                        print("Text excerpt:", speeches[0].get('Body', '')[:200])
                
                break  # Just test one debate
    else:
        print("No debates found for test date")

if __name__ == "__main__":
    print("Starting Hansard Scraper Test...")
    test_scraper()
