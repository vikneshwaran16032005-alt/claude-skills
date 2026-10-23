# Winning template — verbatim source

Source: Instantly campaign `b15ef693-caf5-4dbf-95a3-d90a7420f8cb` ("Dentist").
Performance: 45 replies / 278 leads (~16% reply rate) over 962 emails sent.

Use this as the literal structural exemplar. Mimic the rhythm, line breaks, sentence length, and CTA shape. Translate the *pattern*, not the words.

---

## Email 1 — pre-delay 3 days

**Subject:** `{{companyName}} ` *(note trailing space)*

```html
<div>Jeg tænkte på at ringe til jeres klinik i frokostpausen og efter lukketid, men ville lige skrive først.</div>
<div><br /></div>
<div>Jeg tænkte at i sikkert går glip af 4-5 bookinger om dagen imens i ikke er ved telefonen. <strong><br /></strong><br /></div>
<div>Hvis de opkald i stedet blev besvaret med det samme og patienterne fik booket en tid - ville det hjælpe?</div>
<div><br /></div>
<div>Jeg har lavet et eksempel der viser hvordan det kan se ud. </div>
<div>Ville du have noget imod se den?</div>
```

**Pattern role:** opens with a personal, slightly disarming line ("I was going to call but figured I'd write first"). States a specific, quantified pain hypothesis. Asks a soft permission CTA tied to a concrete artifact.

---

## Email 2 — delay 3 days

**Subject:** *(empty — threaded reply)*

```html
<div>Hej, er der andre hos {{companyName}} jeg burde sende det her til?</div>
```

**Pattern role:** the "wrong person?" bump. Single line. Reopens the thread without restating the pitch.

---

## Email 3 — delay 4 days

**Subject:** `Mistet omsætning beregner` *(the asset name)*

```html
<div>Jeg har lavet en "mistet omsætning beregning" hvor jeg har sat tallene op specifikt for jeres klinik og mistede telefonopkald.</div>
<div><br /></div>
<div>Skal jeg sende den over?</div>
```

**Pattern role:** offers a tangible, name-droppable asset that quantifies the pain. The subject *is* the asset name. Two short lines + one-line CTA.

---

## Email 4 — delay 1 day

**Subject:** *(empty)*

```html
<div>Jeg havde lige lidt tid til at skrive til jer. </div>
<div><br /></div>
<div>Har i haft mulighed for at se min besked ovenover?</div>
```

**Pattern role:** quick, casual polite bump. References the previous email without repeating the offer.

---

## Email 5 — delay 4 days

**Subject:** *(empty)*

```html
<div>Den tandlæge i området med flest stjerne på google er tit dem der får de fleste kunder.</div>
<div><br /></div>
<div>Hvis vi kunne få flere patienter til at lave anmeldelses, ville det hælpe klinikken?</div>
<div>Må jeg vise jer hvordan det fungerer?</div>
```

**Pattern role:** pivots to a *different* angle (social proof / reviews instead of missed calls). One observation, one soft question CTA, one "may I show you" close.

---

## Structural summary (do not deviate)

- 5 steps, delays `3 / 3 / 4 / 1 / 4` days.
- Subjects: `{{companyName}} ` / empty / `<asset name>` / empty / empty.
- Every email ends on a soft question CTA.
- HTML only uses `<div>`, `<br />`, and sparingly `<strong>`.
- No links, no images, no signature, no first-name personalization.
- `{{companyName}}` appears in emails 1 and 2.
