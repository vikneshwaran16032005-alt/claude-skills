# Site Structure — 9 Sections

All sections live in `src/App.jsx` as one file. Build them in this order. Line ranges below refer to the bundled reference file at `~/.claude/skills/build-premium-website/reference/full-reference-app.jsx` — open and read those line ranges when you need the exact markup.

---

## 1. Navbar (lines 75–191)

**Purpose:** Fixed pill nav at top, glass-on-scroll, mobile hamburger.

**Pattern:**
- `fixed top-4 left-1/2 -translate-x-1/2 z-50` — centered pill
- Width: `w-[calc(100%-2rem)] max-w-5xl`, `rounded-full`, `px-4 sm:px-6 py-2.5`
- Glass class applied conditionally when `window.scrollY > 80`
- Logo: 36×36 rounded primary square with brand icon (Droplets/Zap/etc.) + brand name in `font-display font-bold`
- Links: 5 anchors (`#hjem`, `#services`, etc.) — translate labels
- CTA: rounded-full primary button "Get a quote" with `ArrowUpRight` icon
- Mobile: `<lg` shows hamburger → full-screen `bg-deep/90 backdrop-blur-2xl` overlay slides down

**State:** `scrolled` (window scroll listener), `open` (mobile menu)

---

## 2. Hero (lines 196–302)

**Purpose:** Full-viewport entry. `min-h-[100dvh]`.

**Pattern:**
- Background `<img>` absolutely positioned, `object-cover`, low brightness
- Two gradient overlays stacked: `from-deep/80 via-deep/40 to-deep/70` + bottom `from-deep to-transparent`
- Floating themed particles in top-right (3–5 `<div>`s with `animate-float` and staggered `animationDelay`)
- Top + bottom decorative gradient borders (1px lines)
- Content wrapper: `relative z-10 max-w-7xl mx-auto px-6 sm:px-10 lg:px-16 pt-32 pb-20`
- H1: `font-display text-5xl sm:text-7xl lg:text-8xl font-bold text-white tracking-tighter`
  - Two lines: first regular, second `font-serif italic` for flourish
- Subhead: `font-body text-white/70 text-base sm:text-lg max-w-xl`
- CTAs: primary "Get a quote" + secondary glass "Call <number>"
- Scroll indicator at bottom: animated thin line + "Scroll" label in mono

**Animations (GSAP `useEffect`):**
```js
gsap.from('.hero-line-1', { y: 40, opacity: 0, duration: 1, delay: 0.3, ease: 'power3.out' })
gsap.from('.hero-line-2', { y: 60, opacity: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' })
gsap.from('.hero-cta, .hero-meta', { y: 24, opacity: 0, duration: 0.8, delay: 0.8, stagger: 0.12 })
```

---

## 3. Features — 3 cards with interactive components (lines 691–797)

**Purpose:** Showcase 3 service pillars with live animated demos.

**Grid:** `grid grid-cols-1 lg:grid-cols-3 gap-6` inside `max-w-7xl` container, `py-32`.

Each card: `feature-card` class, `rounded-3xl bg-surface border border-divider p-6 sm:p-8`, header (eyebrow mono label + h3), then **interactive component** (h-44 box), then descriptive paragraph + small bullet list.

The three interactive components:

### 3a. Stacked shuffler (HeatingShuffler, lines 305–367)
Three cards stacked z-order, rotate every 3 s. Front: full opacity; back two: scaled down 0.94/0.88, blurred, dimmed. On rotation, front exits up with fade, others advance.

### 3b. Signature animation (MaintenanceRain, lines 372–590)
**THE WATER DROPS** — re-skin to industry. See `animations.md` and `industry-themes.md`. Pipe + 7 falling drops (staggered delays/durations) + ripples + status bar that cycles every 2.3 s.

### 3c. Cursor + scheduler (RenovationScheduler, lines 595–688)
SVG cursor moves to calendar day, click animation, confirmation state. 5-step loop every 1.4 s.

**Reveal animation:**
```js
gsap.from('.feature-card', {
  scrollTrigger: { trigger: ref.current, start: 'top 80%', once: true },
  y: 40, opacity: 0, duration: 0.8, stagger: 0.15, ease: 'power3.out',
})
```

---

## 4. Pillars — 3 trust stats (lines 843–985)

**Purpose:** Animated counter trio. "30+ years", "100% authorized", "24/7 response" — adapt to user's trust signals.

**Layout:** `grid lg:grid-cols-3` with vertical dividers (`lg:divide-x divide-divider`).

Each pillar:
- Eyebrow label (mono, uppercase, tracking-widest)
- Huge number via `<CountUp end={n} suffix="+" duration={2000} />`
- Description paragraph
- Animated baseline sweep: thin gradient line that slides L→R on a `pillar-sweep` keyframe

**Background:** soft blurred colored blobs (primary/accent) absolutely positioned.

**CountUp component:** IntersectionObserver triggers, then `requestAnimationFrame` ticks. Easing: ease-out cubic. See `animations.md`.

---

## 5. Protocol — Sticky stack (lines 990–1125)

**Purpose:** 3-step process where each card "stacks" on top of the previous as you scroll. Most premium-feeling section.

**Container:** tall section, `relative`. Inside, 3 sticky cards each `position: sticky; top: 6rem` with `min-height` so they overlap.

**Cards:** Each takes the full width inside `max-w-7xl`. Layout is 5-col grid: left 3 cols = content (step number, eyebrow, h3, paragraph, bullet list), right 2 cols = image.

**GSAP scrub:**
```js
gsap.to(card, {
  scrollTrigger: {
    trigger: card,
    start: 'top top+=100',
    end: 'top top+=400',
    scrub: 1,
  },
  scale: 0.92,
  filter: 'blur(6px) saturate(0.7)',
  opacity: 0.5,
})
```

Apply to cards 1 and 2 so they recede as 2 and 3 come in.

---

## 6. ServicesGrid — 6 dark tiles (lines 1241–1304)

**Purpose:** All services in compact dark grid.

**Wrapper:** `bg-deep text-white py-32` section.
**Grid:** `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-white/5` (the gap creates 1px dividers).

Each tile (`svc-tile`):
- `bg-deep p-8 sm:p-10`
- Icon in rounded box top-left
- h3 (`font-display text-xl`)
- Paragraph (text-white/60)
- Hover: bg-white/[0.03], icon scale 1.1

**Reveal:** GSAP ScrollTrigger stagger as before.

---

## 7. TrustSignals — 3 credibility badges (lines 1309–1387)

**Purpose:** Third-party validation.

**Layout:** `grid lg:grid-cols-3 gap-6 max-w-5xl mx-auto`.

Each badge: white rounded-2xl card with icon (ShieldCheck / Award / Clock), title, subtext. Soft shadow, hover lift.

Reveal: IntersectionObserver-based fade-in with stagger.

---

## 8. ContactForm (lines 1392–1627)

**Purpose:** Lead capture.

**Layout:** `grid lg:grid-cols-12 gap-12` inside `max-w-7xl`.
- Left col-span-5: heading, three contact cards (Phone / Mail / MapPin), data security blurb
- Right col-span-7: form on white rounded-3xl card

**Form fields:**
- 2-col grid: Name, Email
- 2-col grid: Phone, Zip
- Textarea: Message (rows=5)
- File upload zone: dashed border, drag-drop, Upload icon, accepts images, max 5 files. Shows file list with remove buttons.
- Submit: full-width primary button "Send"

**State:** `'idle' | 'sending' | 'sent'`. On submit set sending → setTimeout 1200ms → sent. Sent state replaces form with centered checkmark card "Thanks — we'll be in touch."

**Field component:** reusable wrapper with label above input, focus ring primary.

---

## 9. Footer (lines 1649–1769)

**Purpose:** Multi-col footer + legal.

**Layout:** dark `bg-deep text-white`. Inner grid `lg:grid-cols-5`:
- Col 1–2: big brand block (logo + tagline + status indicator "System Operational" with pulsing green dot)
- Col 3: Services links
- Col 4: Company links (About, Process, Contact)
- Col 5: Contact (phone, email, address)

Below: thin border-top, then copyright + legal links (Privacy / Terms) row.

---

## Page-level wrapper

In `App` root return:
```jsx
<div className="relative">
  <div className="noise-overlay" />
  <Navbar />
  <Hero />
  <Features />
  <Pillars />
  <Protocol />
  <ServicesGrid />
  <TrustSignals />
  <ContactForm />
  <Footer />
</div>
```

Register ScrollTrigger plugin once at top of file. `useEffect` on App mount: `ScrollTrigger.refresh()` after fonts load.
