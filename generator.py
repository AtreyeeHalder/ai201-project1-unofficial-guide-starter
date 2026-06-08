"""Generation — grounded answer synthesis over retrieved context.

Pipeline stage covered here (see assets/Architecture Mermaid diagram.png):

    Stage 5  Generation
        query + retrieved chunks --> Groq llama-3.3-70b-versatile --> answer
        answer + chunk metadata  --> response (answer + source list)

Grounding is enforced by TWO independent mechanisms, not by trusting the LLM:

  1. Structural gate (in code, before the model is ever called):
     retrieved chunks are filtered by cosine distance (RELEVANCE_MAX_DISTANCE).
     If nothing survives, we return the refusal string and never call Groq —
     the model literally cannot answer from context that isn't there.

  2. Prompt contract: the only knowledge the model is given is the numbered
     context block. The system prompt forbids outside knowledge and requires
     the exact refusal string when the context is insufficient.

Source attribution is PROGRAMMATICALLY guaranteed: the "Sources" list is built
in Python from the retrieved chunks' metadata (source_file + url), deduplicated
in rank order. We never parse citations out of the model's prose, so attribution
can't be dropped, hallucinated, or mis-formatted by the LLM. (The prompt still
asks the model to cite inline [1]/[2] markers for readability, but those are a
convenience layered on top of the guaranteed list — not the source of truth.)

Run directly to test grounded generation end-to-end. With no arguments it
exercises all 5 in-domain Evaluation Plan queries plus 1 out-of-domain query
that should trigger a refusal. Pass one or more questions on the command line
to test those instead, e.g.:

    python generator.py "When is Hoboken street parking free?"
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Optional
from urllib.parse import urlparse

from config import (
    GENERATION_MAX_TOKENS,
    GENERATION_MODEL,
    GENERATION_TEMPERATURE,
    INSUFFICIENT_CONTEXT_REPLY,
    RELEVANCE_MAX_DISTANCE,
    TOP_K,
)
from retriever import RetrievedChunk, retrieve

# ---------------------------------------------------------------------------
# The grounding contract
# ---------------------------------------------------------------------------
# Written as hard rules ("MUST", "ONLY", "EXACTLY"), not suggestions. The model
# is told the context is its *entire* world and given an exact escape hatch so a
# refusal is detectable in code (see _is_refusal).
SYSTEM_PROMPT = f"""You are the Unofficial Guide, a question-answering assistant for commuter \
students at Stevens Institute of Technology. You answer using ONLY the numbered \
context passages provided in each user message. These passages are drawn from \
unofficial student sources (mostly Reddit threads).

Hard rules:
1. Use ONLY information found in the provided context passages. Do NOT use any \
prior or outside knowledge, and do NOT guess or infer beyond what the passages say.
2. If the context passages do not contain enough information to answer the \
question, reply with EXACTLY this sentence and nothing else: \
"{INSUFFICIENT_CONTEXT_REPLY}"
3. The sources are unofficial student opinions and may conflict or be out of \
date. When passages disagree, briefly reflect the disagreement rather than \
presenting one opinion as settled fact.
4. Cite the passages you used inline with their bracketed numbers, e.g. [1], [3]. \
Cite only passages you actually drew from.
5. Be concise and specific. Do not invent a "Sources" section yourself; sources \
are attached automatically after your answer."""

USER_PROMPT_TEMPLATE = """Context passages:
{context}

Question: {question}

Answer using only the context passages above. If they do not contain enough \
information, reply with exactly: "{refusal}\""""


# ---------------------------------------------------------------------------
# Human-readable source labels
# ---------------------------------------------------------------------------
# The chunk metadata carries the .txt filename, but a reader wants a label that
# describes the page the link actually opens. We derive that from the URL.
_SITE_NAMES = {
    "reddit.com": "Reddit",
    "apartments.com": "Apartments.com",
    "walkscore.com": "Walk Score",
}


def _humanize(slug: str) -> str:
    """Turn a URL slug like 'how_is_stevens_for_a_commuter' into a title."""
    return slug.replace("-", " ").replace("_", " ").strip().title()


def source_label(url: str, fallback_file: str) -> str:
    """Build a human-readable label describing where `url` leads.

    Derived from the URL so the link text matches the link target:
      reddit thread  -> 'Reddit r/stevens — How Is Stevens For A Commuter'
      other sites    -> 'Walk Score — Hoboken'
    Falls back to a cleaned-up filename when no URL is available.
    """
    if not url:
        name = fallback_file[:-4] if fallback_file.endswith(".txt") else fallback_file
        return _humanize(name)

    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    site = _SITE_NAMES.get(domain, domain)
    parts = [p for p in parsed.path.split("/") if p]

    # Reddit thread URL: /r/<sub>/comments/<id>/<title-slug>/
    if "reddit.com" in domain and "comments" in parts:
        i = parts.index("comments")
        slug = parts[i + 2] if len(parts) > i + 2 else ""
        sub = f"r/{parts[1]}" if len(parts) > 1 and parts[0] == "r" else ""
        head = f"{site} {sub}".strip()
        return f"{head} — {_humanize(slug)}" if slug else head

    # Any other site: site name + the last (most specific) path segment.
    return f"{site} — {_humanize(parts[-1])}" if parts else site


# ---------------------------------------------------------------------------
# Result data model
# ---------------------------------------------------------------------------
@dataclass
class Source:
    """One attributed source, built from chunk metadata (not from the LLM)."""

    source_file: str
    url: str


@dataclass
class GeneratedAnswer:
    """The full result of a grounded query."""

    answer: str
    sources: List[Source] = field(default_factory=list)
    used_chunks: List[RetrievedChunk] = field(default_factory=list)
    answered: bool = True  # False when we refused (no usable context / refusal reply)

    def to_markdown(self) -> str:
        """Render answer + programmatic source list as markdown for display."""
        if not self.answered or not self.sources:
            return self.answer
        lines = [self.answer, "", "**Sources**"]
        for i, src in enumerate(self.sources, start=1):
            label = source_label(src.url, src.source_file)
            lines.append(f"{i}. [{label}]({src.url})" if src.url else f"{i}. {label}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Groq client (shared singleton)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_client():
    """Initialise the Groq client from GROQ_API_KEY in the environment / .env."""
    from dotenv import load_dotenv
    from groq import Groq

    load_dotenv()  # reads .env if present; real env vars take precedence
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your "
            "free Groq key from https://console.groq.com"
        )
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# Context formatting + source attribution (both done in code, not by the LLM)
# ---------------------------------------------------------------------------
def build_context(chunks: List[RetrievedChunk]) -> str:
    """Format retrieved chunks into a numbered context block.

    Numbering here is what the model cites inline ([1], [2], ...) and lines up
    1:1 with the chunk order, so the deduplicated source list stays consistent
    with anything the model references.
    """
    blocks = []
    for i, c in enumerate(chunks, start=1):
        blocks.append(f"[{i}] (source: {c.source_file})\n{c.text}")
    return "\n\n".join(blocks)


def attribute_sources(chunks: List[RetrievedChunk]) -> List[Source]:
    """Build the source list straight from chunk metadata, deduped in rank order.

    This is the guarantee: attribution is derived from what retrieval returned,
    independent of whatever the model wrote.
    """
    seen = set()
    sources: List[Source] = []
    for c in chunks:
        key = c.source_file
        if key in seen:
            continue
        seen.add(key)
        sources.append(Source(source_file=c.source_file, url=c.url))
    return sources


def _is_refusal(answer: str) -> bool:
    """Detect the model emitting the exact insufficient-context reply."""
    normalized = answer.strip().rstrip(".").lower()
    return normalized == INSUFFICIENT_CONTEXT_REPLY.rstrip(".").lower()


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
def generate_answer(
    query: str,
    chunks: Optional[List[RetrievedChunk]] = None,
    top_k: int = TOP_K,
    max_distance: float = RELEVANCE_MAX_DISTANCE,
) -> GeneratedAnswer:
    """Answer `query` grounded strictly in retrieved context.

    Mechanism 1 (structural gate): retrieve, then drop chunks whose cosine
    distance exceeds `max_distance`. If none remain, refuse WITHOUT calling the
    LLM — there is no grounded answer to give.

    Mechanism 2 (prompt contract): pass only the surviving chunks as numbered
    context and instruct the model to answer solely from them.

    Source attribution is then attached programmatically from the chunks used.
    """
    if chunks is None:
        chunks = retrieve(query, top_k=top_k)

    # Mechanism 1: structural relevance gate.
    relevant = [c for c in chunks if c.distance <= max_distance]
    if not relevant:
        return GeneratedAnswer(
            answer=INSUFFICIENT_CONTEXT_REPLY,
            sources=[],
            used_chunks=[],
            answered=False,
        )

    # Mechanism 2: grounded prompt over the surviving context only.
    context = build_context(relevant)
    user_message = USER_PROMPT_TEMPLATE.format(
        context=context,
        question=query,
        refusal=INSUFFICIENT_CONTEXT_REPLY,
    )

    response = get_client().chat.completions.create(
        model=GENERATION_MODEL,
        temperature=GENERATION_TEMPERATURE,
        max_tokens=GENERATION_MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    answer = response.choices[0].message.content.strip()

    # If the model refused, don't attach sources to a non-answer.
    if _is_refusal(answer):
        return GeneratedAnswer(
            answer=INSUFFICIENT_CONTEXT_REPLY,
            sources=[],
            used_chunks=[],
            answered=False,
        )

    # Programmatic source attribution from the chunks we actually grounded on.
    return GeneratedAnswer(
        answer=answer,
        sources=attribute_sources(relevant),
        used_chunks=relevant,
        answered=True,
    )


def answer_query(query: str) -> str:
    """Convenience wrapper used by the UI: returns ready-to-display markdown."""
    return generate_answer(query).to_markdown()


# ---------------------------------------------------------------------------
# Verification entry point — grounded generation on in-domain + out-of-domain queries
# ---------------------------------------------------------------------------
# All 5 in-domain queries from the Evaluation Plan, plus one deliberately
# out-of-domain question the corpus doesn't cover — the system should refuse
# ("I don't have enough information on that.") rather than answer from general
# knowledge. This exercises both the relevance gate and the prompt contract.
_VERIFICATION_QUERIES = [
    "How much does the Stevens shuttle cost?",
    "What are the disadvantages of parking with a temporary Hoboken pass?",
    "When is Hoboken street parking free?",
    "What is the walkability or walk score of Hoboken?",
    "Will changing from dorming to commuting affect my financial aid package?",
    "How much is it going to rain tomorrow in Hoboken on June 8, 2026?",
]


def _print_generation_report(queries: List[str]) -> None:
    print("=" * 70)
    print("GROUNDED GENERATION REPORT")
    print("=" * 70)
    print(f"Generation model : {GENERATION_MODEL} (Groq)")
    print(f"Temperature      : {GENERATION_TEMPERATURE}")
    print(f"Relevance gate   : distance <= {RELEVANCE_MAX_DISTANCE}")

    for query in queries:
        result = generate_answer(query)
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        print(result.to_markdown())
        if result.used_chunks:
            dists = ", ".join(f"{c.distance:.3f}" for c in result.used_chunks)
            print(f"\n[grounded on {len(result.used_chunks)} chunks | distances: {dists}]")


def main() -> None:
    # Any questions passed on the command line override the default suite, so you
    # can spot-check a single Evaluation Plan question (or anything else) without
    # editing this file.
    queries = sys.argv[1:] or _VERIFICATION_QUERIES
    _print_generation_report(queries)


if __name__ == "__main__":
    main()
