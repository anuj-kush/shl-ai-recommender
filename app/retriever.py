import pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer


VECTOR_DIR = Path("vectorstore")

# Load FAISS index
index = faiss.read_index(str(VECTOR_DIR / "index.faiss"))

# Load metadata
with open(VECTOR_DIR / "metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Load embedding model


model = None

def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model

print(f"Loaded {len(metadata)} assessments")

TEST_TYPE_MAP = {
    "Knowledge & Skills": "K",
    "Personality & Behavior": "P",
    "Ability & Aptitude": "A",
    "Biodata & Situational Judgment": "B",
    "Assessment Exercises": "E",
    "Competencies": "C",
    "Development & 360": "D",
}
def get_test_type(keys):
    for key in keys:
        if key in TEST_TYPE_MAP:
            return TEST_TYPE_MAP[key]
    return "Other"
def search(query: str, top_k: int = 10):
    """
    Search the SHL assessment catalog.
    """

   # Convert query into embedding
    query_embedding = get_model().encode(
    [query],
    convert_to_numpy=True
)

    # Normalize
    faiss.normalize_L2(query_embedding)

    # Search FAISS
    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        assessment = metadata[idx]

        results.append({
            "id": assessment["id"],
            "name": assessment["name"],
            "description": assessment["description"],
            "duration": assessment["duration"],
            "languages": assessment["languages"],
            "job_levels": assessment["job_levels"],
            "keys": assessment["keys"],
            "remote": assessment["remote"],
            "adaptive": assessment["adaptive"],
            "url": assessment["url"],
            "test_type": get_test_type(assessment["keys"]),
            "score": float(score)
        })

    return results

if __name__ == "__main__":
    query = input("Enter your search query: ")

    print(f"\nSearching for: {query}\n")

    results = search(query)

    print("\nTop Results\n")

    for r in results:
        print("-" * 50)
        print("Name :", r["name"])
        print("Score:", round(r["score"], 3))

