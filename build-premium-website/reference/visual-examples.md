# Visual Examples — What Each Section Should Look Like

Use this file as a visual sanity check. If the built section doesn't *feel* like one of these mockups, it's wrong.

The **ground-truth reference** is the bundled file `~/.claude/skills/build-premium-website/reference/full-reference-app.jsx` plus the matching `full-reference-index.css`, `full-reference-tailwind.config.js`, and `full-reference-index.html`. Open them when you need exact markup. The mockups below are skeletons — match the proportions, the spacing, and the visual hierarchy.

---

## Section 1 — Navbar

**Desktop (scrolled state):**
```
    ╭───────────────────────────────────────────────────────────────╮
    │ ⬤ BrandName    Home  Services  About  Process  Contact  [CTA ↗]│
    ╰───────────────────────────────────────────────────────────────╯
        ↑ frosted glass pill, floating 16px from top, centered, max-w-5xl
```

**Desktop (top of page, transparent):**
```
    ⬤ BrandName    Home  Services  About  Process  Contact  [CTA ↗]
    ↑ no background, links + brand are WHITE over hero image
```

**Mobile (closed):**
```
    ╭─────────────────────────╮
    │ ⬤ BrandName         [☰] │
    ╰─────────────────────────╯
```

**Mobile (open — full-screen overlay):**
```
    ╔═══════════════════════════════╗
    ║ BrandName                 [✕] ║
    ║                                ║
    ║  Home          ──────────      ║
    ║  Services      ──────────      ║
    ║  About         ──────────      ║
    ║  Process       ──────────      ║
    ║  Contact       ──────────      ║
    ║                                ║
    ║  ╭────────────────────────╮   ║
    ║  │   Get a quote      ↗   │   ║
    ║  ╰────────────────────────╯   ║
    ╚═══════════════════════════════╝
    ↑ rounded-b-5xl, slides down from top, deep/90 backdrop
```

---

## Section 2 — Hero

```
    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │   (background photo, darkened 55%, gradient overlay)         │
    │                                                              │
    │                                            · ·               │
    │                                          · ⬤ ·  ← floating  │
    │                                            ·                 │
    │                                                              │
    │   EST. 1992 · LOCAL                                          │
    │                                                              │
    │   The work you can                                           │
    │   ―rely on.                          ← serif italic line     │
    │                                                              │
    │   Three decades of craft, every detail measured twice.       │
    │                                                              │
    │   [ Get a quote ↗ ]  [ ☎ Call +1 555 0123 ]                  │
    │                                                              │
    │                                              │ Scroll        │
    └──────────────────────────────────────────────┴───────────────┘
    full 100dvh, content bottom-aligned, h1 ~10–12rem on desktop
```

---

## Section 3 — Features (3 interactive cards)

```
    Heading line — serif italic accent
    Subhead paragraph, max-w-2xl

    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  EYEBROW · 01│  │  EYEBROW · 02│  │  EYEBROW · 03│
    │  Card title  │  │  Card title  │  │  Card title  │
    │              │  │              │  │              │
    │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │
    │ │ Stacked  │ │  │ │SIGNATURE │ │  │ │ Cursor + │ │
    │ │ shuffler │ │  │ │ANIMATION │ │  │ │ calendar │ │
    │ │ (3 cards)│ │  │ │(particles│ │  │ │ scheduler│ │
    │ │          │ │  │ │ falling) │ │  │ │          │ │
    │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │
    │              │  │              │  │              │
    │ Description  │  │ Description  │  │ Description  │
    │ · bullet     │  │ · bullet     │  │ · bullet     │
    │ · bullet     │  │ · bullet     │  │ · bullet     │
    └──────────────┘  └──────────────┘  └──────────────┘
        ↑ each card is interactive — middle one is the re-skinned signature
```

The middle card (signature animation) example for plumbing:
```
    ┌──────────────────────────────────────────┐
    │ 💧 ACUTE STANDBY              07 today  │ ← header strip
    │ ════════════════════════════════════════ │ ← pipe with valves
    │   ▼     ▼   ▼      ▼   ▼  ▼       ▼     │
    │   ░     ░   ░      ░   ░  ░       ░     │ ← teardrops falling
    │   ░     ░   ░      ░   ░  ░       ░     │
    │  ~~~○~~~~~~~○~~~~~~~○~~~~~~~~~~~~~~~~~  │ ← water surface + ripples
    │ ● Stable · monitoring              STABLE│ ← status strip
    └──────────────────────────────────────────┘
```

Same skeleton for **bakery**: oven rack at top, dough drops falling, counter line, "Fresh batch" status. Same skeleton for **electrical**: cable + sparks. Etc.

---

## Section 4 — Pillars (animated counters)

```
    ┌────────────────┬────────────────┬────────────────┐
    │ EYEBROW LABEL  │ EYEBROW LABEL  │ EYEBROW LABEL  │
    │                │                │                │
    │      30+       │     100%       │     24/7       │
    │                │                │                │
    │ years of       │ authorized     │ emergency      │
    │ experience.    │ professionals. │ response.      │
    │ ──────         │ ──────         │ ──────         │ ← sweep line animates
    └────────────────┴────────────────┴────────────────┘
    numbers count up from 0 when section enters viewport
    soft blurred color blobs in background
```

---

## Section 5 — Protocol (sticky stack)

```
    ┌─────────────────────────────────────────────────────────┐
    │ EYEBROW · 01                          ┌───────────────┐ │
    │                                       │               │ │
    │ Step title in big                     │  photograph   │ │
    │ display font                          │   of work     │ │
    │                                       │   in context  │ │
    │ Paragraph describing this stage of    │               │ │
    │ the work with specifics.              │               │ │
    │                                       └───────────────┘ │
    │ · checkpoint one                                        │
    │ · checkpoint two                                        │
    │ · checkpoint three                                      │
    └─────────────────────────────────────────────────────────┘
       ↑ as you scroll, this card shrinks, blurs, fades; next card slides over it
       ↑ sticky-top — stays pinned while you scroll past
```

Three of these stack on top of each other as you scroll. Each subsequent card has a different photo and step number.

---

## Section 6 — ServicesGrid (dark, 6 tiles)

```
    (full bleed dark background)

         All services — your complete partner.

    ┌─────────────┬─────────────┬─────────────┐
    │ ▣ Icon      │ ▣ Icon      │ ▣ Icon      │
    │             │             │             │
    │ Service 1   │ Service 2   │ Service 3   │
    │             │             │             │
    │ Short copy  │ Short copy  │ Short copy  │
    │ describing  │ describing  │ describing  │
    │ the work.   │ the work.   │ the work.   │
    ├─────────────┼─────────────┼─────────────┤  ← 1px white/5 dividers
    │ ▣ Icon      │ ▣ Icon      │ ▣ Icon      │
    │             │             │             │
    │ Service 4   │ Service 5   │ Service 6   │
    │ ...         │ ...         │ ...         │
    └─────────────┴─────────────┴─────────────┘
    on hover: tile bg lifts to white/[0.03], icon scales 1.1
```

---

## Section 7 — TrustSignals

```
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  🛡  Badge 1   │  │  🏆  Badge 2   │  │  ⏱  Badge 3   │
    │  Authorized     │  │  Member of      │  │  30+ years      │
    │  by [body]      │  │  [association]  │  │  in business    │
    └─────────────────┘  └─────────────────┘  └─────────────────┘
    white rounded-2xl cards, subtle shadow, hover lift
```

---

## Section 8 — ContactForm

```
    ┌────────────────────┬────────────────────────────────────┐
    │                    │ ┌────────────────────────────────┐ │
    │ Talk to us         │ │ Name              Email        │ │
    │ ━━━━━━━━━━━        │ │ ___________       ___________  │ │
    │                    │ │                                │ │
    │ ┌───┐ ☎ Phone      │ │ Phone             Zip          │ │
    │ │ ☎ │ +1 555 0123  │ │ ___________       ___________  │ │
    │ └───┘              │ │                                │ │
    │                    │ │ Message                        │ │
    │ ┌───┐ ✉ Email      │ │ ┌────────────────────────────┐ │ │
    │ │ ✉ │ hi@co.com   │ │ │                            │ │ │
    │ └───┘              │ │ │                            │ │ │
    │                    │ │ └────────────────────────────┘ │ │
    │ ┌───┐ 📍 Location  │ │                                │ │
    │ │ 📍│ City, State  │ │ ┌────────────────────────────┐ │ │
    │ └───┘              │ │ │  ⬆  Drop images or browse  │ │ │
    │                    │ │ │     max 5 · jpg, png       │ │ │
    │ 🔒 Data is secure  │ │ └────────────────────────────┘ │ │
    │    and private.    │ │                                │ │
    │                    │ │ ╭────────────────────────────╮ │ │
    │                    │ │ │  Send message          ↗   │ │ │
    │                    │ │ ╰────────────────────────────╯ │ │
    │                    │ └────────────────────────────────┘ │
    └────────────────────┴────────────────────────────────────┘
    grid lg:grid-cols-12 — left col-span-5, right col-span-7
```

**Sent state replaces the form:**
```
    ┌────────────────────────────────────┐
    │                                    │
    │              ✓                     │
    │       Thanks — we'll be            │
    │       in touch within              │
    │       one business day.            │
    │                                    │
    └────────────────────────────────────┘
```

---

## Section 9 — Footer

```
    (dark bg-deep)
    ┌───────────────────────────────────────────────────────────────┐
    │                                                               │
    │   Big tagline line in display font, max-w-3xl                 │
    │   ─ italic serif accent line.                                 │
    │                                                               │
    ├───────────────────────────────────────────────────────────────┤
    │ ⬤ Brand        Services    Company     Contact                │
    │ ―italic        Service 1   About       ☎ +1 555 0123          │
    │  tagline       Service 2   Process     ✉ hi@co.com            │
    │                Service 3   Careers     📍 City, State         │
    │ ● System       Service 4                                      │
    │   operational  Service 5                                      │
    │   (mono)       Service 6                                      │
    ├───────────────────────────────────────────────────────────────┤
    │ © 2026 Brand · All rights reserved.    Privacy · Terms       │
    └───────────────────────────────────────────────────────────────┘
    5-column grid on desktop, stacks on mobile
    green pulsing dot next to "System operational"
```

---

## Responsive collapse — Hero on 375px width

```
    ┌──────────────────────┐
    │ ⬤ BrandName     [☰] │
    │                      │
    │ (background photo,   │
    │  full vertical fill) │
    │                      │
    │                      │
    │  EST. 1992 · LOCAL   │
    │                      │
    │  The work you        │
    │  can ―rely on.       │
    │                      │
    │  Three decades of    │
    │  craft, every detail │
    │  measured twice.     │
    │                      │
    │  ┌─────────────────┐ │
    │  │ Get a quote   ↗ │ │
    │  └─────────────────┘ │
    │  ┌─────────────────┐ │
    │  │ ☎ Call          │ │
    │  └─────────────────┘ │
    │                      │
    └──────────────────────┘
    h1 drops from 8xl → 5xl
    CTAs stack vertically, full width
```

---

## What "premium" feels like (checklist)

If the site doesn't have **all** of these, it's not done:

- [ ] Generous whitespace — `py-32` between sections, `max-w-7xl` container
- [ ] Serif italic accent line on every major heading
- [ ] Mono uppercase tracking-widest eyebrow labels (10px)
- [ ] Floating particles in hero matching the industry theme
- [ ] Smooth GSAP stagger on hero entrance (≥800ms duration)
- [ ] At least one ScrollTrigger-driven reveal that's visible on first scroll
- [ ] Animated counters that tick up on viewport entry
- [ ] Sticky-stack protocol section (the most "premium" feeling element)
- [ ] Signature animation looping in the middle feature card
- [ ] Glass effect on scrolled navbar
- [ ] Magnetic-btn shimmer on every CTA
- [ ] Hover lifts on link rows
- [ ] Live status dot (green pulsing) somewhere in the footer
- [ ] Real photography (Unsplash, not stock-illustration vibes)
- [ ] Noise overlay at 5% mix-blend-mode multiply (subtle texture)
- [ ] Custom thin scrollbar matching brand color

If any of these are missing, the site reads as generic — not premium.
