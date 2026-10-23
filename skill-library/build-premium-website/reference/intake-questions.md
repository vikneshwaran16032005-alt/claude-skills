# Intake Questions

Use `AskUserQuestion` in batches. Below are the recommended question rounds. Pre-fill from `$ARGUMENTS` and skip what's already known.

## Round 1 — Company basics

**Question 1**: "What is the company name?" (free text — use Other field)
**Question 2**: "What industry / what does the business do?" — single-select, header "Industry":
- Plumbing / water
- Electrical
- HVAC / heating
- Bakery / food
- Fitness / wellness
- Tech / SaaS
- Landscaping / garden
- Auto / mechanic
- Finance / accounting
- Beauty / spa
- Real estate
- Construction
- (Other will be available automatically)

## Round 2 — Style & tone

**Question 1**: "What tone fits the brand?" — single-select, header "Tone":
- Premium-technical (sleek, precise — the bundled reference tone)
- Friendly-local (warm, approachable, community)
- Luxury-minimal (sparse, elegant, high-end)
- Bold-modern (high-contrast, confident, energetic)
- Warm-artisanal (handcrafted, textured, story-led)

**Question 2**: "Brand color direction?" — single-select, header "Colors":
- Use industry default (recommended — auto-pick from `industry-themes.md`)
- Cool blue + coral (the reference palette)
- Forest green + rust
- Charcoal + safety-orange
- Navy + gold
- Rose + champagne
- (Other — user supplies hex codes)

**Question 3**: "Site language?" — single-select, header "Language":
- English (recommended)
- Danish
- Spanish
- German
- French

## Round 3 — Services

Ask in free text via Other: "List 4–8 services with a one-line description each (one per line)."

If the user is brief, generate a reasonable list yourself based on the industry. Map each to a lucide-react icon:

| Industry | Suggested icons |
|---|---|
| Plumbing | Droplets, Wrench, Flame, Bath, Hammer, ChefHat |
| Electrical | Zap, Plug, Lightbulb, Cable, Power, ShieldCheck |
| HVAC | Flame, Snowflake, Wind, Thermometer, Fan, Home |
| Bakery | ChefHat, Wheat, Croissant, Cookie, Cake, Coffee |
| Fitness | Dumbbell, HeartPulse, Activity, Bike, Trophy, Timer |
| Tech/SaaS | Code, Cpu, Cloud, Database, GitBranch, Terminal |
| Landscaping | Trees, Leaf, Sprout, Sun, Flower, Shovel |
| Auto | Car, Wrench, Gauge, Battery, Cog, Fuel |
| Finance | Wallet, TrendingUp, PiggyBank, Receipt, LineChart, Calculator |
| Beauty | Sparkles, Scissors, Flower2, Gem, Heart, SprayCan |
| Real estate | Home, Key, MapPin, Building, Sofa, Bed |
| Construction | Hammer, HardHat, Ruler, Construction, Drill, Truck |

## Round 4 — Trust + contact

**Question 1**: "Years in business / certifications / memberships?" (Other — free text)
**Question 2**: "Contact info — phone, email, city/region, hours?" (Other — free text)
**Question 3**: "Hero image direction (Unsplash search terms)?" — single-select, header "Hero":
- Auto-pick from industry (recommended)
- Workshop / behind-the-scenes
- Finished result / portfolio shot
- People / team at work
- Abstract / textural

## Defaults when user is brief

If `$ARGUMENTS` says e.g. "acme bakery" and user gives one-word answers, fall back to:
- Tone: warm-artisanal
- Colors: cream + amber + espresso
- Language: English
- Services: invent 6 sensible bakery services
- Trust: "Family-owned since [year]", "Locally sourced", "Open 7 days"
- Hero: "artisan bakery sourdough bread golden hour"

Never block on intake — the user said "work without stopping for clarifying questions" when this skill was created. Make the call and continue.
