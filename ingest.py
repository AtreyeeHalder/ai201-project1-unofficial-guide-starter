"""Ingestion + chunking

Pipeline stages covered here:

    documents/*.txt  --load-->  --clean-->  --chunk -->  chunks

Each document is a plain-text dump with a small header:

    SOURCE
    <url>

    ORIGINAL POST / CONTENT
    <body...>

    COMMENTS                # reddit threads only
    [-]author N days ago
    <comment text...>

We strip that scaffolding, normalise whitespace, then split the cleaned body
into chunks with an overlap, tokenising with the *same*
model that will embed the chunks (BAAI/bge-base-en-v1.5) so the token counts
are exactly what the embedder sees.

Run directly to ingest everything and print stats + 5 representative chunks,
which is the verification step.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List

from config import CHUNK_OVERLAP, CHUNK_SIZE, DOCUMENTS_DIR, EMBEDDING_MODEL


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class Chunk:
    """A single retrievable unit plus the metadata we'll need downstream."""

    text: str
    source_file: str
    url: str
    chunk_index: int          # position of this chunk within its document
    token_count: int
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Tokenizer (shared with the embedding model)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_tokenizer():
    """Load the bge tokenizer once, via sentence-transformers.

    We reuse the embedding model's own tokenizer so a chunk is
    measured in the same units the model will encode. sentence-transformers is
    already a project dependency and exposes the underlying HuggingFace fast
    tokenizer as `model.tokenizer`, so there's nothing extra to install.
    """
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL).tokenizer


# ---------------------------------------------------------------------------
# Stage 1: Load
# ---------------------------------------------------------------------------
def load_documents(documents_dir=DOCUMENTS_DIR) -> List[dict]:
    """Read every .txt file in documents/ and split off the SOURCE header.

    Returns a list of {"source_file", "url", "raw_body"} dicts.
    """
    documents = []
    for path in sorted(documents_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        url, body = _split_source_header(text)
        documents.append(
            {"source_file": path.name, "url": url, "raw_body": body}
        )
    return documents


def _split_source_header(text: str) -> tuple[str, str]:
    """Pull the URL out of the leading `SOURCE\\n<url>` block.

    Returns (url, remaining_body). If no SOURCE header is present we treat the
    whole file as the body and leave the URL blank.
    """
    lines = text.splitlines()
    url = ""
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip().upper() == "SOURCE":
            # The next non-empty line is the URL.
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    url = lines[j].strip()
                    body_start = j + 1
                    break
            break
    body = "\n".join(lines[body_start:])
    return url, body


# ---------------------------------------------------------------------------
# Stage 2: Clean
# ---------------------------------------------------------------------------

# Section markers that are scaffolding, not content.
_SECTION_MARKERS = re.compile(
    r"^\s*(ORIGINAL POST|COMMENTS|CONTENT)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# Reddit comment author/timestamp lines, e.g.
#   "[-]Voice_Educational 6 days ago"
#   "[-]Effective_Ring2855Chem Eng '29 6 days ago"
# The opening bracket uses an en-dash in the source files, so we accept any of
# en-dash / em-dash / hyphen / plus.
_REDDIT_AUTHOR_LINE = re.compile(
    r"^\s*\[[–—\-+]\].*?\bago\s*$",
    re.MULTILINE,
)

# "submitted 6 days ago by SomeUser" lines under the original post.
_SUBMITTED_LINE = re.compile(
    r"^\s*submitted\b.*\bago\b.*$",
    re.MULTILINE | re.IGNORECASE,
)

# Leftover OP markers like "[S]" embedded in author lines we may have kept.
_OP_MARKER = re.compile(r"\[S\]")

# 3+ consecutive newlines collapse to a paragraph break.
_EXTRA_BLANK_LINES = re.compile(r"\n{3,}")

# Trailing whitespace on each line.
_TRAILING_WS = re.compile(r"[ \t]+$", re.MULTILINE)


def clean_text(body: str) -> str:
    """Strip header scaffolding and reddit metadata, normalise whitespace.

    This keeps the substance of each post/comment (the part worth embedding)
    while dropping usernames, timestamps, and section labels that would only
    add noise to the vectors.
    """
    cleaned = body
    cleaned = _SECTION_MARKERS.sub("", cleaned)
    cleaned = _REDDIT_AUTHOR_LINE.sub("", cleaned)
    cleaned = _SUBMITTED_LINE.sub("", cleaned)
    cleaned = _OP_MARKER.sub("", cleaned)
    cleaned = _TRAILING_WS.sub("", cleaned)
    cleaned = _EXTRA_BLANK_LINES.sub("\n\n", cleaned)
    return cleaned.strip()


# ---------------------------------------------------------------------------
# Stage 3: Chunk
# ---------------------------------------------------------------------------
def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """Split `text` into ~`chunk_size`-token chunks overlapping by `overlap`.

    We tokenise once with offset mapping, then slice the *original* text at the
    character offsets of each token window. Slicing the source string (rather
    than decoding token ids) keeps the chunk text byte-for-byte faithful — no
    word-piece artifacts like "commut ##ing".
    """
    if not text.strip():
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    tokenizer = get_tokenizer()
    encoding = tokenizer(
        text,
        add_special_tokens=False,
        return_offsets_mapping=True,
    )
    offsets = encoding["offset_mapping"]
    n_tokens = len(offsets)

    if n_tokens <= chunk_size:
        return [text.strip()]

    step = chunk_size - overlap
    chunks: List[str] = []
    start = 0
    while start < n_tokens:
        end = min(start + chunk_size, n_tokens)
        char_start = offsets[start][0]
        char_end = offsets[end - 1][1]
        chunk = text[char_start:char_end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n_tokens:
            break
        start += step
    return chunks


def count_tokens(text: str) -> int:
    """Token count under the embedding model's tokenizer."""
    return len(get_tokenizer()(text, add_special_tokens=False)["input_ids"])


# ---------------------------------------------------------------------------
# Orchestration: load -> clean -> chunk -> Chunk objects
# ---------------------------------------------------------------------------
def build_chunks(documents_dir=DOCUMENTS_DIR) -> List[Chunk]:
    """Run the full ingestion + chunking pipeline over documents/."""
    chunks: List[Chunk] = []
    for doc in load_documents(documents_dir):
        cleaned = clean_text(doc["raw_body"])
        for idx, piece in enumerate(chunk_text(cleaned)):
            chunks.append(
                Chunk(
                    text=piece,
                    source_file=doc["source_file"],
                    url=doc["url"],
                    chunk_index=idx,
                    token_count=count_tokens(piece),
                    metadata={
                        "source_file": doc["source_file"],
                        "url": doc["url"],
                        "chunk_index": idx,
                    },
                )
            )
    return chunks


# ---------------------------------------------------------------------------
# Verification entry point
# ---------------------------------------------------------------------------
def _print_report(chunks: List[Chunk]) -> None:
    if not chunks:
        print("No chunks produced — is documents/ empty?")
        return

    token_counts = [c.token_count for c in chunks]
    n_docs = len({c.source_file for c in chunks})
    print("=" * 70)
    print("INGESTION + CHUNKING REPORT")
    print("=" * 70)
    print(f"Documents ingested : {n_docs}")
    print(f"Total chunks       : {len(chunks)}")
    print(f"Chunk size target  : {CHUNK_SIZE} tokens (overlap {CHUNK_OVERLAP})")
    print(
        f"Tokens per chunk   : min {min(token_counts)} / "
        f"avg {sum(token_counts) // len(token_counts)} / max {max(token_counts)}"
    )
    print("\nChunks per document:")
    per_doc: dict[str, int] = {}
    for c in chunks:
        per_doc[c.source_file] = per_doc.get(c.source_file, 0) + 1
    for name, count in sorted(per_doc.items()):
        print(f"  {count:>3}  {name}")

    print("\n" + "=" * 70)
    print("5 REPRESENTATIVE CHUNKS")
    print("=" * 70)
    n = len(chunks)
    sample_idxs = sorted({round(i * (n - 1) / 4) for i in range(5)}) if n > 1 else [0]
    samples = [chunks[i] for i in sample_idxs]
    for c in samples:
        # Show the full chunk
        preview = c.text
        print(
            f"\n[{c.source_file} #{c.chunk_index} | {c.token_count} tokens | "
            f"{len(c.text)} chars]\n"
            f"{c.url}\n"
            f"{'-' * 70}\n"
            f"{preview}"
        )


def main() -> None:
    chunks = build_chunks()
    _print_report(chunks)


if __name__ == "__main__":
    main()
