---
name: rioa-brand-pdf
description: Create polished, on-brand RIOA Consulting PDF documents (client sharables, guides, one-pagers, offer docs) written in Vik's voice. Use whenever Vik asks for a PDF, guide, sharable, doc, or report for RIOA or a RIOA client. Bundles Vik's locked voice profile and the RIOA brand styling so every PDF comes out sounding like Vik and looking like RIOA. Trigger on: "make a RIOA pdf", "client sharable", "write a guide for [client]", "in my voice", "RIOA doc", "brand pdf".
---

# RIOA Brand PDF

Build RIOA-branded PDFs that (1) sound like Vik and (2) look like RIOA. Two pillars, both mandatory: **the voice** and **the styling**. Never ship one without the other.

## Workflow

1. **Get the substance first.** Gather the real content (research, facts, the client's situation). Do not start the PDF until the content is correct. If research is needed, do it first.
2. **Read `references/vik-voice-profile.md` and FOLLOW IT.** This is the source of truth for voice. The hard bans below are non-negotiable.
3. **Write the body copy in Vik's voice** (see cheat-sheet below). Plain, conversational, never reads like a press release.
4. **Wrap it in the RIOA styling.** Build an HTML file using `references/brand-style.css` (or the `references/template.html` skeleton), then render to PDF with `references/build_pdf.py`.
5. **Verify before delivering:**
   - `grep -c "—" file.html` and `grep -c "–" file.html` must BOTH return 0. (em-dashes and en-dashes are banned)
   - Check page count and that no page is a near-empty orphan (every block uses `page-break-inside: avoid`).
   - Read it back: does it sit next to Vik's calibration samples and read as indistinguishable?
6. Save the final PDF to `/Users/vik/RIOA/` (or the relevant connected folder) and present it.

## Voice cheat-sheet (full rules in references/vik-voice-profile.md)

- **Register:** Casual Vik by default. Conversational, goofy, radically simple. "10% more extreme = more JOLLY, not more aggressive."
- **Ellipses** as connective tissue between thoughts...like this...always.
- **"I"-heavy.** "use" not "utilize", "hey" not "dear", "gonna" not "going to".
- Stretched words ("wayyy", "gooo"), multiple "!!!!", ":p", parenthetical asides, escalation builds ("not 1, not 2 hell not even 3 but 4").
- Swears freely where it lands. Humor via absurd exaggeration only. Analogies from money/school/real-world.
- Openers: a story or a humorous problem callout. Closers: a fun PS line with meme energy.
- One-line paragraphs ONLY for jaw-dropping hard-liners, not every line.

### HARD BANS (breaking these = wrong)
1. **NO em-dashes or en-dashes. EVER.** Use ellipses, commas, periods, parentheses, or "/" instead.
2. **No AI-slop cadence.** No clean antithesis ("This is not X. It is Y."), no polished symmetry, no press-release rhythm. Real Vik is messier and hotter.
3. **No LinkedIn clichés** ("let that sink in", "hit different", corny gen-z marketing speak).
4. **Never fake proof / never claim experience he doesn't have.** Industry stats are fine if labelled as industry stats, not his results.
5. **No over-explaining in a serious tone without humor.**

## Styling system (references/brand-style.css)

- Fonts: Helvetica Neue / Arial. A4, ~18-22mm margins.
- Palette: ink navy `#0f1b2d`, warm amber accent `#c9792e`, body `#1c2127`, muted `#5c6470`.
- Components ready to use: `.cover`, `.kicker`, `.lead`, `.callout` / `.callout.warn`, `.deep` (deep-dive teaching block with `.num` / `.title` / `.oneword` / `.think` / `.trap`), `.arc` (dark highlight band), styled `table`, `.checklist`, `.ps`, footer note.
- Headers can be lowercase/casual to match the voice; keep them readable.
- Every boxed component sets `page-break-inside: avoid` to kill orphan pages.

## Reference build command

```bash
pip install weasyprint --break-system-packages -q
python3 references/build_pdf.py input.html "/Users/vik/RIOA/Output_Name.pdf"
```

## Example of a finished doc in this system
The RIOA Market Sophistication Guide (for Saad) was built with this skill. Match that bar.
