# Build pipeline: orchestration mechanics

How to actually produce a book-length course without it dying halfway or drifting. This is
the operational layer under the pipeline in SKILL.md.

## 1. Extraction agents (sources -> briefs)

Spawn one agent per source or source-cluster. Each reads its source (a book PDF by page
range, a folder of transcripts, a set of corpus pulls) and returns a dense brief of
METHODS and FACTS in its own words. Rules for the agents:
- Extract the underlying method/framework, not the source's prose. Any direct quote stays
  under 15 words. Never reproduce copyrighted text; you are learning the method (methods
  and facts are not copyrightable), then re-expressing it.
- Capture exact numbers, sequences, named frameworks, cadences.
- Save each brief to a `_briefs/` folder. These are the shared evidence pack.
For a corpus, run targeted retrievals per topic and stage the cited results as briefs too;
use them to BACK claims (cite creator in the brief, but NOT in the final course body).

## 2. Architecture spec

Write one file that is the course's table of contents: every module, one line on what it
covers, which briefs feed it, and the five-part module shape restated. This is what you
confirm with the user before spending big. Include the locked forks (spine/scope/format/
depth) at the top so every drafting agent inherits them.

## 3. Template-first checkpoint (the most important step)

Draft the FIRST module (or first two) at full intended depth. Render it (see rendering
below). Show the user and get an explicit yes on depth, voice, and format. This single
checkpoint is what saves you from mass-producing the whole course wrong. When they
approve, that file becomes the literal template every other agent matches. If they ask
for a change (e.g. "shorter paragraphs"), apply it to the template and bake it into the
drafting instructions before mass-producing.

## 4. Parallel drafting, scoped small

Spawn drafting agents each owning 1-2 modules. Why small: big drafts (12k+ words or long
runs) reliably hit session/usage limits and die mid-write. 1-2 modules (~7-10k words)
completes. Each agent gets, in its prompt:
- the architecture spec (find your modules + the module shape)
- the APPROVED template module: "match its depth, voice, structure exactly"
- the voice profile + anti-voice
- its specific briefs + the relevant already-written framework source
- the full craft rules (from `craft-rules.md`): from zero, no citations, short paragraphs,
  offer-agnostic teaching with the running example only in "Watch it happen", the voice's
  hard bans, thorough.
- Each writes to its OWN file (e.g. `Module_5-6.md`). This is critical: if one agent dies
  on a limit, its file is missing or partial but every other module is safe. Re-run only
  the failures.

Model choice: use a strong model (Opus-class) for the teaching modules where voice and
depth matter; a cheaper model (Sonnet-class) is fine for mechanical passes (reformatting,
stripping citations, converting an existing draft's voice).

## 5. Recovery

Agents hitting a usage ceiling report a failure but often finished the WRITE before dying
(the failure is in cleanup/reporting). Always check the file on disk before assuming loss:
`wc -w` and read the last lines. If it's complete, keep it. If partial or missing, re-run
that one agent. Completed files persist across the ceiling reset.

## 6. Stitch and render

Write a tiny `assemble.py` that re-stitches the modules + appendix on every edit (it can
assert no em-dashes as a guard). Then render via `rioa-pdf`. BOTH brand renderers handle
`![caption](img/x.png)` diagrams now: Night Ledger (dark) and Day Ledger (light/print) —
offer both editions.
`.../rioa-pdf/.venv/bin/python .../rioa-pdf/_md_to_pdf_nightledger.py <in.md> <out.pdf> "Title -- Subtitle" "Classification" "RUNNING HEADER" "NN"`
(swap `_md_to_pdf_dayledger.py` for the light edition, same args). Run from the course dir
so `img/…` paths resolve. Both cap image height (a tall diagram becomes a centered strip,
never a LayoutError). Upgraded 2026-07-22 (both Night + Day renderers): every `# PART` /
`# APPENDIX` divider (H1 OR H2) now starts on a FRESH page with its first module under it
(no stranded divider, no blank part page), AND the renderer auto-generates a **Table of
Contents** page after the intro via a 3-pass build (captures where each PART/Module heading
lands, so page numbers stay correct even as the TOC shifts pages) — you get a real TOC for
free, no markup needed. The **diagram kit** also crops every image tight (`bbox_inches=
"tight"`; `compare` sizes its divider + height to the item count) so there's no wasted blank
space. Size is not a constraint; hundreds of pages is fine. Watch the
glyph pitfalls (no raw unicode the hand-drawn font lacks, e.g. ★ or a checkmark char →
draw them as strokes instead; the pause-legend "---" is the only allowed triple-dash).
Gotcha: a PDF viewer may show a STALE cached render — verify against the freshly-written
file, not the viewer, before believing a bug (or a fix).

## 7. Self-review, then an adversarial end-to-end read

First, YOU read a sample of rendered pages as a day-one beginner: assumed knowledge,
surviving jargon or citation, walls of text, voice drift, broken diagrams. Fix.

Then, before calling it done, spawn ONE fresh agent to read the ENTIRE course start to
finish as a total beginner and report only real problems. Per-module drafting is
structurally blind to the seams between modules, so this pass reliably finds what you
can't: a module that ends like the course is over (no handoff), the same thing taught
twice across modules (sometimes with contradictory details), a worked example that
discovery and pitch disagree on (2 problems surfaced, 3 delivered), undefined jargon,
price/fact drift, mismatched captions. Apply the fixes surgically in voice, re-stitch,
re-render both editions. Do not skip this even when everything looks finished ... on the
first course built this way it found four real seam bugs after the book already looked
done. Then deliver, and surface any still-open inputs only the user can fill.

## Notes learned in practice

- Confirm the forks (SKILL.md Step 1) with MCQs; users decide fast and it prevents the
  most expensive mistakes.
- Show, don't tell: users steer far better off a rendered sample than an abstract plan.
- Keep the sources map private; the course body is citation-free.
- The running-example module (end-to-end) is best drafted last, by an agent that has read
  the whole rest of the course, so it can point back to each module.
