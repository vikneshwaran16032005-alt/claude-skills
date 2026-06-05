#!/usr/bin/env python3
"""
vault_sync.py — feed the copywriting-master skill from the Second Brain vault.

Scope = "Full Copywriting + Sales topics": every transcript under
`03 - Transcripts/` whose frontmatter `tags:` contains `copywriting` OR `sales`.

This helper is the DETERMINISTIC half of the daily sync. It does NOT call an LLM.
It just computes the delta (in-scope transcripts not yet folded into the skill)
and tracks state. The LLM half (the scheduled task prompt) reads the items this
returns, distills the copy gold, appends to references/vault-insights.md, and
calls `mark` here to record them done.

Subcommands:
  next  --limit N   -> JSON list of up to N unprocessed in-scope items,
                       highest-views first, summary-bearing tie-broken first.
  mark  ID [ID...]  -> record video_ids as processed (after a successful fold).
  stats             -> scope total / processed / remaining (human-readable).

Design notes:
  - Incremental + idempotent: a video is processed exactly once (state.json).
  - Front-loaded by signal: views_raw DESC means the most influential copy/sales
    content lands in the skill first; value does not wait for the long tail.
  - Cheap-input preference: items with a reader summary are surfaced with their
    summary path so the LLM half can read the small distilled file, not the
    50KB raw transcript, when one exists.
  - Read-only against the vault. Only writes inside the skill's own sync/ dir.
"""

import json
import os
import sys
from datetime import datetime, timezone

VAULT = "/Users/vik/Second Brain"
TRANSCRIPTS = os.path.join(VAULT, "03 - Transcripts")
SUMMARIES = os.path.join(VAULT, "scrape_output", "_summaries")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNC_DIR = os.path.join(SKILL_DIR, "sync")
STATE_PATH = os.path.join(SYNC_DIR, "state.json")

SCOPE_TAGS = {"copywriting", "sales"}


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"processed": [], "last_run": None, "runs": 0}


def save_state(state):
    os.makedirs(SYNC_DIR, exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_PATH)


def parse_frontmatter(path):
    """Return dict with video_id, title, creator, niche, views, tags.
    Reads only the frontmatter block (first `---`...`---`). None if no/invalid FM."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            first = f.readline()
            if first.strip() != "---":
                return None
            lines = []
            for _ in range(80):  # frontmatter is short; cap the read
                line = f.readline()
                if line == "":
                    return None
                if line.strip() == "---":
                    break
                lines.append(line.rstrip("\n"))
            else:
                return None
    except OSError:
        return None

    data = {"video_id": None, "title": None, "creator": None,
            "niche": None, "views": 0, "tags": []}
    in_tags = False
    for line in lines:
        if line.startswith("  - ") and in_tags:
            data["tags"].append(line[4:].strip())
            continue
        # a non-list, non-indented line ends any list block
        if not line.startswith(" "):
            in_tags = False
        if line.startswith("tags:"):
            in_tags = True
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip()
        if key == "video_id":
            data["video_id"] = val
        elif key == "title":
            data["title"] = val
        elif key == "creator":
            data["creator"] = val.strip("[]")
        elif key == "niche":
            data["niche"] = val.strip("[]")
        elif key == "views_raw":
            try:
                data["views"] = int(val)
            except ValueError:
                data["views"] = 0
    return data


def scan_scope():
    """Yield frontmatter dicts for every in-scope (copywriting|sales) transcript."""
    for root, _dirs, files in os.walk(TRANSCRIPTS):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            fm = parse_frontmatter(path)
            if not fm or not fm["video_id"]:
                continue
            if SCOPE_TAGS.intersection(fm["tags"]):
                fm["path"] = path
                yield fm


def summary_path_for(video_id):
    p = os.path.join(SUMMARIES, f"{video_id}.md")
    return p if os.path.exists(p) else None


def cmd_next(limit):
    state = load_state()
    processed = set(state["processed"])
    items = []
    seen_ids = set()
    for fm in scan_scope():
        vid = fm["video_id"]
        if vid in processed or vid in seen_ids:
            continue
        seen_ids.add(vid)
        sp = summary_path_for(vid)
        items.append({
            "video_id": vid,
            "title": fm["title"],
            "creator": fm["creator"],
            "niche": fm["niche"],
            "views": fm["views"],
            "transcript_path": fm["path"],
            "summary_path": sp,
            "has_summary": sp is not None,
        })
    # Highest signal first; summary-bearing tie-broken ahead (cheaper to read).
    items.sort(key=lambda x: (x["views"], x["has_summary"]), reverse=True)
    print(json.dumps(items[:limit], indent=2))


def cmd_mark(ids):
    state = load_state()
    processed = set(state["processed"])
    added = 0
    for vid in ids:
        if vid and vid not in processed:
            processed.add(vid)
            added += 1
    state["processed"] = sorted(processed)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["runs"] = state.get("runs", 0) + (1 if added else 0)
    save_state(state)
    print(f"marked {added} new (total processed: {len(processed)})")


def cmd_stats():
    state = load_state()
    processed = set(state["processed"])
    total = 0
    remaining = 0
    in_scope_ids = set()
    for fm in scan_scope():
        vid = fm["video_id"]
        if vid in in_scope_ids:
            continue
        in_scope_ids.add(vid)
        total += 1
        if vid not in processed:
            remaining += 1
    print(f"in-scope (unique): {total}")
    print(f"processed:         {len(processed)}")
    print(f"remaining:         {remaining}")
    print(f"last_run:          {state.get('last_run')}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd = args[0]
    if cmd == "next":
        limit = 15
        if "--limit" in args:
            try:
                limit = int(args[args.index("--limit") + 1])
            except (ValueError, IndexError):
                pass
        cmd_next(limit)
    elif cmd == "mark":
        cmd_mark(args[1:])
    elif cmd == "stats":
        cmd_stats()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
