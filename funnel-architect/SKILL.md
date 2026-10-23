---
name: funnel-architect
description: "Build, audit or fix a client-acquisition funnel (offer ladder, lead magnet, guarantee, email sequence) with a council of direct-response creators (Hormozi, Brunson, Suby, Charlie Morgan and others), then stress-test it. Triggers: 'build/fix/audit my funnel', 'funnel for [client/niche]'."
argument-hint: [whose funnel + the offer/audience, or "audit existing"]
---

# Funnel Architect

You convene a **cooperative council of direct-response masters** to build one bulletproof, money-printing funnel. This is the inverse of an LLM-council debate: the creators do not clash to win — **each contributes the part they're best at, and the funnel is the sum of their expertise**, pressure-tested until it holds. Every claim is grounded in a real transcript quote from the corpus (cite-or-cut). The output is a complete funnel blueprint plus the actual assets.

**Load these before building:**
- `/Users/vik/.claude/skills/funnel-architect/references/creator-council.md` — the distilled creator-experts knowledge base (who owns what, their core principles). This is the council roster + their playbooks.
- `/Users/vik/.claude/skills/funnel-architect/references/corpus-map.md` — where the live transcripts are, and how to mine them.
- `/Users/vik/.claude/skills/funnel-architect/templates/funnel-blueprint.md` — the output template.

## The cooperative council (dimension → experts)

Each funnel dimension is owned by the creators who actually teach it. They build their stage; the architect (you) weaves the stages into one funnel.

| Dimension | Council members |
|---|---|
| **D1 — Offer ladder & pricing** | Alex Hormozi, Russell Brunson, Sam Ovens, Charlie Morgan, Myron Golden, The Futur (Chris Do), Daniel Fazio |
| **D2 — Guarantees & risk reversal** | Alex Hormozi, Charlie Morgan, Sabri Suby, Leila Hormozi, Myron Golden |
| **D3 — Front-end pull** (magnet → opt-in → email → community) | Sabri Suby, Frank Kern, Greg Isenberg, Russell Brunson, Charlie Morgan |
| **D4 — Ascension & qualification** | Cole Gordon, 30 Min to President's Club, Iman Gadzhi, Charlie Morgan |
| **D5 — Traffic** (content + outbound) | Daniel Fazio, Nick Saraev, Lara Acosta, Charlie Morgan |
| **Ops & survivability** (cross-cut) | Leila Hormozi |
| **Copy pass** (Phase 2, after structure) | Alex Cattoni, Copy That!, Joanna Wiebe, Justin Goff, Roy Furr, April Dunford, StoryBrand |

See `creator-council.md` for each member's distilled playbook so you know what each will contribute before mining.

## The process (run in order)

### Phase 0 — Intake (Rule of One for the funnel)
Lock these with the user before building. If fuzzy, ask ONE question at a time.
- **Whose funnel** + the **offer** (what's sold) + the **audience** (one ICP, their awareness/sophistication stage).
- **Build-from-scratch** vs **audit-and-upgrade existing**. (If existing assets exist, read them first.)
- **Real constraints** — team size, cash/runway, market/payment realities, compliance limits. These are what make the funnel *bulletproof or fragile*; the council tests against them.
- **Depth** — quick (3 core dimensions) vs full (all 5 + copy).

### Phase 1 — Convene the council
Map the funnel's dimensions to the council members (table above). For an audit, also read the existing assets so contributions compare against reality.

### Phase 2 — Each expert contributes (parallel mining)
Spawn one read-only subagent per creator (or per dimension), using the corpus paths in `corpus-map.md`. Each agent:
1. Greps its creator's transcripts for the dimension's concepts; reads the highest-signal excerpts (not everything).
2. Extracts that creator's teaching as specific, usable principles — **each carrying a VERBATIM substring quote + source filename** (cite-or-cut: drop any principle whose quote can't be verified).
3. Returns its contribution applied to THIS funnel (what to do, the specific spec, the number it's judged on).
Run the creators for a dimension in parallel; run dimensions in parallel where the window allows.

### Phase 3 — Cooperative synthesis
Weave the contributions into one coherent funnel. The council members mostly complement (each owns a stage). Where two genuinely conflict (e.g. "add a mid-rung" vs "prove one tier first"), **reconcile for THIS context** — the panel's combined answer, decided by the user's real constraints, not by which creator is louder.

### Phase 4 — Adversarial verification (make it bulletproof)
For every high-impact decision, run a skeptic pass: one agent tries to REFUTE it against the funnel's real constraints (budget, team, cash, market, compliance). A decision ships only if it survives. This is the cooperative council pressure-testing its own work — kill plausible-but-fragile choices before they reach the funnel. (Verdicts: SURVIVES / DOWNGRADE / KILL.)

### Phase 5 — Output the blueprint + assets
Write the funnel to the `funnel-blueprint.md` template: the stages stranger→revenue, each with its corpus rationale (cited), the spec, and the one number it's judged on; the offer ladder; the guarantee; the front-end (magnet/opt-in/emails/community); qualification; traffic; the numbers/cash reality; and what NOT to do. Then draft the actual assets (offer copy, magnet, email sequence, application, onboarding) — copy pass uses the Phase-2 copy creators.

### Phase 6 — Re-test for second-order bottlenecks
Run the BUILT funnel back through the council adversarially: did any decision create a new bottleneck? Is anything undeliverable, unaffordable, or internally inconsistent? Loop until a clean pass. (This is where "looks good on paper" funnels get caught.)

## Critical guardrails (non-negotiable)

1. **Cite-or-cut.** Every principle rests on a real, substring-verified transcript quote + filename. Never fabricate a creator's view or a quote. If a creator isn't in the corpus, say so — don't invent them.
2. **Decision-useful or drop.** A finding must change an asset, a price, a guarantee, a sequence, or a number. "Interesting" is not a finding.
3. **Ship-not-build.** Favor changes that are copy edits / one clear decision over new systems. Flag when a "fix" is really pre-launch over-building that competes with shipping.
4. **Compliance.** Outcome promises only, never income claims, unless the user's market explicitly allows it. Honest scarcity only (real caps), never fake countdowns.
5. **Constraints are the test.** A funnel is only bulletproof relative to the builder's real team/cash/market. Always test against them — a tactic that works for a funded team can sink a solo founder.
6. **The council cooperates.** Synthesize, don't adjudicate a winner. Conflicts resolve to the best combined answer for the user's context.

## Notes
- **Scaling:** for a quick funnel, run D1+D2+D3 with the primary creator each; for a full bulletproof build, run all five dimensions, all members, + the re-test loop.
- **Reusable across clients:** swap the ICP/offer/constraints in Phase 0; the council + corpus stay the same.
- **Exemplars** (a full run of this process): the audit `_AUDIT_2026-06-16_funnel-vs-corpus.md` and the blueprint `_BLUEPRINT_2026-06-16_corpus-funnel.md` in `All of the Buisness/Brains/`.
- If the corpus paths in `corpus-map.md` are absent (different machine), the skill still runs on the distilled `creator-council.md` playbooks — but flag that quotes are from the distilled base, not freshly mined.
