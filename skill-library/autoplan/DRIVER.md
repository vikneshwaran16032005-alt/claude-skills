<!-- AUTO-GENERATED from autoplan/DRIVER.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->
# /autoplan driver: run the review loop from a parent agent

Read this file instead of `autoplan/SKILL.md` when you (a parent agent on any host) drive an
unattended /autoplan run through `gstack-autoplan`: the reviewers are subagents you dispatch,
and the runner keeps the state. The commands live in `<root>/bin/`, where `<root>` is the
folder that holds this `autoplan/` directory; `gstack-autoplan --help` and the first `next`
print `DRIVER: <root>/autoplan/DRIVER.md`. Run every command with the `GSTACK_LAUNCH`
assignments your installer printed. Read printed lines and files, never prose: every workflow
command ends with `GSTACK_RESULT: skill=autoplan status=<s> run=<dir>`, and every error line
ends with `(<CODE>)`.

## Phases and scope

Order: ceo → design → dx → eng. Design runs only with UI scope, DX only with DX scope, Eng always and last.
Scope flags on the first `next`: `--ui`, `--no-ui`, `--no-dx`, `--developer-tool`, `--agent-primary`. `--developer-tool` and `--agent-primary` only enable DX.
The first `next` prints `SCOPE: ui=… (terms; visual; files) dx=… (detected) source=ui:<s>,dx:<s>`
(each axis is `flag`, `marker` or `detected`). UI needs a rendered file path or a UI term next
to a visual noun in the Implementation plan. To keep flags for later runs on the same plan, add
the `SCOPE_PIN:` marker it prints (`<!-- gstack-autoplan-scope: … -->`) as the plan's first
line yourself; gstack never writes the plan.

## The loop

1. `next` prints one `ATTEMPT: <id> phase=<p> voice=native|outside prompt=<file> result=<file>`
   per voice. Dispatch the native prompt to a subagent on your model and the outside prompt to
   a subagent on another model family (or `gstack-outside-voice run`). Each writes `result=`.
2. Submit each voice exactly once (`BOUND:`). Both voices in closes the phase (`PHASE_CLOSED:`).
3. Repeat `next` until `status=gate_pending` (`GATE: gate_rev=<n>`); render it with
   `gstack-gate render <dir>/gate.json`. You never approve the gate for the owner: relay it.
4. `answer` with the owner's reply. `APPLY: <id> <title> -> <change>` lines are accepted plan
   changes: edit the plan, then `revise` (the printed `NEXT:` names it). Until then `next`
   refuses with `PLAN_AMEND_PENDING` and `export` will not mark the run complete.
5. `REOPENED: <phases>` means loop `next` again (Eng last). `APPROVED:` means `export`.

### Commands

- `gstack-autoplan next --out <dir> --plan <plan.md> [scope flags] [--light] [--spend-cap <usd>] [--scaffold]`
  first call: init the run, print PHASE:, SCOPE:, DRIVER: and one ATTEMPT: per voice.
- `gstack-autoplan next --out <dir> [--redispatch <attempt>]`
  later calls: open the next phase or reprint open attempts; never redispatches on its own.
- `gstack-autoplan submit --out <dir> --phase <p> --voice native|outside --record <file.md> --model <id> [--attempt <id>]`
  bind a free-form review record (canonical fence, one findings table or list, or `No findings.`).
- `gstack-autoplan submit ... --record <file.md> --attest "<reason>" --attempt <id>`
  bind a record with no INPUT: line as receipt: attested (a wrong INPUT: always refuses).
- `gstack-autoplan submit --out <dir> --phase <p> --voice native|outside --result <file> --model <id> --attempt <id>`
  bind a canonical result (the RESULT FORMAT below).
- `gstack-autoplan submit --out <dir> --phase <p> --voice outside --unavailable|--failed "<reason>"`
  close the phase native-only when no outside voice can run.
- `gstack-autoplan answer --out <dir> --gate-rev <n> --reply "<reply>"`
  answer the gate with the reply grammar below.
- `gstack-autoplan revise --out <dir> --plan <plan v2> --incorporates <decision ids>`
  bind the amended plan; reopens every phase whose reviewed plan changed, Eng last.
- `gstack-autoplan revise --out <dir> --withdraw <decision id>`
  drop a pending amendment instead of applying it.
- `gstack-autoplan export --out <dir>`
  write the artifact set; then `gstack-artifact validate <dir>/run.json`.
- `gstack-autoplan status|resume --out <dir>`
  read the manifest; take ownership after a crash (EXECUTION_UNKNOWN lists unfinished attempts).

## Reviewer result format

Every prompt ends with this contract; `submit --result` enforces it, `submit --record` accepts
the looser record shapes above.

RESULT FORMAT (required by gstack-autoplan; the parent binds your file by this contract):
1. The first line of your result is exactly: INPUT: <phase> <snapshot sha256>
2. Write the complete review as prose, then END with one fenced block of canonical findings, one JSON object per line:
```gstack-findings
{"id":"F1","severity":"High","title":"<one line>","file":"<path or omit>","line":12,"fix":"<the fix>"}
```
   severity is Critical | High | Medium | Low | Informational. Add "user_challenge": true only when you recommend changing the plan's stated direction AND the change alters its scope, cost or direction; then also add "changes": "scope" | "cost" | "direction". Packaging, ordering, naming and other reversible choices are ordinary findings, not user challenges. Add "urgent": true and "suggested_owner": "<who>" for a security or data-loss finding this plan does not own. An empty fence means no findings; a missing fence is refused.
3. Write the whole result to this file: <result file>

## Gate replies

A reply binds to the `gate_rev` you read (`--gate-rev`). Bare `yes`/`no` is unparsed, never guessed.

- `all`: every item takes its recommendation (an agreed change prints APPLY: and needs revise).
- `all as-is`: keep every direction; no plan change.
- `d3b uc1a`: one <id><option> token per item you set; unanswered auto items take their default.
- `all except d3b`: recommendations, with the listed overrides.

## Run directory

Runner state: `run.json`, `attempts.jsonl`, `run.lock`, `spend.json`, `plan-active.md`, `restore.md`, `plan-source.md`. Reviewer files: `<phase>-native-prompt.md`,
`<phase>-outside-prompt.md`, `<phase>-native.md`, `<phase>-outside.md`, `<phase>-consensus.{json,md}`,
`gate.json`, `decisions.jsonl`. `export` writes `plan.md`, `review-record.md`, `findings.jsonl`,
`tasks.jsonl`, `timing.json` and rehashes `run.json`; `gstack-artifact validate <dir>/run.json`
is the completion check. Copy the whole directory, never single files.

## Result codes

- `RUN_NOT_INITIALIZED`: start with `gstack-autoplan next --plan <file> --out <dir>` (the first call initializes the run)
- `PLAN_SECTIONS_INVALID`: add the missing heading, or rerun the first `gstack-autoplan next` with --scaffold to review a scaffolded copy (your plan file is never edited); duplicate, reversed or empty sections are fixed by hand
- `RUN_LOCKED`: wait for it to exit, or if its pid is gone run `gstack-autoplan resume --out <dir>` to take ownership
- `EXECUTION_UNKNOWN`: submit the result file if the reviewer finished (`gstack-autoplan submit ... --attempt <id>`), or redispatch explicitly with `gstack-autoplan next --redispatch <id>`; nothing is redispatched automatically
- `SPEND_CAP_EXCEEDED`: raise `--spend-cap`, settle or release unsettled attempts, or stop; unknown charges count as their reservation
- `PHASE_NOT_AWAITING`: run `gstack-autoplan status --out <dir>` and submit for the attempt `next` printed
- `ATTEMPT_MISMATCH`: pass the attempt id `next` printed for this voice; a result is bound exactly once
- `RESULT_RECEIPT_MISSING`: the reviewer must read the prompt file through EOF and begin its result with the INPUT line the prompt names; a result for another snapshot is refused
- `RESULT_FINDINGS_MISSING`: end the review with one ```gstack-findings fence, one JSON object per line with at least severity and title; `[]` rows are not findings, an empty fence means no findings
- `MODEL_FAMILY_CONFLICT`: pass `--model <id>` of a different family (anthropic, openai, google, xai, deepseek, qwen, zai, moonshot, meta, mistral); a same-family result is not an outside voice
- `CONSENSUS_MISSING`: resume the run so the phase closes through reconciliation; the Eng prompt is never sent without every prior phase summary
- `GATE_REV_STALE`: render the current gate list, read it, and reply with its gate_rev
- `GATE_REPLY_UNPARSED`: reply with `all`, `all as-is`, `<id><option>` tokens (for example `d3b uc1a`), or `all except <tokens>`; bare yes/no is ambiguous
- `PLAN_AMEND_PENDING`: edit the plan, then `gstack-autoplan revise --out <dir> --plan <file> --incorporates <decision id,...>`; or drop one with `gstack-autoplan revise --out <dir> --withdraw <decision id>`
- `GSTACK_VERSION_CHANGED`: nothing to do for an older run (journaled forward migrations ran); a run written by a newer gstack needs that gstack: upgrade with bin/gstack-upgrade

## Coordinator contract (inherited by every lane)

Merge conditions. A lane's PR merges only when: the required gate lanes are green on the stamped tree or the tree receipt says `gate-reuse: eligible`; `gstack-lane-check` reports `clear` for its planned files against every other open lane; the PR body opens with the `gstack-ship-receipt` block; and the coordinator, not the lane, says merge. A lane never merges, rebases another lane, or force-pushes.

Behavior-change notices. Every user-visible behavior change outside the plan's own items is listed in the PR body under `## Behavior changes` with the file, the old behavior and the new one, before the review starts. An omitted change found in review is a CRITICAL finding, whatever its size.

Spend caps. Each lane runs under the `--spend-cap` the coordinator names; a lane that reaches it stops with `status=budget_exhausted` and reports spent, reserved and unknown charges. Paid evals are never retried to change a verdict; a rerun needs a named repair. Host-subagent spend is reported as `unknown`, never zero.

Before done. A lane runs `gstack-pregate run --allow-repo-commands` on its branch (the unit tier on the changed files plus the repo's guards) and reports done only after it passes. In a repo whose `.gstack/pregate.json` has a `sealed` key, it runs `gstack-pregate sealed` before any push or PR creation; a refusal stops the push, because a PR tool may not run local hooks.

Handoff format. A lane reports in this order, identifiers first: PR URL (or `no PR` with branch and SHA), `GSTACK_RESULT` line, the `gstack: ok|fail <rev>` line, the `PREGATE:` line, gate summary (lanes passed/failed/skipped), behavior changes (or `none`), spend (spent/reserved/unknown), then what it could not verify. Full thread ids (`jam_…`), never short codes, in every cross-thread message. Prose after the identifiers may be truncated; nothing before them may be.
