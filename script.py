import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

CONGRESS_RSS_FEEDS = [
    {"name": "Senate Foreign Relations Committee", "url": "https://www.foreign.senate.gov/rss/feeds/?type=all"},
    {"name": "House Judiciary Committee", "url": "https://judiciary.house.gov/rss.xml"},
    {"name": "Sen. Bernie Sanders Press Releases", "url": "https://www.sanders.senate.gov/feed/"}
]

def parse_date_to_iso(date_str):
    """Converts various RSS/Mastodon date formats into ISO standard YYYY-MM-DD for accurate sorting."""
    if not date_str:
        return "1970-01-01T00:00:00Z"
    
    # Try RFC 822 / RSS standard date format (e.g., "Wed, 30 Sep 2026 10:00:00 GMT")
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.isoformat()
    except Exception:
        pass

    # Try ISO format directly (standard in Mastodon APIs)
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.isoformat()
    except Exception:
        pass

    return date_str

def fetch_rss_items(feed_url, max_results=5):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(feed_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            items = root.findall('.//item')
            parsed_items = []
            
            for item in items:
                title = item.find('title').text if item.find('title') is not None else 'No Title'
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                iso_date = parse_date_to_iso(pub_date)
                
                parsed_items.append({
                    "title": title,
                    "url": link,
                    "created_at": iso_date,
                    "content": description
                })
            
            # Sort individual feed items newest to oldest (2026 first)
            parsed_items.sort(key=lambda x: x['created_at'], reverse=True)
            return parsed_items[:max_results]
            
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

results = []
for feed in CONGRESS_RSS_FEEDS:
    print(f"Fetching RSS feed for {feed['name']}...")
    posts = fetch_rss_items(feed['url'], max_results=5)
    
    if posts:
        results.append({
            "handle": feed["name"],
            "posts": posts
        })

# Output to posts.json
with open("posts.json", "w") as f:
    json.dump(results, f, indent=2)

print("Successfully saved latest 2026 posts to posts.json!")
  
