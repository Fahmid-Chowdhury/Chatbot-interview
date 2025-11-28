# build_vector_db.py

import json
from pathlib import Path

import chromadb
from embedder import Embedder


def build_vector_db(
    json_path: str = "data/policy_chunks_ocr.json",
    persist_dir: str = "chroma_db",
    collection_name: str = "policy_chunks",
):
    """
    1. Load extracted policy chunks from JSON.
    2. Embed all texts using Embedder.
    3. Store in ChromaDB using PersistentClient.
    """

    # --- Load chunks from JSON ---
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("No chunks found in JSON. Did you run the PDF extractor first?")

    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    metadatas = [{"page": c["page"]} for c in chunks]

    print(f"Loaded {len(chunks)} chunks from {json_path}")

    # --- Embed texts ---
    embedder = Embedder()
    print("Embedding texts...")
    embeddings = embedder.embed_many(texts)
    print("Done embedding.")

    # --- Init Chroma using the NEW API (PersistentClient) ---
    # This avoids the deprecated 'Client(Settings(...))' setup.
    client = chromadb.PersistentClient(path=persist_dir)

    collection = client.get_or_create_collection(
        name=collection_name,
        # You could optionally specify an embedding_function here
        # but we're passing embeddings manually.
    )

    # Optional: clear existing data in this collection
    count_before = collection.count()
    if count_before > 0:
        print(f"Collection already has {count_before} documents. Deleting them...")
        existing = collection.get()
        if existing and existing.get("ids"):
            collection.delete(ids=existing["ids"])

    # --- Add documents to collection ---
    print("Adding embeddings to Chroma collection...")
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Vector DB built successfully.\n"
        f"- Persist directory: {persist_dir}\n"
        f"- Collection name:   {collection_name}\n"
        f"- Documents stored:  {collection.count()}"
    )


if __name__ == "__main__":
    build_vector_db()
