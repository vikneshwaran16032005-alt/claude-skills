# Architecture

Two projects, one product. They communicate via Trigger.dev.

```
┌──────────────────────────┐         ┌──────────────────────────┐
│  <slug>/  (Next.js 16)   │         │  <slug>_backend/         │
│                          │         │  (Trigger.dev worker)    │
│  • Auth (magic link)     │ trigger │                          │
│  • Dashboard UI          │────────▶│  • schemaTask runs       │
│  • Server actions        │  .dev   │  • PDF render            │
│  • Composio OAuth UI     │         │  • Claude email draft    │
│  • Form submission       │         │  • Composio actions      │
└──────────────────────────┘         └──────────────────────────┘
        │                                       │
        ▼                                       ▼
   MongoDB (auth)                         Gmail / Drive / Claude
   Resend (magic links)                   (via Composio + Anthropic SDK)
```

## Frontend (`<slug>/`)

**App Router (Next.js 16) layout:**

```
src/
├── app/
│   ├── (dashboard)/             # Auth-gated route group
│   │   ├── layout.tsx           # Sidebar + topbar shell, session check
│   │   └── dashboard/
│   │       ├── page.tsx         # Empty state (no automations yet)
│   │       ├── settings/
│   │       └── automations/
│   │           ├── page.tsx     # Lists registry from config/automations.ts
│   │           ├── [slug]/      # Generic detail page
│   │           └── connect-actions.ts  # Shared Composio OAuth server actions
│   ├── api/auth/[...nextauth]/  # NextAuth route handler
│   ├── login/                   # Magic-link entry
│   ├── verify/                  # "Check your inbox"
│   ├── layout.tsx               # Root layout, providers
│   ├── page.tsx                 # Redirect: /dashboard or /login
│   └── globals.css              # Tailwind v4 @theme + tokens + utilities
├── auth.ts                      # NextAuth v5 config, domain-restricted signIn
├── proxy.ts                     # Middleware wrapper (auth-gated routes)
├── config/
│   └── automations.ts           # Empty registry — add new automations here
├── lib/
│   ├── mongodb.ts               # Lazy client singleton
│   ├── resend.ts                # Email client for magic links
│   ├── composio.ts              # Composio client + toolkit status helpers
│   └── utils.ts                 # cn() (clsx + tailwind-merge)
└── components/
    ├── ui/                      # shadcn primitives (button, card, dialog, ...)
    ├── sidebar.tsx              # Driven by config/automations.ts
    ├── topbar.tsx
    ├── connect-modal.tsx        # Composio OAuth wizard (poll-to-connect)
    ├── status-dot.tsx
    ├── theme-toggle.tsx
    └── theme-provider.tsx
```

**Auth model.** NextAuth v5 beta + Resend magic links + MongoDB adapter. `signIn` callback restricts to `*@<CLIENT_DOMAIN>`. Sessions are JWT; the MongoDB adapter stores users and verification tokens only.

**Data flow.** All server work happens via **Server Actions** (`"use server"`). No client-side data fetching libraries. Forms submit → server action validates with Zod → `tasks.trigger("<task-id>", payload)` fires the backend.

**Composio role.** Composio brokers OAuth + tool execution. The frontend lets the user connect Gmail/Drive via a modal that polls status. The backend then executes Gmail/Drive actions on the user's behalf without re-prompting.

## Backend (`<slug>_backend/`)

**Trigger.dev v4** project that auto-discovers tasks from `src/automations/*/`.

```
├── trigger.config.ts            # dirs: ["./src/automations"]
├── src/
│   ├── automations/             # One folder per automation (none yet)
│   │   ├── _example/.gitkeep    # Placeholder so the dir exists
│   │   └── README.md            # How to add a new automation
│   └── shared/
│       ├── anthropic.ts         # anthropic() singleton + safeParseJson helper
│       └── composio.ts          # composio() singleton + Gmail/Drive wrappers
└── scripts/
    └── connect-composio.ts      # One-time OAuth setup (npm run connect)
```

**No database.** Tasks are stateless. Persistent state lives in:

- Gmail (sent emails)
- Google Drive (generated files)
- Composio (OAuth tokens, keyed by `COMPOSIO_USER_ID`)

**Adding an automation later** (do NOT do this during scaffold):

1. `<slug>_backend/src/automations/<auto>/task.ts` — `schemaTask({ id, schema, run })`
2. `<slug>_backend/src/automations/<auto>/schema.ts` — Zod input schema
3. Mirror schema at `<slug>/src/lib/automations/<auto>/schema.ts`
4. Add an entry to `<slug>/src/config/automations.ts`
5. Add a route at `<slug>/src/app/(dashboard)/dashboard/automations/<auto>/page.tsx` that calls a server action that calls `tasks.trigger("<id>", payload)`

## Frontend ↔ backend contract

| Item | Frontend | Backend | Notes |
|------|----------|---------|-------|
| `TRIGGER_PROJECT_REF` | `.env.local` | `.env` | Must match |
| `TRIGGER_SECRET_KEY` | `.env.local` | `.env` | Must match |
| Zod schemas | `src/lib/automations/<auto>/schema.ts` | `src/automations/<auto>/schema.ts` | Mirrored; keep in sync |
| Task IDs | string in server action | `schemaTask({ id })` | String-matched at runtime |
| Composio toolkits | hardcoded list in automation route | implicit (via `composioUserId()`) | OAuth done once via backend `npm run connect` |

## What's "structure" vs "automation"

**Structure** (in templates):
- All auth, dashboard shell, design system, UI primitives
- Composio + Anthropic + Trigger.dev clients (initialized but unused)
- Empty automations registry, empty `src/automations/` directory
- Env scaffolding, configs, scripts

**Automation** (NOT in templates):
- Task bodies (`schemaTask({ id, schema, run })` definitions)
- Per-automation Zod schemas
- Per-automation routes/forms/actions
- Per-automation helpers (PDF render, math, formatting)

Keep this split when adding new automations later — shared infrastructure stays in `shared/`, automation-specific code lives in its own folder.
