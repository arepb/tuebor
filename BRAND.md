# Tuebor Brand Style Guide

*An honor-pledge commitment by the people who really love Michigan.*

This guide is the source of truth for Tuebor's visual identity. The tone is **bold, editorial, monotone with a single disciplined accent** — inspired by Michigan's state flag and tuned for the web.

---

## 1. Voice & Tone

- **Confident, plain-spoken, a little dry.** Michiganders don't oversell.
- **Civic, not corporate.** This is an honor pledge, not a product.
- **Short sentences. Strong verbs.** "I will defend." "Invest in Michigan." "Do it again next year."
- Avoid hype, avoid jargon, avoid exclamation points. The wordmark does the shouting.

### Brand one-liner
> An honor-pledge commitment *(for people who really love Michigan)* to invest in one State of Michigan-based business per year.

### Supporting lines
- *Tuebor* — Latin: "I will defend." The word on Michigan's state flag.
- "Michigan's next sports team."
- "Not investment advice, just a lifelong commitment."

---

## 2. Color

Colors derive from the Michigan state flag (blue field, buckskin accents).

| Token          | Hex       | Role                                                   |
| -------------- | --------- | ------------------------------------------------------ |
| `--blue`       | `#0055A4` | Primary. Hero, brand color, links on light backgrounds.|
| `--blue-dark`  | `#003E79` | Hover / pressed states for primary.                    |
| `--ink`        | `#0A0A0A` | Text, dark sections, rules.                            |
| `--paper`      | `#F4F1EA` | Default page background — warm off-white.              |
| `--paper-2`    | `#ECE8DE` | Secondary surface (pull-quote block, subtle contrast). |
| `--tan`        | `#C4A15E` | **Single accent.** Michigan-flag buckskin. Footer field, period after wordmark, parenthetical highlights. Use sparingly. |
| `--tan-dark`   | `#8A6F3A` | Tan hover / secondary depth.                           |
| `--line`       | `rgba(10,10,10,0.12)` | Hairlines, dividers on paper.               |
| `--muted`      | `rgba(10,10,10,0.55)` | Secondary text on paper.                    |

### Palette rules
- **One accent at a time.** Tan is the *only* non-blue/ink/paper color. Don't introduce greens, reds, or additional hues.
- **Blue is for structure, tan is for warmth.** Use tan in small doses — a period, a phrase, a footer field.
- **Text on blue:** white, with `rgba(255,255,255,0.7)` for eyebrow / secondary. Never use tan as body text on blue (contrast issue).
- **Never tint photography with blue filters beyond the existing halftone portraits.**

---

## 3. Typography

### Type stack

| Token       | Family                                                  | Used for |
| ----------- | ------------------------------------------------------- | -------- |
| `--display` | **BidenBold**, Times New Roman, Georgia, serif          | Wordmark, H1–H3, pull quotes, section heads |
| `--sans`    | `ui-sans-serif`, system-ui, -apple-system, Helvetica Neue | Body copy, paragraphs, UI text |
| `--mono`    | `ui-monospace`, SFMono-Regular, Menlo, Consolas         | Eyebrows, labels, nav, button text, footer metadata |

**BidenBold** is a proprietary display face — condensed, geometric, heavy. It carries the editorial character of the brand. Do not substitute.

### Scale (clamp-based, fluid)

| Use              | Size                                |
| ---------------- | ----------------------------------- |
| Hero wordmark    | `clamp(96px, 22vw, 360px)` — the brand mark |
| Page H1          | `clamp(52px, 10vw, 140px)`          |
| Section H2       | `clamp(40px, 6.5vw, 96px)`          |
| Step / card H3   | `clamp(28px, 4vw, 48px)`            |
| Q&A H3           | `clamp(22px, 2.6vw, 32px)`          |
| Hero tagline     | `clamp(22px, 2.4vw, 30px)` *(25px floor on mobile)* |
| Body             | 17px base / 18px in `.prose`        |
| Eyebrow / label  | 12–13px mono, uppercase, `0.1em`–`0.12em` tracking |

### Typographic rules
- **Line-height is tight on display** (0.85–1.1), generous on body (1.55–1.65).
- **Letter-spacing:** negative on display (`-0.01em` to `-0.03em`), positive on mono labels (`+0.08em` to `+0.12em`).
- Body copy maxes out at **70ch** for readability; prose container at **780px**.
- Never bold body sans (use display font for emphasis).
- Italics are reserved for the *Tuebor* name and the "I will defend" motto.

---

## 4. Layout & Grid

- **Max width:** 1400px.
- **Page padding:** `clamp(20px, 4vw, 56px)` — fluid edge gutter used sitewide.
- **Section vertical rhythm:** `clamp(56px, 9vw, 140px)` top/bottom on slabs; `clamp(32px, 5vw, 56px)` between headline and content.
- **Two-column patterns** (Q&A, section heads, founders) use a fixed `80px` index column + `1fr` text column with `clamp(16px, 3vw, 40px)` gap.
- Grids collapse to single column **at 720px**.
- **Hairline dividers** (`1px` `--line`) separate slabs and Q&A rows. Never use heavier borders.

---

## 5. Components

### Wordmark
- Set in BidenBold. Always includes the **tan period** (`.`) as a subtle flag-reference.
- On the home hero, the giant wordmark *is* the brand mark; the small header wordmark only appears after scrolling past the hero.
- Don't lock the wordmark inside a box or add a tagline beside it.

### Buttons
- Mono, uppercase, `0.12em` tracking, 13px text, square corners (no radius).
- 1px border, 16px/26px padding.
- **Primary:** filled blue on paper, filled white on blue.
- **Secondary:** outlined in current color.
- Arrow glyph is sans (`→`) to contrast with the mono label.
- On mobile <600px, CTAs become full-width with the arrow pushed to the right edge.

### Eyebrow row
- Mono, uppercase, 13px, `0.1em` tracking.
- On paper: `--muted`. On blue: `rgba(255,255,255,0.7)`.
- Stacks vertically under 600px.

### Sections
- `.slab` — default paper surface.
- `.slab.dark` — ink background, paper text (used for "Pledge" / steps).
- `.slab.blue` — blue background, white text (used for "Join" / CTA).

### Footer
- Tan (`--tan`) surface — the brand's one moment of full warmth.
- Giant blue wordmark, mono labels, 4-column grid collapsing to 2 → 1.
- Closing line: *Not investment advice, just a lifelong commitment.*

### Founder portraits
- Blue halftone dot-pattern processing. Don't substitute with full-color photos.
- Two-column on desktop, single-column on mobile.
- Caption stacks vertically: **name** → LinkedIn → email.

---

## 6. Motion

Motion is minimal and editorial, never flashy.

- **Hero → header wordmark crossfade** on scroll (400–500ms, `cubic-bezier(.2,.8,.2,1)`).
- **Background color transition** on home: blue hero → paper (240ms ease).
- **Hover states:** 120ms background/color transitions on buttons and links.
- **Marquee** of Michigan companies: 40s linear infinite.
- No parallax, no animated illustrations, no Lottie.

---

## 7. Imagery

- **Halftone portraits** in `--blue` for founders and key figures.
- **Michigan state flag** may appear as a supporting graphic.
- Photography should feel **documentary and civic**, not corporate stock.
- Never overlay blue gradients on photos; never use drop shadows.

---

## 8. Writing conventions

- **Tuebor** is always capitalized; *Tuebor* is italicized when used as the Latin word.
- Use **non-breaking hyphens** in compound brand phrases so they don't line-break awkwardly: "honor‑pledge," "Michigan‑based."
- Em dashes are flush with words, no spaces: `Michigan—founders`.
- Money: `$10`, `$1,000,000` (no "USD").
- Years: `1837`, `2023`. Dates: spell out months.
- URLs in copy are lowercase.

---

## 9. Accessibility

- Text on blue (`#0055A4`) is always pure white — passes AA at 15px and above.
- Tan (`#C4A15E`) on blue is for **decorative accents only**, not legible body copy.
- Focus states: inherit the existing link/button hover styles; don't remove outlines.
- Respect `prefers-reduced-motion` for scroll-tied transitions (TODO: not yet wired).

---

## 10. Do / Don't

**Do**
- Let the wordmark breathe.
- Keep color to blue + paper + one tan accent.
- Set display type tight and body type open.
- Write short. Cut adjectives.

**Don't**
- Don't introduce a second accent color.
- Don't round the corners of buttons or cards.
- Don't mix more than two typefaces per surface (display + mono, or display + sans).
- Don't add drop shadows, glows, or gradients.
- Don't use stock photography.

---

## 11. Files & tokens

- **Live tokens:** `assets/css/style.scss` (`:root` custom properties).
- **Fonts:** `assets/fonts/BidenBold-Regular.otf`.
- **Social preview:** `assets/images/og-image.png` (1200×630 PNG — never SVG).
- **Favicons:** `assets/images/apple-touch-icon.png`, `favicon.ico`.

When in doubt, grep `--blue`, `--tan`, `--display` to see how the token is already used before introducing a new pattern.
