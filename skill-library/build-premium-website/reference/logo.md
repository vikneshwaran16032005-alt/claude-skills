# Logo Design

The reference uses a simple but effective logo lockup: a 36×36 rounded-full primary-colored badge containing a single lucide icon, next to the brand name in `font-display font-bold`. This pattern works for any industry — only the icon and color change.

## Default lockup (use unless user supplies a custom logo)

```jsx
<a href="#home" className="flex items-center gap-2 group">
  <span className="relative flex h-9 w-9 items-center justify-center rounded-full bg-primary">
    <ICON className="h-5 w-5 text-white" strokeWidth={2.4} />
    <span className="absolute inset-0 rounded-full ring-2 ring-primary/30 group-hover:ring-primary/50 transition" />
  </span>
  <span className={`font-display font-bold tracking-tight text-lg ${scrolled ? 'text-ink' : 'text-white'} transition-colors`}>
    <COMPANY_NAME>
  </span>
</a>
```

The hover `ring` expands subtly — keep it.

## Icon picker (matches the signature animation theme)

| Industry | Logo icon (lucide-react) |
|---|---|
| Plumbing / water | `Droplets` |
| Electrical | `Zap` |
| HVAC heating | `Flame` |
| HVAC cooling | `Snowflake` |
| Bakery / café | `Croissant` or `Wheat` |
| Fitness | `Dumbbell` or `Activity` |
| Tech / SaaS | `Hexagon` or `Cpu` |
| Landscaping | `Leaf` or `Trees` |
| Auto / mechanic | `Wrench` or `Cog` |
| Finance | `TrendingUp` or `LineChart` |
| Beauty / spa | `Sparkles` or `Flower2` |
| Real estate | `Home` or `Key` |
| Construction | `HardHat` or `Hammer` |
| Photography | `Aperture` |
| Legal | `Scale` |
| Restaurant | `Utensils` or `ChefHat` |
| Dental / medical | `Stethoscope` or `HeartPulse` |
| Cleaning | `Sparkles` or `SprayCan` |

The logo icon should usually **echo** the signature-animation theme but not be identical to it. (Example: a plumbing brand pairs `Droplets` as the logo icon with falling teardrops in the signature animation.)

## Lockup variants

### A — Default (icon + wordmark, horizontal)
What's described above. Default everywhere.

### B — Monogram only (favicon / collapsed nav)
Same badge, no wordmark. Use for `favicon.svg` and the footer status corner.

```html
<!-- public/favicon.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">
  <circle cx="18" cy="18" r="18" fill="<PRIMARY_HEX>"/>
  <!-- paste the lucide path here, centered, white, scaled to ~20×20 -->
</svg>
```

### C — Mark + serif flourish (luxury tones)
For `luxury-minimal` or `warm-artisanal` tones, swap the wordmark to the serif font and drop the badge:

```jsx
<a href="#home" className="font-serif italic text-2xl tracking-tight">
  <COMPANY_NAME>
</a>
```

### D — Stacked (footer / hero corner)
Icon on top, wordmark below, tagline beneath in mono uppercase. Use only in the footer.

## Footer logo block (always include)

```jsx
<div className="flex flex-col gap-3">
  <div className="flex items-center gap-2">
    <span className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
      <ICON className="h-5 w-5 text-white" strokeWidth={2.4} />
    </span>
    <span className="font-display font-bold text-2xl"><COMPANY_NAME></span>
  </div>
  <p className="font-serif italic text-white/70 text-lg max-w-xs">
    <TAGLINE_LINE>
  </p>
  <div className="flex items-center gap-2 mt-2">
    <span className="relative h-2 w-2 rounded-full bg-emerald-500">
      <span className="absolute inset-0 rounded-full bg-emerald-500 animate-ping opacity-75" />
    </span>
    <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-white/60">
      <STATUS_LABEL>
    </span>
  </div>
</div>
```

## When the user supplies a custom logo

- If they paste an image URL → put it at `public/logo.svg` (or `.png`) and replace the badge with `<img src="/logo.svg" className="h-9 w-auto" alt="<COMPANY_NAME>" />`.
- If they describe what they want ("a stylized W with a leaf") → render an inline SVG approximation as the badge contents.
- Always keep the 36×40 px height range in the navbar so the pill-nav vertical rhythm holds.

## Color rules for the badge

- `bg-primary` for light navbar (over-image hero) — gives white-icon legibility.
- `bg-deep` with `text-primary` icon for inverted dark sections.
- On `glass` (scrolled nav), keep `bg-primary` — it pops against the frosted backdrop.
- Never put the badge on `bg-accent` unless the brand's accent IS the primary.

## Generate a quick favicon

Always write `public/favicon.svg` matching variant B above so the browser tab shows brand color, not the Vite default.
