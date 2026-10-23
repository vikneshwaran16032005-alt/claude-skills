---
name: new-client-system
description: Scaffold a new client's full stack — Next.js 16 frontend dashboard + Trigger.dev backend worker — from the Shiney automations template. Use when the user says "new client", "onboard a client", "scaffold a client system", "set up <client-name>", or wants to start a fresh frontend+backend project styled and structured like the Shiney automations dashboard. Produces structure only; no automations are scaffolded — those are added later.
argument-hint: [client name or leave blank to be prompted]
auto-activate: false
---

# New Client System

You are scaffolding a **fresh frontend + backend pair** for a new client, modeled on the Shiney automations template. The output is structural only: auth, dashboard shell, design system, integration clients, and an empty automations registry. Automations are intentionally **not** scaffolded here — they're added in a later step once the client's domain is understood.

Read the references in `/Users/albertbakhoj/.claude/skills/new-client-system/references/` for architectural detail:

- `architecture.md` — what's in each project, how frontend and backend communicate, structure-vs-automation split
- `stack.md` — exact dependencies and versions (Next.js 16, React 19, Trigger.dev v4, Composio, Anthropic, NextAuth v5 beta, Tailwind v4, MongoDB)
- `design-system.md` — design tokens, color palette, typography, custom utilities
- `parameters.md` — full list of placeholders the scaffolder substitutes

## Workflow

### Step 1 — Gather context (ALWAYS first)

Before touching the filesystem, use `AskUserQuestion` to collect the client parameters. Ask in **one** call with multiple questions:

1. **Client display name** (e.g. "Acme Co") — used in titles, sidebar, login copy
2. **Client email domain** (e.g. "acme.com") — used to restrict auth (only `*@acme.com` can sign in)
3. **Output directory** — absolute path where the two project folders will be created (default: current working directory)

Then derive (don't ask):

- `CLIENT_SLUG` = lowercase, dashes (e.g. "Acme Co" → "acme")
- `EMAIL_FROM` = `noreply@<domain>` (confirm if user wants different)
- `COMPOSIO_USER_ID` = the user's email (use the value from CLAUDE.md userEmail context, e.g. `albert@shiney.ai`, unless the client should manage their own — ask if unsure)
- `BUSINESS_EMAIL` = `billing@<domain>`
- `MONGODB_DB` = the slug

If any derived value is non-obvious or could go either way, confirm with one follow-up question. Otherwise proceed.

### Step 2 — Run the scaffold script

Call the bash script with all collected values:

```bash
/Users/albertbakhoj/.claude/skills/new-client-system/scripts/scaffold.sh \
  --out "<OUT_DIR>" \
  --client-name "<Display Name>" \
  --client-domain "<domain>" \
  --client-slug "<slug>" \
  --email-from "<email>" \
  --composio-user-id "<email>" \
  --business-email "<email>" \
  --mongodb-db "<dbname>"
```

This:

1. Copies `templates/frontend/` → `<OUT_DIR>/<slug>/`
2. Copies `templates/backend/` → `<OUT_DIR>/<slug>_backend/`
3. Substitutes all `{{PLACEHOLDER}}` tokens via `sed`
4. Warns if any unsubstituted placeholders remain

The script refuses to overwrite existing folders — fail loudly is correct.

### Step 3 — Verify

After scaffolding, run a quick check:

```bash
grep -rE '\{\{[A-Z_]+\}\}' <OUT_DIR>/<slug> <OUT_DIR>/<slug>_backend || echo "All placeholders substituted."
```

Also verify both projects' `package.json` parse cleanly with `node -e "JSON.parse(require('fs').readFileSync('<path>/package.json'))"`.

### Step 4 — Report and next steps

Tell the user, concisely:

- The two folder paths created
- Required env vars they need to fill in (`.env.local` for frontend, `.env` for backend) — point to the `.example` files
- The four bootstrap commands (don't run them — just list):
  ```
  cd <slug>           && npm install
  cd <slug>_backend   && npm install
  cd <slug>_backend   && npm run connect   # Composio OAuth for Gmail + Drive
  cd <slug>           && npm run dev       # http://localhost:3000
  ```
- That **no automations are scaffolded yet**, and the next step (when ready) is to add one under `<slug>_backend/src/automations/<auto-slug>/` with a matching entry in `<slug>/src/config/automations.ts` and route under `<slug>/src/app/(dashboard)/dashboard/automations/<auto-slug>/`. The `_backend/src/automations/README.md` explains the convention.

## Critical Rules

1. **Always gather context with AskUserQuestion first** — never scaffold with guessed values.
2. **Do not invent placeholders** — only the seven defined in `parameters.md` are substituted. Anything else stays as-is.
3. **Do not scaffold automations** — the template has an empty automations registry on purpose. Don't add `invoice` or any other example task; the user adds those separately.
4. **Do not modify the templates** during scaffolding — substitution is the only change. If the user wants the template itself updated, that's a separate task.
5. **Do not run `npm install` automatically** — list it as a next step. Installs are slow and may fail on the user's machine; let them control it.
6. **Refuse to overwrite** existing destination folders. The script already does this; don't override.
7. **Both projects share the same Trigger.dev project** — `TRIGGER_PROJECT_REF` and `TRIGGER_SECRET_KEY` must match between frontend `.env.local` and backend `.env`. Mention this in the next-steps report.
8. **Stack is non-standard** — Next.js 16 with breaking changes (see frontend `AGENTS.md`), NextAuth v5 beta, Tailwind v4. Don't "fix" things that look unfamiliar; the versions are intentional.
9. **The Composio user ID** defaults to the user running the scaffold (Albert), not the client. The client doesn't manage Composio directly — Albert connects Gmail/Drive on their behalf via `npm run connect`. Clarify if the user wants a different setup.
10. **Schema mirroring** — when automations are eventually added, Zod schemas are duplicated between `<slug>/src/lib/automations/<auto>/schema.ts` and `<slug>_backend/src/automations/<auto>/schema.ts`. Both must stay in sync. Flag this when automations are introduced.

## Final Note

This skill is **standalone** — the `templates/` directory contains the full source for both projects with placeholders. It does not depend on the original `aisystem` or `aisystem_backend` folders existing. Use `$ARGUMENTS` (if provided) as a hint for the client name, but always confirm via `AskUserQuestion` before scaffolding.
