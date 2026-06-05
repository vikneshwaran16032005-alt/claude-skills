# Design System

## Color slot mapping

The reference site uses 11 semantic color slots. When the user picks a brand palette, derive each slot:

| Slot | Role | Reference value | How to derive |
|---|---|---|---|
| `primary` | Brand main — buttons, accents, icons | `#85c4eb` | User's brand primary |
| `primary-dark` | Hover, text-on-light, deep accents | `#5fa9d6` | Primary × 0.85 lightness |
| `primary-light` | Tints, gradients, surfaces | `#b3d9f2` | Primary × 1.15 lightness |
| `accent` | Secondary highlight (sparingly) | `#E8956F` | Complementary or analogous |
| `accent-dark` | Hover for accent | `#d97e54` | Accent × 0.85 lightness |
| `background` | Page background | `#F9F9F9` | Always near-white; `#0F0F10` for dark mode |
| `surface` | Cards, raised panels | `#FFFFFF` | Pure white; `#161618` dark |
| `ink` | Body text | `#1A1A1A` | Always near-black; `#FAFAFA` dark |
| `muted` | Secondary text | `#6A6A6A` | Mid-gray |
| `divider` | Borders | `#E0E0E0` | Light gray |
| `deep` | Dark sections (ServicesGrid, Footer) | `#0F1419` | Always near-black |

## Typography roles

| Role | Reference font | When used |
|---|---|---|
| Display | Plus Jakarta Sans | h1, h2, h3, brand name, big numbers |
| Serif | Cormorant Garamond (italic) | Hero second line, taglines, flourishes |
| Body | Inter | Paragraphs, buttons, form fields |
| Mono | JetBrains Mono | Eyebrows, labels, meta, status indicators |

## Type scale (responsive)

| Element | Mobile → Desktop classes |
|---|---|
| H1 hero | `text-5xl sm:text-7xl lg:text-8xl tracking-tighter` |
| H2 section | `text-3xl sm:text-5xl lg:text-6xl tracking-tighter` |
| H3 card | `text-xl sm:text-2xl` |
| Body large | `text-base sm:text-lg leading-relaxed` |
| Body | `text-sm sm:text-base leading-relaxed` |
| Mono eyebrow | `text-[10px] sm:text-xs uppercase tracking-[0.18em]` |

## Spacing rhythm

| Token | Class | Use |
|---|---|---|
| Section padding y | `py-24 sm:py-32 lg:py-40` | Vertical breathing between sections |
| Container | `max-w-7xl mx-auto px-6 sm:px-10 lg:px-16` | Inner content |
| Card padding | `p-6 sm:p-8` | Feature cards |
| Gap (grid) | `gap-6` (cards), `gap-px` (dark-tile dividers), `gap-12` (form layout) | |
| Border radius | `rounded-3xl` (cards), `rounded-full` (buttons/nav), `rounded-2xl` (small cards) | |

## Button variants

**Primary CTA:**
```html
<a class="magnetic-btn inline-flex items-center gap-2 bg-primary text-white px-6 py-3 rounded-full font-semibold shadow-lg shadow-primary/30">
  Get a quote
  <ArrowUpRight className="h-4 w-4" />
</a>
```

**Secondary (glass):**
```html
<a class="magnetic-btn inline-flex items-center gap-2 glass-dark text-white px-6 py-3 rounded-full font-semibold border border-white/15">
  Call +1 555 0123
</a>
```

**Tertiary text link:**
```html
<a class="text-sm font-medium text-primary lift-on-hover inline-flex items-center gap-1">
  Read more <ArrowRight className="h-3.5 w-3.5" />
</a>
```

## Visual primitives

- `glass` — frosted light surface (use on scrolled navbar)
- `glass-dark` — frosted dark surface (mobile menu, secondary CTAs on hero)
- `noise-overlay` — fixed full-screen 5%-opacity noise (mounted once at root)
- `grid-bg` — subtle grid lines (use behind Pillars or Hero secondary content)
- `ring-pulse` — expanding ring pulse on small dots (status indicators)
- `magnetic-btn` — scale + shimmer on hover (every CTA)
- `lift-on-hover` — micro y-translate (nav links, text links)
- `gradient-text` — primary→primary-dark text gradient (use on big numbers, occasional headline word)

## Iconography rules

1. Always use `lucide-react`.
2. Match icon to service semantics (see `intake-questions.md` table).
3. Sizes: nav `h-5 w-5`, CTAs `h-4 w-4`, cards `h-6 w-6` in rounded-2xl primary/10 boxes.
4. `strokeWidth={2.2}` to `{2.4}` for crisper look.
