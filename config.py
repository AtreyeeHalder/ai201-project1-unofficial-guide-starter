"""The chunking numbers below come from the
Chunking Strategy section of planning.md.
"""

from pathlib import Path

# --- Paths -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
CHROMA_DIR = PROJECT_ROOT / "chroma"  # persistent vector store

# --- Chunking (planning.md -> Chunking Strategy) -----------------------------
# Measured in *tokens*, using the embedding model's own tokenizer so that
# "180 tokens" means exactly what the embedder will encode.
CHUNK_SIZE = 175        # tokens per chunk
CHUNK_OVERLAP = 40      # tokens shared between consecutive chunks

# --- Embedding + retrieval (planning.md -> Retrieval Approach) ----------------
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
COLLECTION_NAME = "unofficial_guide"
TOP_K = 5
