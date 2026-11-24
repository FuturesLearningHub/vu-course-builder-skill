# The Working Smarter pattern

Working Smarter is the reference course. Its source is
`FuturesLearningHub/FLH-Learning-Library-`:

- `learn/index.html` is the self-paced edition.
- `learn/classroom/index.html` is the classroom edition.
- `learn/STYLE.md` is the house style for copy.

This file describes what those files do so you can build a new course to
match without guessing. When this file and the source disagree, the source
wins. Open it and check.

## 1. One file, one page, one book

A course is a single HTML file with all its CSS in one `<style>` and all its
JS in inline `<script>` blocks. There is no framework, no build step and no
backend. It ships three things together:

1. **The scroll layout.** Every section is a `<section>` inside
   `<main id="main">`, in course order. This is the no-JS fallback and must
   read correctly on its own.
2. **The pager.** A script that runs before the app script and regroups the
   sections into `.page` articles, one visible at a time ("book mode").
3. **The app script.** Progress, the route diagnostic, and every interactive
   module.

The first script in `<head>` adds `js` and `paged` to `<html>`. If the pager
throws while building, it removes `paged` and hides the book bar, and the
scroll layout stands.

## 2. The section spine

Every course uses this order. Teaching sections are the only part that
changes in number (4 to 8 of them).

| # | Selector | Pager key | Theme | Mode | What it holds |
|---|---|---|---|---|---|
| 1 | `section.hero` | `home` | `th-dark` | whole | Program eyebrow, `h1.metal` with one italic word, "Welcome to <Course>.", lead, 4 to 5 Bloom's-verb outcomes (`ul.outcomes`, bold verb first), closer line, meta line with Core/Full minutes, Start button to `#start`, `ol.hw-mini` with four how-to steps |
| 2 | `.topics` + `#start` | `belief` | `th-light` bar + `th-cream` | whole | Topic marquee bar (`role="img"` with a full `aria-label`, marquee `aria-hidden`), then the creed: one sentence ending on an italic phrase |
| 3 | `#mission` | `mission` | `th-dark` | whole | The Chancellor's charge. Verbatim from `mission.md` with two slots |
| 4 | `section.howworks` | `how` | `th-light` | whole | "What you will *cover*." Four `hw-step` stops with minute chips, the meta line, the progress line, the tagline, the five-question route diagnostic, and a `bridge` into section 01 |
| 5 to n | `#<key>` per teaching section | `<key>` | alternate `th-light` / `th-cream` / `th-dark` | split | Numbered teaching sections (Working Smarter: learn, readiness, crit, playground, tools, simulator, responsible) |
| n+1 | `#quiz` | `quiz` | `th-cream` | split | Knowledge check: 8 questions over two pages, then results plus the L1 feedback form |
| n+2 | `#summary` | `summary` | `th-light` | whole | "What you now *know.*" A `recap-grid` of one card per big idea. Not tracked |
| n+3 | `#nextstep` | `nextstep` | `th-cream` | whole | The L3 commitment: a five-step loop for the real week |
| n+4 | `#resources` | `resources` | `th-light` | whole | Keep learning: grouped `res` links, sources, and the plain-language glossary |
| last | `section.cta` + `footer` | `end` | `th-dark` | whole | Wrap-up headline, link back to next step, nudge to the quiz, the Oracle Learning strip, then the footer |

"Split" means the pager breaks the section into several pages at `data-pg`
markers (see 4). "Whole" means the section is one page.

Themes alternate so neighboring pages never share a ground. Never put
`th-dark` on two sections in a row.

## 3. Anatomy of a teaching section

```html
<section id="learn" class="th-light" aria-label="Learn the fundamentals">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="you-are">You are here: foundations, the five terms everything builds on.</span>
      <span class="eyebrow"><span class="tick" aria-hidden="true"></span><span class="mono">Learn / 01</span></span>
      <h2>What AI is, and how it <em class="s">works</em>.</h2>
      <p>In this section, you will learn ...</p>
    </div>

    <div class="module reveal">                      <!-- first page: no data-pg -->
      <div class="module-head">
        <span class="mno">Module A</span>
        <h3>The five terms</h3>
        <p>In this activity, you will ... (Click or press Enter.)</p>
        <div class="lframe">
          <span class="lf-chip"><b>You&rsquo;ll learn</b>...</span>
          <span class="lf-chip"><b>You&rsquo;ll do</b>...</span>
          <span class="lf-chip"><b>Time</b>3 min</span>
        </div>
      </div>
      <div class="concept reveal">
        <span class="c-label">The idea</span>
        <p>...</p>
      </div>
      <!-- the interaction -->
    </div>

    <div class="module reveal" data-pg="How an LLM works">  <!-- starts page 2 -->
      ...
    </div>

    <div class="bridge reveal"><span class="b-label">Next</span>
      <p>Transition line that ends on one <em>italic</em> word.</p></div>
  </div>
</section>
```

Required on every teaching section:

- **`you-are`**: one line saying where the learner is in the course.
- **Eyebrow**: `Section name / 0N` in Antonio caps.
- **`h2`**: Libre Caslon, exactly one italic word, ends in a period.
- **Lead**: starts "In this section, you will ...".
- **At least one module** with a `module-head` (`mno` label, `h3`, an
  "In this activity, you will ..." line with the input hint, and the three
  `lf-chip`s: You'll learn / You'll do / Time).
- **"The idea"** (`.concept` with `c-label`) before the interaction.
- **An interaction.** Reading is not a module.
- **`evidence` blocks** (`e-label`, body, `e-src` with author, year and a
  link) for every claim about impact or research.
- **A `bridge`** at the end that hands off to the next section.

Module labels are `Module A`, `Module B`, `Module B · continued`, `Drill`,
`Builder`, `App 01`, `Centerpiece`, `Practice`, `Closing step`. Pick the one
that tells the learner what kind of work is coming.

## 4. The pager contract

The pager has three pieces of config near the bottom of the file.

**`PLAN`** is one entry per top-level block, in order:

```js
{ sel:'#learn', key:'learn', label:'Learn', mode:'split' }
{ sel:'#start', key:'belief', label:'The belief', mode:'whole', extras:['.topics'] }
{ sel:'section.cta', key:'end', label:'Wrap-up', mode:'whole', extras:['footer'] }
```

- `key` becomes the hash segment and the `data-sec` on each page.
- `label` is what the bottom bar shows.
- `mode:'whole'` puts the section on one page. `extras` pulls other blocks
  onto that page.
- `mode:'split'` walks the children of the section's `.wrap`. A child with
  `data-pg="Page label"` starts a new page. The first page takes the
  section label. Later pages take their `data-pg` text. Each page gets
  a shell `<section>` with the original class, so the theme carries
  over, and an `aria-label` like "Learn the fundamentals (2 of 6)".

**`TRACKED`** is the list of sections that count toward progress, as
`[key, number, name]`. It must mirror `PROG_SECTIONS` in the app script and
the numbered links in the mobile menu. Working Smarter tracks 10: the seven
teaching sections plus quiz, nextstep and resources. `summary` is not
tracked.

**Routing.** The pager writes `#p/<key>/<n>` with `history.replaceState`.
Old-style `#<id>` anchors still work. The pager finds the page holding that
element and turns to it. On load it opens the deep link first, then the
saved page (`chart-page`), then page one.

**Page turns:**

- The incoming page gets `.cur` and loses `aria-hidden`. The outgoing page
  gets `aria-hidden="true"`.
- If focus was inside the outgoing page, or the turn came from a link,
  focus moves to the incoming `.page` (`tabIndex=-1`).
- Slide animation runs only when `prefers-reduced-motion` is off.
- Every turn fires `document` event `chart:page` with
  `{ key, index, label }`.

**Controls:**

- Prev and next buttons in the bottom bar.
- Left and right arrow keys, ignored in form fields, with modifiers, or while
  the menu, progress panel or Oracle modal is open.
- Horizontal swipe over 50px.
- Clicking any in-page `#` link turns pages instead of scrolling.

**`window.chartPager`** is the only API other scripts may use:

```js
chartPager.go(i, { focus:true })   // turn to page index i
chartPager.goToEl(el)               // turn to the page containing el, then scroll to it
chartPager.goToKey('quiz')          // first page of a section
chartPager.current()                // { key, index }
chartPager.count                    // total pages
```

A long page scrolls inside itself. The `#pgMore` "Scroll for more" cue
appears while there is more below. A `ResizeObserver` re-checks it when
content grows.

## 5. Chrome around the page

- **Skip link** `a.skip` to `#main`, first in `<body>`.
- **Top nav** `header.nav`: lockup (`alt="Vanderbilt University"`, link
  labelled "Vanderbilt University, <Course> home"), section links, the gold
  Knowledge check button, the Progress button (`aria-expanded`,
  `aria-controls="progPanel"`), and the menu button.
- **Progress panel** `#progPanel` (`role="region"`, hidden by default): a
  list of every tracked section with a deep link and a Mark done toggle
  (`aria-pressed`), plus the privacy line.
- **Mobile menu** `nav.mobile-menu`: numbered links with `data-prog` so
  they show Done, plus a line like "0 of 10 sections complete".
- **Book bar** `#bookBar` (`role="navigation"`, "Book controls"): section
  label, one dot per tracked section (`aria-label` says done or not done,
  `aria-current` on the current one), a Mark done toggle, a live page count,
  and prev/next.
- **Status line** `#progStatus` (`role="status"`), visually hidden, which
  announces progress changes.
- **Footer**: program line, legal and ownership line, contact, the
  accessibility statement, the cross-link to the other edition, and
  Reset progress.

## 6. Progress and privacy contract

The learner is told exactly what is saved, and only this is saved:

| Key | Value | Set by |
|---|---|---|
| `chart-progress-<key>` | `"1"` per tracked section | finishing a module's activity, or Mark done |
| `chart-page` | `<key>/<n>` | every page turn |
| `chart-route` | JSON array of the five route answers | the route diagnostic |
| `chart-focus-task` | one task string | the readiness report (Working Smarter only) |
| `chart-progress-oracle-attested` | `"1"` | the completion modal |

The classroom edition uses the same keys under `chartc-` so the two editions
never share state. A new course gets its own prefix (for example `dc-` and
`dcc-`), because every course is served from the same origin.

Rules:

- Quiz answers, feedback text and anything else typed are never stored and
  never sent.
- Test storage once at startup. If it is blocked (private browsing), show the
  `#progStorageNote` warning and keep marks for the visit only.
- Footer Reset clears every key with the course prefix, then re-renders.
- Retired keys from old section names are ignored and swept on load.
- When every tracked section is done, the Oracle completion modal opens once
  per visit until the learner attests.
- Say all of this to the learner in the progress panel, in plain words.

## 7. The module vocabulary

Build from these. Each one has an accessible recipe in `accessibility.md`.
If a course needs something new, write its keyboard and screen reader
behavior there first.

| Type | Working Smarter example | Markup core | Done when |
|---|---|---|---|
| **Flip cards** | The five terms, Limits to know | `.flip-grid > .fcard > button.flip-btn[aria-expanded]` holding `.face.front` and `.face.back` | Viewed |
| **Reveal list** | Myths vs. facts | `.myth > button[aria-expanded]` + `.verdict` with a `vtag` (Myth / Fact) | All opened |
| **Find-the-flaw drill** | Spot the hallucination | `.hal` items, each a sentence with `button.hal-span[data-fab]` choices, `.hal-reveal[role=status]`, running `#halStatus` | All found |
| **Live demo** | Next-word demo | Controls plus a `role="img"` chart with a text `aria-label`, and an `aria-live` sentence | Played |
| **Builder** | CRIT builder, Prompt Lab | Labelled `textarea`/`input` fields with `hinttxt`, fill chips (`button.sim-chip[data-fill]`), a live `.preview`, and Copy | Prompt assembled |
| **Grader** | Prompt Grader | Paste field, Grade button, `#grOut[role=status]` with letter and missing parts | Graded once |
| **Matcher** | Tool Match | `form` of `fieldset.tm-q` yes/no radios, submit button, `#tmOut[role=status]` with the pick and the why | Submitted |
| **Self-check** | Keep the time | Same yes/no fieldsets, "Tally" button, a scored read-out with next moves | Tallied |
| **Scenarios** | Four judgment scenarios | `article.dilemma` with `.d-choices[role=group]` of `aria-pressed` buttons, then `.d-take[role=status]` with the reaction, "Our take" and "The takeaway" | All answered |
| **Assessment / simulator** | Role readiness, Opportunity simulator | A multi-step form (`sim-step`), chips with `aria-pressed`, a generated report in a live region | Report built |
| **Route diagnostic** | Your route (in How it works) | Five `.route-q` groups of `aria-pressed` buttons, Show my route button, `#routeOut[aria-live]` | n/a |
| **Knowledge check** | Quiz | `fieldset.qz[data-answer]` with `legend` and radio labels, a `.expl` shown after scoring, `#quizProgress` live count, `#quizResult[role=status]` | Scored |
| **Feedback (L1)** | After the quiz | `role="radiogroup"` rating scales with legends, a comment field, a send link that stays `aria-disabled` until a rating is picked | n/a |
| **Video** | How LLMs work, CRIT source video | `div.yt[data-embed][data-title]` with a `button.yt-btn` poster that loads a `youtube-nocookie.com` iframe on click, plus a `.yt-fallback` "Open on YouTube" link and a short-on-time note. Pick videos that have captions | n/a |

Every teaching module needs a play moment. Every activity says how to
operate it ("Click or press Enter") in its `module-head`.

## 8. Classroom vs self-paced

These are two files at two links. They share everything except this layer.

**Classroom edition only (`classroom/index.html`):**

- Hero meta says "One session · guided by your instructor". The `hw-mini`
  steps say the instructor drives the screen and learners scan the QR to
  follow along on their own device.
- A QR panel (`.qr-side > .qr-card`) on the hero, drawn client-side by
  `assets/js/qrcode.js`. The QR box is `role="img"` with
  `aria-label="QR code linking to this course"`, and the URL is printed in
  text under it.
- Gold **Together** cards (`div.moment` with an `aria-hidden` people icon,
  `m-label` "Together" and one prompt) at the points where the room
  discusses, pairs up or votes. Working Smarter has 10.
- The How it works meta line says modules can be trimmed to fit the time.
- Storage prefix `chartc-`.

**Self-paced edition only (`index.html`):**

- Meta line with Core and Full minutes and "self-paced".
- Reflection prompts in place of Together cards, and a commitment takeaway.
- The route diagnostic is the main way to skip modules.

**Both:** the same sections, modules, quiz, mission and sources. Each
footer links to the other edition. There is no mode picker.

Before publish, grep the self-paced file for `class="moment`, `qr-`,
`Together` and "instructor". All four must return nothing.

## 9. Copy patterns that are structural

- Headlines: one italic word, ending in a period (`What you now <em>know.</em>`).
- Lead sentences: "In this section, you will ..." and "In this activity, you will ...".
- `you-are` lines: "You are here: <stage>, <what this part does>."
- Bridges end on one italic word.
- Every module states its time in an `lf-chip`. The How it works stop
  chips and hero minutes must agree with those times.
- No em or en dashes anywhere (see `STYLE.md` and SKILL.md).
