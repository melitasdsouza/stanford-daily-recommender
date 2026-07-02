import requests
import json
import time
from datetime import datetime, timedelta


BASE_URL = "https://stanforddaily.com/wp-json/wp/v2/posts"
PER_PAGE = 100
OUTPUT_FILE = "../data/raw_articles.json"
CUTOFF_DATE = datetime.now() - timedelta(days=5 * 365)

def fetch_all_articles():
    all_articles = []
    page = 1

    while True:
        params = {
            "per_page": PER_PAGE,
            "page": page
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Stopped at page {page}, status code {response.status_code}")
            break

        posts = response.json()

        if not posts:
            print("No more posts. Done.")
            break

        for post in posts:
            post_date = datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S")
            if post_date < CUTOFF_DATE:
                print(f"Reached articles older than 5 years at page {page}. Stopping.")
                return all_articles
    
            article = {
                "id": post["id"],
                "slug": post["slug"],
                "title": post["title"]["rendered"],
                "content": post["content"]["rendered"],
                "link": post["link"],
                "date": post["date"],
                "image_url": post.get("jetpack_featured_media_url", ""),
                "tags_readable": [c for c in post["class_list"] if c.startswith("tag-") or c.startswith("category-")]
            }
            all_articles.append(article)

        print(f"Fetched page {page} ({len(posts)} articles)")
        page += 1
        time.sleep(0.5)

    return all_articles
    
if __name__ == "__main__":
    articles = fetch_all_articles()
    print(f"Total articles fetched: {len(articles)}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(articles, f, indent=2)

    print(f"Saved to {OUTPUT_FILE}")