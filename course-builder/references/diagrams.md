# Illustrating the course: hand-drawn diagrams (no image credits)

A from-zero course lands far harder when the load-bearing ideas have a simple picture next
to them. The reference we aim for is the charming hand-drawn marker-doodle style people
love in business books (think a coach sketching a concept on a napkin). This is how we get
that look reliably, consistently, for free, with legible labels and zero AI-image credits.

## The technique: matplotlib "xkcd" mode

matplotlib has a built-in hand-drawn sketch mode (`plt.xkcd()`) that renders wobbly marker
lines and hand-ish lettering. It produces PNGs directly, no image model or credits needed,
and YOU control every label so text is always legible (no AI text-garble). It renders
consistently across dozens of diagrams, which one-off image generation can't.

Install once into the render venv if missing:
`<rioa-pdf .venv>/bin/python -m pip install matplotlib`

## The diagram kit (bundled)

`assets/diagram_kit.py` (in this skill) is a ready-to-use kit. Copy it into the course
folder. It fixes ONE consistent look (dark marker ink on a warm cream "napkin" card, so a
framed sketch reads like it's pinned onto the page) and exposes 8 composer functions that
each build a clean, auto-laid-out diagram from short label lists:

- `fraction(name, top, bottom, left)` ... a value-equation / ratio (things up top, things below)
- `flow(name, steps, direction)` ... boxes + arrows, left-to-right or top-down (a process, a call shape)
- `compare(name, left_title, left_items, right_title, right_items)` ... this vs that (X's vs checks)
- `funnel(name, stages)` ... a narrowing funnel (a pipeline)
- `timeline(name, points)` ... a horizontal line with ticks + notes (a cadence, a day-by-day plan)
- `ladder(name, rungs)` ... rungs climbing up (an offer ladder, an escalation)
- `meter(name, label, left_end, right_end, marker_frac, marker_label)` ... a dial/spectrum (how fast you talk)
- `cycle(name, steps)` ... a loop (agree -> answer -> ask again)

Each writes `img/<name>.png` and returns the path. Composing a diagram is 1-2 lines, so
agents can't easily produce ugly layouts ... the kit does the layout, they pick the shape
and the labels. Extend the kit with new composers only when a concept genuinely needs a
shape the 8 don't cover; keep the same INK/PAPER/xkcd constants so everything matches.

## The build flow (sample-first, then fan out)

1. **Prove one, in context.** Generate ONE diagram, drop it under the REAL teaching
   paragraph it illustrates, render that page, and show the user. Confirm the look before
   making dozens. (Note: the user may not see images from your tool results ... save the
   sample PDF into their project and give them the file path to open.)
2. **Fan out.** One agent per module (or module-pair). Each: reads its module + the kit,
   picks the 3-5 load-bearing concepts per module (aim ~1 per major section ... "heavy" if
   the user wants it), composes the fitting diagram from the kit, and inserts the image.
3. **Quality gate (required).** Each agent builds a contact-sheet PNG of its new diagrams
   and READS it (subagents can read images), then fixes any cramped or overflowing labels
   and regenerates until clean. This catches the one real failure mode: long labels
   spilling their boxes. Keep labels to a few words; use `\n` to wrap.
4. **Placement.** Insert on its own line, blank line before and after, right after the
   paragraph that teaches the concept (before the next heading):
   `![plain lowercase caption that says what the picture shows, no em-dashes](img/<name>.png)`
5. **Re-assemble and render.** Re-run the assembler, then the Night Ledger renderer, which
   already frames `![caption](path)` images as a bordered card with a gold caption.

## Rules

- One visual language for the whole course: only the kit composers, one palette. Mixed
  styles read as sloppy.
- Labels short and legible; the quality gate is not optional.
- Captions obey the same voice bans (no em-dashes, plain words).
- Reuse a diagram across modules if the same picture fits (don't redraw the value equation).
- The renderer's default page break puts each `## PART` divider on its own page; ordinary
  section headers use a conditional break. (Both live in `_md_to_pdf_nightledger.py`.)

## Exemplar

The first illustrated course, "Zero to Closer," lives at `/Users/vik/Project 7/course/`:
`diagram_kit.py` (the kit), `img/` (the rendered diagrams), and the module files with the
`![...](img/...)` inserts. Read those for a concrete pattern of concept -> composer choice.
