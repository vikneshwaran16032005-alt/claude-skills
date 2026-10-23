# Stack & Versions

## Frontend (`<slug>/`)

**Framework:** Next.js 16.2.6 (App Router, React 19.2.4, TypeScript 5).

> ⚠️ Next.js 16 contains breaking changes vs prior versions. The template ships an `AGENTS.md` noting this. When working on a scaffolded project, read `node_modules/next/dist/docs/` before assuming API shape.

**Auth:** NextAuth.js v5.0.0-beta.31 with the Resend (magic link) provider and `@auth/mongodb-adapter` v3 for verification token storage. JWT session strategy.

**Styling:** Tailwind v4 via `@tailwindcss/postcss` (no `tailwind.config.js` — theme is inline in `globals.css` via `@theme`). `tw-animate-css` for animation utilities. `clsx` + `tailwind-merge` exposed as `cn()`.

**UI primitives:** shadcn/ui (`base-nova` base), built on `@base-ui/react`. `lucide-react` for icons.

**Data layer:** No client fetching library. Server Actions only. `mongodb` v7 for the Auth adapter. `zod` v4 for form validation.

**Integrations:** `@trigger.dev/sdk` v4 (fires backend tasks), `@composio/core` v0.10 (OAuth + tool execution), `resend` v6 (magic-link email).

**Theming:** `next-themes` v0.4 — light / dark / system cycle.

Full list (verbatim from template `package.json`):

```json
{
  "dependencies": {
    "@auth/mongodb-adapter": "^3.11.2",
    "@base-ui/react": "^1.4.1",
    "@composio/core": "^0.10.0",
    "@trigger.dev/sdk": "^4.4.6",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "lucide-react": "^1.16.0",
    "mongodb": "^7.2.0",
    "next": "16.2.6",
    "next-auth": "^5.0.0-beta.31",
    "next-themes": "^0.4.6",
    "react": "19.2.4",
    "react-dom": "19.2.4",
    "resend": "^6.12.3",
    "shadcn": "^4.7.0",
    "tailwind-merge": "^3.6.0",
    "tw-animate-css": "^1.4.0",
    "zod": "^4.4.3"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "eslint": "^9",
    "eslint-config-next": "16.2.6",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```

## Backend (`<slug>_backend/`)

**Runtime:** Node.js (ESM, `"type": "module"`), TypeScript 5.7.

**Framework:** Trigger.dev v4 — `schemaTask` discovery from `src/automations/`.

**Integrations:** `@anthropic-ai/sdk` v0.39 (Claude — model `claude-sonnet-4-6`), `@composio/core` v0.10 (Gmail / Drive), `@react-pdf/renderer` v4 (server-side PDF — included even though no automations ship yet, because most automations will need it).

**Validation:** `zod` v3.23 (note: **v3 in backend, v4 in frontend** — when mirroring schemas, the API is largely compatible but be aware).

**Scripts:**

```json
{
  "trigger:dev": "npx trigger.dev@latest dev",
  "trigger:deploy": "npx trigger.dev@latest deploy",
  "connect": "tsx scripts/connect-composio.ts",
  "typecheck": "tsc --noEmit"
}
```

## Env vars required for boot

### Frontend `.env.local`

```
AUTH_SECRET=                 # openssl rand -base64 32
NEXTAUTH_URL=                # http://localhost:3000 in dev
RESEND_API_KEY=
EMAIL_FROM=                  # e.g. noreply@<domain>
MONGODB_URI=
MONGODB_DB=                  # template default = client slug
TRIGGER_SECRET_KEY=
TRIGGER_PROJECT_REF=
COMPOSIO_API_KEY=
COMPOSIO_USER_ID=
```

### Backend `.env`

```
TRIGGER_PROJECT_REF=         # MUST match frontend
TRIGGER_SECRET_KEY=          # MUST match frontend
COMPOSIO_API_KEY=
COMPOSIO_USER_ID=
ANTHROPIC_API_KEY=
BUSINESS_NAME=               # template default = client display name
BUSINESS_EMAIL=              # billing@<domain>
BUSINESS_ADDRESS_LINE1=
BUSINESS_ADDRESS_LINE2=
BUSINESS_PHONE=
BUSINESS_LOGO_URL=
BUSINESS_BANK_DETAILS=
DEFAULT_CURRENCY=USD
DEFAULT_TAX_RATE_PCT=0
DEFAULT_PAYMENT_TERMS=Payment due within 14 days.
DEFAULT_DUE_DAYS=14
GOOGLE_DRIVE_FOLDER_ID=      # optional
```

(`BUSINESS_*` vars are pre-staged for the typical invoice/billing automation pattern. They're harmless if no automation consumes them yet.)
