# Automations

Each automation lives in its own folder under `src/automations/<slug>/`. The Trigger.dev runtime auto-discovers any file exporting a task.

## Add a new automation

1. Create `src/automations/<slug>/task.ts` exporting a `schemaTask({ id: "<slug>", schema, run })`.
2. Define input validation in `src/automations/<slug>/schema.ts` with Zod.
3. Mirror the schema in the frontend at `{{CLIENT_SLUG}}/src/lib/automations/<slug>/schema.ts`.
4. Register the automation in the frontend's `src/config/automations.ts`.
5. Add a route at `{{CLIENT_SLUG}}/src/app/(dashboard)/dashboard/automations/<slug>/page.tsx`.

## Conventions

- `task.ts` — entry point; exports the schemaTask
- `schema.ts` — Zod schemas, mirrored with the frontend
- Co-locate helpers (rendering, math, formatting) in the same folder
- Use `src/shared/` for cross-automation infrastructure (LLM clients, Composio wrappers)
