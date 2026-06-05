# Parameters

The seven placeholders the scaffold script substitutes via `sed`. Anything else in the templates is intentional and stays as-is.

| Placeholder | Description | Example | Where it appears |
|-------------|-------------|---------|------------------|
| `{{CLIENT_NAME}}` | Brand display name | `Acme Co` | Page titles, sidebar branding, login copy, verify page, settings header, backend `BUSINESS_NAME` default |
| `{{CLIENT_DOMAIN}}` | Email domain used to gate auth | `acme.com` | `src/auth.ts` ALLOWED_DOMAIN, login error/placeholder copy, `.env*.example` defaults |
| `{{CLIENT_SLUG}}` | Lowercase kebab-case slug | `acme` | `package.json` names (frontend = slug, backend = slug-backend), Mongo DB default, scaffold script output paths |
| `{{EMAIL_FROM}}` | Sender address for magic links | `noreply@acme.com` | Frontend `.env.local.example` `EMAIL_FROM=` |
| `{{COMPOSIO_USER_ID}}` | Composio account that owns Gmail/Drive OAuth | `albert@shiney.ai` | Both `.env*.example` files. Default to the operator's email, not the client's (Albert connects services on the client's behalf). |
| `{{BUSINESS_EMAIL}}` | Billing email | `billing@acme.com` | Backend `.env.example` `BUSINESS_EMAIL=` |
| `{{MONGODB_DB}}` | Mongo DB name | `acme` | Frontend `.env.local.example` `MONGODB_DB=` |

## Derivation rules

Given user input `CLIENT_NAME` and `CLIENT_DOMAIN`:

```
CLIENT_SLUG       = lowercase(CLIENT_NAME), spaces → '-', strip non-[a-z0-9-]
EMAIL_FROM        = "noreply@" + CLIENT_DOMAIN          (confirm if user wants different)
BUSINESS_EMAIL    = "billing@" + CLIENT_DOMAIN          (confirm if user wants different)
MONGODB_DB        = CLIENT_SLUG
COMPOSIO_USER_ID  = operator's email (from CLAUDE.md userEmail, NOT the client's)
```

## Things that look like placeholders but aren't

- `shiney-*` CSS keyframe identifiers in `globals.css` — these are local keyframe names, not branding. Leave them.
- `EXECUTE_OPTS`, `EMAIL_FROM`, `TRIGGER_SECRET_KEY` in env-variable names — env var names are part of the contract with the runtime and stay verbatim.
- `proj_REPLACE_ME` in `trigger.config.ts` — this is the default for an unset env var, not a scaffold placeholder. Users fill in `TRIGGER_PROJECT_REF` in `.env`.

## After substitution

`scaffold.sh` runs a final `grep -rE '\{\{[A-Z_]+\}\}'` over both output trees. If anything matches, it warns. That should not happen — if it does, either the template has a typo or a new placeholder was added without updating the script.
