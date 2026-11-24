#!/usr/bin/env python3
"""Contrast + palette gate for a Vanderbilt FLH Learning Library course.

Bundled with the vu-course-builder skill. Copy it into the course as
tools/contrast-check.py. It reads the course root (the folder above tools/)
or the folder you pass with --root.

Two jobs:
  1. Every foreground/background pair the theme scopes can produce must clear
     WCAG 2.2 AA: 4.5:1 for normal text, 3:1 for large text and UI borders.
  2. No component may hard-code a raw brand hex. Components read theme-scope
     variables (--tx, --eyebrow, --acc, --focus, --btn-bg) so they survive a
     move between a dark and a light section.

Run: python3 tools/contrast-check.py [--root DIR] [page.html ...]
     (default pages: index.html, classroom/index.html, facilitator/index.html;
      pages that do not exist are skipped, and at least one must exist)
Exit 0 = gate passes. Exit 1 = gate fails, with the failures listed.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "classroom/index.html", "facilitator/index.html"]


def parse_args(argv):
    """--root DIR and an optional list of pages override the defaults."""
    global ROOT, PAGES
    args = list(argv)
    if "--root" in args:
        i = args.index("--root")
        ROOT = pathlib.Path(args[i + 1]).resolve()
        del args[i:i + 2]
    if args:
        PAGES = args

# The approved Vanderbilt FLH palette. Nothing else may appear as a color.
APPROVED = {
    "#1c1c1c": "VU Black",
    "#ffffff": "White",
    "#cfae70": "Flat Gold",
    "#feeeb6": "Gold gradient light stop",
    "#b49248": "Gold gradient dark stop",
    "#f5f3ef": "Cream",
    "#e0d5c0": "Sand",
    "#e4e4e4": "Gray light",
    "#777777": "Gray dark",
    "#ecb748": "Highlight",
    "#946e24": "Oak",
    "#b3c9cd": "Sky",
    "#8ba18e": "Sage",
}
OFF_BRAND = {"#a94438": "off-brand red", "#8c6822": "off-brand oak"}


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    lo, hi = sorted((a, b))
    return round((hi + 0.05) / (lo + 0.05), 3)


# Every scoped pairing the course actually renders, per theme scope.
# (scope, role, foreground, background, minimum)
PAIRS = [
    # ── dark scope: black ground. Gold and highlight are safe here. ─────────
    ("th-dark", "--tx body text",        "#FFFFFF", "#1C1C1C", 4.5),
    ("th-dark", "--tx2 secondary text",  "#BDBDBD", "#1C1C1C", 4.5),
    ("th-dark", "--tx3 muted text",      "#A3A3A3", "#1C1C1C", 4.5),
    ("th-dark", "--eyebrow on ground",   "#CFAE70", "#1C1C1C", 4.5),
    ("th-dark", "--eyebrow on card",     "#CFAE70", "#262624", 4.5),
    ("th-dark", "--strong highlight",    "#ECB748", "#1C1C1C", 4.5),
    ("th-dark", "--focus ring",          "#ECB748", "#1C1C1C", 3.0),
    ("th-dark", "--acc rule on ground",  "#CFAE70", "#1C1C1C", 3.0),
    ("th-dark", "card text on card",     "#FFFFFF", "#262624", 4.5),
    ("th-dark", "secondary on card",     "#BDBDBD", "#262624", 4.5),
    ("th-dark", "muted on card2",        "#A3A3A3", "#212120", 4.5),
    ("th-dark", "code text on field",    "#FFFFFF", "#141414", 4.5),
    ("th-dark", "gold button label",     "#1C1C1C", "#CFAE70", 4.5),
    ("th-dark", "sage self-paced label", "#8BA18E", "#1C1C1C", 4.5),
    ("th-dark", "sage on card",          "#8BA18E", "#262624", 4.5),
    ("th-dark", "sky accent",            "#B3C9CD", "#1C1C1C", 4.5),
    # ── light scope: white ground. Gold cannot carry text or rules here, so
    #    every accent becomes Oak. Cream is a FILL behind dark text only. ────
    ("th-light", "--tx body text",       "#1C1C1C", "#FFFFFF", 4.5),
    ("th-light", "--tx2 secondary text", "#555555", "#FFFFFF", 4.5),
    ("th-light", "--tx3 muted text",     "#6E6E6E", "#FFFFFF", 4.5),
    ("th-light", "--eyebrow oak",        "#946E24", "#FFFFFF", 4.5),
    ("th-light", "--link oak",           "#946E24", "#FFFFFF", 4.5),
    ("th-light", "--strong oak",         "#946E24", "#FFFFFF", 4.5),
    ("th-light", "--focus ring oak",     "#946E24", "#FFFFFF", 3.0),
    ("th-light", "--acc rule oak",       "#946E24", "#FFFFFF", 3.0),
    ("th-light", "card text on card",    "#1C1C1C", "#FFFFFF", 4.5),
    ("th-light", "dark button label",    "#FFFFFF", "#1C1C1C", 4.5),
    # cream is only ever a fill behind VU Black or the secondary grey
    ("th-light", "body on cream fill",   "#1C1C1C", "#F5F3EF", 4.5),
    ("th-light", "secondary on cream",   "#555555", "#F5F3EF", 4.5),
    ("th-light", "muted on cream fill",  "#63615C", "#F5F3EF", 4.5),
    ("th-light", "sand rule on white",   "#E0D5C0", "#FFFFFF", 1.0),
    # ── the facilitator script rail: its own dark surface whatever page it
    #    sits beside, so these pairs hold in every section theme ────────────
    ("fac-rail", "purpose text",         "#FFFFFF", "#141414", 4.5),
    ("fac-rail", "body text",            "#D6D6D6", "#141414", 4.5),
    ("fac-rail", "meta text",            "#BDBDBD", "#141414", 4.5),
    ("fac-rail", "head + time labels",   "#CFAE70", "#141414", 4.5),
    ("fac-rail", "Say tag",              "#1C1C1C", "#CFAE70", 4.5),
    ("fac-rail", "Do tag",               "#1C1C1C", "#B3C9CD", 4.5),
    ("fac-rail", "Ask tag",              "#1C1C1C", "#8BA18E", 4.5),
    ("fac-rail", "Debrief tag",          "#1C1C1C", "#ECB748", 4.5),
    ("fac-rail", "Transition tag",       "#FFFFFF", "#4F4F4F", 4.5),
    ("fac-rail", "briefing box text",    "#D6D6D6", "#262624", 4.5),
    ("fac-rail", "briefing box heading", "#CFAE70", "#262624", 4.5),
    ("fac-rail", "template block text",  "#D6D6D6", "#1C1C1C", 4.5),
    # Ink is what sits on the tinted fills; Oak on those same fills lands at
    # 4.3:1, which is why check_tints_are_dark_only() below forbids the pairing.
    ("th-light", "ink on gold-tint fill",  "#1C1C1C", "#FCF7F1", 4.5),
    ("th-light", "ink on sage-tint fill",  "#1C1C1C", "#F5F7F5", 4.5),
]


def check_pairs():
    fails = []
    print("Scoped contrast pairs")
    print("-" * 72)
    for scope, role, fg, bg, minimum in PAIRS:
        r = ratio(fg, bg)
        ok = r >= minimum
        if not ok:
            fails.append((scope, role, fg, bg, r, minimum))
        print(f"  {'PASS' if ok else 'FAIL'}  {scope:9s} {role:24s} {fg} on {bg}  {r:>6}:1  (min {minimum})")
    return fails


def check_palette():
    """No off-brand hex, and no raw-palette color written into a component rule."""
    fails = []
    print()
    print("Palette purity")
    print("-" * 72)
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        found = {m.lower() for m in re.findall(r"#[0-9A-Fa-f]{6}\b", text)}
        before = len(fails)
        for hexv in sorted(found):
            if hexv in OFF_BRAND:
                fails.append((page, hexv, OFF_BRAND[hexv]))
                print(f"  FAIL  {page}: {hexv} is {OFF_BRAND[hexv]}")
            elif hexv not in APPROVED and hexv not in NEUTRAL_OK:
                fails.append((page, hexv, "not in the approved palette"))
                print(f"  FAIL  {page}: {hexv} is not in the approved palette")
        if len(fails) == before:
            print(f"  PASS  {page}: every hex is on-palette")
    return fails


def check_raw_palette_in_components():
    """Component rules must read theme-scope vars, never --vu-* directly.

    A component that can appear in either theme scope has to resolve its color
    through --tx / --eyebrow / --acc / --link, because gold reads at 2.1:1 on
    white and Oak reads at 3.7:1 on black. Either raw token is a latent
    contrast failure the moment the component moves.

    The exemptions below are surfaces that are permanently on one ground and
    cannot move: the hero and its QR panel, the mobile menu overlay, the
    footer, the book bar, and the scroll affordance (which paints its own dark
    background). Gold is correct on all of them and is measured in PAIRS above.
    """
    fails = []
    print()
    print("Component variable discipline")
    print("-" * 72)
    FIXED_DARK = (
        ":root", ".th-dark", ".th-light", "html", "body", "::selection",
        ".metal", ".skip", ".nav", ".bar", ".logo", ".links",
        ".mobile-menu", ".mfoot", ".menu-btn",
        ".hero", ".qr-side", ".qr-card", ".qr-sub",
        "footer", ".fcenter", ".fprogram", ".flegal", ".preset",
        ".book-bar", ".bb-", "a.bb-dot", "#pgMore", ".page",
        # the hero montage chip and scrim live only on the hero's dark ground,
        # like #pgMore; the gold-on-black pair is measured in PAIRS above
        ".hv-toggle", ".hero-media", ".hero-scrim", ".hero-poster", ".hero-video",
        # the facilitator script rail and the briefing are their own dark
        # surfaces whatever section theme they sit beside, so gold is correct
        # on them and their pairs are measured under "fac-rail" in PAIRS above
        ".facnote", ".facshow", ".fac__badge", ".brief__", "#briefing",
        ".t-say", ".t-do", ".t-ask", ".t-deb", ".t-tra", "body.fac",
    )
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            continue
        css = re.search(r"<style>(.*?)</style>", path.read_text(encoding="utf-8"), re.S)
        if not css:
            continue
        # strip comments first, or a comment body parses as a selector
        body_css = re.sub(r"/\*.*?\*/", "", css.group(1), flags=re.S)
        bad = 0
        for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", body_css):
            sel, decls = rule.group(1).strip(), rule.group(2)
            if not re.search(r"(^|;)\s*color\s*:\s*var\(--vu-", decls):
                continue
            if sel.startswith("@") or sel.startswith(FIXED_DARK):
                continue
            fails.append((page, sel))
            print(f"  FAIL  {page}: `{sel[:58]}` sets color from a raw brand token")
            bad += 1
        if not bad:
            print(f"  PASS  {page}: movable components take color from theme-scope vars")
    return fails


def check_tints_are_dark_only():
    """Alpha gold and sage fills must be scoped to .th-dark.

    Over white those tints resolve to roughly #FCF7F1 and #F5F7F5, where Oak
    drops to 4.37:1 and 4.32:1. Both are under AA for normal text, and Oak is
    what every eyebrow and label in the light scope uses. So the tints stay on
    the black ground, and in the light scope the same distinction is carried by
    the left rule and the label text.
    """
    fails = []
    print()
    print("Tinted fills stay on the dark ground")
    print("-" * 72)
    TINT = re.compile(r"background:\s*rgba\((?:207,174,112|139,161,142)\s*,")
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            continue
        css = re.search(r"<style>(.*?)</style>", path.read_text(encoding="utf-8"), re.S)
        if not css:
            continue
        body_css = re.sub(r"/\*.*?\*/", "", css.group(1), flags=re.S)
        bad = 0
        for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", body_css):
            sel, decls = rule.group(1).strip(), rule.group(2)
            if not TINT.search(decls):
                continue
            # allowed on permanently-dark chrome, or explicitly under .th-dark
            if ".th-dark" in sel or sel.startswith((".hero", ".nav", ".bar", ".mobile-menu",
                                                    "footer", ".book-bar", ".bb-", "a.bb-dot",
                                                    "#pgMore", ".skip", ".metal", ".qr-")):
                continue
            # ::selection names its own foreground (#1C1C1C), so the tint under
            # it is measured, not inherited.
            if sel.startswith("::selection"):
                continue
            # Icon wells hold a stroked glyph and no text. WCAG 1.4.11 asks 3:1
            # of a non-text graphic; Oak on the gold wash over white measures
            # 4.37:1, so these clear it with room.
            if sel.endswith(".m-ic") or ".m-ic" in sel:
                continue
            fails.append((page, sel))
            print(f"  FAIL  {page}: `{sel[:58]}` paints a brand tint outside the dark scope")
            bad += 1
        if not bad:
            print(f"  PASS  {page}: brand tints appear only on the dark ground")
    return fails


# Neutral greys derived for the scopes above (opaque equivalents of the alpha
# text colors the template used). They are tints of the approved black/white
# grounds, so they stay inside the palette's intent.
NEUTRAL_OK = {"#bdbdbd", "#a3a3a3", "#262624", "#212120", "#141414",
              "#555555", "#6e6e6e", "#63615c", "#d6d6d6", "#4f4f4f",
              "#efe0c4", "#e0d5c0"}

if __name__ == "__main__":
    parse_args(sys.argv[1:])
    present = [p for p in PAGES if (ROOT / p).exists()]
    if not present:
        print(f"GATE FAILED: none of {PAGES} found under {ROOT}.")
        sys.exit(1)
    print(f"Checking {', '.join(present)} under {ROOT}\n")
    failures = (check_pairs() + check_palette()
                + check_raw_palette_in_components() + check_tints_are_dark_only())
    print()
    if failures:
        print(f"GATE FAILED: {len(failures)} problem(s).")
        sys.exit(1)
    print("GATE PASSED: contrast and palette are clean.")
    sys.exit(0)
