# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

I chose the domain "Stevens Institute of Technology Commuter Guide" which covers the practical realities and tips for commuter students at my university from unofficial sources. This knowledge is valuable and hard to find through official channels because they cover general information such as permit prices and transit links, but they do not capture the lived experiences that drive commuter decisions, such as overnight parking locations, commute accessibility, and pros and cons of commuting vs dorming. Personal, specific questions about these experiences and the tradeoffs associated can be answered only by students who have lived through them. Sources about the area could also be useful information.

---

## Documents



| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Student discussion about the overall commuter experience at Stevens, including campus culture, social life, scheduling, and challenges faced by commuters. | https://www.reddit.com/r/stevens/comments/1tt8xaw/how_is_stevens_for_a_commuter/ |
| 2 | Reddit | Advice comparing living near campus versus commuting, with insights into travel times, costs, and student preferences. | https://www.reddit.com/r/stevens/comments/1rlx081/housingcommute_advice/ |
| 3 | Reddit | Discussion weighing the pros and cons of dorming versus commuting, including social opportunities, convenience, and financial considerations. | https://www.reddit.com/r/stevens/comments/1s0tapv/dorm_or_commute/ |
| 4 | Reddit | Community recommendations and experiences regarding free overnight parking options near Stevens and Hoboken. | https://www.reddit.com/r/stevens/comments/1g8gnag/where_can_i_park_overnight_for_free/ |
| 5 | Reddit | Information about parking availability, permits, pricing, and challenges for students commuting by car. | https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/ |
| 6 | Reddit | Older discussion covering overnight parking rules, permits, and alternative parking arrangements around campus. | https://www.reddit.com/r/stevens/comments/p5on9u/overnight_parking/ |
| 7 | Apartments.com | Overview of off-campus housing options near Stevens, including rental costs, neighborhoods, and apartment availability. | https://www.apartments.com/local-guide/off-campus-housing/nj/hoboken/stevens-institute-of-technology/ |
| 8 | Walk Score | Quantitative data on walkability, transit accessibility, and bike-friendliness of Hoboken, useful for evaluating commuting options. | https://www.walkscore.com/NJ/Hoboken |
| 9 | Reddit | Student experiences and administrative considerations when switching from residential to commuter status. | https://www.reddit.com/r/stevens/comments/acryhw/change_dorming_to_commuting/ |
| 10 | Reddit | Information about obtaining and using NJ Transit student discounts, passes, and commuter benefits. | https://www.reddit.com/r/stevens/comments/1f54e7d/nj_transit_student_pass_assistance_needed/ |
| 11 | Reddit | Discussion of commuting between New York City and Stevens, including PATH, NJ Transit, travel times, and convenience. | https://www.reddit.com/r/stevens/comments/1hwd40y/nyc_access/ |
| 12 | Reddit | Student perspectives on campus safety, the surrounding Hoboken neighborhood, walking at night, and general safety considerations for commuters traveling to and from campus | https://www.reddit.com/r/stevens/comments/14rt7wy/how_safe_is_the_campus_and_neighbourhood/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 400 tokens

**Overlap:** 50 tokens

**Reasoning:** The corpus is review and disussion-heavy since it is mostly composed of Reddit threads. Almost every comment in a thread is a complete, retrievable thought, which can either be a few sentences or a paragraph. Thus, I picked a medium chunk size: 400. If the chunk size is too large, several unrelated comments may be included in a single embedding and the vector will not match any of those individual topics well. As a result, more specific, precise prompts may lead to a vague answer. If the chunk size is too small, embeddings may miss important context and be meaningless individually. As a result, answers may be hallucinated, fragmented or inaccurate due to the absence of surrounding context.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
