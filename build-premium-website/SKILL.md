---
name: build-premium-website
description: Build a premium, animated marketing website (React + Vite + Tailwind + GSAP) for any industry. Use when the user asks to "build a website", "make a landing page for [business]", "build a marketing site", or wants a high-end animated company website. Adapts color, copy, services, and signature animation to the industry.
argument-hint: [business name or industry, optional]
---

# Build Premium Website

You are an expert at building high-end, animated, single-page marketing websites (React 19 + Vite + Tailwind CSS + GSAP). Your job is to gather business context, then scaffold a complete, responsive, production-quality site that adapts a refined visual system to any industry.

This skill is fully self-contained. A complete reference implementation lives inside the skill at `~/.claude/skills/build-premium-website/reference/full-reference-app.jsx` (and accompanying `full-reference-*.css/html/json` files). Read those when you need ground-truth markup or component code. Never copy industry-specific copy verbatim — translate every string to match the target business.

## Phase 1 — Intake (REQUIRED before any code)

Use `AskUserQuestion` to gather business context. Do not skip this. Batch into ~4 question rounds. See `~/.claude/skills/build-premium-website/reference/intake-questions.md` for exact question phrasing and option lists.

Collect at minimum:
- Company name + tagline
- Industry / what they do (one sentence)
- Tone (premium-technical, friendly-local, luxury-minimal, bold-modern, warm-artisanal)
- Brand colors (primary, accent) — or auto-suggest from industry
- 4–8 services (title + one-line description each)
- Contact info (phone, email, location, hours)
- Trust signals (years, certifications, memberships)
- Language (English / Danish / other)
- Hero imagery search terms (Unsplash keywords)
- Signature animation theme — auto-pick from industry table in `reference/industry-themes.md`

If the user gives short answers, fill in sensible defaults and proceed. The reminder says "work without stopping for clarifying questions" — make reasonable calls.

## Phase 2 — Scaffold

Create the project in the user's preferred projects directory (ask if unclear; default `~/Desktop/websites/<slug>/`):

```bash
cd <PROJECTS_DIR>
npm create vite@latest <slug> -- --template react
cd <slug>
npm install
npm install gsap lucide-react react-router-dom
npm install -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

Then drop in configs from `reference/tech-setup.md`:
- `tailwind.config.js` — substitute brand colors into the token slots
- `postcss.config.js`
- `vite.config.js` (port 5173, autoOpen)
- `index.html` — Google Fonts links + base meta
- `src/index.css` — copy verbatim from `reference/code-snippets.md`, substituting hex values for the brand colors
- `src/main.jsx` — React Router setup with three routes (/, /privacy, /terms)

## Phase 3 — Build sections in order

Build `src/App.jsx` as a single file containing all components (mirror reference structure). Follow `reference/structure.md` section-by-section. Each section:

1. **Navbar** — fixed pill nav, glass-on-scroll, mobile hamburger overlay
2. **Hero** — full-dvh, background image + dual gradient overlays, GSAP staggered entrance, floating themed particles (top-right)
3. **Features** — 3 interactive cards: one stacked-shuffler, one signature-animation (water-drops adapted to industry), one cursor-on-calendar/scheduler
4. **Pillars** — 3 trust stats with animated `CountUp` via IntersectionObserver + RAF
5. **Protocol** — 3-step sticky-stack with GSAP ScrollTrigger scrub (cards scale/blur/fade as next overlaps)
6. **ServicesGrid** — 6-tile dark grid with gap-px dividers and hover state
7. **TrustSignals** — 3 credibility badges with stagger fade-in
8. **ContactForm** — name/email/phone/zip + message + drag-drop file upload + idle/sending/sent states
9. **Footer** — multi-col grid + status pulse + legal links

Use `lucide-react` icons matched to the user's services. Use the brand's primary color throughout, accent sparingly. Default typography roles: display headings = Plus Jakarta Sans, italic flourish = Cormorant Garamond, body = Inter, labels = JetBrains Mono.

## Phase 4 — Signature animation

The reference's signature is the **falling water drops + ripples on a pipe**. Adapt to the industry by swapping the SVG shape and recoloring while reusing the same keyframes (`rain-fall`, `rain-ripple`, `rain-fadein`). Match table in `reference/industry-themes.md`:

| Industry | Shape | Colors |
|---|---|---|
| Plumbing/water/cleaning | Teardrop | blues |
| Electrical | Lightning bolt / spark | yellow + cyan arc |
| HVAC/heating | Flame OR snowflake | warm orange / icy blue |
| Bakery/food | Flour mote / dough drop | cream + amber |
| Fitness/wellness | Pulse ring / heartbeat line | crimson + lime |
| Tech/SaaS | Code bracket / scan dot | violet + neon |
| Landscaping | Falling leaf | forest green + rust |
| Auto/mechanic | Gear / oil drop | graphite + amber |
| Finance | Coin / ascending bar | navy + gold |
| Beauty/spa | Sparkle / petal | rose + champagne |
| Real estate | Key / pin drop | slate + brass |
| Construction | Spark + iron filing | charcoal + safety-orange |

Always re-skin — never just leave the teardrop.

## Phase 5 — Polish & verify

- `npm run dev` (background) and open `http://localhost:5173` via claude-in-chrome
- Resize to 375 / 768 / 1440 to verify responsive layout
- Scroll the full page — confirm hero stagger, feature reveals, sticky-stack scrub, pillar counters, signature animation loop
- Submit the contact form (mock state) — verify idle → sending → sent transition
- Read console messages — fix any errors
- Report the local URL to the user

## Critical Rules

1. **Always run Phase 1 intake first.** Never start coding before AskUserQuestion has returned.
2. **Translate every string.** No Danish text leaks into a non-Danish site. No plumbing terms leak into a non-plumbing site.
3. **Re-skin the signature animation** to match the industry — never ship water drops on a non-water business.
4. **Preserve the design system intact** — the typography stack, spacing scale, glass/magnetic-btn/grid-bg utilities are what make it look premium. Don't simplify them away.
5. **All 9 sections by default.** Only drop one if the user explicitly says so.
6. **Mobile-first.** Test at 375px. Hamburger menu, single-column stack, scaled type.
7. **Read the bundled reference freely.** When a pattern is unclear, open the in-skill copy at `~/.claude/skills/build-premium-website/reference/full-reference-app.jsx` (cited by line range in `reference/structure.md`).
8. **Use real images.** Pull Unsplash URLs matching the user's hero terms. Never use placeholder boxes.
9. **Match icon to service.** Pick semantically correct lucide-react icons. Don't reuse Droplets for a bakery.
10. **Don't write a README or docs** unless asked. Build the site.

## Reference files (read lazily as needed)

- `~/.claude/skills/build-premium-website/reference/intake-questions.md` — exact questions to ask
- `~/.claude/skills/build-premium-website/reference/structure.md` — section-by-section anatomy with line citations
- `~/.claude/skills/build-premium-website/reference/tech-setup.md` — package.json, configs, index.html
- `~/.claude/skills/build-premium-website/reference/design-system.md` — color slots, typography, components
- `~/.claude/skills/build-premium-website/reference/animations.md` — GSAP patterns, keyframes, CountUp
- `~/.claude/skills/build-premium-website/reference/industry-themes.md` — signature animation per industry
- `~/.claude/skills/build-premium-website/reference/logo.md` — logo lockups, icon picker per industry, favicon
- `~/.claude/skills/build-premium-website/reference/visual-examples.md` — ASCII mockups of every section + "premium" checklist
- `~/.claude/skills/build-premium-website/reference/code-snippets.md` — index.css, key component skeletons

## Final note

Use `$ARGUMENTS` as a starting hint for the business if provided (e.g. `/build-premium-website acme bakery`). Begin Phase 1 immediately if no arguments, or pre-fill what was given and ask only for the rest.
