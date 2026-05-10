# Tuebor — CLAUDE.md

Michigan investment pledge site. Live at [tuebor.org](https://tuebor.org).  
Repo: `github.com/arepb/tuebor` · Deploys via GitHub Actions → GitHub Pages.

## Stack

- **Jekyll 4.3.x** static site, GitHub Pages (Actions-based deploy)
- `_pledgees/` collection → `/roster/:slug/` URLs
- Plugins: `jekyll-seo-tag`, `jekyll-sitemap`
- Fonts: `BidenBold-Regular.otf` (display), system sans/mono for body
- No JS framework — all vanilla JS in `_includes/`

## Key Files

| File | Role |
|------|------|
| `_config.yml` | Site config, collection definition |
| `BRAND.md` | Full design system — colors, type, components. Read before any visual change. |
| `_pledgees/*.md` | One file per pledgee — front matter drives portrait, card, profile page |
| `_includes/pledgee-card.html` | Trading-card partial used on /roster/ and profile pages |
| `_layouts/pledgee.html` | Full profile page layout |
| `assets/images/_dither.py` | Halftone portrait generator (run locally; outputs go to `assets/images/pledgees/`) |
| `assets/images/pledgees/_sources/` | Raw portrait photos — gitignored, stored locally |
| `backed.md` | /backed/ page — Liquid groups by `company | downcase` |

## Pledgee Front Matter

```yaml
layout: pledgee
name: First Last
last_name: Last           # for sort
slug: first-last          # URL slug + output filename prefix
city: City Name
year_joined: 2023
portrait_source: first-last-source.jpg   # raw photo in _sources/
portrait_face_y: 0.40    # 0..1 vertical center of face in source (default 0.5)
portrait_face_x: 0.50    # 0..1 horizontal center of face in source (default 0.5)
portrait_card_x: 0.0     # CSS object-position X% for 4:5 card crop (omit if 50% is fine)
portrait_scale: 0.70     # <1 = tighter crop around face (default 1.0)
portrait: /assets/images/pledgees/first-last-halftone.png
og_image: /assets/images/pledgees/first-last-og.png
linkedin: https://www.linkedin.com/in/...
quote: "Short quote for pull-quote section."
founder: true            # omit if not a founder
roster_order: 1          # lower = earlier in roster grid
backed:
  - year: 2025
    company: "Company Name"
    url: "https://..."
    public: true
published: true
```

## Portrait Generation (`_dither.py`)

Run: `python assets/images/_dither.py`

Produces `<slug>-halftone.png` (900×900 px, Michigan-blue halftone dots on warm paper).

**Crop geometry:**
- `portrait_face_y` — vertical center of face as fraction of image height (0=top, 1=bottom). Eyes typically at ~0.3–0.4 of image height.
- `portrait_face_x` — horizontal center of face (0=left, 1=right). Default 0.5. Use when face is off-center in source photo.
- `portrait_scale` — fraction of min(w,h) to use as crop side. Smaller = tighter, more zoomed in on the face. Start around 0.6–0.7.

**Card display (4:5 aspect ratio):**  
The roster card renders the 900×900 halftone in a `aspect-ratio: 4/5` container with `object-fit: cover`, clipping ~10% from each horizontal side. If the face is off-center in the halftone, set `portrait_card_x` (0..1) to shift the visible window:
- `0.0` = show leftmost 80% (face shifted right of center in final display)
- `0.5` = default centered crop
- `1.0` = show rightmost 80%

The `portrait_card_x` value drives `object-position: X% 50%` in `_includes/pledgee-card.html`.

**Skip logic:** `_dither.py` skips regeneration if the source mtime ≤ output mtime. Touch the source file or delete the output to force regeneration.

Also generates OG images — check `_dither.py` for the `og_image` pipeline if it exists, or generate separately.

## /backed Page — Company Deduplication

`backed.md` groups by `company | downcase`. If two pledgees back the same company, their entries must use **exactly the same company name** (case-insensitive) to merge into one row. Inconsistent casing (e.g., "Moksa" vs "mokSa.ai") creates duplicate rows.

## Image Alt Text Convention

All pledgee portrait images use: `[Name], Tuebor Michigan investment pledge`  
This is baked into `_includes/pledgee-card.html`. Match this pattern for any new image alt text on the site.

## Adding a New Pledgee

1. Copy `_pledgees/_template.md` → `_pledgees/first-last.md`, fill front matter
2. Drop raw portrait photo in `assets/images/pledgees/_sources/`
3. Run `python assets/images/_dither.py` to generate halftone
4. Generate OG image (900×1080 or 1200×630) and place at `og_image` path
5. Add `backed:` entries — company names must match existing casing for deduplication

## QA

Use `/qa` (gstack) to run a full QA pass against the live site.  
Browse binary: `~/.claude/skills/gstack/browse/dist/browse`  
Screenshot path must be within the worktree or `/private/tmp`.

Key pages to check: `/`, `/origin.html`, `/roster/`, `/backed/`, `/howto.html`, `/howto/makepublic.html`, `/legal-disclaimer.html`, all `/roster/<slug>/` pages.

## Skill Routing

When the user's request matches an available gstack skill, invoke it via the Skill tool.

- QA / test the live site → `/qa`
- Bug / broken layout → `/investigate`
- Visual design audit → `/design-review`
- Browsing / fetching URLs → `/browse`
- Ship / PR / deploy → `/ship`
