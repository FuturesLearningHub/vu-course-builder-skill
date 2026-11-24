# vu-course-builder

A Claude skill for building Vanderbilt Learning Series ("Learning on Demand")
interactive course sites: FLH brand, three editions per course (classroom,
self-paced web, facilitator), horizontal right-to-left deck navigation, ATD
facilitator runbooks, Kirkpatrick/Bloom learning architecture, and
Course_Library catalog integration.

## Layout

- `SKILL.md` - the skill entry point (frontmatter description + workflow)
- `references/brand.md` - FLH color tokens, type stack, components, motion
- `references/deck.md` - horizontal deck CSS/JS contracts
- `references/facilitator.md` - notes.json schema, briefing page, printable guide
- `references/library.md` - catalog cards, skill pills, core competencies, syllabi
- `evals/evals.json` - test prompts and assertions used to validate the skill
- `assets/img/` - VU lockups, V icon, favicons (authorized use only)
- `assets/fonts/` - the seven self-hosted brand fonts (woff2)

## Install

Copy the repo (or the packaged `.skill` file) into your Claude skills
directory, e.g. `~/.claude/skills/vu-course-builder/`, or place it in a
project's `.claude/skills/`.

Related repos: the six course sites (AI_Classroom, AI-Advanced,
Difficult_Conversations, Coaching-for-Performance, Emotional-Intelligence,
Presentation-Public-Speaking) and the catalog, me5231979/Course_Library.
