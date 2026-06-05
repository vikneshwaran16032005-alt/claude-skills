# Code Snippets — Paste-Ready

These are starting skeletons. Substitute brand colors and copy from intake. The full reference markup for any unclear section lives in the bundled file `~/.claude/skills/build-premium-website/reference/full-reference-app.jsx` — open it by line range from `structure.md`.

---

## src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
  body { @apply bg-background text-ink font-body; overflow-x: hidden; }
  ::selection { background-color: <PRIMARY>; color: #1A1A1A; }
  ::-webkit-scrollbar { width: 10px; }
  ::-webkit-scrollbar-track { background: #F9F9F9; }
  ::-webkit-scrollbar-thumb { background: <PRIMARY_LIGHT>; border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: <PRIMARY>; }
}

@layer components {
  .noise-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 1; opacity: 0.05; mix-blend-mode: multiply;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
  .magnetic-btn { position: relative; overflow: hidden; transition: transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94); }
  .magnetic-btn:hover { transform: scale(1.03) translateY(-1px); }
  .magnetic-btn:active { transform: scale(0.98); }
  .magnetic-btn::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0));
    transform: translateY(100%);
    transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94);
  }
  .magnetic-btn:hover::before { transform: translateY(0); }
  .lift-on-hover { transition: transform 0.3s cubic-bezier(0.25,0.46,0.45,0.94); }
  .lift-on-hover:hover { transform: translateY(-1px); }
  .gradient-text {
    background: linear-gradient(135deg, <PRIMARY> 0%, <PRIMARY_DARK> 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }
  .glass {
    background: rgba(249,249,249,0.65);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(<PRIMARY_RGB>,0.18);
  }
  .glass-dark {
    background: rgba(15,20,25,0.75);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  }
  .ring-pulse { box-shadow: 0 0 0 0 rgba(<PRIMARY_RGB>,0.6); animation: ring-pulse 2s infinite; }
  @keyframes ring-pulse {
    0%   { box-shadow: 0 0 0 0 rgba(<PRIMARY_RGB>,0.6); }
    70%  { box-shadow: 0 0 0 14px rgba(<PRIMARY_RGB>,0); }
    100% { box-shadow: 0 0 0 0 rgba(<PRIMARY_RGB>,0); }
  }
  .grid-bg {
    background-image:
      linear-gradient(rgba(<PRIMARY_RGB>,0.07) 1px, transparent 1px),
      linear-gradient(90deg, rgba(<PRIMARY_RGB>,0.07) 1px, transparent 1px);
    background-size: 40px 40px;
  }
  .text-balance { text-wrap: balance; }
  .scrollbar-hide::-webkit-scrollbar { display: none; }
}

@layer utilities {
  .perspective { perspective: 1200px; }
  .preserve-3d { transform-style: preserve-3d; }
  .clip-wave { clip-path: polygon(0 0, 100% 0, 100% 88%, 50% 100%, 0 88%); }
}
```

Replace `<PRIMARY>`, `<PRIMARY_DARK>`, `<PRIMARY_LIGHT>` with the brand hex codes. `<PRIMARY_RGB>` is the same color as comma-separated R,G,B integers (e.g. `133,196,235`).

---

## App.jsx skeleton

```jsx
import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { /* lucide icons by service */ } from 'lucide-react'

gsap.registerPlugin(ScrollTrigger)

const NAV_LINKS = [
  { label: '<HOME_LABEL>', href: '#home' },
  { label: '<SERVICES_LABEL>', href: '#services' },
  { label: '<APPROACH_LABEL>', href: '#approach' },
  { label: '<PROCESS_LABEL>', href: '#process' },
  { label: '<CONTACT_LABEL>', href: '#contact' },
]

const SERVICES = [
  // 6 entries from intake — each { icon, title, text }
]

function Navbar() { /* per structure.md §1 */ }
function Hero() { /* per structure.md §2 */ }
function Features() { /* 3-card grid; includes SignatureAnim */ }
function Pillars() { /* per structure.md §4 */ }
function Protocol() { /* per structure.md §5 */ }
function ServicesGrid() { /* per structure.md §6 */ }
function TrustSignals() { /* per structure.md §7 */ }
function ContactForm() { /* per structure.md §8 */ }
function Footer() { /* per structure.md §9 */ }
function CountUp({ end, suffix, duration }) { /* per animations.md */ }
function SignatureAnim() { /* per industry-themes.md */ }

export default function App() {
  useEffect(() => {
    const id = setTimeout(() => ScrollTrigger.refresh(), 200)
    return () => clearTimeout(id)
  }, [])
  return (
    <div className="relative">
      <div className="noise-overlay" />
      <Navbar />
      <main>
        <Hero />
        <Features />
        <Pillars />
        <Protocol />
        <ServicesGrid />
        <TrustSignals />
        <ContactForm />
      </main>
      <Footer />
    </div>
  )
}
```

---

## Hero skeleton (substitute imagery + copy)

```jsx
function Hero() {
  const ref = useRef(null)
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from('.hero-line-1', { y: 40, opacity: 0, duration: 1, delay: 0.3, ease: 'power3.out' })
      gsap.from('.hero-line-2', { y: 60, opacity: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' })
      gsap.from('.hero-cta, .hero-meta', { y: 24, opacity: 0, duration: 0.8, delay: 0.8, stagger: 0.12, ease: 'power3.out' })
    }, ref)
    return () => ctx.revert()
  }, [])
  return (
    <section id="home" ref={ref} className="relative min-h-[100dvh] overflow-hidden">
      <img src="<UNSPLASH_HERO_URL>" alt="" className="absolute inset-0 h-full w-full object-cover brightness-[0.55]" />
      <div className="absolute inset-0 bg-gradient-to-br from-deep/80 via-deep/40 to-deep/70" />
      <div className="absolute inset-x-0 bottom-0 h-64 bg-gradient-to-t from-deep to-transparent" />
      {/* themed floating particles top-right (3-5 dots with animate-float and staggered delays) */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 sm:px-10 lg:px-16 pt-32 pb-20 min-h-[100dvh] flex flex-col justify-end">
        <p className="hero-meta font-mono text-xs uppercase tracking-[0.25em] text-white/70 mb-6">
          <ESTABLISHED_LABEL>
        </p>
        <h1 className="font-display text-5xl sm:text-7xl lg:text-8xl font-bold text-white tracking-tighter leading-[0.95] max-w-5xl">
          <span className="hero-line-1 block"><HEADLINE_LINE_1></span>
          <span className="hero-line-2 block font-serif italic font-medium"><HEADLINE_LINE_2></span>
        </h1>
        <p className="hero-meta mt-8 max-w-xl text-white/70 text-base sm:text-lg leading-relaxed">
          <HERO_SUBTEXT>
        </p>
        <div className="hero-cta mt-10 flex flex-wrap gap-3">
          <a href="#contact" className="magnetic-btn inline-flex items-center gap-2 bg-primary text-white px-6 py-3 rounded-full font-semibold shadow-lg shadow-primary/30">
            <CTA_PRIMARY> <ArrowUpRight className="h-4 w-4" />
          </a>
          <a href="tel:<PHONE_TEL>" className="magnetic-btn inline-flex items-center gap-2 glass-dark text-white px-6 py-3 rounded-full font-semibold border border-white/15">
            <Phone className="h-4 w-4" /> <PHONE_DISPLAY>
          </a>
        </div>
      </div>
    </section>
  )
}
```

---

## ContactForm state machine

```jsx
const [status, setStatus] = useState('idle') // 'idle' | 'sending' | 'sent'
const onSubmit = (e) => {
  e.preventDefault()
  setStatus('sending')
  setTimeout(() => setStatus('sent'), 1200)
}
```

Sent state renders centered `CheckCircle2` card with thanks message.

---

## Drag-drop file zone

```jsx
const [files, setFiles] = useState([])
const onDrop = (e) => {
  e.preventDefault()
  const list = [...e.dataTransfer.files].filter(f => f.type.startsWith('image/')).slice(0, 5 - files.length)
  setFiles(prev => [...prev, ...list])
}
// <div onDragOver={e => e.preventDefault()} onDrop={onDrop} ...>
```

---

## When unclear

Open the reference markup directly:
- Navbar mobile menu → `App.jsx` lines 143–188
- Hero scroll indicator → ~lines 280–300
- HeatingShuffler → lines 305–367
- MaintenanceRain (water drops) → lines 372–590 (paste verbatim then re-skin)
- RenovationScheduler → lines 595–688
- Protocol sticky stack → lines 990–1125
- ContactForm full → lines 1392–1627
- Footer → lines 1649–1769

Copy structure, replace copy.
