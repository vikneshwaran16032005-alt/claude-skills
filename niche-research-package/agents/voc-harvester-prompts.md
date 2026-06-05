# VOC Harvester Agent Prompts

Canonical agent prompt templates for the parallel VOC research dispatch in the `niche-research-package` skill workflow.

**Important: dispatch all three agents in parallel** (single message, multiple Agent tool calls). Each agent uses `subagent_type: "general-purpose"`.

Replace `{NICHE}`, `{BUYER_PERSONA}`, `{TOOLS}`, `{INDUSTRY_VOICES}`, `{CLIENT_NAME}` with the engagement-specific inputs before dispatching.

---

## Agent A — Reddit & Forums VOC Harvest

**Description:** `Reddit/forum VOC harvest — {NICHE}`
**Subagent type:** `general-purpose`

**Prompt:**

```
You're harvesting voice-of-customer (VOC) data for an IVOC research deliverable. The niche: **{NICHE}** — buyer persona: **{BUYER_PERSONA}**. Common tools/competitors: {TOOLS}.

I need REAL verbatim quotes with REAL citations. NO fabrication. Every quote must be a direct quote from a real Reddit post or comment, with the URL.

**Task: Harvest verbatim VOC data from Reddit and niche-specific forums.**

Search across:
- Reddit subreddits relevant to this niche (identify 4-8 from search results)
- Quora topics (niche-specific)
- Niche-specific forums you can identify from search

Use WebSearch with site:reddit.com queries and exact-phrase queries — e.g. `site:reddit.com/r/{subreddit} "I hate"`, `site:reddit.com/r/{subreddit} {tool} frustrated`, `site:reddit.com {niche} owner pain`, etc.

For each verbatim quote you find, capture:
1. **The verbatim quote** (exact words, in quotes — do NOT paraphrase)
2. **Source URL** (full thread URL)
3. **Subreddit/forum + thread title** (so I can verify)
4. **What IVOC bucket it fits into**: Pain/Fear, Desire, Firm Belief, Shakeable Belief, Identification (who they see themselves as), or Common Phrase
5. **Brief context** (one line on what was happening in the thread)

**Target: 25-40 verbatim quotes total**, distributed roughly:
- 10-12 pain points (workflow, tools, AI, customer management)
- 5-8 desires/dream outcomes
- 5-8 firm beliefs (things they hold strongly)
- 3-5 shakeable beliefs (things they could be talked out of)
- 3-5 identifications (e.g. "I'm a builder of teams" / "I built this from nothing")
- 5-10 common words/phrases that recur across multiple posters

Format your response as a structured Markdown document I can paste directly into the IVOC research deliverable. Group by IVOC bucket. Every quote MUST have its source URL right next to it.

CRITICAL HONESTY RULE: Reddit and most public Reddit mirrors are hard-blocked from automated tooling. If WebFetch returns 403/blocked errors and WebSearch only returns AI-generated summaries (not verbatim text), you cannot fabricate quotes to fill the brief. Report back the exact constraint hit, list the URLs you tried, and return zero verified quotes if zero is what you can verify. Better 15 verified quotes than 40 fabricated ones.

Report back inside 1500 words.
```

---

## Agent B — Software Review Sites VOC Harvest

**Description:** `G2/Capterra/Trustpilot review harvest — {NICHE}`
**Subagent type:** `general-purpose`

**Prompt:**

```
You're harvesting voice-of-customer (VOC) data from public software-review sites for an IVOC research deliverable. The target: **{BUYER_PERSONA} using {TOOLS} or similar tools in the {NICHE} space**.

I need REAL verbatim quotes with REAL citations. NO fabrication. Every quote must be a direct quote from a real review, with the URL.

**Task: Harvest verbatim VOC data from review sites.**

Search across:
- G2 reviews of the dominant tools in this niche
- Capterra reviews of the same
- Trustpilot UK and Trustpilot.com (especially for tools with known service issues)
- Software Advice / GetApp reviews

Useful search query patterns:
- `site:g2.com {tool} review complaints`
- `site:capterra.com {tool} {buyer-persona}`
- `site:trustpilot.com {tool} review`
- `{tool} "I hate" OR "frustrating" OR "wasted"`
- `{tool} review 2025 OR 2026`

For each verbatim quote you find, capture:
1. **The verbatim quote** (exact words, in quotes — do NOT paraphrase)
2. **Source URL** (full review-page URL)
3. **Tool reviewed** and **reviewer role if visible** (e.g. "Owner, agency, 11-50 employees")
4. **What IVOC bucket it fits into**: Pain/Fear, Desire, Firm Belief, Shakeable Belief, Identification, or Common Phrase
5. **Star rating** if visible (e.g. 2/5)

**Target: 20-30 verbatim quotes total**, weighted toward:
- Pains/frustrations with tools (the loudest signal in reviews)
- Common phrases that recur (e.g. "click-heavy", "double entry", "support is unhelpful")
- Workarounds people describe (e.g. "we ended up exporting to Excel")
- "Tried and dropped" stories
- Pricing complaints

Format as structured Markdown grouped by IVOC bucket. Every quote MUST have its source URL.

CRITICAL: ONLY return verbatim quotes you can verify with a URL. If a search summary references a complaint but you can't pull the literal quote, mark it as paraphrase-risk and exclude it — don't invent the quote. Better 15 verified quotes than 30 fabricated ones. Note: G2/Capterra/Trustpilot often block direct WebFetch — Google search-result snippets are usually the only verbatim source. Use them when the snippet is verbatim; mark as paraphrase-risk when the snippet is summarised.

Report back inside 1500 words.
```

---

## Agent C — Industry Voice & Publications Harvest

**Description:** `Industry voice + LinkedIn comments harvest — {NICHE}`
**Subagent type:** `general-purpose`

**Prompt:**

```
You're harvesting voice-of-customer (VOC) data for an IVOC research deliverable. The niche: **{NICHE}** — buyer persona: **{BUYER_PERSONA}**.

I need REAL verbatim quotes with REAL citations. NO fabrication.

**Task: Harvest verbatim VOC data from industry thought leaders, LinkedIn comment threads, and niche-industry publications.**

Sources to mine:
1. **Top industry voices** for this niche — identify 3-5 dominant voices (bloggers, podcasters, newsletter writers, thought leaders) from search results. Likely candidates for {NICHE}: {INDUSTRY_VOICES}. Pull verbatim quotes from their recent (last 12 months) posts AND from agency-owner/buyer comments on those posts (when visible).

2. **Industry newsletters and Substacks** — pull verbatim from recent issues.

3. **LinkedIn posts and comments from niche voices** — comment threads on their posts often have buyers venting verbatim.

4. **Industry publications** — trade journals, niche-specific blogs, op-ed pieces with quoted buyer sources.

5. **Macro signal** — major industry-news coverage (profit warnings, market reports, layoffs, regulatory shifts). Pull verbatim industry-reaction quotes from named executives.

Use WebSearch + WebFetch to actually pull the page content, then extract verbatim quotes.

For each quote, capture:
1. **The verbatim quote** (exact words)
2. **Speaker** (name and role — e.g. "Greg Savage" or "Mark T., agency MD commenting on Savage post")
3. **Source URL**
4. **Date** (if visible)
5. **IVOC bucket**: Pain/Fear, Desire, Firm Belief, Shakeable Belief, Identification, Common Phrase

**Target: 20-30 verbatim quotes**, weighted toward:
- Industry-leader pronouncements about where the industry is going (Firm/Shakeable Beliefs)
- Buyer comments venting in public (Pains, Common Phrases)
- Specific numbers/data points cited in industry coverage
- Identifications: how do {BUYER_PERSONA}s describe THEMSELVES?

Format as structured Markdown grouped by IVOC bucket. Every quote MUST have its source URL.

CRITICAL: Real quotes only. If a source says "according to X, agency owners are saying Y", that's NOT a verbatim quote — flag it as paraphrase or skip. Only the exact words, attributed.

Report back inside 1500 words.
```

---

## Tuning notes

- **The targets (25-40 / 20-30 / 20-30) are aspirational ceilings, not floors.** Real harvests routinely return less. 15 verified per agent is acceptable.
- **Reddit harvest will likely return 0–5 quotes.** That's expected. The block is real and stable.
- **Software-review harvest is the highest-yield source** for B2B SaaS niches. Expect 20-30 for tool-heavy markets.
- **Industry-voice harvest yields highest-leverage quotes** (Firm Notion territory, the "category-naming" finds). Quality over quantity.
- **All three agents combined should yield 50-90 verified quotes for a healthy harvest.** Below 40 = consider re-running with refined queries before synthesizing.

## When to add a fourth agent

For some niches, a fourth parallel agent may help:
- **Consumer/B2C niches:** add a YouTube-comments harvester. YouTube is where consumers vent.
- **Highly regulated niches (legal, medical, finance):** add a regulatory-publication harvester focusing on compliance pain.
- **Geographic-specific niches:** add a country-specific publication harvester (e.g. UK trade press for UK niches).

Don't bloat with more than 4 parallel agents — diminishing returns and longer wait time.
