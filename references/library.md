# Course_Library integration

Catalog repo: `me5231979/Course_Library`, live at
`https://me5231979.github.io/Course_Library/`. It republishes automatically
when `main` is pushed (GitHub Pages workflow). **Always `git pull` before
editing**; parallel sessions also work in this repo.

## The card

Each course is one card in `index.html` carrying, in order: topic tag,
title, length badge, description, objectives line, skill pills, optional
Voyage tag, and three edition buttons plus a syllabus link.

- Filter topics via `data-topics` on the card: space-separated subset of `ai`, `communication`, `leadership`. The filter bar chips (`.filterchip`, `data-topic` of `all|ai|communication|leadership`) show and hide cards.
- Length badge `.course__length`, standardized wording: `Classroom X min · Self-paced ~Y min` (e.g. `Classroom 90 min · Self-paced ~45 min`). Keep the duration in the description too, but the badge is the visible source of truth.
- Skill pills in `.course__skills`: 3 to 5 per course, `class="skillpill"`, with core competencies as `class="skillpill skillpill--core"`. **Every course carries at least one core competency.** No definitions, just the skill name.
- Manager courses (currently Difficult Conversations, Coaching for Performance, Presentation & Public Speaking) get `<p class="course__voyage">✦ Part of the Manager Voyage program</p>`.
- Buttons: Classroom edition -> `/<Repo>/`, Self-paced -> `/<Repo>/web/`, Facilitator -> `/<Repo>/facilitator/`. All external links open in a new tab (the page's script adds it).

## The seven VU core competencies

1. Radically collaborates and cultivates belonging
2. Embodies an entrepreneurial spirit and leverages data and technology
3. Continuously strives for excellence
4. Grows self and others
5. Leads and inspires teams
6. Develops and implements University strategy
7. Makes effective and ethical decisions for the University

Pick core competencies plus specific skills (e.g. Conflict Resolution,
Public Speaking, Coaching Techniques, Artificial Intelligence) that a
recruiter or LMS would recognize. Judgment over completeness: the 3 to 5
most defensible skills, not everything the course touches.

## Syllabus pages

`tools/build-syllabi.py` generates `syllabus-<course>.html` from its config
block: description, audience (prefix manager-course audiences with the
Voyage line), objectives, the standardized length fields, `coreSkills` and
`skills` arrays rendered as pills, and links to all three editions. Add a
config entry for each new course and regenerate.

## Checklist for adding a course

1. `git pull` the library.
2. Add the card (copy the newest card's markup; keep the class inventory identical).
3. Add the syllabus config entry, run `python3 tools/build-syllabi.py`.
4. Verify the filter shows the card under its topics and the length badge reads correctly.
5. Push `main`; the workflow publishes.
