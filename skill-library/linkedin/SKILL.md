---
name: linkedin
version: 1.0.0
description: >
  Scrape LinkedIn profiles, companies, jobs, and company posts using the
  joeyism/linkedin-scraper library (Playwright). Use when the user asks to pull a
  LinkedIn profile, company page, job listings, or company posts into structured data
  for their own or explicitly authorized use (research, meeting prep, recruiting with
  consent). Requires a one-time manual login. Not for mass-harvesting or third-party
  personal-data collection.
allowed-tools: Bash, Read, Write
---

# LinkedIn (scraper)

Wraps [`joeyism/linkedin-scraper`](https://github.com/joeyism/linkedin_scraper) (v2, Playwright).

## ⚠️ Use responsibly — read before running
- **LinkedIn's User Agreement prohibits automated scraping.** Running this risks **rate-limiting, restriction, or a permanent ban** of the logged-in account. The user accepts that risk.
- **Only for the user's own data or explicitly authorized targets** (e.g. their own profile/connections, recruiting research with consent). Do **not** mass-harvest or compile strangers' personal data.
- **Go slow.** Scrape a few items at a time with pauses. Never loop hundreds of profiles.
- If the user's intent looks like bulk lead-harvesting, suggest their compliant tools instead (Apollo, ZoomInfo, Nimble, Common Room).

## Paths
- venv python: `~/.claude/skill-library/linkedin/.venv/bin/python`
- scripts: `~/.claude/skill-library/linkedin/scripts/`
- session (auth): `~/.config/linkedin-scraper/session.json` (user-only)

## Step 1 — one-time login (USER runs this; do not automate the password)
A browser window opens; the **user** logs into LinkedIn manually, then the session is saved.
```bash
~/.claude/skill-library/linkedin/.venv/bin/python ~/.claude/skill-library/linkedin/scripts/login.py
```
Tell the user to run it themselves if a session does not already exist. Never ask for or type their LinkedIn password.

## Step 2 — scrape (Claude may run these once a session exists)
```bash
PY=~/.claude/skill-library/linkedin/.venv/bin/python
S=~/.claude/skill-library/linkedin/scripts/scrape.py
$PY $S --type person  --url "https://www.linkedin.com/in/<handle>/"
$PY $S --type company --url "https://www.linkedin.com/company/<slug>/"
$PY $S --type posts   --url "https://www.linkedin.com/company/<slug>/" --limit 10
$PY $S --type jobs    --keywords "Python Developer" --location "Chicago" --limit 10
```
Each prints structured JSON to stdout. If it reports "No session", the user must do Step 1 first. Parse the JSON and summarize for the user; do not dump raw personal data unnecessarily.

## Notes
- First run downloads Playwright Chromium (one-time).
- If LinkedIn shows a checkpoint/2FA, the user resolves it in the Step 1 browser window.
- Session expires periodically; re-run Step 1 when scrapes start failing auth.
