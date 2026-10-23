# Claude Code Skills — backup

Off-machine backup of Vik's Claude Code skills. Updated 2026-10-23.

- **Top level: 30 active skills** (mirror of `~/.claude/skills/`; these load every session).
- **`skill-library/`: 381 on-demand skills** (mirror of `~/.claude/skill-library/`; read only when a task needs one, indexed in `skill-library/INDEX.md`).

## Restore on a new machine
```bash
git clone https://github.com/vikneshwaran16032005-alt/claude-skills.git ~/.claude/skills-restored
rsync -a --exclude skill-library --exclude README.md --exclude .gitignore ~/.claude/skills-restored/ ~/.claude/skills/
rsync -a ~/.claude/skills-restored/skill-library/ ~/.claude/skill-library/
```
Then restart Claude Code so the `/` picker re-indexes them.

## Not included
- Anthropic's docx, pdf, pptx and xlsx skills and NT Site Mirror: their licenses forbid redistribution. Reinstall from the source.
- claude.ai account-synced skills (`synced/`): they come back on sign-in.
- Python venvs, node_modules, `.env` files (only `.example` templates), backups. Symlinks are stored as real files.
