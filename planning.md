# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

I chose the domain "Stevens Institute of Technology Commuter Guide" which covers the practical realities and tips for commuter students at my university from unofficial sources. This knowledge is valuable and hard to find through official channels because they cover general information such as permit prices and transit links, but they do not capture the lived experiences that drive commuter decisions, such as overnight parking locations, commute accessibility, and pros and cons of commuting vs dorming. Personal, specific questions about these experiences and the tradeoffs associated can be answered only by students who have lived through them. Sources about the campus area could also be useful information.

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

**Chunk size:** 175 tokens

**Overlap:** 40 tokens

**Reasoning:** The corpus is review and discussion-heavy since it is mostly composed of Reddit threads. Almost every comment in a thread is a complete, retrievable thought, which can either be a few sentences of a short review or a paragraph describing a personal experience. If the chunk size is too large, several unrelated comments may be included in a single embedding and the vector will not match any of those individual topics well. As a result, more specific, precise prompts may lead to a vague answer. If the chunk size is too small, embeddings may miss important context and be meaningless individually. As a result, answers may be hallucinated, fragmented or inaccurate due to the absence of surrounding context. I initially chose a medium chunk size of 400 tokens, but the corpus turned out to produce only 23 chunks as entire threads collapsed into a single embedding. I therefore decreased the chunk size to 175 tokens, which yields 55 chunks and lands each chunk on roughly one or two comments. Moreover, I chose a 40-token overlap since it is a small fraction of the chunk, and each chunk tends to capture a complete idea so a heavy overlap is not required to preserve meaning. Even if a small part of a thought gets split at a boundary when chunking, a small split idea remains intact and retrievable through the 40-token overlap.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `BAAI/bge-base-en-v1.5` via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** If I were deploying this for real users and cost were not a constraint, I would consider a stronger embedding model and weigh several tradeoffs.
- A larger or API model would better distinguish nuanced, contradicting student opinions than small local models, reducing off-topic retrieval and improving domain-specific text.
- I would also consider the latency vs. accuracy tradeoff since bigger, more accurate models are slower per query. I would weigh response time against retrieval quality.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How much does the Stevens shuttle cost? | It is free. |
| 2 | What are the disadvantages of parking with a temporary Hoboken pass? | It can be competitive, and the car should be moved for street cleaning every week or day depending on the parking spot. Oil changes cannot be done when parked on the street. |
| 3 | When is Hoboken street parking free? | It is free overnight, from 9 PM to 9 AM. |
| 4 | What is the walkability or walk score of Hoboken? | Any number between 97-100. |
| 5 | Will changing from dorming to commuting affect my financial aid package? | The financial aid package will likely not change since it is based on tuition only. However, it is best to call the school to confirm. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Noisy and contradictory documents:** Since the corpus is mostly Reddit threads, the same question gets many conflicting answers from different students. Retrieval may pull several contradictory chunks, and the generator could either pick one opinion as if it were fact or blend contradictory claims into an incoherent answer.

2. **Outdated advice:** Some of the advice may be from years ago that may not be accurate or relevant today. The system may generate the answer to a user query and cause a misunderstanding that the information is current.

3. **Off-topic retrieval and lost context from chunking thread comments:** Reddit threads mix jokes and replies that only make sense relative to context or a previous comment. Splitting them into chunks can sever a reply from the comment it answers. This may lead to off-topic answers.

4. **Chunking strategy may not fit all sources perfectly:** In addition to Reddit threads, the corpus also consists of Apartments.com and Walk Score sources, which are structured, fact-heavy pages. The chunk size is too big for sources like these, since it may merge unrelated surrounding text and produce inaccurate answers.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

![Architecture pipeline diagram](assets/Architecture%20Mermaid%20diagram.png)

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

**Milestone 3 — Ingestion and chunking:** I will give Claude Code my Documents, Chunking Strategy, and Architecture sections of the planning.md to implement chunk_text() with my specified chunk size and overlap. To verify the output, I will print 5 representative chunks and check if they are good chunks.

**Milestone 4 — Embedding and retrieval:** I will give Claude Code my Retrieval Approach section and pipeline diagram to implement embedding and retrieval with the embedding model `BAAI/bge-base-en-v1.5` via sentence-transformers, storing in ChromaDB with source metadata, and top-k value 5. To verify the output, I will test retrieval with 3 of my Evauation Plan queries, printing the returned chunks and their distance scores, and checking if the retrieved answers are relevant to the question.

**Milestone 5 — Generation and interface:**
