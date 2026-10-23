---
name: rioa-pdf
description: "Convert markdown into a RIOA-branded PDF matching rioaconsulting.com (SITE theme by default; legacy styles only on request). Use for 'rioa pdf', 'brand pdf', 'make this a pdf', 'ship as pdf' or any client-facing document; not for questions about PDFs."

---

# RIOA PDF Generator

Convert a markdown file into a brand-aligned PDF in RIOA's house style.

## DEFAULT THEME: SITE (decided by Vik 2026-10-13: "match the live site")

The brand source of truth is the live site, rioaconsulting.com. Its CSS tokens (read 2026-10-13): field `#080807`, panel `#10100e`, edge `#29261f`, text `#f4f0e6`, cream `#f0e8d9`, muted `#a39e92`, gold `#b89452`, aura `rgba(168,112,38,.36)`. Type: Instrument Sans (headings 500, body 400, bold 600), Cormorant Garamond italic for emphasis words, Space Mono for code and ledger labels. The fonts in `fonts/` were converted from the site's own woff2 files (OFL licences included). If the site's tokens change, update `_md_to_pdf_site.py` to match; the site wins.

Run (reportlab is not installed system-wide; `uv` supplies it in a cached throwaway env):

```bash
uv run --no-project --with reportlab python ~/.claude/skills/rioa-pdf/_md_to_pdf_site.py <in.md> <out.pdf> "Title -- italic subtitle" "Client Confidential" "Websites for U.S. local businesses"
```

Args 3-5 are optional: title (`" -- "` splits an Instrument Sans title from a Cormorant italic subtitle on the cover), footer classification, cover pill text. Page 1 is a site-style cover (wordmark with gold dot, pill eyebrow, large title, soft gold aura); content starts on page 2 with the running header/footer. Verify by rendering pages to PNG (`uv run --no-project --with pymupdf python -c "import pymupdf; ..."`) and looking at them before shipping.

Everything below describes the older themes and the shared renderer behavior (tables, callouts, lists, TOC, SOP cards), which the SITE theme inherits.

## Legacy editorial theme (`_md_to_pdf.py`)

Takes a markdown file. Spits out a print-ready PDF with:

- **Headings**: Cormorant Garamond (display serif) -- 30pt H1, 20pt H2, gold-colored H3
- **Body**: Jost (clean sans-serif) -- 10.5pt charcoal text
- **Palette**: charcoal `#1a1614` (headings) / `#2a2622` (body) / cream `#f5ede0` (code+table backgrounds) / gold `#b08d57` (accents)
- **Tables**: cream/gold header band, warm borders, subtle alternating row backgrounds
- **Prose callouts** (markdown `>` blockquote): cream-filled, gold-bordered box with body font. If first line is ALL CAPS and short, it renders as a gold label above the prose.
- **Code blocks** (markdown ` ``` `): cream background, gold border, Courier text -- use only for actual code/CLI strings/template values.
- **Lists**: gold bullet markers `•` and nested chevrons `›`, gold-bold numbered list numbers
- **Horizontal rules**: thin gold lines
- **Page break on every H2 section**: each `## Section X` starts on a fresh page (skipped only when the H2 is the literal first flowable in the doc).
- **Persistent header & footer on every page**: header has "RIOA CONSULTING" (gold bold) on the left and the document title (warm gray) on the right, with a thin gold rule below. Footer has the classification (warm gray) on the left and "Page N" on the right, with a thin gold rule above.

Fonts auto-download from Google Fonts on first use (~3-5MB), cached in `./fonts/`. Falls back to Times-Roman + Helvetica if download fails.

## When to use this

Use this skill when Vicky says any of:

- "Convert [file].md to PDF"
- "Ship [doc] as a PDF"
- "Make this a brand PDF"
- "Generate the PDF in my style"
- "PDF it"
- "Make it brand-voice"

Do NOT use for plain markdown rendering questions, PDF *theory* questions, or non-RIOA branding requests.

## How to use

### Step 1: Confirm the inputs

You need:

1. **Source markdown file path** (absolute path)
2. **Output PDF path** (absolute path -- usually same directory, same name with `.pdf`)
3. **Document title** (shown in PDF metadata; usually the H1 of the doc)

Ask Vicky for these if not obvious from context.

### Step 2: Make sure the markdown is in brand voice

Before converting, check the markdown matches RIOA brand voice (per `CLAUDE.md` in any RIOA project):

- Energetic, motivational, casual
- Short punchy sentences
- Conversational tone
- American spelling
- Grade 5-7 reading level
- Questions as hooks
- Caps/bold for emphasis
- Analogies from: restaurants, laundromats, grocery lines, airplanes, sports teams
- No em dashes -- use `--` instead
- Straight quotes only
- No buzzwords or vague claims
- Every claim backed by a number or test to run

If the markdown is NOT in brand voice, OFFER to rewrite it before converting. Don't silently push generic copy through the brand styling.

### Step 3: Run the converter

Copy `_md_to_pdf.py` from this skill folder into the same directory as the markdown file (or a sibling directory). Run it with CLI args:

```bash
python _md_to_pdf.py <input.md> <output.pdf> "<Title>"
```

If no args, the script falls back to its embedded `jobs` list (useful for batch jobs).

The script handles:

- **H1**: large display heading, no auto page break
- **H2**: section heading -- triggers a `PageBreak` so each section starts on a fresh page
- **H3**: gold sub-heading
- All headings have `keepWithNext` so they don't orphan at page bottoms
- **Markdown tables** -> styled ReportLab Tables with cream/gold header band, alternating rows
- **Fenced code blocks** ( ``` ``` ``` ``` ) -> cream-bordered Tables with Courier paragraphs (lines wrap). Use ONLY for actual code/template strings.
- **Markdown blockquotes** (`>` prefix) -> prose callouts with cream fill and gold border, body font. ALL-CAPS first line auto-renders as gold label.
- **Bullet lists** -> gold `•` markers, with `›` for nested (3+ leading spaces)
- **Numbered lists** -> gold-bold numbers
- **Horizontal rules** -> gold HRFlowable
- **Inline `**bold**`** -> Helvetica-Bold (variable fonts can't do bold cleanly)
- **Inline `*italic*`** -> brand italic font
- **Inline `` `code` ``** -> Courier inline
- **Running header** on every page: RIOA CONSULTING (gold bold) + doc title (warm gray) with thin gold rule
- **Running footer** on every page: classification text (warm gray) + Page N with thin gold rule

### Step 4: Read the PDF back to verify

ALWAYS read the resulting PDF with the Read tool after generating it. Inspect every page for:

- Lines that should be separate but got concatenated -> add blank lines in markdown
- Glyphs rendering as `■` (filled square) or invisible -> see "Known Glyph Pitfalls" below
- Headings orphaned at bottom of page -> already handled via `keepWithNext` but verify
- Tables splitting awkwardly across pages
- Pages with only 1-2 lines and rest blank (page-break issues)

Fix any issues found, then regenerate. Don't ship a PDF you haven't visually inspected.

## Brand voice reminder (for the markdown content)

If you're WRITING the markdown (not just converting an existing one), follow Vicky's brand voice from his `CLAUDE.md` PART 6:

- **Open every section with a hook question or punchy claim** -- "Ever wondered why X?", "Two big rules:", "Here's the deal:"
- **Use analogies often** -- restaurants, laundromats, grocery lines, airplanes, sports
- **Punchy short sentences** -- avoid commas, prefer periods
- **CAPS for hard rules** -- "DON'T", "RULE 1:", "FOREVER"
- **Numbered every step explicitly** -- "Step 1.2.3", "Day 1, Day 2"
- **Cost notes inline** -- "$30", "$85/month", "free tier"
- **Time estimates per section** -- "Time: 30 minutes"
- **Real talk** callouts for blunt truths: "Real talk: 9 times out of 10 it's a copy-paste error."
- **Closer like a coach** -- "You got this. Now go build."

## Known glyph pitfalls (DON'T trip on these)

Jost variable font (the body face) is missing several decorative Unicode glyphs. Use only confirmed-safe glyphs in markers and content:

| Glyph | Codepoint | Renders? |
|-------|-----------|----------|
| `•` | U+2022 BULLET | ✅ |
| `›` | U+203A SINGLE RIGHT-POINTING ANGLE QUOTATION MARK | ✅ |
| Standard ASCII | various | ✅ |
| `--` (two hyphens) | -- | ✅ |
| `→` | U+2192 RIGHTWARDS ARROW | ❌ INVISIBLE |
| `◦` | U+25E6 WHITE BULLET | ❌ FALLS BACK TO `■` |
| `▪` | U+25AA BLACK SMALL SQUARE | ❌ INVISIBLE |
| `☐` | U+2610 BALLOT BOX | ❌ FALLS BACK TO `■` |

For any glyph Jost lacks, wrap it in `<font name="Helvetica" color="#b08d57">CHAR</font>` to force Helvetica fallback. **Note: the attribute is `name`, NOT `face` -- `face` is silently ignored.**

For checkboxes in checklists, use literal `[ ]` not Unicode boxes.

For arrows, use `->` (ASCII) or `›` (chevron we already use for nested bullets).

## Other gotchas

- **Consecutive non-blank lines collapse into one paragraph.** Add blank lines between any 3 facts you want on 3 separate lines (subtitle blocks, cost summaries, etc.)
- **Variable fonts render at default weight only.** `<b>` tags inside body text won't visually bold using Jost-Regular as parent. The skill's converter pairs Jost with Helvetica-Bold for inline bold (acceptable family mix).
- **Headings have `keepWithNext=1`** so they don't orphan -- already in the script.
- **Code blocks render as cream-bordered tables** with Courier paragraphs that wrap on long lines.
- **First run downloads ~3-5MB of fonts.** Subsequent runs are instant. Delete `./fonts/` to force re-download.

## Example invocation

User says: "Convert this to a PDF in brand voice -- E:/clients/aziz/onboarding.md"

Steps you take:

1. Verify the file exists and is in brand voice (skim it)
2. If not in brand voice, offer to rewrite first
3. Run directly from the skill folder (no copy needed):
   `python "~/.claude/skills/rioa-pdf/_md_to_pdf.py" "E:/clients/aziz/onboarding.md" "E:/clients/aziz/onboarding.pdf" "Onboarding -- AurexAuto" "Client Confidential"`
4. Read the resulting PDF back, page by page
5. Fix any issues (glyph fallbacks, line concatenation, page breaks)
6. Confirm clean output

## Markdown conventions for best results

- **Use `## Section X:` for major sections** -- each gets its own page automatically.
- **Use `>` blockquotes for callouts/quotes/highlights** (NOT triple-backticks). The first ALL-CAPS line becomes a gold label.
- **Use ` ``` ` triple-backticks ONLY for actual code/template values** (DNS records, command lines, raw email subject lines).
- **Add blank lines between facts you want as separate visible lines** (subtitle blocks, cost summaries). Consecutive non-blank lines collapse into one paragraph.
- **Tables**: standard markdown `| col | col |` syntax. Cells wrap automatically.
- **Sub-bullets**: use 3+ leading spaces under a parent bullet to trigger nested `›` style.

## Reference: canonical implementation

The current canonical converter lives at:
`E:/linkedin messages/Clients/Aziz (client)/Cold Email Setup/_md_to_pdf.py`

This skill ships a copy of that file. If the canonical version is updated (better features, bug fixes), copy it back into this skill folder so future invocations get the improvements.

---

## LEGACY THEME: NIGHT LEDGER / DAY LEDGER (locked 2026-07-13, superseded by SITE on 2026-10-13; use only if Vik asks)

**Design principle ("First Blood"):** one ink field · one red wound (the vertical cut + node, the day-90 tick — red is INFORMATION, never decoration) · gold ledger craft (rules, ticks, numerals) · bone words. (The philosophy doc lived under `/Users/vik/RIOA/`, which no longer exists.)

**Typography (locked):** Anton (display/H1/H2) · Space Grotesk (body) · Space Mono (code/ledger labels). Fonts ship in `fonts/`.

**Palette:** ink #0d0a0b · blood #8f1116 (titles + the wound) · gold #c39f63 / #d4b884 (headings, accents, chapter label) · bone #e8e0d5 (body) — Night. Day Ledger = paper #f2ece1 field, charcoal body, gold #b08d57, same red wound.

**Renderers (same CLI as the original, plus a 6th arg = chapter number):**
```bash
.venv/bin/python _md_to_pdf_nightledger.py <in.md> <out.pdf> "Title -- Subtitle" "Client Deliverable" "FIRST CLIENT SPRINT" "03"
.venv/bin/python _md_to_pdf_dayledger.py   ...same args...   # light/print version
```
Cover = full-bleed page 1 (content starts page 2): giant tone-on-tone chapter numeral, 90-tick day scale, the cut + node, CHAPTER NN lockup. Client deliverables = chapters 00–05 by folder. Use NIGHT for client-facing digital; DAY for print/light contexts. The original charcoal/cream/gold `_md_to_pdf.py` remains for legacy/editorial docs.

**Gotcha:** there is no `.venv` in this skill folder any more. Run any renderer with `uv run --no-project --with reportlab python <script> ...` (reportlab is not in system Python).
