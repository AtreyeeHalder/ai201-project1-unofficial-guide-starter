# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
I chose the domain "Stevens Institute of Technology Commuter Guide" which covers the practical realities and tips for commuter students at my university from unofficial sources. This knowledge is valuable and hard to find through official channels because they cover general information such as permit prices and transit links, but they do not capture the lived experiences that drive commuter decisions, such as overnight parking locations, commute accessibility, and pros and cons of commuting vs dorming. Personal, specific questions about these experiences and the tradeoffs associated can be answered only by students who have lived through them. Sources about the campus area could also be useful information.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 175 tokens

**Overlap:** 40 tokens

**Why these choices fit your documents:** The corpus is review and discussion-heavy since it is mostly composed of Reddit threads. Almost every comment in a thread is a complete, retrievable thought, which can either be a few sentences of a short review or a paragraph describing a personal experience. If the chunk size is too large, several unrelated comments may be included in a single embedding and the vector will not match any of those individual topics well. As a result, more specific, precise prompts may lead to a vague answer. If the chunk size is too small, embeddings may miss important context and be meaningless individually. As a result, answers may be hallucinated, fragmented or inaccurate due to the absence of surrounding context. I initially chose a medium chunk size of 400 tokens, but the corpus turned out to produce only 23 chunks as entire threads collapsed into a single embedding. I therefore decreased the chunk size to 175 tokens, which yields 55 chunks and lands each chunk on roughly one or two comments. Moreover, I chose a 40-token overlap since it is a small fraction of the chunk, and each chunk tends to capture a complete idea so a heavy overlap is not required to preserve meaning. Even if a small part of a thought gets split at a boundary when chunking, a small split idea remains intact and retrievable through the 40-token overlap.

**Preprocessing:**
- Removed boilerplate code such as comment counts, reply, report, etc. buttons
- Excluded ads
- Removed alt text of pictures which already have explanations
- regex stripping

**Final chunk count:** 55

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `BAAI/bge-base-en-v1.5` via sentence-transformers.
I chose this model mainly because it runs fully local and free. There is no API key, no per-call cost, and no network dependency for embedding. Moreover, it does not truncate larger overlap sizes and is mostly accurate.

**Production tradeoff reflection:** If I were deploying this for real users and cost were not a constraint, I would consider a stronger embedding model and weigh several tradeoffs.
- A larger or API model would better distinguish nuanced, contradicting student opinions than small local models, reducing off-topic retrieval and improving domain-specific text.
- I would also consider the latency vs. accuracy tradeoff since bigger, more accurate models are slower per query. I would weigh response time against retrieval quality.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The retriever returns the top-5 chunks by cosine distance, then `generate_answer()` drops every chunk whose distance exceeds `RELEVANCE_MAX_DISTANCE = 0.80`. If nothing survives the gate, the system returns the fixed refusal string `"I don't have enough information on that."` and never calls the model since it cannot answer from context that is not there. The surviving chunks are formatted into a numbered context block and passed with a system prompt written as hard rules. The instruction given to the model is:

> You are the Unofficial Guide, a question-answering assistant for commuter students at Stevens Institute of Technology. You answer using ONLY the numbered context passages provided in each user message. These passages are drawn from unofficial student sources (mostly Reddit threads).
>
> Hard rules:
> 1. Use ONLY information found in the provided context passages. Do NOT use any prior or outside knowledge, and do NOT guess or infer beyond what the passages say.
> 2. If the context passages do not contain enough information to answer the question, reply with EXACTLY this sentence and nothing else: "I don't have enough information on that."
> 3. The sources are unofficial student opinions and may conflict or be out of date. When passages disagree, briefly reflect the disagreement rather than presenting one opinion as settled fact.
> 4. Cite the passages you used inline with their bracketed numbers, e.g. [1], [3]. Cite only passages you actually drew from.
> 5. Be concise and specific. Do not invent a "Sources" section yourself; sources are attached automatically after your answer.

**How source attribution is surfaced in the response:** Attribution is derived in Python from the retrieved chunks' metadata. After generation, `attribute_sources()` walks the chunks that actually passed the relevance gate, deduplicates them by source file in rank order, and builds the `Sources` list directly from each chunk's `source_file` + `url`. This list is then rendered as a numbered, linked markdown footer beneath the answer. Because the list is built from what retrieval returned, not from what the LLM wrote, attribution cannot be dropped, hallucinated, or mis-formatted by the model. The inline `[1]`/`[2]` bracket markers the model is asked to produce (rule 4) line up with the numbered context block and exist only as a readability convenience layered on top of the guaranteed list; they are not the source of truth. When the system does not have enough information on a query, no sources are attached, since there is no grounded answer to cite.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How much does the Stevens shuttle cost? | It is free. | The Stevens shuttle is free [1]. (with links to sources) | Relevant (Distances of all 5 retrieved chunks are <0.5) | Accurate (Response matches expected answer) |
| 2 | What are the disadvantages of parking with a temporary Hoboken pass? | It can be competitive, and the car should be moved for street cleaning every week or day depending on the parking spot. Oil changes cannot be done when parked on the street. | The disadvantages of parking with a temporary Hoboken pass include it being competitive at times, having to move your car for street cleaning every week/day depending on where you park, and not being able to do oil changes or other maintenance when parked on the street [1], [4]. (with links to sources) | Relevant (Distances of all 5 retrieved chunks are <0.5) | Accurate (Response matches expected answer) |
| 3 | When is Hoboken street parking free? | It is free overnight, from 9 PM to 9 AM. | Hoboken street parking is free from 9pm to 9am (and on Sundays) [1], and meters aren’t checked overnight in metered zones off campus from 9pm until sometime in the morning [2]. (with links to sources) | Relevant (Distances of all 5 retrieved chunks are <0.5) | Partially accurate (It is not free on Sundays anymore for some streets. Generation failed here because of outdated advice) |
| 4 | What is the walkability or walk score of Hoboken? | Any number between 97-100. | The walkability or walk score of Hoboken is 97, indicating that Hoboken is a "Walker’s Paradise" where daily errands do not require a car [1]. This is consistently mentioned in multiple passages [1], [2], and [4] (with links to sources) | Relevant (Distances of all 5 retrieved chunks are <0.5) | Accurate (Response matches expected answer) |
| 5 | Will changing from dorming to commuting affect my financial aid package? | The financial aid package will likely not change since it is based on tuition only. However, it is best to call the school to confirm. | According to [1] and [2], changing from dorming to commuting may not affect your financial aid package, as financial aid is based on tuition only. However, [3] suggests that institutional aid may be reduced when switching to commuting. The extent of the reduction is unclear, as the user in [3] mentions they will call their financial aid counselor to determine the exact amount. Therefore, the impact on financial aid is somewhat uncertain, with [1] and [2] indicating no change, while [3] indicates a possible reduction. | Relevant (Distances of all 5 retrieved chunks are <0.5) | Accurate (Response matches expected answer and correctly shows uncertainty instead of confidently stating one answer as if it is a fact) |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** When is Hoboken street parking free?

**What the system returned:** Hoboken street parking is free from 9pm to 9am (and on Sundays) [1], and meters aren’t checked overnight in metered zones off campus from 9pm until sometime in the morning [2].

**Sources**
1. [Reddit r/stevens — Overnight Parking](https://www.reddit.com/r/stevens/comments/p5on9u/overnight_parking/)
2. [Reddit r/stevens — Where Can I Park Overnight For Free](https://www.reddit.com/r/stevens/comments/1g8gnag/where_can_i_park_overnight_for_free/)
3. [Reddit r/stevens — Offcampus Parking Situation](https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/)
4. [Walk Score — Hoboken](https://www.walkscore.com/NJ/Hoboken)

[grounded on 5 chunks | distances: 0.303, 0.306, 0.324, 0.375, 0.380]

**Root cause (tied to a specific pipeline stage):** The root cause is in the cleaning step of the ingestion stage. The "free on Sundays" claim comes from an old Reddit comment for which the raw document contains a timestamp, but the regexes in the code strip those "... ago" lines as scaffolding noise before chunking. By the time the chunk reaches the embedder and the model, it no longer carries the date, so neither the relevance gate nor the LLM can tell an old claim from a current one. The model did exactly what rule 1 told it to (answer only from context) and confidently surfaced the outdated claim as fact.

**What you would change to fix it:** I would not discard the timestamp in `clean_text()`. Instead, I would parse the "submitted N years/months ago" line during cleaning, normalize it to an approximate date, and attach it to each `Chunk`'s metadata alongside `source_file`/`url`. Then I would surface that age in the numbered context block passed to the model, and extend the system prompt so it flags stale or conflicting time-sensitive details (e.g. "this advice is several years old; verify current rules") and prefers the most recent passage when sources disagree.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The Architecture section of the planning.md helped me the most in shaping my implementation because I got an overview of what the RAG pipeline should look like in context of my domain. I was able to make a concrete plan of what tools I would be using at every stage of the pipeline. This helped me make decisions and tradeoffs more effectively, and prompt those specifications more precisely when I used AI to assist me with coding.

**One way your implementation diverged from the spec, and why:** In the Chunking Strategy of the planning.md, I initially chose a medium chunk size of 400 tokens because I neither wanted too large, vague chunks nor too small chunks with missing context. However, when I ran the ingestion and chunking code for verification, the corpus turned out to produce only 23 chunks as entire threads collapsed into a single embedding. I therefore decreased the chunk size to 175 tokens, which yields 55 chunks and lands each chunk on roughly one or two comments.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude Code my Documents, Chunking Strategy, and Architecture sections of the planning.md to implement chunk_text() with my specified chunk size (400 initially) and overlap.
- *What it produced:* It generated the ingestion and chunking code within ingest.py using the chunk size and overlap initially mentioned in planning.md, putting these values in config.py
- *What I changed or overrode:* To verify the output, I printed 5 representative chunks and checked if they are good chunks. I overrode the chunk size from 400 to 175 because the total chunks were initially only 23 across 12 documents, so I realized my chunk size may be too large. With a chunk size of 175, the total chunks are now 55.

**Instance 2**

- *What I gave the AI:* I gave Claude Code my planning.md pipeline diagram to generate the generation and interface code with my grounding requirement (answering only from document context), the output format, and Gradio web UI skeleton structure for the query interface. The LLM used for this step will be Groq's `llama-3.3-70b-versatile`.
- *What it produced:* It generated the generation and interface code within generator.py using my grounding requirements to construct the system prompt and the Gradio web UI within app.py
- *What I changed or overrode:* To verify the output, I tested grounded generation end-to-end on 3 queries. A few seconds elapsed between the user entering the query and the LLM generating the output in the UI, but there was no visible loading signal during that time, which might have led to the user thinking the system was frozen. So, I asked Claude Code to add a feature where a loading message is shown at that time.
