import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_website(self):
        try:
            # Send GET request to the URL
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: scraping all headlines (h1, h2, h3 tags)
            headlines = []
            for tag in ['h1', 'h2', 'h3']:
                headlines.extend(soup.find_all(tag))
            
            # Save results to CSV
            self.save_to_csv(headlines)
            
            return headlines
            
        except requests.RequestException as e:
            print(f"Error fetching the website: {e}")
            return None

    def save_to_csv(self, data):
        filename = f"scraping_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Tag', 'Text'])
            
            for item in data:
                writer.writerow([item.name, item.text.strip()])

def main():
    # Example usage
    url = input("Enter the website URL to scrape: ")
    scraper = WebScraper(url)
    
    print("Scraping website...")
    results = scraper.scrape_website()
    
    if results:
        print(f"Found {len(results)} headlines!")
        print("Results have been saved to CSV file.")
        
        # Print first few results
        print("\nSample results:")
        for item in results[:5]:
            print(f"{item.name}: {item.text.strip()}")

if __name__ == "__main__":
    main()
