#!/usr/bin/env python3
"""PreToolUse hook: a codex "double-check" before every code edit.

Claude Code runs this before Edit/Write/MultiEdit. It pipes the *proposed*
change to `codex exec` and asks for a verdict:

  - VERDICT: APPROVE  -> allow the edit
  - VERDICT: BLOCK    -> deny the edit, feed codex's concerns back to Claude

Design notes:
  - The change isn't on disk yet at PreToolUse time (and the project may not be
    a git repo), so we use `codex exec` (text in) rather than `codex review`.
  - FAIL OPEN: if codex errors, times out, is logged out, or returns no verdict,
    the edit is ALLOWED with a warning. A broken/logged-out codex must never
    brick editing.
  - Only "code" files are reviewed (see CODE_EXTENSIONS); docs/config are skipped.
  - Approved (file, content) hashes are cached so identical content isn't
    re-reviewed and we don't loop.
"""

import datetime
import hashlib
import json
import os
import subprocess
import sys

# --- config -----------------------------------------------------------------

# Only these extensions get the codex double-check. Everything else is allowed
# immediately (no codex call). Tune to taste.
CODE_EXTENSIONS = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".py", ".rb", ".go", ".rs", ".java", ".kt", ".swift",
    ".c", ".h", ".cpp", ".cc", ".hpp", ".cs",
    ".php", ".sh", ".bash", ".zsh",
    ".sql", ".vue", ".svelte", ".astro",
}

CODEX_TIMEOUT_SECS = 110  # stay under the hook's 120s budget
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
CACHE_FILE = os.path.join(PROJECT_DIR, ".claude", ".codex-cache")
LOG_FILE = os.path.join(PROJECT_DIR, ".claude", "codex-precheck.log")
MAX_CHANGE_CHARS = 24000  # cap prompt size for very large writes

# Context about the change under review, set in main() so emit()/log() can
# reference it without threading it through every call site.
_CTX = {"tool": "-", "file": "-"}


# --- logging -----------------------------------------------------------------

def log(outcome, detail=""):
    """Append one line to the audit log. Best-effort; never raises."""
    try:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{ts}\t{outcome}\t{_CTX['tool']}\t{_CTX['file']}"
        if detail:
            # keep it to a single line
            line += "\t" + " ".join(detail.split())[:300]
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass  # logging is best-effort, must never break the hook


# --- output helpers ---------------------------------------------------------

def emit(decision, reason=None, system_message=None):
    """Print the PreToolUse hook JSON and exit 0."""
    hook_out = {"hookEventName": "PreToolUse", "permissionDecision": decision}
    if reason:
        hook_out["permissionDecisionReason"] = reason
    out = {"hookSpecificOutput": hook_out}
    if system_message:
        out["systemMessage"] = system_message
    print(json.dumps(out))
    sys.exit(0)


def allow(system_message=None, outcome="ALLOW", detail=""):
    log(outcome, detail or (system_message or ""))
    emit("allow", system_message=system_message)


def deny(reason):
    log("BLOCK", reason)
    emit("deny", reason=reason)


# --- cache -------------------------------------------------------------------

def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except OSError:
        return set()


def remember(digest):
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "a", encoding="utf-8") as f:
            f.write(digest + "\n")
    except OSError:
        pass  # cache is best-effort


# --- change reconstruction ---------------------------------------------------

def build_change_text(tool_name, tool_input):
    """Return (file_path, human-readable description of the proposed change)."""
    file_path = tool_input.get("file_path", "<unknown>")

    if tool_name == "Write":
        body = tool_input.get("content", "")
        return file_path, f"Full new contents of {file_path}:\n\n{body}"

    if tool_name == "Edit":
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")
        return file_path, (
            f"Proposed edit to {file_path}.\n\n"
            f"--- REPLACE THIS ---\n{old}\n\n--- WITH THIS ---\n{new}"
        )

    if tool_name == "MultiEdit":
        parts = [f"Proposed multi-edit to {file_path}."]
        for i, e in enumerate(tool_input.get("edits", []), 1):
            parts.append(
                f"\n[edit {i}]\n--- REPLACE ---\n{e.get('old_string', '')}\n"
                f"--- WITH ---\n{e.get('new_string', '')}"
            )
        return file_path, "\n".join(parts)

    # Unknown tool shape -> nothing useful to review.
    return file_path, ""


# --- main --------------------------------------------------------------------

def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        allow(system_message="⚠️ codex pre-check skipped: could not parse hook input.")

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}
    _CTX["tool"] = tool_name or "-"

    if tool_name not in ("Write", "Edit", "MultiEdit"):
        emit("allow")  # not an edit we gate; allow without logging noise

    file_path, change_text = build_change_text(tool_name, tool_input)
    _CTX["file"] = file_path

    # Only review code files.
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in CODE_EXTENSIONS:
        allow(outcome="SKIP", detail=f"non-code file ({ext or 'no ext'})")

    if not change_text.strip():
        allow(system_message="⚠️ codex pre-check skipped: empty/unreadable change.",
              outcome="SKIP")

    if len(change_text) > MAX_CHANGE_CHARS:
        change_text = change_text[:MAX_CHANGE_CHARS] + "\n...[truncated for review]..."

    # Dedupe: skip if this exact change was already approved.
    digest = hashlib.sha256((file_path + "\0" + change_text).encode("utf-8")).hexdigest()
    if digest in load_cache():
        allow(outcome="CACHE_HIT", detail="identical change previously approved")

    prompt = (
        "You are doing a PRE-WRITE double-check of a proposed code change before it is "
        "written to disk. Review ONLY for clear correctness bugs, security issues, or "
        "obvious breakage. Ignore style, formatting, and minor nits. Be decisive and "
        "lean toward APPROVE unless there is a real problem.\n\n"
        "First, briefly explain any concerns (one or two sentences each). Then end your "
        "reply with a single final line that is EXACTLY one of:\n"
        "VERDICT: APPROVE\n"
        "VERDICT: BLOCK\n\n"
        f"=== PROPOSED CHANGE ===\n{change_text}\n=== END ===\n"
    )

    cmd = [
        "codex", "exec",
        "--skip-git-repo-check",
        "-s", "read-only",
        "-C", PROJECT_DIR,
        "-",
    ]
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=CODEX_TIMEOUT_SECS,
        )
    except FileNotFoundError:
        allow(system_message="⚠️ codex pre-check skipped: `codex` not found on PATH.",
              outcome="SKIP")
    except subprocess.TimeoutExpired:
        allow(system_message=f"⚠️ codex pre-check skipped: timed out after {CODEX_TIMEOUT_SECS}s.",
              outcome="SKIP")

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

    # Auth / hard failures -> fail open.
    # IMPORTANT: only scan stderr, and only when codex actually failed
    # (non-zero exit). codex echoes the reviewed diff in stdout, so a file that
    # legitimately contains strings like "please log out and sign in" (e.g. this
    # very hook) would otherwise trigger a false "logged out" skip.
    err = stderr.lower()
    if proc.returncode != 0 and (
        "401 unauthorized" in err or "refresh_token" in err
        or "please log out and sign in" in err
    ):
        allow(system_message="⚠️ codex pre-check skipped: codex is logged out (run `codex login`).",
              outcome="SKIP")

    # Find the verdict on its own line, scanning from the end.
    verdict = None
    concern_lines = []
    for line in stdout.splitlines():
        s = line.strip()
        up = s.upper()
        if up == "VERDICT: APPROVE":
            verdict = "APPROVE"
        elif up == "VERDICT: BLOCK":
            verdict = "BLOCK"
        elif s and not s.startswith("VERDICT:"):
            concern_lines.append(s)

    if verdict == "APPROVE":
        remember(digest)
        allow(outcome="APPROVE", detail="codex approved")
    elif verdict == "BLOCK":
        concerns = "\n".join(concern_lines[-40:]).strip() or "(no detail provided)"
        deny(
            "codex (double-check) flagged this change and BLOCKED it. Address these "
            f"concerns, then retry:\n\n{concerns}"
        )
    else:
        # No parseable verdict -> fail open rather than wedge editing.
        if proc.returncode != 0:
            tail = (stderr.strip() or stdout.strip())[-300:]
            allow(system_message=f"⚠️ codex pre-check skipped: codex exited {proc.returncode}: {tail}",
                  outcome="SKIP")
        allow(system_message="⚠️ codex pre-check skipped: no VERDICT line in codex output.",
              outcome="SKIP")


if __name__ == "__main__":
    main()
