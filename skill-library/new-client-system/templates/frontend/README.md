# {{CLIENT_NAME}} — Automations Dashboard

Internal dashboard for the automations {{CLIENT_NAME}} runs for the client. Login is restricted to `@{{CLIENT_DOMAIN}}` email addresses.

## Stack

- **Next.js 16** (App Router, TypeScript)
- **Auth.js v5** (NextAuth beta) with **Resend** magic links — JWT sessions, no Google login
- **Tailwind CSS v4** + **shadcn/ui**
- **MongoDB** (helper only — no schemas wired up yet)
- **Trigger.dev** (scaffold only — `trigger.config.ts` + empty `src/trigger/`)

## Layout

```
src/
├── auth.ts                       # NextAuth config (@{{CLIENT_DOMAIN}}-only signIn callback)
├── middleware.ts                 # protects /dashboard/**
├── app/
│   ├── login/                    # magic-link form
│   ├── verify/                   # "check your inbox" screen
│   ├── api/auth/[...nextauth]/   # NextAuth route handler
│   └── (dashboard)/
│       └── dashboard/
│           ├── page.tsx          # overview
│           ├── automations/      # list + [slug] detail
│           └── settings/         # account + sign out
├── components/
│   ├── sidebar.tsx               # nav (driven by config/automations.ts)
│   ├── sign-out-button.tsx
│   └── ui/                       # shadcn primitives
├── config/automations.ts         # single source of truth for sidebar entries
├── lib/
│   ├── mongodb.ts                # cached MongoClient promise
│   ├── resend.ts                 # Resend client
│   └── utils.ts                  # shadcn cn()
└── trigger/                      # (empty — future Trigger.dev tasks live here)
```

## Setup

```bash
cp .env.local.example .env.local
# fill in AUTH_SECRET, RESEND_API_KEY, EMAIL_FROM
npm install
npm run dev
```

Open http://localhost:3000 — you'll be redirected to `/login`.

### Adding an automation to the sidebar

Append to `src/config/automations.ts`. The sidebar, the `/dashboard/automations` index, and `/dashboard/automations/[slug]` are all driven by that file.

### Backend (Trigger.dev) — not yet initialized

When you're ready to add backend tasks:

```bash
npx trigger.dev@latest init
```

Then create tasks in `src/trigger/` and call them from server actions or route handlers.
