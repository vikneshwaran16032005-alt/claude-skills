# Claude Code Skills — backup

Off-machine backup of all locally-registered Claude Code skills from `~/.claude/skills/`.
Captured 2026-06-05. **39 skills.**

## Restore on a new machine
```bash
git clone https://github.com/vikneshwaran16032005-alt/claude-skills.git ~/.claude/skills-restored
cp -r ~/.claude/skills-restored/*/ ~/.claude/skills/
# (omit README.md / .gitignore — they aren't skills)
```
Then restart Claude Code so the `/` picker re-indexes them.

## Notes
- Private repo (contains proprietary + personal skills).
- `token-optimizer` is included as real files (symlink dereferenced); its Python venv is excluded — recreate with its installer if needed.
- No live credentials are stored (`.env` files are `.example` templates only).
