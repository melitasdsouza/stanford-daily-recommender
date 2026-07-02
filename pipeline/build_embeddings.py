import json
from sentence_transformers import SentenceTransformer

INPUT_FILE = "../data/cleaned_articles.json"
OUTPUT_FILE = "../data/embeddings.json"

MODEL_NAME = "all-MiniLM-L6-v2"

def load_articles():
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

def build_embeddings(articles):
    model = SentenceTransformer(MODEL_NAME)

    texts = [article["content"] for article in articles]
    print("Encoding articles... (this may take a minute the first time)")
    vectors = model.encode(texts, show_progress_bar=True)

    embedded_articles = []
    for article, vector in zip(articles, vectors):
        embedded_articles.append({
            "id": article["id"],
            "slug": article["slug"],
            "title": article["title"],
            "link": article["link"],
            "date": article["date"],
            "image_url": article["image_url"],
            "tags_readable": article["tags_readable"],
            "embedding": vector.tolist()
        })

    return embedded_articles

def save_embeddings(embedded_articles):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(embedded_articles, f)

if __name__ == "__main__":
    articles = load_articles()
    print(f"Loaded {len(articles)} cleaned articles")

    embedded_articles = build_embeddings(articles)
    print(f"Generated embeddings for {len(embedded_articles)} articles")

    save_embeddings(embedded_articles)
    print(f"Saved to {OUTPUT_FILE}")