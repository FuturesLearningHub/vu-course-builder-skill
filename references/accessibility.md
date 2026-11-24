# Accessibility: the WCAG 2.2 AA contract

Every course must pass WCAG 2.2 Level AA before it ships. This file covers
four things:

1. The rules that apply everywhere.
2. A recipe for each interaction type in `pattern.md`.
3. The two audit scripts that ship with this skill.
4. The gate itself.

The recipes describe what Working Smarter already does. Where Working
Smarter falls short, that is noted under "Known gaps". Fix those in any new
course. Do not copy them.

## 1. Global rules

**Structure**

- `<html lang="en">`, a unique `<title>`, and `<meta name="viewport" content="width=device-width, initial-scale=1">`. Never disable zoom.
- `a.skip` "Skip to content" is the first focusable element and targets `#main`. In book mode the click handler focuses the current `.page`.
- One `h1` (the hero). Each section has an `h2`, each module an `h3`, each card an `h4`. Never skip a level to get a size. Restyle the heading instead.
- Landmarks: `header.nav`, `nav.links[aria-label="Primary"]`, `nav.mobile-menu[aria-label="Mobile"]`, `main#main`, the book bar `role="navigation"` with `aria-label="Book controls"`, and `footer`. Every `<section>` has an `aria-label`.
- Decorative SVGs, tick marks, numbers repeated in text and marquees get `aria-hidden="true"`. Any SVG inside a button is `aria-hidden` and the button carries the name.
- Images need real `alt`. Lockups use `alt="Vanderbilt University"`. A purely decorative image uses `alt=""`.

**Keyboard and focus**

- Every control is a native `<button>`, `<a href>`, `<input>`, `<select>` or `<textarea>`. Never put a click handler on a `div` or `span`.
- `:focus-visible{ outline:2px solid var(--focus); outline-offset:3px }`. `--focus` resolves per theme scope (Highlight on dark, Oak on light) so the ring always reaches 3:1. Never use `outline:none` without a replacement.
- Page turns move focus into the new `.page` when focus would otherwise be stranded on a hidden page. Hidden pages are `aria-hidden="true"`. No focusable element may remain reachable inside one. The pager guarantees this; do not work around it.
- Arrow-key paging is ignored inside form fields and while a menu, panel or dialog is open.
- Overlays (mobile menu, progress panel, Oracle modal) set `aria-expanded` on their trigger and close on Escape. Focus goes into the overlay on open and back to the trigger on close. The modal is `role="dialog" aria-modal="true" aria-labelledby` and traps Tab.
- Nothing appears only on hover. Anything shown on hover is also shown on focus.

**Announcements**

- Results, scores, running counts and generated reports go in a live region: `role="status"` (it is polite) or `aria-live="polite"`. The region exists in the markup at load time, empty. Only its text changes. A region inserted at the moment of the result is not announced reliably.
- Never use `aria-live="assertive"`.
- `#progStatus` (visually hidden, `role="status"`) announces "Learn marked done. 3 of 10 sections complete."
- Toggle buttons carry state in `aria-pressed` or `aria-expanded`, never in color or class alone.

**Color, contrast and state**

- 4.5:1 for body text, 3:1 for large text (24px, or 18.66px bold), focus rings, borders that identify a control, and meaningful graphics.
- Components read theme-scope variables (`--tx`, `--tx2`, `--eyebrow`, `--focus`, `--btn-bg`, `--link`), never `var(--vu-gold)` and friends. Gold on white is 2.1:1, and Oak on black is 3.7:1. `contrast-check.py` enforces this.
- There is no approved red or green. Right and wrong are carried by **words and an icon** ("Found it." / "Not that one."), with color added on top.
- Links inside body text are underlined.

**Layout and motion**

- Reflow at 320px wide and at 200% zoom with no horizontal scrolling and no clipped text (1.4.10).
- Text spacing overrides (1.4.12) must not clip. Use `min-height`, not a fixed `height`, on anything holding text.
- Touch targets are at least 24 by 24px, or spaced so a 24px circle around each does not overlap its neighbors (2.5.8). Small dots and chips need padding or a larger hit area.
- `@media (prefers-reduced-motion:reduce)` must:
  - kill all animations and transitions
  - show `.reveal` content immediately
  - hide the hero video
  - stop and wrap the marquee
  - drop smooth scrolling

  The pager skips its slide animation.
- Motion stays at 400ms or under. Nothing flashes more than 3 times a second.
- Hero video is `muted autoplay loop playsinline`, `aria-hidden`, and has a visible pause control (`.hv-toggle`). Teaching videos are click-to-load, pick ones with captions, and always have a text link out.

**Forms**

- Every field has a visible `<label for>`. Placeholder text is never the label.
- Helper text (`.hinttxt`) is tied to its field with `aria-describedby`.
- Groups of radios sit in a `fieldset` with a `legend` that holds the question.
- Error and empty-state messages say what to do, in text, in a live region.
- `autocomplete="off"` on practice forms. Nothing typed is stored.

## 2. Recipes by interaction type

### Flip cards

```html
<div class="fcard">
  <button type="button" class="flip-btn" aria-expanded="false">
    <span class="face front"> <h4>Term</h4> <span class="def">Short line</span> <span class="hint">Flip for the real story</span> </span>
    <span class="face back"> ... </span>
  </button>
</div>
```

- One native button holds both faces. Click, Enter and Space toggle it. JS flips `aria-expanded` and the `.flipped` class.
- The back face is in the DOM and readable. Do not hide it with `display:none`, or screen reader users never reach it. Hide it visually with the 3D transform only.
- Under reduced motion, swap faces with no rotation.
- An `h4` inside a button is not exposed as a heading. That is acceptable here because the button name is the term. Do not rely on these headings for navigation.

### Reveal list (myths vs. facts)

- `button[aria-expanded]` holding the claim, followed by the `.verdict`. The verdict label is text ("Myth" or "Fact"), never just a colored tag.
- The `+` icon that rotates on open is `aria-hidden`.

### Find-the-flaw drill (spot the hallucination)

- Each candidate detail is a `<button type="button" class="hal-span">` inline in the sentence. Never a clickable span.
- Each item has its own `.hal-reveal[role=status]`, present at load. It says "Found it. The tell: ..." or "Not that one. ... Keep looking."
- A section-level `#halStatus[role=status]` keeps the running count: "2 of 4 found."
- Correct and wrong states add a text marker or icon as well as color.
- After an item is solved, its buttons are disabled or ignore clicks, and that state is announced.

### Live demo (next-word prediction)

- The controls are native: buttons, and a labelled `input type="range"` with its value shown in text (`.tval`).
- The chart is `role="img"` with an `aria-label` that describes it. Also write the top choice and its percent into the live sentence, because a static label does not update.
- The sentence is `aria-live="polite"`. Announce once per step, not once per animation frame.

### Builder and Prompt Lab

- Each part (Context, Role, Interview, Task) is a labelled field with `aria-describedby` hint text.
- Fill chips are buttons that write into their `data-target` field and then focus it. A chip group with an `aria-label` must have `role="group"`, or the label is ignored.
- `.preview[aria-live=polite]` updates as the learner types. Debounce updates to about 500ms so the reader is not interrupted on every key.
- Copy button: after copying, its text changes to "Copied" and the change is announced through a status region.

### Grader

- Paste field with a label, plus a Grade button.
- `#grOut[role=status]` holds the letter grade as text ("Grade: B"), then the missing parts as a list. A grade conveyed only by color fails.

### Matcher and self-check (yes/no fieldsets)

- `form` holding `fieldset.tm-q` per question. The `legend` holds the question number and text. Each option is `<label><input type="radio"> Yes</label>`.
- The submit or Tally button stays enabled. If questions are unanswered, the output region says which ones ("Answer Q3 and Q5 first"). Do not leave a disabled button with no reason given.
- The result goes in `#tmOut` or `#wbOut` `[role=status]`: the pick first, then the reasons.

### Scenarios (judgment dilemmas)

- `.d-choices[role=group][aria-label="Your response to scenario 01"]` holding `button[aria-pressed]`. Choosing one sets it to `true` and the others to `false`.
- `.d-take[role=status]` gets the reaction and reveals "Our take" and "The takeaway". Reveal with a class, not by injecting the whole block, so the live region stays the same node.

### Route diagnostic, assessment and simulator

- Option groups are `role="group"` with `aria-labelledby` pointing at the question text. Options are `button[aria-pressed]`.
- "Show my route" starts `disabled`. The visible `#routeHint` says why ("Answer all five to see your route."). Connect the hint to the button with `aria-describedby`.
- Multi-step forms (`sim-step`): each step has a heading. When moving to a step, focus its heading. The generated report renders into an existing live region, and its first line is a summary sentence.

### Knowledge check

- `fieldset.qz` + `legend` ("1/8" + question) + native radios with labels. Never custom radio divs.
- `#quizProgress[aria-live=polite]` reads "3 of 8 answered".
- On scoring, each `.expl` appears beside its question. Mark right or wrong in text ("Correct." / "Not quite."), not only with color. `#quizResult[role=status]` announces the score and the pass message.
- Do not move focus on scoring. The status announcement is enough. Learners then tab through the explanations in order.

### Feedback (L1)

- The rating scales are `role="radiogroup"` with `aria-labelledby` their legend, built from native radios. Otherwise each option button needs `role="radio"` and `aria-checked` with arrow-key handling, which is harder to get right.
- When the send control is an `<a role="button">`, it needs `aria-disabled="true"` until a rating is chosen. Its click handler must also do nothing while disabled, because `aria-disabled` does not block clicks. `#fbStatus[role=status]` says what happened.

### Together cards (classroom)

- A `div.moment` with an `aria-hidden` icon, the visible label "Together", and a paragraph. Nothing interactive. The label is text, so it reads in order.

### QR welcome (classroom)

- The QR container is `role="img" aria-label="QR code linking to this course"`. The URL is printed as text under it, so people who cannot scan can type it.

### Video

- Poster `button.yt-btn` with an accessible name ("Play: <title>") that loads a `youtube-nocookie.com` iframe. The iframe has a `title`.
- After it loads, move focus to the iframe.
- `.yt-fallback` always offers "Open on YouTube" as a plain link.
- Choose videos with accurate captions. If there are none, link a transcript.

## 3. The audit scripts

Both scripts ship with this skill in `scripts/`. Copy them into the course:

```bash
mkdir -p tools
cp ~/.claude/skills/vu-course-builder/scripts/a11y-audit.mjs tools/
cp ~/.claude/skills/vu-course-builder/scripts/contrast-check.py tools/
```

If the skill was installed into a project instead, the path is
`.claude/skills/vu-course-builder/scripts/`.

### `tools/a11y-audit.mjs` (axe-core, every page)

One-time setup in the course repo:

```bash
npm i -D playwright @axe-core/playwright
npx playwright install chromium
```

Run it with the server going from the course root:

```bash
python3 -m http.server 8765
node tools/a11y-audit.mjs
```

What it does:

- Finds every edition that is served: `/`, `/classroom/`, `/facilitator/`. It skips any that return 404.
- Clears storage, then walks `window.chartPager` through **every page**, at 1440x900 and 320x640.
- Runs axe (WCAG 2.0, 2.1 and 2.2, A and AA) on each page. Any critical or serious violation fails the gate.
- Checks for horizontal scrolling on every page, plus a 200% zoom pass (a 720x450 viewport).
- With reduced motion turned on, checks that no infinite or long animation and no visible video is still playing.
- Collects console errors, ignoring proxy, `net::` and favicon noise.
- Scans `facilitator/guide.html` if it exists.

Environment variables:

- `BASE`: the server address.
- `EDITIONS`: override the editions, for example `self-paced=/,classroom=/classroom/`.
- `CHROME_PATH`: use a specific browser binary. In the cloud image that is `/opt/pw-browsers/chromium`. On a Mac you can use installed Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

It does not need a section list. If the pager failed to build, it says so
and fails.

### `tools/contrast-check.py` (palette and scoped contrast)

```bash
python3 tools/contrast-check.py                    # course root = folder above tools/
python3 tools/contrast-check.py --root path/to/course
python3 tools/contrast-check.py index.html other.html
```

It runs four checks:

1. **Scoped pairs**: every text, ring and rule color pair each theme scope renders, measured against 4.5:1 or 3:1. When a course adds a new surface, add its pairs to `PAIRS`.
2. **Palette purity**: every 6-digit hex in each page must be in `APPROVED` or `NEUTRAL_OK`. `#A94438` and `#8C6822` are named as off-brand.
3. **Variable discipline**: a component rule may not set `color: var(--vu-*)` unless its selector is a fixed-dark surface listed in `FIXED_DARK`.
4. **Tints stay dark**: alpha gold and sage fills only under `.th-dark` or on fixed-dark chrome.

Exit 0 means it passed. Exit 1 lists every failure.

## 4. The gate (blocks publish)

All eight must pass. Record the date and result in the course README.

1. `node tools/a11y-audit.mjs` prints `A11Y GATE PASSED`.
2. `python3 tools/contrast-check.py` prints `GATE PASSED`.
3. **Keyboard-only pass.** Do the whole course with Tab, Shift+Tab, Enter, Space and the arrow keys:
   - every control is reachable and works
   - focus is always visible
   - there are no traps
   - page turns and panel changes put focus somewhere sensible
   - the skip link works
4. **Screen reader pass.** Use VoiceOver (Safari) or NVDA (Firefox or Chrome) on one full flow of every interaction type the course uses. Every result, count and state change is announced. Nothing important is silent.
5. **Reduced motion.** Turn the OS setting on and reload. The marquee, pulses, flips, page slides, smooth scroll and hero video all stop.
6. **Zoom and reflow.** At 200% browser zoom and at 320px wide there is no horizontal scroll and no clipped or overlapping text.
7. **Media.** Every video has captions or a transcript and a link out. Nothing plays sound on its own.
8. **Footer.** It carries an accessibility statement (the course targets WCAG 2.2 AA) and a contact address for reporting barriers.

## Known gaps in the current Working Smarter source

Running both scripts against `learn/index.html` and `learn/classroom/index.html`
(November 2026) shows that the reference course does **not** pass the gate
yet. Do not copy these into a new course. Fix them in Working Smarter when
someone is next in that file.

- **target-size (2.5.8), 320px.** The book bar dots (`a.bb-dot`) are under 24px with no spacing around them. Every page fails because of them.
- **scrollable-region-focusable.** When a `.page` scrolls internally and holds nothing focusable, keyboard users cannot scroll it. Give scrollable pages `tabindex="0"` while they overflow, or make sure every long page contains a focusable element.
- **color-contrast.** `.hw-no` step numbers in How it works and Next step measure under 4.5:1. Some creed words (`#creed .w`) also flag, possibly while their fade-in is still running. Check them with motion on and off.
- **Off-palette hex.** `#A94438`, `#8C6822`, `#3E5A66`, `#42604A`, `#7A5C1E`, `#D6D0C4` and `#E0D8C8` appear in the source.
- **Raw brand tokens** in about 20 movable components (for example `.fcard .abbr`, `.yt-sub`, `button.hal-span.wrong`), and brand tints outside the dark scope (`.myth .vtag`, `.hal-status`, `button.hal-span.correct`).
- **Footer** has no accessibility statement or barrier-report contact.
