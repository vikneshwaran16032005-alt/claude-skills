# Animations

The reference combines GSAP (scroll-driven, stagger reveals), CSS keyframes (continuous loops), and IntersectionObserver (one-shot counters). Use all three.

## GSAP setup

At top of `App.jsx`:
```js
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)
```

Inside `App`, after mount:
```js
useEffect(() => {
  const id = setTimeout(() => ScrollTrigger.refresh(), 200)
  return () => clearTimeout(id)
}, [])
```

## Hero entrance (stagger)

In `Hero` component's `useEffect`:
```js
const ctx = gsap.context(() => {
  gsap.from('.hero-line-1', { y: 40, opacity: 0, duration: 1, delay: 0.3, ease: 'power3.out' })
  gsap.from('.hero-line-2', { y: 60, opacity: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' })
  gsap.from('.hero-cta, .hero-meta', { y: 24, opacity: 0, duration: 0.8, delay: 0.8, stagger: 0.12, ease: 'power3.out' })
}, heroRef)
return () => ctx.revert()
```

## Feature cards reveal

```js
gsap.from('.feature-card', {
  scrollTrigger: { trigger: sectionRef.current, start: 'top 80%', once: true },
  y: 40, opacity: 0, duration: 0.8, stagger: 0.15, ease: 'power3.out',
})
```

## Protocol sticky stack (scrub)

For each card except the last:
```js
gsap.to(card, {
  scrollTrigger: {
    trigger: card,
    start: 'top top+=100',
    end: '+=500',
    scrub: 1,
  },
  scale: 0.92,
  filter: 'blur(6px) saturate(0.7)',
  opacity: 0.5,
  ease: 'none',
})
```

Each card is `position: sticky; top: 6rem` inside a tall parent (`min-height: 300vh` for 3 cards).

## CountUp component (IntersectionObserver + RAF)

```jsx
function CountUp({ end, suffix = '', duration = 2000 }) {
  const [value, setValue] = useState(0)
  const ref = useRef(null)
  const started = useRef(false)

  useEffect(() => {
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !started.current) {
        started.current = true
        const startTs = performance.now()
        const tick = (now) => {
          const t = Math.min(1, (now - startTs) / duration)
          const eased = 1 - Math.pow(1 - t, 3)
          setValue(Math.round(end * eased))
          if (t < 1) requestAnimationFrame(tick)
        }
        requestAnimationFrame(tick)
      }
    }, { threshold: 0.4 })
    if (ref.current) obs.observe(ref.current)
    return () => obs.disconnect()
  }, [end, duration])

  return <span ref={ref} className="tabular-nums">{value}{suffix}</span>
}
```

## CSS keyframes (place in inline `<style>` blocks inside the component that uses them)

### Signature falling particles (rename per industry but keep same animation)
```css
@keyframes rain-fall {
  0%   { transform: translate(-50%, -10px); opacity: 0; }
  12%  { opacity: 1; }
  82%  { opacity: 1; }
  100% { transform: translate(-50%, 95px); opacity: 0; }
}
@keyframes rain-ripple {
  0%   { transform: translateX(-50%) scale(0.4); opacity: 0.9; }
  80%  { transform: translateX(-50%) scale(3.5); opacity: 0; }
  100% { transform: translateX(-50%) scale(3.5); opacity: 0; }
}
@keyframes rain-fadein {
  from { opacity: 0; transform: translateY(2px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Pillar sweep (under big numbers)
```css
@keyframes pillar-sweep {
  0%   { transform: translateX(-100%); }
  50%  { transform: translateX(100%); }
  100% { transform: translateX(100%); }
}
```
Apply to a thin gradient line: `bg-gradient-to-r from-transparent via-primary to-transparent h-px` with `animation: pillar-sweep 3s ease-in-out infinite`.

### Ring pulse (status dots)
```css
@keyframes ring-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(133,196,235,0.6); }
  70%  { box-shadow: 0 0 0 14px rgba(133,196,235,0); }
  100% { box-shadow: 0 0 0 0 rgba(133,196,235,0); }
}
```

### Float (hero particles)
Already in tailwind config as `animate-float`. 6s ease-in-out infinite, ±8px y.

## Signature-animation component anatomy

Whatever the industry, the component is a 176px-tall rounded box (`h-44 rounded-3xl`) with:
1. **Background gradient** matching the theme (sky-blue for water; warm gradient for electrical; etc.)
2. **Atmospheric blur blobs** (2–3 absolutely positioned blurred circles, white/60)
3. **Source element** (pipe for water; conduit for electrical; oven rack for bakery — placed top region as SVG)
4. **Falling particle field** — 7 SVG particles with random `left%`, staggered `animationDelay`, varied size, `rain-fall` animation
5. **Surface line** (water surface; ground line; counter) — wavy SVG path at bottom
6. **Ripples** (3 circles on surface) using `rain-ripple`
7. **Header strip** (top): mono eyebrow label + count
8. **Footer strip** (bottom): status dot + cycling status text (state cycles every ~2.3s)
9. **Inline `<style>` tag** with the three keyframes above

Reuse all 9 structural elements; only re-skin shape, colors, and text labels.

## Reduce-motion

At top of App, gate animations:
```js
const prefersReducedMotion = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
```
Skip GSAP timelines if true; CSS keyframes will still run but should be subtle.
