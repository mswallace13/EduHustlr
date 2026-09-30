import json
import urllib.request
import xml.etree.ElementTree as ET

# Example list of official Congressional RSS feeds
CONGRESS_RSS_FEEDS = [
    {"name": "Senate Foreign Relations Committee", "url": "https://www.foreign.senate.gov/rss/feeds/?type=all"},
    {"name": "House Judiciary Committee", "url": "https://judiciary.house.gov/rss.xml"},
    {"name": "Sen. Bernie Sanders Press Releases", "url": "https://www.sanders.senate.gov/feed/"}
]

def fetch_rss_items(feed_url, max_results=3):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(feed_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # Locate channel items (standard RSS 2.0 format)
            items = root.findall('.//item')[:max_results]
            parsed_items = []
            
            for item in items:
                title = item.find('title').text if item.find('title') is not None else 'No Title'
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                parsed_items.append({
                    "title": title,
                    "url": link,
                    "created_at": pub_date,
                    "content": description
                })
            return parsed_items
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

results = []
for feed in CONGRESS_RSS_FEEDS:
    print(f"Fetching RSS feed for {feed['name']}...")
    posts = fetch_rss_items(feed['url'], max_results=3)
    
    results.append({
        "handle": feed["name"],
        "posts": posts
    })

# Output to static posts.json
with open("posts.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved RSS updates to posts.json!")
