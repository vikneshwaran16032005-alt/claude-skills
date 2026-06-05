---
name: setup-codex-precheck
description: Install the codex pre-edit "double-check" hook into the current project — a PreToolUse hook that asks the codex CLI to review every Edit/Write/MultiEdit before it is written, blocking risky changes. Checks prerequisites (codex, python3, codex login) and installs anything missing, idempotently. Use when the user wants to "set up the codex check", "install the codex double-check / pre-check / review hook", "make Claude check with codex before editing", or "add the codex gate to this project".
argument-hint: [optional: target project dir, defaults to current]
auto-activate: false
---

# Setup codex pre-check

You install (and verify) a codex "double-check" gate into the **current project only**: a
`PreToolUse` hook that pipes every proposed `Edit`/`Write`/`MultiEdit` to the `codex` CLI for
an independent review before it is written. codex returns `VERDICT: APPROVE` (edit proceeds)
or `VERDICT: BLOCK` (edit denied, concerns fed back to Claude). It **fails open** — if codex
is missing/logged-out/erroring, edits are allowed with a warning, never blocked.

This skill bundles the canonical hook and an idempotent installer. Do **not** hand-write the
hook — always install the bundled copy so it stays consistent.

## What it installs (into the current project)
- `.claude/hooks/codex-precheck.py` — the hook (copied from this skill's directory).
- `.claude/settings.json` — a `PreToolUse` entry (`matcher: "Edit|Write|MultiEdit"`), merged
  in without clobbering existing settings/hooks.
- `CLAUDE.md` — a short policy section (appended only if not already present).

At runtime (not install time) the hook also creates, inside the project's `.claude/`:
- `codex-precheck.log` — an append-only audit trail; one tab-separated line per gated edit:
  `<timestamp>  <OUTCOME>  <tool>  <file>  <detail>`, where OUTCOME is `APPROVE`, `BLOCK`,
  `CACHE_HIT`, or `SKIP` (any fail-open reason). Tell users they can `tail -f` it to watch
  the gate, or to confirm whether a given edit was actually reviewed.
- `.codex-cache` — sha256 digests of already-approved changes, so an identical re-write is a
  `CACHE_HIT` and isn't re-sent to codex (avoids redundant reviews and loops).

The bundled hook scans **only stderr on a non-zero exit** to detect a logged-out codex, so a
file that legitimately contains auth strings (e.g. the hook itself) no longer trips a false
"logged out" skip.

## Process

1. **Run the installer** from this skill's directory, targeting the current project. Pass
   `$ARGUMENTS` as the target dir if the user supplied one, otherwise default to `$PWD`:
   ```bash
   bash "$HOME/.claude/skills/setup-codex-precheck/install.sh" ${ARGUMENTS:-"$PWD"}
   ```
   The installer prints a status report: prerequisites (`python3`, `codex`, codex login),
   what was already present (`✓`), what it added (`+`), warnings (`!`), and a self-test.

2. **Read the report back to the user** in plain language: which prerequisites are satisfied,
   what was installed vs already present, and the self-test result.

3. **If codex is logged out or not installed**, tell the user clearly that the gate is active
   but currently **fails open** (no real review happens) until they run `codex login` (or
   install codex). Suggest they run `! codex login` in the session. Do not attempt the
   interactive login yourself.

4. **If codex is installed and logged in**, optionally confirm the live path with a quick
   smoke test, then show the user how to verify the block path:
   ```bash
   printf 'Reply exactly: VERDICT: APPROVE' | codex exec --skip-git-repo-check -s read-only -
   ```

5. **Remind the user to restart Claude Code or run `/hooks`** so the new hook is loaded — a
   freshly written `settings.json` is not picked up mid-session automatically.

## Critical Rules

1. **Current project only.** Install into the target dir (default `$PWD`); never touch
   `~/.claude/settings.json`. This is a per-project gate by design.
2. **Idempotent.** The installer is safe to re-run; it detects an existing install and skips.
   If the user re-invokes the skill, just run it again and report "already present".
3. **Never clobber** existing `settings.json` or `CLAUDE.md` — the installer merges/appends.
   Don't bypass it with a raw overwrite.
4. **Fail-open is intentional.** Don't "fix" the hook to hard-block when codex is unavailable —
   that would brick editing. A logged-out codex must allow edits with a warning.
5. **Don't fake the prereq check.** Report exactly what `install.sh` found. If `python3` is
   missing, the hook can't run — say so.
6. **Flag the trade-off** if asked: this reviews on *every* code edit, so each edit waits for a
   codex call (up to the 120s hook timeout). Mention an end-of-task `Stop` hook as the lighter
   alternative if the user finds per-edit latency annoying.

## Final Note

`$ARGUMENTS` is an optional target project directory; default to the current directory when
empty. The skill's job is: run the bundled installer, faithfully report its findings, and tell
the user the one manual step (`codex login`) if it's needed.
