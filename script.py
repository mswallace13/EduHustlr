import json
import requests

def get_mastodon_posts(mastodon_handle: str, max_results: int = 3):
    parts = mastodon_handle.strip("@").split("@")
    if len(parts) != 2:
        return []
        
    username, instance = parts[0], parts[1]
    
    lookup_url = f"https://{instance}/api/v1/accounts/lookup"
    try:
        res = requests.get(lookup_url, params={"acct": username}, timeout=10)
        if res.status_code != 200:
            return []
        account_id = res.json()["id"]

        statuses_url = f"https://{instance}/api/v1/accounts/{account_id}/statuses"
        res = requests.get(statuses_url, params={"limit": max_results, "exclude_replies": True}, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error fetching {mastodon_handle}: {e}")
    
    return []

# Load dataset
with open("my_congress_project.json", "r") as f:
    data = json.load(f)

mastodon_members = [m for m in data if m.get("social", {}).get("mastodon")]

results = []
for member in mastodon_members:
    handle = member["social"]["mastodon"]
    print(f"Fetching posts for {handle}...")
    
    posts = get_mastodon_posts(handle, max_results=3)
    
    clean_posts = [
        {
            "id": p.get("id"),
            "created_at": p.get("created_at"),
            "content": p.get("content"),
            "url": p.get("url")
        }
        for p in posts
    ]
    
    results.append({
        "bioguide": member["id"]["bioguide"],
        "handle": handle,
        "posts": clean_posts
    })

# Save output to posts.json
with open("posts.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved Mastodon posts to posts.json!")
