# Corpus map — where the live transcripts are + how to mine

The funnel-architect council is grounded in a local transcript corpus (~47k transcripts, ~185 creators on sales/marketing/client-acquisition/persuasion). This file tells the mining agents where to look. If these paths don't exist (different machine), fall back to the distilled `creator-council.md` and flag that quotes are distilled, not freshly mined.

> **2026-10-13: `/Users/vik/Second Brain` no longer exists.** The roots below are historical. The surviving creator transcripts (Hormozi, Leila Hormozi, Charlie Morgan, Codie Sanchez, Naval, Sahil Bloom; ~1,692) are in Vik's Personal Brain library: `cd "/Users/vik/Personal Brain" && python3 tools/library.py search 'terms' --category 'Creator transcripts'`. Otherwise use the fallback above.

## Roots (historical)

| Path | What's there | Format |
|---|---|---|
| `/Users/vik/Second Brain/02 - Creators/<Name>.md` | per-creator index (video list, counts) | wikilink index |
| `/Users/vik/Second Brain/03 - Transcripts/<Category>/<Creator>/*.md` | the main transcript set, by topic then creator | markdown |
| `/Users/vik/Second Brain/scrape_output/<Creator>/transcripts/*.txt` | raw deep scrapes (Alex_Hormozi, Leila_Hormozi, Charlie_Morgan_Business, Charlie_Morgan_Main, Codie_Sanchez, Naval, Sahil_Bloom) | raw .txt |
| `/Users/vik/Second Brain/scrape_output_v2/<Category>/<Creator>/` | second scrape, by category → creator | mixed |
| `/Users/vik/Second Brain/06 - Research/_Coverage Report.md` | which creators are transcribed vs ZERO_TX | report |

Categories under `03 - Transcripts/`: AI · Bootstrapping Indie Hacker · Branding · Business Operations · Business Opportunities · Client Acquisition · Client Delivery and Results · Content Creation on LinkedIn and TwitterX · Human Psychology Persuasion · Marketing · Mindset · Negotiation · Personal Branding · Product Strategy PM · Sales

## Known creator → path (the council)

| Creator | Primary path |
|---|---|
| Alex Hormozi | `scrape_output/Alex_Hormozi/transcripts/` (~496) |
| Leila Hormozi | `scrape_output/Leila_Hormozi/transcripts/` (~276) |
| Charlie Morgan | `scrape_output/Charlie_Morgan_Business/transcripts/` + `Charlie_Morgan_Main/transcripts/` |
| Russell Brunson | `03 - Transcripts/Marketing/Russell Brunson/` |
| Sam Ovens | `03 - Transcripts/Client Acquisition/Sam Ovens/` |
| Myron Golden | `03 - Transcripts/Sales/Myron Golden/` |
| Daniel Fazio | `03 - Transcripts/Client Acquisition/Daniel Fazio (Cold Email Wizard)/` |
| The Futur / Chris Do | `03 - Transcripts/Branding/The Futur/` (+ a key file misfiled at `scrape_output_v2/Client_Delivery_and_Results/_videos/Pricing Creativity Livestream (The Futur).txt`) |
| Sabri Suby | `03 - Transcripts/Marketing/Sabri Suby (King Kong)/` |
| Frank Kern | `03 - Transcripts/Client Acquisition/Frank Kern/` |
| Greg Isenberg | `03 - Transcripts/AI/Greg Isenberg/` |
| Cole Gordon | `03 - Transcripts/Client Acquisition/Cole Gordon/` |
| 30 Min to President's Club | `03 - Transcripts/Sales/30 Minutes to President's Club/` |
| Nick Saraev | `03 - Transcripts/AI/Nick Saraev/` |
| Lara Acosta | `03 - Transcripts/Content Creation on LinkedIn and TwitterX/Lara Acosta/` |
| Iman Gadzhi | `03 - Transcripts/Client Acquisition/Iman Gadzhi/` (note: thin — mostly mindset, little funnel content) |
| Copy creators | `03 - Transcripts/Marketing/` + `scrape_output_v2/Marketing/` (Alex Cattoni, Copy That!, Joanna Wiebe/Copyhackers, Justin Goff, Roy Furr, April Dunford, StoryBrand) |

## Mining protocol (per agent, read-only)

1. **Locate** the creator's folder (try the table; if absent, `ls`/`find`/grep the roots). If a folder is empty / ZERO_TX, report unavailable and STOP for that creator (cite-or-cut — never invent).
2. **Grep** the transcripts for the dimension's key terms; read excerpts around the strongest 6–15 hits. Don't read everything.
3. **Extract** the creator's teaching as specific principles, each with a **VERBATIM substring quote + source filename**. Verify the quote is a real substring before keeping it (transcripts carry per-line timestamp prefixes — normalize for those).
4. **Apply** to THIS funnel: what to do, the spec, the number it's judged on. Return structured findings.

## Saving / porting the corpus

- The **distilled IP** (the reusable essence) lives in `creator-council.md` — that travels with the skill and works anywhere.
- The **live transcripts** stay in the vault (too large to bundle — ~47k files). This map points to them for fresh mining on Vik's machine.
- To make the skill fully portable with raw quotes on another machine, snapshot just the council creators' folders (the ~20 above), not the whole corpus. Ask before doing this — it's hundreds of MB.
