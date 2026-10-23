---
name: niche-research-package
description: "Build the 3-document client research package for a niche (IVOC Methodology Guide, IVOC Worked Example, Pain Map) from real, cited web research, as RIOA-brand PDFs. Use for 'build the research package for [niche]' or 'IVOC + pain map docs for [client]'."

---

# Niche Research Package

Generate the canonical 3-document research foundation Vik ships to founding clients ahead of their own direct-research weekend. Same workflow we ran for Saad on the recruitment-agency niche on 2026-05-09.

## What this skill produces

Three markdown files + three RIOA-brand PDFs in the client's folder:

1. **`<Client>_IVOC_Methodology_Guide_v1.md/.pdf`** — the *how*. Educational. Teaches the client how to do indirect voice-of-customer research themselves. Largely niche-agnostic but with niche-flavored examples.

2. **`<Client>_IVOC_Worked_Example_<Niche>_v1.md/.pdf`** — the *what good looks like*. The IVOC research framework filled in for the client's niche, populated with **real verbatim quotes from real web sources**, every quote cited with a working URL.

3. **`<Client>_<Niche>_PainMap_v0.md/.pdf`** — the broader strategic intel. Industry overview with real stats, top 10 pain points ranked with cost math, language dictionary, fears, dream outcomes, market gaps, big changes coming, recommended product solution with pricing & positioning, and full GTM. Built on real research, not fabricated.

## When to invoke

- Vik says "build the research package for [niche/client]"
- Vik says "make the IVOC + pain map docs for [client]"
- Vik says "research foundation for [niche]"
- Vik says "generate the 3-doc bundle for [client]"
- Onboarding a new founding client and the next deliverable is the research foundation
- A client is preparing for their immersive research weekend and needs the v0 hypothesis

**Don't invoke for:**
- A single-document request (use `niche-research` skill for just the market-intel doc, or hand-build the single doc)
- Light research (use `niche-opportunity-finder` or a direct web search)
- Re-running on a niche where the package already exists in the client folder (offer to refresh instead)

## Required inputs

Confirm these before running. **Ask Vik if any are missing.**

1. **Client name** (e.g. "Saad", "Aziz", "Mohammed Saad") — used in filenames and document titles
2. **Client folder path** (absolute) — usually `E:/linkedin messages/Clients/<Client>/`
3. **Niche specification** — the more specific the better. Format: *industry + size + geography + sub-vertical(s)*. Examples:
   - "US & UK recruitment agencies, 20–50 employees, Bullhorn/JobAdder/Vincere users, contingent + retained + exec search"
   - "US wedding photographers, 1–3 person studios, 20–50 events/year"
   - "UK pediatric dental practices, 2–5 chairs, NHS + private mix"
4. **Buyer persona** — role of the buyer within the niche (Founder/MD/Owner, Director of X, etc.)
5. **Optional: product hypothesis** — if Vik already has a working hypothesis of what the client is building. Shapes the Pain Map's *Perfect Software Solution* section.

If all 5 are clear, proceed. If any are fuzzy, ask before starting — research time is expensive.

## Workflow (5 phases)

### Phase 1 — Confirm scope and dispatch research

Acknowledge the inputs. Restate the niche back to Vik in one sentence. Then dispatch **parallel research agents** for VOC harvest. **All agents run concurrently — single message, multiple Agent tool calls.**

Three required agents (use `general-purpose` subagent type):

#### Agent A — Reddit & forums VOC harvest
Targets `r/<niche-relevant subreddits>`, niche-specific forums, Quora topics. Briefs the agent that Reddit is **hard-blocked from automated tooling** (no WebFetch, no mirror access). Tells the agent to be honest if it can't get verbatim quotes — return zero rather than fabricate. Likely yields 0–10 verified quotes; that's expected.

#### Agent B — Software review sites + competitor analysis
Targets G2, Capterra, Trustpilot UK, Software Advice. Searches reviews of the dominant tools in the niche (the agent identifies these from search results). Looks for verbatim 1- and 2-star quotes — that's where the loud language lives. Yields ~20–30 verified quotes typically.

#### Agent C — Industry voice & publications harvest
Targets industry-leader blogs, newsletters, podcasts, named industry publications, LinkedIn posts (read-only — comment threads if accessible). For each niche there are 3–5 dominant voices; the agent identifies them from search results then mines their recent (last 12 months) content for direct quotes. Yields ~20–30 quotes.

**Each agent's hard rules** (encode in the prompt):
1. Only verbatim quotes — no paraphrase, no fabrication
2. Every quote MUST have a real source URL
3. If a search summary cites a quote without exposing the literal wording, mark it as paraphrase-risk and exclude it
4. Better return 15 verified quotes than 50 plausible ones
5. Group quotes by IVOC bucket (Pain/Fear, Desire, Firm Belief, Shakeable Belief, Identification, Common Phrase)

Use `agents/voc-harvester-prompts.md` for the canonical agent prompt templates.

### Phase 2 — Synthesize the IVOC Methodology Guide (Doc A)

Largely templated — the methodology is niche-agnostic. Copy `templates/ivoc-methodology-guide.md` to the client folder, replacing the few illustrative examples with niche-relevant ones if helpful (the recruitment-flavored examples in the template work for most niches as illustrations of what good IVOC looks like — only swap them if Vik specifically asks).

File: `<client folder>/<Client>_IVOC_Methodology_Guide_v1.md`

### Phase 3 — Synthesize the IVOC Worked Example (Doc B)

Use `templates/ivoc-worked-example-skeleton.md` as the structure. Fill it with the verified quotes from Phase 1.

Sections to populate:
- Header: Note on this document (with sourcing-constraint disclosure if Reddit was blocked)
- Product / One reader (use the inputs Vik provided — niche, buyer persona, product hypothesis)
- Things searched for (real list of platforms mined; transparent about what was blocked)
- **Raw IVOC Data** — verbatim quotes by bucket (Desires, Firm Notions, Shakeable Notions, Identifications, Characteristics, Other—Pains&Fears, Common Words & Phrases)
- IVOC Summaries — 2–4 sentence pattern reads per bucket
- Summary Rankings — top 3 per bucket by intensity × frequency
- Final IVOC Summary — one-page synthesis
- Sources (every URL traceable)

**Quality bar:** ≥40 verified quotes total, ≥10 quotes in the loudest bucket (usually Other—Pains&Fears), zero fabricated quotes. If under 40 verified, flag transparently in the doc and note manual harvest is the next step.

File: `<client folder>/<Client>_IVOC_Worked_Example_<Niche>_v1.md`

### Phase 4 — Synthesize the Pain Map (Doc C)

Use `templates/pain-map-skeleton.md`. This is the broader strategic intel doc. Sections to fill (every section grounded in real data with citations):

1. Honesty preface — "Pain Map v0, hypothesis to validate"
2. Industry Overview — market size, agency count, CAGR (real stats — IBISWorld, named industry sources)
3. Where They Hang Out Online — by tier (Reddit, software reviews, industry voices, podcasts, conferences)
4. Top 10 Pain Points (Ranked) — each pain with: cost math, workarounds tried, why nobody's fixed it
5. Language Dictionary — industry jargon, pain phrases, success phrases, terms to avoid
6. What Keeps Them Up at Night — top 5–6 fears with specific scenarios
7. Dream Outcome — what good looks like for the buyer
8. Market Gaps — what doesn't exist; underserved segments
9. Big Changes Coming Soon — urgency levers (AI disruption, regulation, generational handover, etc.)
10. Perfect Software Solution — concrete product hypothesis with MVP, P2, integrations, pricing, positioning, defensibility
11. Go-to-Market — channels, opening message, expected objections + responses
12. Sources — every URL cited

**Use the same VOC research from Phase 1** to ground pain rankings. Cite industry-leader quotes inline.

File: `<client folder>/<Client>_<Niche>_PainMap_v0.md`

### Phase 5 — Generate PDFs and verify

Run rioa-pdf on all three markdown files in parallel:

```bash
python "~/.claude/skills/rioa-pdf/_md_to_pdf.py" "<input.md>" "<output.pdf>" "<Title -- Client Name>" "Client Confidential"
```

Document titles convention:
- `IVOC Methodology Guide -- <Client Name>`
- `IVOC Worked Example: <Niche> -- <Client Name>`
- `<Niche> Pain Map v0 -- <Client Name>`

**Then verify** — per the saved feedback memory on PDF pagination, scan every page of every PDF for near-empty pages. Use this snippet:

```python
import fitz
for path in [methodology_pdf, worked_example_pdf, pain_map_pdf]:
    doc = fitz.open(path)
    for i, p in enumerate(doc, 1):
        t = p.get_text()
        lines = [l for l in t.split('\n') if l.strip()]
        chrome = sum(1 for l in lines if any(x in l for x in ['RIOA CONSULTING', 'Client Confidential', 'Page ']))
        body_lines = len(lines) - chrome
        if body_lines < 5:
            print(f'{path} p{i}: NEAR EMPTY')
```

If any page is flagged, fix before delivering — either via markdown content tightening or by checking the canonical rioa-pdf script still uses `CondPageBreak(400)` (it should — but verify if regression suspected).

Also verify hyperlink integrity — every `[text](url)` should render as a clickable hyperlink. Spot-check by counting `doc.get_links()` per page.

## Hard rules — non-negotiable

1. **Real data only. Real citations only.** No fabricated quotes, no invented URLs, no speculative pain points presented as findings. If a source can't be verified, exclude it. Better 15 real than 50 fake.
2. **Every quote in the worked example has a working URL.** No exceptions.
3. **If Reddit (or any other planned source) is blocked, disclose it transparently in the doc.** Don't quietly skip — the client needs to know what manual research is the next step.
4. **The IVOC Methodology Guide is mostly templated.** Don't burn agent time regenerating it from scratch each engagement — it's niche-agnostic by design.
5. **The Pain Map is "v0" — explicitly framed as hypothesis to validate.** Encode this in the doc's opening preface. The client's immersive research weekend produces v1.
6. **All three PDFs use the same title casing convention** for the running header (per the rioa-pdf style).
7. **Verify near-empty pages after PDF generation, every time.** The fix is in the script (CondPageBreak(400)) but verify anyway.
8. **Use Vik's voice, not generic AI copywriting voice.** RIOA brand: direct, opinionated, prescriptive, no corporate filler. Cormorant Garamond + Jost styling is applied automatically by rioa-pdf.

## Outputs at the end of the workflow

When the skill completes, summarize back to Vik:
- Three PDF paths with page counts
- Total verified quotes used (split by source: review sites / industry blogs / Reddit)
- Top 3 strongest patterns from the research that the worked example surfaced
- The product hypothesis the Pain Map landed on (one sentence)
- Any flagged constraints (blocked sources, paraphrase-risk excluded quotes, manual harvest TODOs)
- Recommended next move (usually: WhatsApp handover note to client + start of immersive-research weekend)

## What "done" looks like

- 3 markdown files in the client folder, all containing real-data-grounded content with citations
- 3 RIOA-brand PDFs in the client folder, all paginated cleanly with no near-empty pages
- Every URL in the worked example resolves to a real source (spot-check 5)
- The Pain Map's *Perfect Software Solution* section names a specific product hypothesis with concrete pricing
- The skill's transparency requirements are met (any blocked sources disclosed, paraphrase-risk quotes excluded)
- Vik can hand the bundle to the client immediately — no "let me just clean this up first"

## References

- `templates/ivoc-methodology-guide.md` — canonical methodology doc (mostly niche-agnostic)
- `templates/ivoc-worked-example-skeleton.md` — structural skeleton for the worked example
- `templates/pain-map-skeleton.md` — structural skeleton for the Pain Map v0
- `agents/voc-harvester-prompts.md` — canonical agent prompts for parallel VOC harvest
- Canonical rioa-pdf converter: `~/.claude/skills/rioa-pdf/_md_to_pdf.py`
- Companion skill: `niche-research` (single-doc market intel — useful when only the Pain Map is needed)
- Companion skill: `copywriting-master` (for the IVOC framework itself — references/principles.md)

## Pro tips

- **Always use the same client name** as in the existing client folder. Don't switch between "Saad" and "Mohammed Saad" — pick what's already used.
- **The harder the niche, the more you'll lean on review sites.** B2B SaaS niches (where Reddit is silent) make Capterra/G2 the loudest signal source. Consumer niches lean on Reddit + YouTube comments.
- **For UK-specific niches, Trustpilot is gold.** UK reviewers are direct and unfiltered.
- **Hung Lee–style "category-naming" quotes are the highest-leverage finding** — when an industry voice publicly articulates a category that doesn't exist yet, that's the buyer's product hypothesis already named for you. Look for them.
- **The Pain Map's *Perfect Software Solution* section is the most important.** It's where the research becomes commercially actionable. Anchor pricing against an alternative the buyer is already considering (the in-house hire, the failed vendor, etc.) — never against another vendor pitch.
