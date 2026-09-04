import faiss
import numpy as np
import pickle
import os
from chunking.embedder import generate_embeddings

INDEX_PATH = "repo.index"
METADATA_PATH = "metadata.pkl"


def store_chunks(chunks, embeddings):
    embedding_matrix = np.array(embeddings).astype("float32")

    dim = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embedding_matrix)

    faiss.write_index(index, INDEX_PATH)

    metadata = []
    for chunk in chunks:
        metadata.append({
            "content": chunk["content"],
            "file_path": chunk["file_path"],
            "file_name": chunk["file_name"],
            "chunk_id": chunk["chunk_id"]
        })

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Stored {len(chunks)} chunks in FAISS")


def search_chunks_by_embedding(query_embedding, top_k=5):
    if not os.path.exists(INDEX_PATH):
        return []

    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results



def search_chunks(query: str, top_k=5):

    embedding = generate_embeddings(query)

    return search_chunks_by_embedding(
        embedding,
        top_k
    )