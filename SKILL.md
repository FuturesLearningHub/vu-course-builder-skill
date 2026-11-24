---
name: vu-course-builder
description: Build and maintain Vanderbilt FLH Learning Library interactive course sites. Use this whenever the user asks to create a new course, training, workshop, learning module, or classroom experience for the Vanderbilt series, or to edit an existing one (Working Smarter, AI Basics, AI 201, Difficult Conversations, Coaching for Performance, Emotional Intelligence, Presentation & Public Speaking), or mentions the course library, facilitator guides, self-paced editions, FLH brand, the black-and-gold Vanderbilt look, or accessibility of a course site. Covers the full pipeline: the Working Smarter section pattern, copy, interactive modules, classroom and self-paced editions, ATD facilitator runbook, WCAG 2.2 AA accessibility gate, publishing, and the library catalog card.
---

# Vanderbilt FLH Learning Library course builder

Every new course is built to match **Working Smarter**, the reference
implementation. Source: `FuturesLearningHub/FLH-Learning-Library-`, files `learn/index.html`
(self-paced) and `learn/classroom/index.html`. Live at
`https://flh-learning-library.vercel.app/learn/` and mirrored at
`https://futureslearninghub.github.io/FLH-Learning-Library-/learn/`. That file defines the
standard look, the page architecture, the copy voice, and the interaction
vocabulary. When a question about structure or styling comes up, the answer
is whatever Working Smarter does. Read the source, not your memory of it.

Each course is one self-contained HTML file: inline styles, inline scripts,
no framework, no build step, no backend. Assets and fonts live in
`./assets/`.

Two things are non-negotiable on every course this skill produces:

1. **It matches the Working Smarter pattern.** Not a new layout, not a new
   navigation model. See `references/pattern.md`.
2. **It passes WCAG 2.2 Level AA.** Accessibility is a ship gate, not a
   polish pass. See `references/accessibility.md`.
3. **It uses only the approved Vanderbilt palette and type.** Fourteen colors,
   three typefaces, per `brand.vanderbilt.edu`. There is no approved red, so
   state is carried by words and icons. See `references/brand.md`.
4. **It carries the Chancellor's charge.** The `mission` section is required in
   every course, verbatim, with two course-specific slots. See
   `references/mission.md`.

## Starting a new course

Do not scaffold from scratch and do not invent a layout. Clone the Working
Smarter source repo and replace the content. It already carries the shell,
the progress engine, the panel router, the fonts, the brand CSS, the
accessible component patterns, and the classroom / self-paced split.

1. Copy `learn/index.html` from `FuturesLearningHub/FLH-Learning-Library-` as the starting file, along with `assets/`. Keep the `:root` palette, the theme scopes, the pager, the progress engine, and the accessibility helpers intact. Work the `[EDIT]` banner at the top of the file: it lists every placeholder a new course must swap. If the repo is not reachable, this skill's own `assets/` directory carries the lockups, favicons, and all seven brand fonts.
2. Map the course to the section spine in `references/pattern.md`: home / hero, belief, the Chancellor's charge, how the course works, then 4 to 8 numbered teaching sections, then knowledge check, summary, next step, resources.
3. Write the copy section by section. Each section gets a "you are here" line, an eyebrow, a one-italic-word headline, a lead, "The idea", and at least one interactive module.
4. Build the interactive modules from the vocabulary in `references/pattern.md` (flip cards, drills, builders, graders, matchers, self-checks, simulators). Every one has an accessible recipe in `references/accessibility.md`. Do not invent a new interaction without writing its keyboard and screen reader behavior first.
5. Write the classroom-only layer: the instructor how-to, the QR panel, and the gold **Together** cards. The self-paced edition drops them.
6. Drop in the `mission` section from `references/mission.md` and fill its two slots. Do not rewrite the rest of it.
7. Write `facilitator/notes.json` if the course is facilitated (see the runbook reference).
8. Run the accessibility and palette gate. It blocks publish.
9. Publish, then add the library card and syllabus.

## Design system in one paragraph

Vanderbilt FLH brand: black `#1C1C1C`, white, Flat Gold `#CFAE70`, and Oak
`#946E24` where gold cannot survive a white ground. The approved palette is
fourteen colors and nothing else; `#A94438` and `#8C6822` are in the current
source and are both off-brand. Headlines are Libre Caslon with exactly **one
italic word** per headline, ending in a period. Body is Inter. Eyebrows and
labels are Antonio, all caps, tracked at 3%. Motion stays at or under 400ms
and respects `prefers-reduced-motion`. Real VU lockups only. Palette,
typography, theme scopes, and measured ratios: `references/brand.md`.

## Navigation: book mode

A pager regroups the scroll page into `.page` articles at `data-pg` markers,
one visible at a time, routed by `#p/<section>/<n>`. Without JS the scroll
layout stands as the fallback. A sticky top nav carries the lockup, the
section anchors, and a progress readout; a bottom bar carries the section
label, dots, count, and prev/next. Progress is three `localStorage` keys and
nothing else, stated plainly to the learner and resettable from the footer.
Page turns move focus into the incoming page and mark the outgoing one
`aria-hidden`. Full contract, including the `PLAN` array and the
`window.chartPager` API: `references/pattern.md`.

Components read **theme scope** variables (`--tx`, `--eyebrow`, `--focus`,
`--btn-bg`), never the raw brand palette, because sections alternate between
dark and light grounds. Writing `var(--vu-gold)` into a component breaks it
the moment it lands in a light section.

## Copy rules (do not regress)

- **Zero em or en dashes anywhere**: HTML, JS strings, JSON, worksheets. Rewrite around them; grep before shipping.
- Human-sounding, warm, direct. Avoid negative parallelisms ("not X, but Y"), rule-of-three stacks, and arrow chains. If it sounds like marketing filler, cut it.
- Match register to audience. Working Smarter assumes a working professional who has never used AI seriously; explain every term the first time and put it in the glossary.
- Every teaching module has a play moment. Reading is not a module.
- Every efficiency or impact claim carries a cited, linked source, named author and year.
- Section transitions end on one italicized word.
- Links open in a new tab (the engine adds `target="_blank" rel="noopener"` to non-hash links).
- The AI courses share one data rule and it must never be contradicted: sensitive data goes to Amplify or Copilot on a Vanderbilt account, ChatGPT EDU is approved to a lower level, and children's information goes into no tool at all.
- Plain-language glossary at the end, one line per term, covering every technical word the course used.

## Learning architecture

Bloom's-verb objectives on the hero, Kirkpatrick L1/L2/L3 evaluation (rating
plus open comment, the scored knowledge check, and a committed next step),
and an ATD-style facilitator runbook with Say / Do / Ask / Debrief /
Transition per section. Facilitated courses carry two timed paths (Full and
Core) whose per-section minutes **must sum exactly** to the advertised
lengths. Schema and timing rules: `references/facilitator.md`.

## Accessibility gate (blocks publish)

No course ships until all of these pass. Details, component recipes, and the
scripts are in `references/accessibility.md`.

1. `node tools/a11y-audit.mjs` reports zero critical and zero serious axe violations across every section and panel, at 1440x900 and at 320px wide.
2. `python3 tools/contrast-check.py` reports no raw-palette text usage and no scoped pairing under 4.5:1, in both theme scopes.
3. Keyboard-only pass: every control reachable and operable, visible focus everywhere, no traps, panel changes move focus, skip link works.
4. Screen reader pass on one flow per interaction type: results and feedback announce, state changes announce, nothing important is silent.
5. Reduced-motion pass: marquees, pulses, flips, and smooth scrolling all stop.
6. Zoom and reflow: 200% zoom and 320px width with no horizontal scrolling and no clipped content.
7. Every video has captions and a link out; no autoplay with sound.
8. The footer carries the accessibility statement and a contact address.

Record the run in the course README so the next session knows when it last
passed.

## Testing before publish

Serve locally (`python3 -m http.server`) and run Playwright (Chromium at
`/opt/pw-browsers/`, `--no-sandbox`) to verify: every interactive module
round-trips, panel routing works from a cold URL, the progress rail marks and
resets, the classroom-only layer is absent from the self-paced edition, and
the console is clean (ignore TUNNEL/net:: noise). Also grep for em dashes and
for classroom-only markers leaking into the self-paced build.

## Reference files

- `references/mission.md` - the required Chancellor's charge section, verbatim, with its two course-specific slots.
- `references/pattern.md` - the Working Smarter section and panel architecture, the module vocabulary, classroom vs self-paced, progress and privacy contract.
- `references/accessibility.md` - the WCAG 2.2 AA contract, an accessible recipe for every interaction type, the audit scripts, and the ship gate.
- `references/brand.md` - color tokens with verified contrast ratios, type stack, component classes, motion rules.
- `references/facilitator.md` - notes.json schema, timing invariants, briefing page, printable guide, slide screenshot workflow.
- `references/library.md` - catalog card, filter topics, skills and core competencies, syllabus, length badge format.
- `references/deck.md` - **legacy**. The horizontal 100vw slide deck used by the older course repos. Read it only when editing one of those; never build a new course this way.
