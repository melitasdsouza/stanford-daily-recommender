import json
from bs4 import BeautifulSoup

INPUT_FILE = "../data/raw_articles.json"
OUTPUT_FILE = "../data/cleaned_articles.json"

def load_articles():
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")
    text = " ".join(text.split())
    return text

def clean_all_articles(articles):
    cleaned = []
    for article in articles:
        cleaned_article = {
            "id": article["id"],
            "slug": article["slug"],
            "title": clean_html(article["title"]),
            "content": clean_html(article["content"]),
            "link": article["link"],
            "date": article["date"],
             "image_url": article["image_url"],
            "tags_readable": article["tags_readable"]
        }
        cleaned.append(cleaned_article)
    return cleaned

def save_articles(articles):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(articles, f, indent=2)

if __name__ == "__main__":
    raw_articles = load_articles()
    print(f"Loaded {len(raw_articles)} raw articles")

    cleaned_articles = clean_all_articles(raw_articles)
    print(f"Cleaned {len(cleaned_articles)} articles")

    save_articles(cleaned_articles)
    print(f"Saved to {OUTPUT_FILE}")