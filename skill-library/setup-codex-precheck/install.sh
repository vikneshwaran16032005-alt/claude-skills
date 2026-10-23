#!/usr/bin/env bash
# Install the codex pre-edit "double-check" hook into the CURRENT project.
# Idempotent: safe to re-run. Checks prerequisites, installs what's missing,
# never clobbers existing settings/hooks. Prints a status report.
#
# Usage: install.sh [TARGET_PROJECT_DIR]   (defaults to $PWD)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD}"
HOOK_SRC="$SCRIPT_DIR/codex-precheck.py"
HOOK_DST="$TARGET/.claude/hooks/codex-precheck.py"
SETTINGS="$TARGET/.claude/settings.json"
CLAUDE_MD="$TARGET/CLAUDE.md"

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
add()  { printf '  \033[33m+\033[0m %s\n' "$1"; }
warn() { printf '  \033[31m!\033[0m %s\n' "$1"; }

echo "Installing codex pre-check into: $TARGET"
echo

# --- 1. prerequisites -------------------------------------------------------
echo "Prerequisites:"
PY="$(command -v python3 || true)"
if [ -n "$PY" ]; then ok "python3 ($PY)"; else
  warn "python3 NOT found — the hook cannot run without it. Install Python 3 first."
fi

CODEX="$(command -v codex || true)"
if [ -n "$CODEX" ]; then ok "codex ($CODEX)"; else
  warn "codex NOT found on PATH. Install it (e.g. 'npm i -g @openai/codex'). The hook will FAIL OPEN until then."
fi

CODEX_LOGIN="unknown"
if [ -n "$CODEX" ]; then
  if [ -f "$HOME/.codex/auth.json" ]; then
    ok "codex auth.json present (run a smoke test to confirm it's not expired)"
    CODEX_LOGIN="present"
  else
    warn "codex appears logged OUT (no ~/.codex/auth.json). Run 'codex login'. Hook FAILS OPEN until then."
    CODEX_LOGIN="missing"
  fi
fi
echo

# --- 2. install hook script -------------------------------------------------
echo "Hook script:"
mkdir -p "$TARGET/.claude/hooks"
if [ ! -f "$HOOK_SRC" ]; then
  warn "canonical hook not found at $HOOK_SRC — aborting."; exit 1
fi
if [ -f "$HOOK_DST" ] && cmp -s "$HOOK_SRC" "$HOOK_DST"; then
  ok ".claude/hooks/codex-precheck.py already up to date"
else
  cp "$HOOK_SRC" "$HOOK_DST"
  add ".claude/hooks/codex-precheck.py installed"
fi
chmod +x "$HOOK_DST"
echo

# --- 3. merge settings.json (never clobber) ---------------------------------
echo "settings.json hook registration:"
if [ -z "$PY" ]; then
  warn "skipping settings.json merge (needs python3)"
else
  "$PY" - "$SETTINGS" <<'PYEOF'
import json, os, sys
path = sys.argv[1]
try:
    with open(path) as f: data = json.load(f)
    if not isinstance(data, dict): data = {}
except (OSError, ValueError):
    data = {}

hooks = data.setdefault("hooks", {})
pre = hooks.setdefault("PreToolUse", [])

CMD = 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/codex-precheck.py"'

def already():
    for entry in pre:
        for h in (entry or {}).get("hooks", []):
            if "codex-precheck.py" in (h or {}).get("command", ""):
                return True
    return False

if already():
    print("STATUS=present")
else:
    pre.append({
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{"type": "command", "command": CMD, "timeout": 120}],
    })
    data.setdefault("$schema", "https://json.schemastore.org/claude-code-settings.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2); f.write("\n")
    print("STATUS=added")
PYEOF
  case "$(grep -c codex-precheck.py "$SETTINGS" 2>/dev/null || echo 0)" in
    0) warn "could not confirm registration in $SETTINGS" ;;
    *) ok "PreToolUse hook registered in .claude/settings.json (matcher: Edit|Write|MultiEdit)" ;;
  esac
fi
echo

# --- 4. CLAUDE.md policy note (optional, idempotent) ------------------------
echo "CLAUDE.md policy note:"
MARKER="codex double-check"
if [ -f "$CLAUDE_MD" ] && grep -qi "$MARKER" "$CLAUDE_MD"; then
  ok "CLAUDE.md already documents the policy"
else
  cat >> "$CLAUDE_MD" <<'MDEOF'

## Code-change policy — codex double-check

Before updating code, every `Edit`/`Write`/`MultiEdit` is automatically reviewed by `codex`
as an independent second opinion, via the `PreToolUse` hook in
`.claude/hooks/codex-precheck.py`. If codex returns `VERDICT: BLOCK`, the edit is denied and
its concerns are returned to you — address them, then retry. If codex is unavailable (logged
out / timed out / erroring) the gate FAILS OPEN and prints a `⚠️ codex pre-check skipped`
warning — treat that as "no second opinion was obtained" and re-run `codex login` if needed.
Only code files are reviewed; docs/config are skipped.

Every gated edit is recorded in `.claude/codex-precheck.log` (one line per edit:
`<timestamp>  <OUTCOME>  <tool>  <file>  <detail>`, OUTCOME ∈ APPROVE/BLOCK/CACHE_HIT/SKIP).
`tail -f .claude/codex-precheck.log` to watch the gate or confirm an edit was actually reviewed.
MDEOF
  add "appended policy section to CLAUDE.md"
fi
echo

# --- 5. self-test (fail-open path always works) -----------------------------
echo "Self-test:"
if [ -n "$PY" ]; then
  OUT=$(echo '{"tool_name":"Write","tool_input":{"file_path":"selftest.js","content":"export const a=1"}}' \
        | CLAUDE_PROJECT_DIR="$TARGET" "$PY" "$HOOK_DST" 2>/dev/null)
  if echo "$OUT" | grep -q '"permissionDecision"'; then
    ok "hook returned valid JSON: $OUT"
  else
    warn "hook did not return expected JSON. Output: $OUT"
  fi
else
  warn "skipped (needs python3)"
fi
echo

echo "Done. Restart Claude Code (or run /hooks) so the new hook is picked up."
if [ "$CODEX_LOGIN" = "missing" ] || [ -z "$CODEX" ]; then
  echo "NEXT STEP: run 'codex login' — until then the gate allows all edits (fail-open)."
fi
