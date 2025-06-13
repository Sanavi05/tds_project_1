import json

# Load the saved JSON file
with open("discourse_posts.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Extract topics and users
topics = raw_data.get("topic_list", {}).get("topics", [])
users = raw_data.get("users", [])

# Build a user id to name mapping
user_map = {user["id"]: user["username"] for user in users}

# Extract clean post data
posts = []
for topic in topics:
    post = {
        "id": topic["id"],
        "title": topic["title"],
        "slug": topic["slug"],
        "author": user_map.get(topic.get("posters", [{}])[0].get("user_id"), "unknown"),
        "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{topic['slug']}/{topic['id']}"
    }
    posts.append(post)

# Save the clean list
with open("posts_clean.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2)

print(f"Extracted {len(posts)} posts.")
