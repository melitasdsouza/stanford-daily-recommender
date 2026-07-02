import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

INPUT_FILE = "../data/embeddings.json"
OUTPUT_FILE = "../data/recommendations.json"

TOP_N = 5
MIN_SIMILARITY = 0.3

def load_embeddings():
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

def compute_similarity_matrix(articles):
    vectors = [article["embedding"] for article in articles]
    matrix = np.array(vectors)

    print(f"Matrix shape: {matrix.shape}")

    similarity_matrix = cosine_similarity(matrix)

    return similarity_matrix

def build_recommendations(articles, similarity_matrix):
    recommendations = {}

    for i, article in enumerate(articles):
        scores = similarity_matrix[i]

        scored_matches = []
        for j, score in enumerate(scores):
            if j == i:
                continue
            if score < MIN_SIMILARITY:
                continue
            scored_matches.append((j, score))

        scored_matches.sort(key=lambda pair: pair[1], reverse=True)
        top_matches = scored_matches[:TOP_N]

        recommendations[article["slug"]] = [
            {
                "title": articles[j]["title"],
                "slug": articles[j]["slug"],
                "link": articles[j]["link"],
                "image_url": articles[j]["image_url"],
                "score": round(float(score), 4)
            }
            for j, score in top_matches
        ]

    return recommendations

def save_recommendations(recommendations):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(recommendations, f, indent=2)

if __name__ == "__main__":
    articles = load_embeddings()
    print(f"Loaded {len(articles)} articles with embeddings")

    similarity_matrix = compute_similarity_matrix(articles)

    recommendations = build_recommendations(articles, similarity_matrix)
    print(f"Built recommendations for {len(recommendations)} articles")

    save_recommendations(recommendations)
    print(f"Saved to {OUTPUT_FILE}")