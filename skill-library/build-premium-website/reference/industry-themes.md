# Industry → Signature Animation Themes

Match the user's industry to one of these signature animations. Each reuses the same structural pattern (h-44 rounded box, header eyebrow, falling-particle field, surface line, ripples, cycling status) but re-skins the SVG shapes, source element, gradient, and colors.

If no exact match, pick the closest analog or combine elements.

---

## Plumbing / water / cleaning (DEFAULT)
- **Source:** SVG pipe with valve caps (lines 456–474 of reference)
- **Particle:** Teardrop `M12 2 C 9 9, 4 17, 4 24 a 8 8 0 0 0 16 0 C 20 17, 15 9, 12 2 Z` with vertical gradient (primary-light → primary → primary-dark) + white highlight ellipse
- **Surface:** Two wavy SVG paths (quadratic curves)
- **Ripples:** Circles with expanding scale
- **Gradient bg:** `linear-gradient(180deg, #F0F8FC 0%, #E2EEF6 70%, #D6E8F2 100%)`
- **Status labels:** "Stable", "Leak detected", "Tech on the way", "Fixed"

## Electrical / electricians
- **Source:** Horizontal cable/conduit SVG with junction boxes
- **Particle:** Lightning bolt path `M13 2 L4 14 H11 L9 22 L20 10 H13 L13 2 Z` with cyan→yellow gradient + white core glow
- **Surface:** Sine-wave AC line
- **Ripples:** Tiny arc flashes (semicircles fading out)
- **Gradient bg:** `linear-gradient(180deg, #FFFBE6 0%, #FFE9A8 70%, #FFD86B 100%)`
- **Status labels:** "Stable load", "Surge detected", "Inspecting circuit", "Safe"

## HVAC / heating / cooling
- **Source:** Vent grille SVG (rounded slots)
- **Particle:** Snowflake `<path>` for cooling OR flame teardrop for heating; six-point snowflake works well
- **Surface:** Thermometer scale tick marks
- **Ripples:** Concentric heat waves (or chill rings)
- **Gradient bg cool:** `linear-gradient(180deg, #E8F4FF 0%, #C9E2F5 100%)`
- **Gradient bg warm:** `linear-gradient(180deg, #FFF1E0 0%, #FFD6A5 100%)`
- **Status labels:** "21.5° steady", "Boost requested", "Calibrating", "Comfortable"

## Bakery / café / food
- **Source:** Oven rack SVG (horizontal slats) or rolling pin
- **Particle:** Round dough drop with warm amber gradient OR flour mote (small circle, white/cream)
- **Surface:** Counter line with subtle wood grain (parallel strokes)
- **Ripples:** Steam wisps (small circles fading up not out)
- **Gradient bg:** `linear-gradient(180deg, #FFF6E8 0%, #F2DDB5 70%, #E5C28A 100%)`
- **Status labels:** "Baking now", "Fresh batch", "Cooling rack", "Ready"

## Fitness / wellness / gym
- **Source:** Heart rate monitor bar at top
- **Particle:** Pulse ring (expanding circle outline) OR heartbeat dot
- **Surface:** ECG line (SVG zigzag)
- **Ripples:** Concentric pulse rings
- **Gradient bg:** `linear-gradient(180deg, #FFF0F2 0%, #FFD3D8 70%, #FFB5BC 100%)`
- **Status labels:** "Resting", "Active session", "Peak zone", "Recovering"

## Tech / SaaS / software
- **Source:** Server rack SVG (horizontal slots with LEDs)
- **Particle:** Code bracket `< />` or scanning dot
- **Surface:** Terminal cursor line
- **Ripples:** Scan-line sweeps (horizontal bars)
- **Gradient bg:** `linear-gradient(180deg, #ECEAFF 0%, #C9C3FF 70%, #9D93FF 100%)`
- **Status labels:** "All systems nominal", "Deploying", "Tests passing", "Shipped"

## Landscaping / garden / outdoor
- **Source:** Tree branch SVG (horizontal limb with leaves)
- **Particle:** Leaf path (oval with central vein) rotating slightly as it falls
- **Surface:** Grass line (small upward triangles)
- **Ripples:** Soil ripple OR small flowers blooming
- **Gradient bg:** `linear-gradient(180deg, #EAF5E1 0%, #C5E4B5 70%, #98C77E 100%)`
- **Status labels:** "Tending", "Pruning", "Planting", "Thriving"

## Auto / mechanic / detailing
- **Source:** Lift bar SVG (auto hoist) or wrench-set rail
- **Particle:** Oil drop (darker teardrop) OR small gear icon (6 teeth, slow rotation)
- **Surface:** Floor line with grid checkers
- **Ripples:** Oil-puddle rings
- **Gradient bg:** `linear-gradient(180deg, #F0F0F2 0%, #D6D6DB 70%, #B8B8C0 100%)`
- **Status labels:** "Diagnostics", "In service", "Test drive", "Ready for pickup"

## Finance / accounting / advisory
- **Source:** Top axis line with tick marks
- **Particle:** Coin (circle with $ or generic) OR ascending bar segment
- **Surface:** Baseline with rising chart line
- **Ripples:** Glow halos behind coins
- **Gradient bg:** `linear-gradient(180deg, #F5F1E8 0%, #E8DDB8 70%, #D4C088 100%)`
- **Status labels:** "Markets stable", "Reviewing", "Strategy updated", "On target"

## Beauty / spa / cosmetics
- **Source:** Vanity bar SVG (with two bulb dots)
- **Particle:** 4-point sparkle SVG with rose-gold gradient OR petal
- **Surface:** Mirror line with subtle shimmer dots
- **Ripples:** Shimmer halos
- **Gradient bg:** `linear-gradient(180deg, #FFF0F0 0%, #FAD6D6 70%, #E8B5B5 100%)`
- **Status labels:** "Booking open", "In treatment", "Refreshing", "Glowing"

## Real estate / property
- **Source:** Roofline SVG (horizontal with peak markers)
- **Particle:** Pin drop OR key icon
- **Surface:** Ground line with property tick marks
- **Ripples:** Map-pin pulses
- **Gradient bg:** `linear-gradient(180deg, #F1F1ED 0%, #D8D4C6 70%, #B8B19D 100%)`
- **Status labels:** "Listing", "Open house", "Offer received", "Closed"

## Construction / general contracting
- **Source:** I-beam SVG (horizontal girder)
- **Particle:** Welding spark (4-point burst) with safety-orange + white
- **Surface:** Foundation line (cross-hatched)
- **Ripples:** Spark scatter
- **Gradient bg:** `linear-gradient(180deg, #F3EFE8 0%, #D9CFBC 70%, #B8A788 100%)`
- **Status labels:** "Surveying", "Building", "Inspecting", "Delivered"

---

## How to re-skin

1. Replace the teardrop `<path d="...">` with the new shape (keep viewBox ~24×36).
2. Update the `<linearGradient>` stops to match the theme palette.
3. Swap the pipe SVG at the top for the new "source" element (cable / oven / branch / etc.).
4. Adjust the bottom surface SVG path.
5. Translate the 4 status strings to the industry's vocabulary.
6. **Keep** the keyframes (`rain-fall`, `rain-ripple`, `rain-fadein`) — they're industry-agnostic.

If the user picked a theme not in this table, invent one following the same 6-step pattern: pick a source, a particle, a surface, ripples, gradient, and 4 status labels that tell a mini-story of the service.
