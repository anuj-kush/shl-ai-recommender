import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INPUT_FILE = Path("data/clean_catalog.json")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded.")

texts = [item["search_text"] for item in catalog]

print(f"Embedding {len(texts)} documents...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

print(embeddings.shape)
faiss.normalize_L2(embeddings)
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print(index.ntotal)

VECTOR_DIR = Path("vectorstore")
VECTOR_DIR.mkdir(exist_ok=True)

faiss.write_index(
    index,
    str(VECTOR_DIR / "index.faiss")
)

print("FAISS index saved.")
with open(
    VECTOR_DIR / "metadata.pkl",
    "wb"
) as f:
    pickle.dump(catalog, f)

print("Metadata saved.")