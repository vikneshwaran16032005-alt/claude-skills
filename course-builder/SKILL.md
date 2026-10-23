---
name: course-builder
description: "Turn source material (books, transcripts, courses, notes, expert knowledge) into a from-zero teaching course in the user's own voice that takes a total beginner to competent. Use for courses, curricula, playbooks, bootcamps, onboarding or 'teach my team X from scratch' requests."
metadata:
  type: reference
---

# Course Builder

Build a course that takes a real beginner from zero to competent, in the user's own
voice, from whatever source material they've got. This skill is the validated playbook,
distilled from actually building one end to end (a sales course, "Zero to Closer," from
Imperium Academy + Alex Hormozi's ACQ + Copy That + a 96k-transcript operator corpus).

The whole point: a person who has never done the thing, and has never read any of the
source material, works through the course in order and comes out able to do it. Nothing
assumed. Nothing left out. Sounds like the person who made it, not like a manual.

## THE HARD RULE (above everything else)

**Quality over anything. Full depth, always. Leave no stone unturned.**

Size is never a constraint and never a reason to trim. The course must carry someone from
absolute zero to complete hero, covering absolutely everything, in full depth. A PDF that
runs into hundreds of pages is a success, not a problem.

Whenever "shorter" and "more complete" pull against each other, choose complete. Every
time. The only real failure this skill can produce is a GAP ... something a beginner
needed that got left out, glossed, rushed, or assumed. There is no such thing as "too
thorough" here. Cover it all.

Every other rule below serves this one. If a rule ever seems to argue for cutting depth,
you're misreading it ... depth wins.

## The locked formula (what "done right" looks like)

Everything below was learned by getting it wrong first (see "Why these rules exist"). If
you follow only this section, you'll get 90% of the way there.

1. **Multi-part, numbered modules, in order.** A beginner follows a path, not a reference
   binder. Each module builds on the last.
2. **Every module has the same five-part shape** so the reader never gets lost:
   1. *What this is, and why it matters* (short, plain)
   2. *How it works* (the actual teaching, from zero)
   3. *Watch it happen* (a concrete worked example)
   4. *Your drills* (things they DO before moving on)
   5. *Checkpoint* (how they know they're ready for the next module)
3. **The user's own voice, all the way through.** Pull the KNOWLEDGE from the sources,
   never the source author's voice. If the user has a voice profile, that is the
   authority; match it. Full casual if that's them. See `references/craft-rules.md`.
4. **Zero assumed knowledge. No blindspots.** The reader has never read the source books
   and has never done the thing. Every insider term is renamed to plain English or
   explained the first time it appears. Never gloss a heading with jargon.
5. **No source citations in the body.** The reader doesn't care that a play came from
   Hormozi or ACQ. Citations make it read like a research paper. Teach it as one seamless
   system. (Keep a private sources map in a brief, not in the deliverable.)
6. **Offer/context-agnostic teaching, anchored by ONE running worked example.** Teach the
   transferable craft so it works for anything, then show it landing in one concrete case
   the reader can follow the whole way through. Abstract-only doesn't stick; example-only
   doesn't transfer. You need both.
7. **Short paragraphs.** Mostly 1-3 sentences, then a line break. Walls of text kill
   readability. Longer only when a thought genuinely must hold together.
8. **Thorough beats short.** When "simple" and "complete" fight, stay complete and say it
   in simpler words. A beginner should never hit a gap. Length is fine; confusion is not.
9. **Keep it simple stupid.** If a smart friend who's never done the thing couldn't follow
   a line on first read, rewrite it simpler.
10. **Illustrate it.** A from-zero course lands far harder with a simple hand-drawn
    picture next to every load-bearing idea. Build them in a consistent charming
    marker-doodle style, for free, with legible labels ... see `references/diagrams.md`
    and the bundled `assets/diagram_kit.py`. Sample one in context first, then fan out.

## The build pipeline

Follow this order. Read `references/build-pipeline.md` for the detailed mechanics
(agent orchestration, recovery, rendering).

**Step 1 — Nail the forks before building anything.** A course can be built five
different ways and only one is what they want. Ask (MCQs are great here):
- Spine: taught through ONE running example, or general/agnostic with examples?
- Scope: just the core craft, or the surrounding business/ops layer too?
- Format: one document, or numbered multi-part modules?
- Depth: and confirm they want thorough-from-zero (they usually do; confirm the ceiling).
Getting these wrong is the single most expensive mistake. Confirm them explicitly.

**Step 2 — Extract the sources into briefs.** Don't draft from raw sources. Spawn
extraction agents (one per source or source-cluster) that distill each into a dense brief
of METHODS and FACTS in your own words (quotes under 15 words, no reproduction of
copyrighted text). Save briefs to a `_briefs/` folder. These become the shared evidence
pack every drafting agent reads. Pull from the corpus / real practitioners where a claim
needs backing.

**Step 3 — Map the architecture.** Write a course-architecture spec: the full module
list, what each covers, which briefs feed it, and the five-part module shape. This is the
table of contents you'll confirm with the user before spending big.

**Step 4 — Build ONE part as the depth template, and CONFIRM it.** Draft the first
module (or first two) at full intended depth. Render it. Put it in front of the user and
ask: is this the right depth, voice, and format? This one checkpoint saves you from
building 14 modules wrong. Do not skip it. Lock the template on their yes.

**Step 5 — Mass-produce, in parallel, scoped small.** Once the template is locked, spawn
drafting agents each responsible for 1-2 modules, all pointed at: the architecture spec,
the approved template module (match it exactly), the voice profile, and their specific
briefs. Small scope per agent matters: big drafts hit session/usage limits and die
mid-write. Each agent writes to its own file so nothing is lost if one fails; re-run only
the ones that don't complete.

**Step 6 — Stitch and render.** Concatenate the modules in order (a small `assemble.py`
that re-stitches on every edit is worth writing), add any appendix (a script/template
bank), and render via the `rioa-pdf` skill. BOTH editions now handle diagrams: the Night
Ledger (`_md_to_pdf_nightledger.py`, dark) and the Day Ledger (`_md_to_pdf_dayledger.py`,
light/print) — offer both. Size doesn't matter, it can be hundreds of pages. Both cap
image height (a tall diagram becomes a centered strip, never a crash) and put part
dividers on the same page as their first module (no stranded empty part page). Read a few
rendered pages yourself as a day-one beginner before it ships. Gotcha: a PDF viewer can
show a STALE cached render, so verify against the freshly-written file, not the viewer.

**Step 7 — Voice pass if needed.** If any drafting drifted toward the source author's
voice or got corporate, run a voice-conversion pass (agents, against the voice profile)
that keeps every fact and only changes how it's said. See `references/craft-rules.md`.

**Step 8 — Adversarial end-to-end read (do NOT skip).** Even when it all looks done,
spawn ONE fresh agent to read the whole course start to finish AS A TOTAL BEGINNER and
report only real problems: seam breaks (a module that ends like the course is over, or
opens cold), cross-module repetition or contradictions (the same thing taught twice, or
two versions that disagree), worked-example discontinuity (discovery surfaces 2 problems
but the pitch delivers 3), undefined jargon, price/fact drift, mismatched diagram
captions. Then apply the fixes surgically (in voice), re-stitch, and re-render. This
catches the seam issues that per-module drafting structurally cannot see.

## Why these rules exist (the corrections, learned the hard way)

Each rule above is a scar. Building the same deliverable went through these corrections,
in this order. Knowing WHY protects you from repeating them:

- **Started as a modular "kit" (a folder of reference files).** The user wanted a single
  guided artifact you read start to finish, not a filing cabinet. → Lesson: a course is a
  JOURNEY, structure it as one path.
- **Drafted in the source author's voice.** Mirroring a source's architecture quietly
  imports its voice too (the clipped maxims, the drill-sergeant tone). The user said "this
  isn't my voice... I want the knowledge, not the guy's mannerisms." → Lesson: extract
  knowledge, write in the USER's voice via their profile; strip the source's stylistic tics.
- **Too corporate / stiff.** "Keep it simple stupid, I'm building this with friends, not
  a corporation." → Lesson: plain, warm, casual to the user's actual register; kill
  parallel-triad maxims and press-release symmetry.
- **Assumed the reader knew the source material.** Citations like "(ACQ)" and undefined
  jargon everywhere. "My mates haven't read any of this." → Lesson: ZERO assumed
  knowledge, strip citations from the body, explain/rename every term on first use.
- **Kept the reference structure instead of a beginner's path.** "Organize it as if you're
  leading someone by the hand from start to finish, no blindspots." → Lesson: chronological
  handholding journey.
- **Then the real reframe:** the deliverable wasn't "how to run our specific thing," it
  was "teach a total beginner the craft so they could do it anywhere." → Lesson: nail the
  spine/scope/format forks (Step 1) BEFORE building; a specific-application handbook and a
  from-zero general course are different books.
- **Depth confirmed perfect, but walls of text.** → Lesson: short paragraphs, always.
- **The text was great but wanted pictures.** The user loved hand-drawn marker-doodle
  diagrams and asked for one at every major section. The image generator was out of
  credits, so we built our own with matplotlib's hand-drawn mode... free, consistent,
  legible. → Lesson: illustrate from-zero courses; a shared diagram kit + a
  sample-first check + a fan-out with a per-agent quality gate makes 40+ diagrams clean
  and cheap. See `references/diagrams.md`.
- **Looked completely done, but a beginner-read found four seam bugs.** After all modules,
  diagrams, and both PDFs were rendered, a fresh end-to-end read caught: a module that
  ended like the whole course was over (no handoff to the next), the same booking/no-show
  material re-taught across two modules with a contradictory move-count, a worked example
  whose discovery surfaced 2 problems while the pitch delivered 3, and undefined
  team-jargon in the appendix. → Lesson: per-module drafting is blind to the seams between
  modules; a whole-course beginner-read (Step 8) is not optional.

The meta-lesson under all of these: **confirm the shape with the user on a small sample
before mass-producing.** Every correction above would have been cheaper caught on one
module than on the whole course.

## Where the source resources live (use the master map)

Do NOT hardcode source paths from memory; they move and go stale. The authority on WHERE
every source resource is, what's inside it, and its condition is the **Master Map** ...
The old `/mastermap` skill and `/Users/vik/RIOA/_MASTER-MAP.md` no longer exist (removed 2026-10-13).
For any "where is / what's inside / is it usable" question, search Vik's Personal Brain library first:
`cd "/Users/vik/Personal Brain" && python3 tools/library.py search 'terms'` (then `read RECORD_ID`), before sending extraction agents anywhere.

The standard source pack for a course, as mapped there (verify the entry's date; re-check
anything older than ~30 days):
- **Imperium Academy extracts** (Estate 1) ... the cold-call / DM / lead-sourcing /
  appointment-setting / closing / offers systems. `/Users/vik/{PROJECT} Next Level!/1. Imperium Academy/0. RIOA Extracts/`.
- **Copy That** (Estate 2) ... the copywriting + persuasion library.
  `/Users/vik/{PROJECT} Next Level!/2. Copy That/0. RIOA Extracts/`.
- **Hormozi + the direct-response canon + ACQ handbooks** (Estate 3).
  `/Users/vik/{PROJECT} Next Level!/4. Alex Hormozi/` and `/2. Copywriting/`.
- **The 96k operator corpus** (Estate 4) ... cited consensus to BACK claims. LOST: `~/OperatorBrain` and the
  `/brain` skill no longer exist; do not cite the 96k corpus. Use the Personal Brain library's creator transcripts (Hormozi, Charlie Morgan, Leila Hormozi, Codie Sanchez, Naval, Sahil Bloom) via `tools/library.py search`.
- **The user's voice profile** ... `~/.claude/skills/copywriting-master/references/vik-voice-default.md` (canonical; the old OperatorBrain profile is lost).

**Worked precedent (the first course built with this skill):** "Zero to Closer" ...
course at `/Users/vik/Project 7/course/` (modules + `Module_1-2_Foundation.md` = the
approved depth/voice template), source distillations in
`/Users/vik/Project 7/ops/sales-kit/_briefs/`, render via the `rioa-pdf` Night Ledger
script. Read those `_briefs/` as examples of the extraction-brief format Step 2 produces.

When this skill adds, moves, or repairs a resource, obey the master map's MAINTENANCE LAW:
update the matching entry and its changelog.

## Reference files

- `references/craft-rules.md` — the voice rules, the zero-assumed-knowledge discipline,
  the format bans (no em-dashes if the voice bans them, no citations, short paragraphs),
  and how to run a voice-conversion pass. Read before drafting or converting voice.
- `references/build-pipeline.md` — the agent orchestration in detail: extraction agents,
  the template-first checkpoint, parallel drafting scoped to 1-2 modules, session-limit
  recovery, stitching, and rendering. Read when setting up the build.
- `references/module-template.md` — the five-part module shape with an annotated exemplar,
  so drafting agents have a concrete target. Point every drafting agent at this.
- `references/diagrams.md` — how to illustrate the course with consistent hand-drawn
  diagrams for free (matplotlib xkcd mode), the bundled `assets/diagram_kit.py`, the
  sample-first + fan-out + quality-gate flow, and placement rules. Read when adding visuals.
