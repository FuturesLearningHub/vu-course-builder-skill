# FLH brand system

The series uses Vanderbilt's FLH identity. Everything below already exists in
each course's `assets/css/styles.css`; when starting from a cloned sibling
repo you keep it and only write new component styles on top.

## Color tokens (CSS custom properties in `:root`)

```css
--vu-black: #1C1C1C;        /* page background */
--vu-white: #FFFFFF;        /* body text on black */
--vu-gold-flat: #CFAE70;    /* THE accent: eyebrows, borders, pills, active states */
--vu-gold-gradient: linear-gradient(135deg, #FEEEB6 0%, #CFAE70 45%, #B49248 100%);
--vu-cream: #F5F3EF;  --vu-sand: #E0D5C0;
--vu-gray-light: #E4E4E4;  --vu-gray-dark: #777777;
--vu-highlight: #ECB748;  --vu-oak: #946E24;
--vu-sky: #B3C9CD;  --vu-sage: #8BA18E;
```

Gold is an accent, never a field: thin borders `rgba(207,174,112,.2)` to `.45`,
text, small fills at `rgba(207,174,112,.12)`. Surfaces that need separation
from the black use `#141414` (bars) or subtle white alphas.

The traffic-light colors in the AI courses (green / yellow / red cards) are
semantic and sit outside the brand palette; keep them consistent between
AI Basics and AI 201.

## Type stack (self-hosted woff2 in `assets/fonts/`)

- **Headlines**: Libre Caslon Display 400. Every `.h2` headline italicizes exactly one word: `<h2 class="h2">Before the room <em>fills</em>.</h2>`. The `<em>` is Libre Caslon Text italic.
- **Body**: Inter 400/500/600.
- **Eyebrows, labels, bars**: Antonio 700 (`var(--font-condensed)`), uppercase, letter-spacing .08em to .1em, usually gold, sizes .68rem to .8rem.

Eyebrow pattern above each section headline:

```html
<p class="eyebrow">Section name / 03 · Short label</p>
```

## Components you will reuse

- `.wrap` - content column, centered, max-width clamp.
- `.card` grids - bordered panels, 1px `rgba(255,255,255,.14)` borders, gold border on the active or featured card.
- `.pill` / `.skillpill` - small bordered capsules, Antonio, gold border.
- Buttons - bordered, transparent fill, gold hover (`border-color: var(--vu-gold-flat); background: rgba(207,174,112,.12)`), transition 200ms.
- Trainer feedback states - correct answers flash gold, wrong answers shake briefly; both settle within 400ms.

## Motion

All transitions and animations run 400ms or less, eased. Honor
`prefers-reduced-motion: reduce` (kill pulses and smooth scrolling). The hero
montage streams from the Higgsfield CDN with a particle-canvas fallback when
the video cannot load.

## Lockups and bundled assets

Use real Vanderbilt University lockups only (authorized use); the white
wordmark sits in the top nav, and the footer carries the small lockup inside
the closing slide.

The skill bundles the brand assets in its own `assets/` directory in case no
sibling course repo is available to clone from:

- `assets/img/` - `vu-lockup-white.png` / `vu-lockup-black.png` (horizontal wordmark, nav and footer), `vu-centered-white.png` / `vu-centered-black.png` (stacked lockup), `vu-v-icon.png` / `vu-v-icon-nav.png` (the gold V mark), `favicon.svg` / `favicon-96.png`.
- `assets/fonts/` - the seven self-hosted woff2 files: Libre Caslon Display 400, Libre Caslon Text 400 + italic, Inter 400/500/600, Antonio 700.

Copy them into a new course's `assets/img/` and `assets/fonts/` unchanged.
Cloning a sibling course repo already brings identical copies, so prefer
that; the bundle is the fallback.
