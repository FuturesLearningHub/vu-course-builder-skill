# Facilitator edition and runbook

The facilitator edition is generated, never hand-edited:
`python3 tools/build-facilitator.py` reads `facilitator/notes.json` and the
classroom `index.html`, then writes `facilitator/index.html` (the deck with a
script rail on every slide) and `facilitator/guide.html` (the printable
packet). Regenerate after every change to `index.html` or `notes.json`.

## notes.json schema

```json
{
  "meta": {
    "program": "Course Name · Vanderbilt Learning Series",
    "totalMinutes": 90,
    "audience": "…", "roomSetup": "…", "postSession": "…",
    "paths": { "full": 90, "core": 60 },
    "framework": "…",
    "materials": ["…"],
    "prep": { "weekBefore": ["…"], "dayBefore": ["…"], "thirtyMinBefore": ["…"] },
    "contingencies": [{ "if": "…", "then": "…" }],
    "toughQuestions": [{ "q": "…", "a": "…" }],
    "templates": [{ "label": "Pre-work invite", "body": "Subject: …" }]
  },
  "sections": [
    {
      "id": "s-agenda",              // MUST match a slide id in index.html
      "title": "Agenda",
      "minutes": 3, "coreMinutes": 2,
      "coreNote": "Core: skip the second story.",
      "purpose": "Why this section exists, one sentence.",
      "say": "Verbatim-usable facilitator script for the slide.",
      "facilitate": ["Do steps, one action each."],
      "ask": "Question to the room, with the expected answers named.",
      "validate": "How you know the learning landed (the L2 check).",
      "watchFor": "Common failure mode and the recovery move.",
      "transition": "One line that lands the section and points to the next."
    }
  ]
}
```

Rules that must hold:
- **Timing sums exactly.** Sum of `minutes` = the Full path (90, or 60 for beginner courses); sum of `coreMinutes` = the Core path (60, or 30). Verify with a quick python sum before regenerating; the advertised lengths appear on the library card, the syllabus, and the rail heads.
- Every section id exists as a slide id; the generator injects the rail by id.
- Say / Do (facilitate) / Ask / Debrief (validate) / Transition is the ATD structure. Write `say` so a nervous first-time facilitator could read it aloud verbatim.
- No em dashes in any string.

## Learning model

- Objectives on the hero use Bloom's verbs (identify, apply, reframe, build), five per course, echoed on the syllabus.
- Kirkpatrick L1: fist-to-five close. L2: the scored recap quiz and each section's `validate`. L3: the capstone commitment card plus a 7-day pulse email (in `postSession`); first-try or commitment count is the program metric.

## The script rail

Each slide gets a sticky right rail (grid `minmax(0,1fr) 350px`): head with
"Facilitator script", `Full X min · Core Y`, and a **Hide** button
(`body.fac-hide` class, floating `.facshow` pill to bring it back, persisted
in `localStorage['facScriptHidden']`). Tags: `t-say` Say, Do, Ask, Debrief,
Transition, gold Antonio chips. Facilitator slides keep
`overflow-y: auto; overflow-x: hidden` (never `visible`, which breaks
internal scrolling on the horizontal deck).

## The briefing page ("Before the room fills")

Slide 1 of the facilitator edition, facilitator-only, generated from `meta`:

- You-are-here line: "You are here: the facilitator prep page. Learners start on the next page."
- Eyebrow "Run this course / 00 · Facilitator only", headline `Before the room <em>fills</em>.`
- Lead: the two paths, what the rail carries, and that learners never see this edition.
- Print button "Print the facilitator guide 🖨" opening `guide.html`, with a note describing the paper packet.
- Numbered prep cards `01 · A week before / 02 · The day before / 03 · 30 minutes before`, each with a bold sub-headline and gold ✓ check bullets, then `04 · Materials`, `05 · When things go sideways` (contingencies), `06 · Tough questions`, `07 · Copy-paste templates`.
- The pre-work invite sits in the briefing's script rail in a bordered `.facnote__invite` block.

Escape trap: the ✓ comes from CSS `content: "\2713"`. In a non-raw Python
string that reads as octal and renders garbage; write it `"\\2713"` inside
the generator.

## Printable guide (`guide.html`)

Front matter (audience, room, framework, run-of-show table with Full and Core
columns), then one two-column block per section: **slide image left
(290px), notes right**. Images live at `facilitator/img/<slide-id>.jpg`,
captured with Playwright (serve the repo locally, viewport ~1440x900,
`reducedMotion`, hide `.scrollhint` and `.bottombar`, jpeg quality ~68).
Re-shoot after any visual change to the slides. A missing image degrades
gracefully via an `onerror` class; do not ship missing images anyway.

## QR codes

The facilitator welcome QR encodes the LEARNER url (the classroom edition),
never the facilitator url. `data-url` on the QR container carries it.
