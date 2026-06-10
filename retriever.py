"""Embedding + Vector Store + Retrieval

Pipeline stages covered here (see assets/Architecture Mermaid diagram.png):

    Stage 3  Embedding + Vector Store
        chunks --embed(BAAI/bge-base-en-v1.5)--> vectors
        vectors + metadata --> ChromaDB (persistent)

    Stage 4  Retrieval
        user query --embed--> similarity search (top-k = 5) --> chunks

The chunks come straight from the ingestion pipeline in ingest.build_chunks(),
so the same cleaning + chunking decisions made in Milestone 3 flow through
unchanged. We embed each chunk with sentence-transformers, store the vectors in
a persistent ChromaDB collection alongside the source metadata (source_file,
url, chunk_index), and expose retrieve() for the generation step downstream.

Run directly to (re)build the index and verify retrieval against 3 of the
Evaluation Plan questions, printing the returned chunks and their distances.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import List

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)
from ingest import Chunk, build_chunks

# bge models are trained with an asymmetric retrieval objective: passages are
# embedded as-is, but *queries* are prefixed with a short instruction. Skipping
# this prefix measurably hurts recall, so we apply it to every query embedding.
# (Passages/chunks are embedded without any prefix.)
BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "


# ---------------------------------------------------------------------------
# Result data model
# ---------------------------------------------------------------------------
@dataclass
class RetrievedChunk:
    """One hit from a similarity search, with everything generation needs."""

    text: str
    source_file: str
    url: str
    chunk_index: int
    distance: float  # cosine distance; lower = more similar


# ---------------------------------------------------------------------------
# Embedding model (shared singleton)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_embedder():
    """Load BAAI/bge-base-en-v1.5 once via sentence-transformers."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL)


def embed_passages(texts: List[str]) -> List[List[float]]:
    """Embed chunk texts for storage. Normalised so cosine distance is valid."""
    model = get_embedder()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=len(texts) > 1,
    )
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a single query, applying the bge retrieval instruction prefix."""
    model = get_embedder()
    vector = model.encode(
        BGE_QUERY_INSTRUCTION + query,
        normalize_embeddings=True,
    )
    return vector.tolist()


# ---------------------------------------------------------------------------
# Stage 3: Vector store (ChromaDB, persistent)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_collection():
    """Return the persistent ChromaDB collection, creating it if absent.

    We pin the index to cosine space because bge vectors are normalised and the
    model is tuned for cosine similarity. We do NOT attach a Chroma embedding
    function: embeddings are computed explicitly with our bge model (and the
    query instruction prefix) and passed in, so retrieval stays under our
    control rather than Chroma's default all-MiniLM.
    """
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def _chunk_id(chunk: Chunk) -> str:
    """Stable, unique id for a chunk: '<source_file>::<chunk_index>'."""
    return f"{chunk.source_file}::{chunk.chunk_index}"


def build_index(rebuild: bool = False) -> int:
    """Embed all chunks from the ingestion pipeline and store them in Chroma.

    Idempotent: if the collection already holds the expected number of chunks
    and `rebuild` is False, we skip the (slow) re-embedding. Pass rebuild=True
    after changing the corpus or chunking strategy to force a fresh index.

    Returns the number of chunks in the collection.
    """
    import chromadb

    chunks = build_chunks()
    if not chunks:
        raise RuntimeError("No chunks produced — is documents/ empty?")

    collection = get_collection()

    if rebuild and collection.count() > 0:
        # Drop and recreate so stale vectors don't linger.
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        client.delete_collection(COLLECTION_NAME)
        get_collection.cache_clear()
        collection = get_collection()

    if not rebuild and collection.count() == len(chunks):
        return collection.count()

    embeddings = embed_passages([c.text for c in chunks])
    collection.add(
        ids=[_chunk_id(c) for c in chunks],
        documents=[c.text for c in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "source_file": c.source_file,
                "url": c.url,
                "chunk_index": c.chunk_index,
                "token_count": c.token_count,
            }
            for c in chunks
        ],
    )
    return collection.count()


# ---------------------------------------------------------------------------
# Stage 4: Retrieval
# ---------------------------------------------------------------------------
def retrieve(query: str, top_k: int = TOP_K) -> List[RetrievedChunk]:
    """Return the `top_k` chunks most similar to `query`.

    Embeds the query with the bge instruction prefix, then runs a cosine
    similarity search over the stored chunk vectors. Auto-builds the index on
    first use so callers don't have to remember to run build_index() first.
    """
    collection = get_collection()
    if collection.count() == 0:
        build_index()
        collection = get_collection()

    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=top_k,
    )

    # Chroma nests every field one level deep (one list per query); we sent one
    # query, so we unwrap index 0.
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return [
        RetrievedChunk(
            text=doc,
            source_file=meta.get("source_file", ""),
            url=meta.get("url", ""),
            chunk_index=meta.get("chunk_index", -1),
            distance=dist,
        )
        for doc, meta, dist in zip(documents, metadatas, distances)
    ]


# ---------------------------------------------------------------------------
# Verification entry point
# ---------------------------------------------------------------------------
# All 5 questions from the Evaluation Plan in planning.md.
_VERIFICATION_QUERIES = [
    "How much does the Stevens shuttle cost?",
    "What are the disadvantages of parking with a temporary Hoboken pass?",
    "When is Hoboken street parking free?",
    "What is the walkability or walk score of Hoboken?",
    "Will changing from dorming to commuting affect my financial aid package?",
]


def _print_retrieval_report() -> None:
    count = build_index()
    print("=" * 70)
    print("EMBEDDING + RETRIEVAL REPORT")
    print("=" * 70)
    print(f"Embedding model : {EMBEDDING_MODEL}")
    print(f"Vector store    : ChromaDB @ {CHROMA_DIR}")
    print(f"Collection      : {COLLECTION_NAME} ({count} chunks)")
    print(f"Top-k           : {TOP_K}")

    for query in _VERIFICATION_QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        for rank, hit in enumerate(retrieve(query), start=1):
            print(
                f"\n[#{rank} | distance {hit.distance:.4f} | "
                f"{hit.source_file} chunk {hit.chunk_index}]\n"
                f"{hit.url}\n"
                f"{'-' * 70}\n"
                f"{hit.text}"
            )


def main() -> None:
    _print_retrieval_report()


if __name__ == "__main__":
    main()
