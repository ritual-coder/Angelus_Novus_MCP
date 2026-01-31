import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_top_trends(woeid=1, window_hours=17):
    """
    Fetches the top trends from trends24.in for the last 'window_hours'.
    Aggregates top 3 trends from each hour to creating a diverse pool.
    """
    url = "https://trends24.in/"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch trends24.in. Status Code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # trends24 puts hourly lists in <div class="list-container">
        containers = soup.find_all('div', class_='list-container')
        
        if not containers:
            logger.error("Could not find any list-containers.")
            return []
            
        logger.info(f"Found {len(containers)} hourly lists. Scanning the first {window_hours}...")
        
        # We will collect unique trends. 
        # Using a dictionary to deduplicate by name, keeping the one with higher volume or first occurrence.
        seen_trends = {}
        
        scan_count = 0
        for container in containers:
            if scan_count >= window_hours:
                break
            
            trend_list = container.find('ol', class_='trend-card__list')
            if not trend_list:
                continue
                
            items = trend_list.find_all('li')
            
            # Take top 3 from each hour to avoid overloading but get variety
            for item in items[:3]:
                link_tag = item.find('a', class_='trend-link')
                if link_tag:
                    name = link_tag.get_text().strip()
                    count_span = item.find('span', class_='tweet-count')
                    volume = count_span.get_text().strip() if count_span else "Unknown"
                    
                    # Store logic: if not seen, add it.
                    if name not in seen_trends:
                        seen_trends[name] = {
                            "name": name,
                            "tweet_volume": volume,
                            "url": link_tag['href']
                        }
            
            scan_count += 1
            
        # Convert back to list
        trends = list(seen_trends.values())
        
        logger.info(f"Aggregated {len(trends)} unique trends from the last {scan_count} hours.")
        return trends

    except Exception as e:
        logger.error(f"Error scraping trends: {e}")
        return []
