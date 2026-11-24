# vu-course-builder

A Claude skill for building Vanderbilt Learning Series ("Learning on Demand")
interactive course sites: FLH brand, three editions per course (classroom,
self-paced web, facilitator), book-mode page navigation (the Working Smarter pattern), ATD
facilitator runbooks, Kirkpatrick/Bloom learning architecture, and
Course_Library catalog integration.

## Layout

- `SKILL.md` - the skill entry point (frontmatter description + workflow)
- `references/pattern.md` - the Working Smarter section spine, pager contract, module vocabulary, classroom vs self-paced, progress and privacy
- `references/accessibility.md` - WCAG 2.2 AA rules, an accessible recipe per interaction type, the audit scripts, the ship gate
- `references/mission.md` - the required Chancellor's charge section with its three slots
- `references/brand.md` - FLH color tokens, type stack, components, motion
- `references/facilitator.md` - notes.json schema, briefing page, printable guide
- `references/library.md` - catalog cards, skill pills, core competencies, syllabi
- `references/deck.md` - legacy horizontal deck CSS/JS contracts
- `scripts/a11y-audit.mjs` - axe-core gate that walks every page of every edition (copy into a course's `tools/`)
- `scripts/contrast-check.py` - palette and scoped-contrast gate (copy into a course's `tools/`)
- `assets/img/` - VU lockups, V icon, favicons (authorized use only)
- `assets/fonts/` - the seven self-hosted brand fonts (woff2)

## Install

```bash
git clone https://github.com/FuturesLearningHub/vu-course-builder-skill ~/.claude/skills/vu-course-builder
```

Or place it in a project's `.claude/skills/vu-course-builder/`. Start a new
Claude session afterwards; skills load at session start. To update an
existing install, `git -C ~/.claude/skills/vu-course-builder pull`.

The skill is markdown, brand assets and two optional audit scripts. The
scripts never run on their own; you copy them into a course and run them
yourself.

Related repos: the six course sites (AI_Classroom, AI-Advanced,
Difficult_Conversations, Coaching-for-Performance, Emotional-Intelligence,
Presentation-Public-Speaking) and the catalog, FuturesLearningHub/FLH-Learning-Library-.
