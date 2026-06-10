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

**5 Representative Chunks**

======================================================================
5 REPRESENTATIVE CHUNKS
======================================================================

[apartments_com.txt #0 | 175 tokens | 922 chars]
https://www.apartments.com/local-guide/off-campus-housing/nj/hoboken/stevens-institute-of-technology/
----------------------------------------------------------------------
Innovation is at the core of Stevens Institute of Technology, established in 1870 by America’s First Family of Inventors. Stevens is now a premier private research university recognized for its unique curriculum blending technical training, teamwork, design projects, internships, and cooperative education opportunities. Graduates of SIT are consistently in high demand by employers seeking highly prepared and solutions-oriented employees. The SIT campus is nearby a wide range of apartments available for rent in Hoboken and surrounding cities such as Jersey City, Union City, North Bergen, Weehawken, Secaucus, and Bayonne. Public transportation with access to Hoboken is available in most surrounding cities, via the PATH, Light Rail, or bus system. Stevens also provides free campus shuttle service to and from each Hoboken station. In addition to stunning views of the Manhattan skyline, the SIT campus is rich with

[reddit_dorm_vs_commute.txt #0 | 175 tokens | 688 chars]
https://www.reddit.com/r/stevens/comments/1s0tapv/dorm_or_commute/
----------------------------------------------------------------------
Dorm or commute

I got accepted to the class of 2030, Im not sure if it is required to dorm or not for incoming freshmans, but in the case that it isnt required, would it be better for me to commute.

With dorming, tuition would be ≈28,500k, without dorming it would be ≈ 7,700k

My I live in Bergen county, and I have a train station in my area readily available, and it would like a 1 hour commute via train or a 40 minute car ride, which I can also do, due to having a license/car.

Im just stuck on this decision because its so stupid but I really want a cat and my mom promised me one if i commit to stevens (which i do want to go to as wel, I got in for Engineering undecidedbut ill

[reddit_housing_commute.txt #6 | 175 tokens | 622 chars]
https://www.reddit.com/r/stevens/comments/1rlx081/housingcommute_advice/
----------------------------------------------------------------------
's gonna be traffic. I'm currently commuting from Bridgeport CT, which is a 3 hr commute ( drive to train station -> train to GCT -> shuttle to times square -> walk to PATH -> 126 to Hoboken -> walk to campus ), for a total commute of 6h back n forth. Now nobody sane should ever do this, but if i can handle a 6 hr commute, you can definitely do a 25.-3hr twice/three times a week :P

Best of luck!

P.S. You probably saw i didn't even mention renting, as a 1 bedroom within walking distance of campus, say ~15 mins, will run you like 2.5k. Your 1k is a literal dream

omg a 3 hour commute is insane ur a trooper for that

[reddit_nyc_access.txt #3 | 141 tokens | 611 chars]
https://www.reddit.com/r/stevens/comments/1hwd40y/nyc_access/
----------------------------------------------------------------------
up wherever you’re trying to go on apple or google maps and click the public transit option. It’ll break down all the ways you can get a place, and show you where to go. Most public transit places take Apple Pay and have lots of signs to direct you

damn alr, on apply maps its says abt an hr😢, i have traveled before and taken public transits before but its typically places like nyc where my parents have been, my dad grew up in nyc so hes very familiar and it was easy to follow. I think ill get the hang of it. Thanks!

Best bet for meadowlands might be splitting an uber with friends

Citibike to the path!

[walkscore_hoboken.txt #7 | 112 tokens | 450 chars]
https://www.walkscore.com/NJ/Hoboken
----------------------------------------------------------------------
un’s Falafel has been serving high quality Middle Eastern Food since it first opened its doors to the public in 1971. It is the oldest falafel restaurant in New York and one of the first Middle Eastern establishments in the United States. Best Falafel in hoboken and even in New York. They literally have lines up to 70 people (thats nearly 2 blocks of people waiting) You wont even know if its Black Friday or not!

Kashyap Joshi
on Mamoun’s Falafel

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

## Retrieval Test

======================================================================
EMBEDDING + RETRIEVAL REPORT
======================================================================
Embedding model : BAAI/bge-base-en-v1.5
Vector store    : ChromaDB @ C:\Users\halde\OneDrive\Desktop\CodePath\AI 201 Summer 2026\ai201-project1-unofficial-guide-starter\chroma
Collection      : unofficial_guide (55 chunks)
Top-k           : 5

======================================================================
QUERY: How much does the Stevens shuttle cost?
======================================================================

[#1 | distance 0.4341 | reddit_housing_commute.txt chunk 3]
https://www.reddit.com/r/stevens/comments/1rlx081/housingcommute_advice/
----------------------------------------------------------------------
within walking distance from campus (although it's a relatively long walk; there's also the Stevens shuttle).

Since you likely won't need to be on-campus more than 3 days a week as a graduate student, I think commuting is the (financial) way to go; it's plenty tolerable and the saved $$ would be very nice

tysm! i haven’t heard of the stevens shuttle, do u have to pay for that? where does it stop? is there an app to order it to come?

It's free! There are 4 designated pickup/drop-o on campus and a few designated ones around Hoboken (mostly the train/ferey stations and hospital). Up until 8pm I think, it only goes between campus and the designated spots around town; 8pm-3am it

[#2 | distance 0.4670 | apartments_com.txt chunk 1]
https://www.apartments.com/local-guide/off-campus-housing/nj/hoboken/stevens-institute-of-technology/
----------------------------------------------------------------------
, Light Rail, or bus system. Stevens also provides free campus shuttle service to and from each Hoboken station. In addition to stunning views of the Manhattan skyline, the SIT campus is rich with activity and engagement from almost 100 student organizations, Greek life, and NCAA Division III Duck athletics. Hoboken is the most walkable city in New Jersey, home to endless dining choices, a thriving arts scene, and tons of green space. Manhattan and its world-class amenities are just a short train ride away.

Rent Trends
As of June 2026, the average apartment rent in Hoboken, NJ is $3,110 for a studio, $3,832 for one bedroom, $4,922 for two bedrooms, and $6,485 for three bedrooms. Apartment rent in Hoboken has increased by 2.3% in the past

[#3 | distance 0.4681 | apartments_com.txt chunk 0]
https://www.apartments.com/local-guide/off-campus-housing/nj/hoboken/stevens-institute-of-technology/
----------------------------------------------------------------------
Innovation is at the core of Stevens Institute of Technology, established in 1870 by America’s First Family of Inventors. Stevens is now a premier private research university recognized for its unique curriculum blending technical training, teamwork, design projects, internships, and cooperative education opportunities. Graduates of SIT are consistently in high demand by employers seeking highly prepared and solutions-oriented employees. The SIT campus is nearby a wide range of apartments available for rent in Hoboken and surrounding cities such as Jersey City, Union City, North Bergen, Weehawken, Secaucus, and Bayonne. Public transportation with access to Hoboken is available in most surrounding cities, via the PATH, Light Rail, or bus system. Stevens also provides free campus shuttle service to and from each Hoboken station. In addition to stunning views of the Manhattan skyline, the SIT campus is rich with

[#4 | distance 0.4722 | reddit_nyc_access.txt chunk 0]
https://www.reddit.com/r/stevens/comments/1hwd40y/nyc_access/
----------------------------------------------------------------------
nyc access

hi all, i’m very interested in stevens (fingers crossed i get in) and one of the main draws for me is the proximity to nyc. how often do y’all go into the city? is the bus or path more efficient? thanks!

You can take the path train and it will take you to manhattan in 10 minutes

Bus and PATH are about a similar time from campus to NYC, the bus involves a bit less walking. The bus will take you to the 42nd street Port Authority station (next to Time's Square), and the PATH can take you as far as 34th street (by the Empire State), or you can get off at 23rd, 14th, 9th, or Christopher street stops. The bus costs $4 each way and the PATH costs $2.75 each way and you'll have to pay more to get onto

[#5 | distance 0.4907 | reddit_housing_commute.txt chunk 1]
https://www.reddit.com/r/stevens/comments/1rlx081/housingcommute_advice/
----------------------------------------------------------------------
minute walk from the terminal to campus so then that becomes closer to 1.5 hours total effort commute and walking that during winter or non ideal weather sounds absolutely brutal.

So:

• Is the bus/train lines reliable enough to count on every day? How’s that walk too?

• Does Stevens have any decent grad housing, or any tips for finding something affordable nearby that isn’t going to bankrupt me?

• If you commute, do you regret it? Are you able to make a schedule that works with commuting like going in only 2-3 times a week?

Any advice would be huge help! Tysm in advance :)

Making the commute work is definitely doable, especially only 2-3 days a week. I'd definitely advise the train here: cutting through Essex/Hudson counties daily with traffic can get absolutely maddening

======================================================================
QUERY: What are the disadvantages of parking with a temporary Hoboken pass?
======================================================================

[#1 | distance 0.3018 | reddit_offcampus_parking.txt chunk 0]
https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/
----------------------------------------------------------------------
Off-campus parking situation

I'm considering living in the Hudson dorms for my senior year. With that, I would love to have my car with me in Hoboken, which would make my biweekly commutes back home way easier than riding NJ transit and would make running errands easier. For those living off campus, what's your parking situation like (available space, rates, distance from campus)?

Also, do any parking spaces allow for basic maintenance such as oil changes?

Easiest thing would be a temporary Hoboken pass which is $700 for the year. You can park on one side of most streets in Hoboken. It can be competitive at times, and you will have to move your car for street cleaning every week/day depending on where you park. Also you cannot do oil changes or anything when parked on the

[#2 | distance 0.3329 | reddit_overnight_parking_free.txt chunk 0]
https://www.reddit.com/r/stevens/comments/1g8gnag/where_can_i_park_overnight_for_free/
----------------------------------------------------------------------
Where can I park overnight for free?

I'm a commuter student attending this school. I have a parking pass but I don't think I can park overnight on campus without getting ticketed. What are my options, preferably free?

Meters aren’t checked overnight in metered zones off campus. You can’t park on the resident side, but the side that makes you pay won’t request payment after 9pm until sometime in the morning, I’m not sure exactly when but the Hoboken parking authority website probably says. Just be sure to move your car or pay when required and be aware of street cleaning/other signs nearby limiting parking or you’ll certainly get a ticket or towed

It’s 9pm-9am

You can more or less get away with it in CPH lot, 8th st, or possibly River Lot. If

[#3 | distance 0.3468 | reddit_overnight_parking.txt chunk 0]
https://www.reddit.com/r/stevens/comments/p5on9u/overnight_parking/
----------------------------------------------------------------------
Overnight Parking (self.stevens)

What are the best options for overnight parking? I know I can’t park overnight on campus without the proper permit(campus police said I would be ticketed and towed). I know that there is a student discount for Garage B on 2nd street, but according to reviews on Google and Parkopedia it’s quite prone to vandalism. Let me know about any other options.

Hoboken street parking is free from 9pm to 9am (and on Sundays) and you don't need a permit to park on the side of the street with white signs with green text.

You can stay in a spot for either 2 hrs or 4 hrs (depending on the location). So if you park at 7pm/5pm you can leave your car there until 11am/1pm and only pay for

[#4 | distance 0.3527 | reddit_offcampus_parking.txt chunk 1]
https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/
----------------------------------------------------------------------
It can be competitive at times, and you will have to move your car for street cleaning every week/day depending on where you park. Also you cannot do oil changes or anything when parked on the street.

Garages are very expensive and hard to get into at times. I would just recommend NJ Transit as having a car in Hoboken comes with a lot of unnecessary stress if you can avoid it.

Best option for parking would be to move to a high-rise building with in-building parking. Hudson Dorms luxury tier could be that, but you would be sharing your own bedroom. A better option could be to find a roommate on a site like Spareroom and move into their apartment or get a studio apartment.

I know the municipal garages used to have a deal for Stevens students. Was like $125/mo. Not sure if it still exists.

[#5 | distance 0.3854 | reddit_njtransit_student_pass.txt chunk 1]
https://www.reddit.com/r/stevens/comments/1f54e7d/nj_transit_student_pass_assistance_needed/
----------------------------------------------------------------------
.

Any suggestions from regular commuters or the-one-who-knows-about-this is appreciated

Thank-you!

NJ transit is also discounting regular passes for September only such that they're equivalent to the student rate. You should choose via Secaucus, since there's no consistent direct way from Newark Penn to Hoboken

Oh yeah I did look into that..and figured out the logistics.. Thanks for responding!

To get from Newark to Hoboken you would need to take the PATH. The light rail might be an option. A connection through Secaucus is easier and often faster.

Gotcha..will look into that.. Thanks!

That's not too bad. I drive 1.5 hours each way to stevens because the train is out of the way and takes longer. You can take the North East Corridor to

======================================================================
QUERY: When is Hoboken street parking free?
======================================================================

[#1 | distance 0.3027 | reddit_overnight_parking.txt chunk 0]
https://www.reddit.com/r/stevens/comments/p5on9u/overnight_parking/
----------------------------------------------------------------------
Overnight Parking (self.stevens)

What are the best options for overnight parking? I know I can’t park overnight on campus without the proper permit(campus police said I would be ticketed and towed). I know that there is a student discount for Garage B on 2nd street, but according to reviews on Google and Parkopedia it’s quite prone to vandalism. Let me know about any other options.

Hoboken street parking is free from 9pm to 9am (and on Sundays) and you don't need a permit to park on the side of the street with white signs with green text.

You can stay in a spot for either 2 hrs or 4 hrs (depending on the location). So if you park at 7pm/5pm you can leave your car there until 11am/1pm and only pay for

[#2 | distance 0.3065 | reddit_overnight_parking_free.txt chunk 0]
https://www.reddit.com/r/stevens/comments/1g8gnag/where_can_i_park_overnight_for_free/
----------------------------------------------------------------------
Where can I park overnight for free?

I'm a commuter student attending this school. I have a parking pass but I don't think I can park overnight on campus without getting ticketed. What are my options, preferably free?

Meters aren’t checked overnight in metered zones off campus. You can’t park on the resident side, but the side that makes you pay won’t request payment after 9pm until sometime in the morning, I’m not sure exactly when but the Hoboken parking authority website probably says. Just be sure to move your car or pay when required and be aware of street cleaning/other signs nearby limiting parking or you’ll certainly get a ticket or towed

It’s 9pm-9am

You can more or less get away with it in CPH lot, 8th st, or possibly River Lot. If

[#3 | distance 0.3236 | reddit_offcampus_parking.txt chunk 0]
https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/
----------------------------------------------------------------------
Off-campus parking situation

I'm considering living in the Hudson dorms for my senior year. With that, I would love to have my car with me in Hoboken, which would make my biweekly commutes back home way easier than riding NJ transit and would make running errands easier. For those living off campus, what's your parking situation like (available space, rates, distance from campus)?

Also, do any parking spaces allow for basic maintenance such as oil changes?

Easiest thing would be a temporary Hoboken pass which is $700 for the year. You can park on one side of most streets in Hoboken. It can be competitive at times, and you will have to move your car for street cleaning every week/day depending on where you park. Also you cannot do oil changes or anything when parked on the

[#4 | distance 0.3755 | walkscore_hoboken.txt chunk 4]
https://www.walkscore.com/NJ/Hoboken
----------------------------------------------------------------------
and subtle touches from a bygone era.

Kashyap Joshi
on Madison Bar & Grill

74 Transit Score of Hoboken, NJ
Hoboken has Excellent Transit
Transit is convenient for most trips. Find Hoboken apartments for rent on Redfin.

Public Transit Routes
Hoboken has excellent public transportation and about 7 bus, 11 rail and 1 light rail lines.

Transit Time
The map above shows how far you can travel in 30 minutes from Hoboken on public transit.

Neighborhood Guides
Thinking of renting an apartment or buying in Hoboken? Ask our neighborhood guides a question.

Kashyap Joshi

Madison Bar & Grill
1 Republik
800 Madison St
78 Bike Score of Hoboken, NJ
Hoboken is Very Bikeable
Biking is convenient for most trips.

800 Madison St
Hoboken Terminal
River St
Hoboken South Waterfront
Benny Tu

[#5 | distance 0.3798 | reddit_offcampus_parking.txt chunk 1]
https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/
----------------------------------------------------------------------
It can be competitive at times, and you will have to move your car for street cleaning every week/day depending on where you park. Also you cannot do oil changes or anything when parked on the street.

Garages are very expensive and hard to get into at times. I would just recommend NJ Transit as having a car in Hoboken comes with a lot of unnecessary stress if you can avoid it.

Best option for parking would be to move to a high-rise building with in-building parking. Hudson Dorms luxury tier could be that, but you would be sharing your own bedroom. A better option could be to find a roommate on a site like Spareroom and move into their apartment or get a studio apartment.

I know the municipal garages used to have a deal for Stevens students. Was like $125/mo. Not sure if it still exists.

======================================================================
QUERY: What is the walkability or walk score of Hoboken?
======================================================================

[#1 | distance 0.1638 | walkscore_hoboken.txt chunk 0]
https://www.walkscore.com/NJ/Hoboken
----------------------------------------------------------------------
Living in Hoboken
Hoboken Apartments for Rent
map of Hoboken apartments for rent
97 Walk Score of Hoboken, NJ
74 Transit Score of Hoboken, NJ
78 Bike Score of Hoboken, NJ
Hoboken has an average Walk Score of 97 with 50,005 residents.

Hoboken has excellent public transportation and is very bikeable.

97 Walk Score of Hoboken, NJ
Hoboken is a Walker’s Paradise
Daily errands do not require a car.

United States New Jersey Hoboken
Madison Bar & Grill
1 Republik
Hoboken has an average Walk Score of 97 with 50,005 residents.

Hoboken has excellent public transportation and is very bikeable.

Hoboken Apartments for Rent
Hoboken Homes for Sale
Search for apartments in Hoboken or check out apartments in other Ho

[#2 | distance 0.2920 | walkscore_hoboken.txt chunk 4]
https://www.walkscore.com/NJ/Hoboken
----------------------------------------------------------------------
and subtle touches from a bygone era.

Kashyap Joshi
on Madison Bar & Grill

74 Transit Score of Hoboken, NJ
Hoboken has Excellent Transit
Transit is convenient for most trips. Find Hoboken apartments for rent on Redfin.

Public Transit Routes
Hoboken has excellent public transportation and about 7 bus, 11 rail and 1 light rail lines.

Transit Time
The map above shows how far you can travel in 30 minutes from Hoboken on public transit.

Neighborhood Guides
Thinking of renting an apartment or buying in Hoboken? Ask our neighborhood guides a question.

Kashyap Joshi

Madison Bar & Grill
1 Republik
800 Madison St
78 Bike Score of Hoboken, NJ
Hoboken is Very Bikeable
Biking is convenient for most trips.

800 Madison St
Hoboken Terminal
River St
Hoboken South Waterfront
Benny Tu

[#3 | distance 0.3121 | apartments_com.txt chunk 1]
https://www.apartments.com/local-guide/off-campus-housing/nj/hoboken/stevens-institute-of-technology/
----------------------------------------------------------------------
, Light Rail, or bus system. Stevens also provides free campus shuttle service to and from each Hoboken station. In addition to stunning views of the Manhattan skyline, the SIT campus is rich with activity and engagement from almost 100 student organizations, Greek life, and NCAA Division III Duck athletics. Hoboken is the most walkable city in New Jersey, home to endless dining choices, a thriving arts scene, and tons of green space. Manhattan and its world-class amenities are just a short train ride away.

Rent Trends
As of June 2026, the average apartment rent in Hoboken, NJ is $3,110 for a studio, $3,832 for one bedroom, $4,922 for two bedrooms, and $6,485 for three bedrooms. Apartment rent in Hoboken has increased by 2.3% in the past

[#4 | distance 0.3147 | walkscore_hoboken.txt chunk 3]
https://www.walkscore.com/NJ/Hoboken
----------------------------------------------------------------------
Apartments Llewellyn Park Apartments

Eating & Drinking
There are about 253 restaurants, bars and coffee shops in Hoboken.

People in Hoboken can walk to an average of 15 restaurants, bars and coffee shops in 5 minutes.

Mamoun’s Falafel
Benny Tudino's
Restaurant Choices Map
= More Choices

The Madison Bar and Grill is filled with an ambiance and class that is usually reserved for Manhattan eateries. The formal dining room is cleverly decorated in a 1940s style reminiscent of a chic roadside inn. The décor works an evocative, magical mood, with bare wood floors, wainscoted walls, soft lighting and subtle touches from a bygone era.

Kashyap Joshi
on Madison Bar & Grill

74 Transit Score of Hoboken, NJ
Hoboken has Excellent Transit
Transit is convenient for most

[#5 | distance 0.3218 | walkscore_hoboken.txt chunk 1]
https://www.walkscore.com/NJ/Hoboken
----------------------------------------------------------------------
.

Hoboken has excellent public transportation and is very bikeable.

Hoboken Apartments for Rent
Hoboken Homes for Sale
Search for apartments in Hoboken or check out apartments in other Hoboken neighborhoods. Links will open on our partner site Redfin.com.

Chelsea, Hoboken apartments for rent
Downtown, Hoboken apartments for rent
Downtown Jersey City, Hoboken apartments for rent
Downtown Union City, Hoboken apartments for rent
Heights, Hoboken apartments for rent
Hudson City, Hoboken apartments for rent
Midtown Bloomfield, Hoboken apartments for rent
Midtown Manhattan, Hoboken apartments for rent
Mount Pleasant, Hoboken apartments for rent
Newport, Hoboken apartments for rent
North East Hoboken, Hoboken apartments for rent
Northwest Hoboken, Hoboken apartments for rent
Shipyard, Hoboken apartments for rent

======================================================================
QUERY: Will changing from dorming to commuting affect my financial aid package?
======================================================================

[#1 | distance 0.2031 | reddit_change_dorm_to_commute.txt chunk 0]
https://www.reddit.com/r/stevens/comments/acryhw/change_dorming_to_commuting/
----------------------------------------------------------------------
Change dorming to commuting

Hello so I went to the reply to decision but it says I am going to be dorming. I probably put it there before but now I can’t because it would be too expensive. I can probably change it to commuting by calling Stevens but would it affect the grants and financial aid?

Are you asking if you switch from on campus housing to off campus housing will your scholarship/financial aid be unchanged?

They likely won’t change your aid package. To be sure though, I’d give financial aid a call when they open on Monday. Changing your status from on campus resident to commuting isn’t that difficult- send your admissions advisor an email or call admissions. You can change that piece even after you accept your offer of admission.

[deleted]

No it won't lol. Financial aid is

[#2 | distance 0.2742 | reddit_change_dorm_to_commute.txt chunk 1]
https://www.reddit.com/r/stevens/comments/acryhw/change_dorming_to_commuting/
----------------------------------------------------------------------
difficult- send your admissions advisor an email or call admissions. You can change that piece even after you accept your offer of admission.

[deleted]

No it won't lol. Financial aid is based on tuition only.(applies only to tuition) People will full rides don't also get room and board iirc. I mean my scholarship and everyone I know who has a scholarship did not lose money when they either moved home or to a non stevens apartment in Hoboken/ JC.

Not sure why the downvotes; I was told a few years ago that I’d lose some aid if I turned to commuter. It may depend on what aid you get?

[#3 | distance 0.3023 | reddit_dorm_vs_commute.txt chunk 6]
https://www.reddit.com/r/stevens/comments/1s0tapv/dorm_or_commute/
----------------------------------------------------------------------
, etc. and dorming makes it much easier. You can easily choose to commute from sophomore or junior year onward to save money, have proximity to family/cat, etc

Dorming isn’t required, but ask before you decide. We were told that it could reduce the amount of aid offered.

I called up the financial aid office and it does reduce it, The institutional (cast im guessing) aid does in fact get reduced. Im going to try and call my financial aid counselor today to see by how much it will get reduced by. Thanks for letting me know!!

Of course! I’d want to know too!!!

And by how much they did?

[#4 | distance 0.3162 | reddit_dorm_vs_commute.txt chunk 0]
https://www.reddit.com/r/stevens/comments/1s0tapv/dorm_or_commute/
----------------------------------------------------------------------
Dorm or commute

I got accepted to the class of 2030, Im not sure if it is required to dorm or not for incoming freshmans, but in the case that it isnt required, would it be better for me to commute.

With dorming, tuition would be ≈28,500k, without dorming it would be ≈ 7,700k

My I live in Bergen county, and I have a train station in my area readily available, and it would like a 1 hour commute via train or a 40 minute car ride, which I can also do, due to having a license/car.

Im just stuck on this decision because its so stupid but I really want a cat and my mom promised me one if i commit to stevens (which i do want to go to as wel, I got in for Engineering undecidedbut ill

[#5 | distance 0.3411 | reddit_dorm_vs_commute.txt chunk 5]
https://www.reddit.com/r/stevens/comments/1s0tapv/dorm_or_commute/
----------------------------------------------------------------------
. I think commuting guarantees you more happiness since you'll have your cat and you'll spend much less than ~20k commuting.

I think a better option than both is to get an off-campus apartment. Many of the freshman dorms are not that nice and you could get a decent off-campus apartment with a roommate for similar rent and keep your cat.

I recommend dorming at least as a freshman. People who dorm often don't appreciate how much harder it is to integrate yourself into campus life as a commuter. Freshman year is absolutely critical for building friendships, exploring your place in the community, adjusting to the increased academic workload, etc. and dorming makes it much easier. You can easily choose to commute from sophomore or junior year onward to save money, have proximity to family/cat, etc

Dorming isn’

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

---

## Example Responses

======================================================================
GROUNDED GENERATION REPORT
======================================================================
Generation model : llama-3.3-70b-versatile (Groq)
Temperature      : 0.1
Relevance gate   : distance <= 0.8

======================================================================
QUERY: When is Hoboken street parking free?
======================================================================
Hoboken street parking is free from 9pm to 9am (and on Sundays) [1], and meters aren’t checked overnight in metered zones off campus from 9pm until sometime in the morning [2].

**Sources**
1. [Reddit r/stevens — Overnight Parking](https://www.reddit.com/r/stevens/comments/p5on9u/overnight_parking/)
2. [Reddit r/stevens — Where Can I Park Overnight For Free](https://www.reddit.com/r/stevens/comments/1g8gnag/where_can_i_park_overnight_for_free/)
3. [Reddit r/stevens — Offcampus Parking Situation](https://www.reddit.com/r/stevens/comments/1ri7x7p/offcampus_parking_situation/)
4. [Walk Score — Hoboken](https://www.walkscore.com/NJ/Hoboken)

[grounded on 5 chunks | distances: 0.303, 0.306, 0.324, 0.375, 0.380]

======================================================================
QUERY: What is the walk score of Hoboken?
======================================================================
The Walk Score of Hoboken is 97 [1], [1], indicating that Hoboken is a "Walker’s Paradise" where "Daily errands do not require a car" [1].

**Sources**
1. [Walk Score — Hoboken](https://www.walkscore.com/NJ/Hoboken)
2. [Apartments.com — Stevens Institute Of Technology](https://www.apartments.com/local-guide/off-campus-housing/nj/hoboken/stevens-institute-of-technology/)

[grounded on 5 chunks | distances: 0.188, 0.331, 0.340, 0.350, 0.367]

======================================================================
QUERY: How much is it going to rain tomorrow in Hoboken on June 8, 2026?
======================================================================
I don't have enough information on that.

---

## Demo Video

Google Drive link: https://drive.google.com/file/d/1HQx1OBfdwaFcW5CDe3hh_CH_JiJlYAwP/view?usp=drive_link

Due to technical difficulties, I was unable to record audio for the demo video. The video covers the following parts:

The first few seconds of the video shows the system prompt passed to the generator

**PART 1:** Using Terminal - `python generator.py "your query"`

QUERY 1: What is the walkability or walk score of Hoboken?

The LLM was successful in generating an accurate answer since the retrieved chunks were relevant (distance < 0.5 with relevant top sources like Walk Score) and the answer was as expected.

QUERY 2: When is Hoboken street parking free?

The LLM failed at this question, giving a partially accurate answer due to considering outdated advice, which was true years ago but not anymore, as a fact confidently.

**PART 2:** Using Gradio web UI - `python app.py`

QUERY 3: How much will it rain tomorrow, on June 8, 2026?

This demonstrates Gradio UI, and the loading screen shown to the user while the LLM is generating a response. Here, the LLM correctly indicates that there is no information on this topic in the sources, showing the refusal response.

**PART 3:** Evaluation Report table walkthrough

Test queries 1, 2, 4, 5 all retrieve relevant chunks (distance < 0.5) and have accurate reponses (matches expected answer) with links to sources and references to them using numbers [1], [2] etc. Test query 3 is a question where the LLM fails because of outdated advice and not having the date of the Reddit comments as context. Test query 5 correctly shows the existence of uncertainty instead of confidently asserting unverified statements.
