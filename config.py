"""The chunking numbers below come from the
Chunking Strategy section of planning.md.
"""

from pathlib import Path

# --- Paths -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
CHROMA_DIR = PROJECT_ROOT / "chroma"  # persistent vector store

# --- Chunking -----------------------------
# Measured in *tokens*, using the embedding model's own tokenizer so that
# "180 tokens" means exactly what the embedder will encode.
CHUNK_SIZE = 175        # tokens per chunk
CHUNK_OVERLAP = 40      # tokens shared between consecutive chunks

# --- Embedding + retrieval ----------------
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
COLLECTION_NAME = "unofficial_guide"
TOP_K = 5

# Cosine-distance gate for retrieved chunks
# bge vectors are normalised, so distance is in [0, 2]; closely related student
# comments land well under 0.5, clearly unrelated passages drift past ~0.8.
# Chunks above this distance are dropped *before* generation; if nothing
# survives the gate we refuse rather than letting the model improvise.
RELEVANCE_MAX_DISTANCE = 0.80

# --- Generation ---------------------------------
GENERATION_MODEL = "llama-3.3-70b-versatile"   # Groq, free-tier, OpenAI-compatible
GENERATION_TEMPERATURE = 0.1                    # low: factual, grounded answers
GENERATION_MAX_TOKENS = 600

# Exact string the model must emit when the context can't answer the question.
# Kept as a constant so the generator can detect a refusal and suppress source
# attribution programmatically (no point citing sources for a non-answer).
INSUFFICIENT_CONTEXT_REPLY = "I don't have enough information on that."
