import json
import requests
from bs4 import BeautifulSoup
import time

# Load cleaned post metadata
with open("posts_clean.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Prepare to store full post content
full_posts = []

headers = {
    "User-Agent": "Mozilla/5.0"  # Prevents Discourse from blocking requests
}

for i, post in enumerate(posts):
    print(f"Fetching post {i+1}/{len(posts)}: {post['title']}")
    
    try:
        res = requests.get(post["url"], headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Get the first post (main content)
        post_div = soup.find("div", class_="post")
        cooked_div = post_div.find("div", class_="cooked") if post_div else None
        content = cooked_div.get_text(separator="\n").strip() if cooked_div else "[No content found]"
        
        post["content"] = content
        full_posts.append(post)
        
        time.sleep(1.5)  # Be nice to the server
    except Exception as e:
        print(f"Error fetching {post['url']}: {e}")

# Save to file
with open("full_posts.json", "w", encoding="utf-8") as f:
    json.dump(full_posts, f, indent=2)

print(f"Saved {len(full_posts)} full posts.")
