# {{CLIENT_SLUG}}-backend

Standalone Trigger.dev project that powers the automations exposed in the [{{CLIENT_SLUG}}](../{{CLIENT_SLUG}}) dashboard. No Next.js — this project only contains background tasks.

## Layout

```
src/
  shared/                  # reusable across automations
    anthropic.ts           # Claude client singleton + JSON helpers
    composio.ts            # Composio singleton + Gmail/Drive wrappers
  automations/             # one folder per automation; auto-discovered by trigger.config.ts
    _example/              # placeholder — replace with your first automation
scripts/
  connect-composio.ts      # one-time Gmail + Drive OAuth
```

## Setup

```sh
cd {{CLIENT_SLUG}}_backend
npm install
cp .env.example .env.local       # fill in TRIGGER_*, COMPOSIO_*, ANTHROPIC_*, BUSINESS_*
npm run connect                  # one-time Gmail + Drive OAuth for COMPOSIO_USER_ID
npm run trigger:dev              # registers tasks with the Trigger.dev cloud
```

The Next.js frontend (`{{CLIENT_SLUG}}`) needs the **same** `TRIGGER_SECRET_KEY` and `TRIGGER_PROJECT_REF` so its server actions can call into this project via `tasks.trigger(...)`.

## Adding a new automation

1. Create `src/automations/<slug>/task.ts` and export a `schemaTask({ id, schema, run })`.
2. (Optional) put supporting domain files alongside it — schema, helpers, integrations.
3. Reuse `src/shared/composio.ts` for new Composio toolkits — just add a new wrapper there.
4. Create the matching page + form in `{{CLIENT_SLUG}}/src/app/(dashboard)/dashboard/automations/<slug>/` and append a `{ slug, title, ... }` entry to `{{CLIENT_SLUG}}/src/config/automations.ts`.
5. Restart `npm run trigger:dev` so the new task gets registered.

No code change to `trigger.config.ts` is needed — `dirs: ["./src/automations"]` picks up new folders automatically.

## Deploy (later)

```sh
DOCKER_CONFIG=/tmp/empty-docker npx trigger.dev@latest deploy
```

Set the same env vars in the Trigger.dev dashboard's production environment, and swap the frontend's `TRIGGER_SECRET_KEY` to a `tr_prod_…` key in Vercel.
