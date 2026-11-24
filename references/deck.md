# Horizontal deck navigation

Courses advance left to right, one full-viewport slide at a time, matching
the Working Smarter UI. The engine already exists in every course's CSS/JS;
this file documents the contract so edits do not break it.

## CSS contract

```css
html, body { height: 100%; }
body { overflow: hidden; }                       /* the page never scrolls; the deck does */
.deck { display: flex; flex-direction: row; overflow-x: auto; overflow-y: hidden;
  scroll-snap-type: x mandatory; height: 100dvh; scrollbar-width: none; }
.slide { flex: 0 0 100vw; height: 100dvh; overflow-y: auto; overflow-x: hidden;
  scroll-snap-align: start; scroll-snap-stop: always;
  padding: calc(var(--nav-h) + …) 0 calc(56px + …); }   /* clears top nav and bottom bar */
.slide > .wrap { margin-top: auto; margin-bottom: auto; }  /* vertical centering when content fits */
```

Key trap: the slide itself must keep `overflow-y: auto` so tall content can
scroll vertically inside the slide. Any override to `overflow: visible`
(facilitator CSS once did this) silently kills internal scrolling.

## JS contract (in `assets/js/main.js`)

- `goTo(i)` scrolls with `scrollIntoView({ inline: 'start' })`.
- Reveal-on-view checks use horizontal geometry: `r.left < innerWidth && r.right > 0`.
- The deck's `scroll` event drives the top progress bar (`deck.scrollLeft`) and toggles `nav.scrolled`.
- Anchor links (`a[href^="#"]`) jump the deck to the target slide instead of native anchor scrolling.
- **Wheel advance**: vertical wheel on a slide that is already at its bottom (or fits) advances to the next slide; wheel at the top goes back. Guarded by a ~900ms `wheelLock` and a deltaY threshold (~24) so slide-internal scrolling still feels normal.
- **New-tab pass**: every `a[href]` whose href does not start with `#` gets `target="_blank" rel="noopener"`.

## Bottom bar

Fixed 56px bar: section title left (`#barTitle`, Antonio gold, updated in
`setActive`), snap dots center (hidden under 900px), `current / total` count
plus square bordered prev/next buttons right. `.deckbar { display: none; }`
retires the old floating arrows.

## Scroll-for-more hint

`.scrollhint` is a fixed gold pill above the bottom bar, shown only when the
active slide overflows: `slide.scrollHeight - slide.clientHeight > 56` and the
slide is not scrolled to its end. It pulses (disabled under reduced motion)
and clicking it scrolls the slide down. Re-check on slide change and on
slide scroll.

## Fitting content on screen

The standing goal is all or most content visible without scrolling at
1440x900. Techniques that worked: clamp() font sizes down on dense slides,
two-column grids instead of stacks, trim lead paragraphs, and compact the
closing footer. When a slide genuinely needs more room, let it scroll and
rely on the hint; never shrink text below readable sizes to force a fit.

## Top nav

`.nav` keeps a solid near-black background on every slide:
`background: rgba(20,20,20,.97); border-bottom: 1px solid rgba(207,174,112,.18);`.
