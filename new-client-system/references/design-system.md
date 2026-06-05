# Design System

The visual language is defined entirely in `<slug>/src/app/globals.css` via Tailwind v4's `@theme` block. There is no separate `tailwind.config.js`. Tokens are OKLch-based so they tone-shift cleanly between light and dark.

## Color tokens (light mode)

| Token | Value | Use |
|-------|-------|-----|
| `--background` | `oklch(0.985 0.002 270)` | App background |
| `--surface` | `oklch(1 0 0)` | Card / panel background |
| `--foreground` | `oklch(0 0 0)` | Body text |
| `--muted` | low-chroma gray | Secondary text |
| `--border` | hairline gray | Default border |
| `--border-strong` | darker hairline | Emphasized border |
| `--primary` | `oklch(0.55 0.18 285)` | Brand purple |
| `--destructive` | `oklch(0.62 0.22 25)` | Red |
| `--status-active` | `oklch(0.72 0.17 150)` | Green |
| `--status-draft` | `oklch(0.62 0.005 270)` | Neutral gray |
| `--status-paused` | `oklch(0.78 0.16 80)` | Amber |

**Dark mode** (under `.dark`): background `oklch(0.13 0.008 270)`, surface `oklch(0.165 0.008 270)`, primary brightens to `oklch(0.7 0.17 285)`.

## Typography

- **Sans** — Geist Sans (`next/font/google`)
- **Mono** — Geist Mono
- **Heading** — same as sans (no separate display face)

CSS vars: `--font-geist-sans`, `--font-geist-mono`. Inject via the root layout.

## Radii

Base `--radius: 0.375rem` (6px). Scales: `sm` (60%), `md` (80%), `lg` (100%), `xl` (140%), `2xl` (180%), `3xl` (220%), `4xl` (260%).

## Custom utilities (in `@layer utilities`)

| Class | Purpose |
|-------|---------|
| `.font-tabular` | tabular-nums + slashed-zero — for numeric tables |
| `.text-mono-label` | uppercase mono micro-label, `tracking-[0.18em]`, 10px |
| `.hairline` / `.hairline-strong` | thin / emphasized borders |
| `.bg-grid` | radial dot pattern background |
| `.bg-grid-lines` | linear grid lines background |
| `.animate-enter` | 220 ms slide-up + fade in |
| `.animate-enter-delay-1/2/3` | staggered entry |
| `.animate-pulse-soft` | gentle pulse loop |
| `.animate-loader-dots` | three-dot loader |
| `.sweep` | top-to-bottom gradient sweep line |

## Theme toggle

`next-themes` with three modes: `light` / `dark` / `system`. The toggle in the topbar cycles through all three.

## Voice & copy

Sober, hairline-light, low-chrome. Form labels are mono-uppercase micro-labels (`text-mono-label`). Status dots use the four status colors (active / draft / paused / danger / neutral). Typography is left-aligned with generous line height. No emojis. Headings are short.

When customizing for a new client, swap the **primary** hue first — that's the only color the brand "owns." The status colors are universal across clients. The neutral grays stay put.
