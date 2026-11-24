# Vanderbilt brand system

The series uses the Vanderbilt identity. Everything below already exists in
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

## Vanderbilt identity (required on everything)

Every course page, slide deck, landing page and demo carries the real
Vanderbilt University lockup. Never draw, retype or recolor the logo; use the
bundled PNGs. Vanderbilt is the only name on the page as the maker. Never
credit Futures Learning, FLH or Futures Learning Hub as the maker, owner,
publisher or brand, in visible text or in `<title>`, meta tags, alt text,
`aria-label`s or the copyright line.

**Header lockup.** The top bar opens with the logo, a 1px gold divider, then
the program or course name in Antonio, gold, all caps:

```html
<a class="logo" href="#top" aria-label="Vanderbilt University, <Course> home">
  <img src="assets/img/vu-lockup-white.png" alt="Vanderbilt University" width="166" height="43">
  <span class="lockup-div" aria-hidden="true"></span>
  <span class="lockup-name"><Program or course name></span>
</a>
```

```css
.logo{ display:flex; align-items:center; gap:14px; min-width:0; text-decoration:none; }
.logo img{ height:48px; width:auto; display:block; flex:none; }   /* 30px in a compact toolbar */
.lockup-div{ width:1px; align-self:stretch; min-height:22px; background:var(--vu-oak); flex:none; }
.lockup-name{ font-family:var(--cond); font-weight:700; font-size:.95rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--vu-gold); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; min-width:0; }
@media (max-width:520px){ .lockup-div, .lockup-name{ display:none; } }
```

**Hero eyebrow.** `Vanderbilt University &middot; <Program or course name>`.

**Footer.** The stacked lockup (`vu-centered-white.png`, about 100px wide) and
`&copy; <year> Vanderbilt University.` beside the accessibility statement.

**Slide decks.** The lockup sits in the presenter toolbar, on the title slide
(white lockup on a dark slide) and on the closing slide (black lockup on a
light slide). In a narrow reflowed toolbar, swap to `vu-v-icon-nav.png`.

**Light grounds** take `vu-lockup-black.png` / `vu-centered-black.png`.

## Bundled assets

The skill bundles the brand assets in its own `assets/` directory in case no
sibling course repo is available to clone from:

- `assets/img/` - `vu-lockup-white.png` / `vu-lockup-black.png` (horizontal wordmark, nav and footer), `vu-centered-white.png` / `vu-centered-black.png` (stacked lockup), `vu-v-icon.png` / `vu-v-icon-nav.png` (the gold V mark), `favicon.svg` / `favicon-96.png`.
- `assets/fonts/` - the seven self-hosted woff2 files: Libre Caslon Display 400, Libre Caslon Text 400 + italic, Inter 400/500/600, Antonio 700.

Copy them into a new course's `assets/img/` and `assets/fonts/` unchanged.
Cloning a sibling course repo already brings identical copies, so prefer
that; the bundle is the fallback.
