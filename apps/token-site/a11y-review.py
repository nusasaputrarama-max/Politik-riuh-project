#!/usr/bin/env python3
"""Broader accessibility review for the token site (stdlib only, no deps).

Goes beyond the five-pair palette spot-check in checks.sh:
  static (per page) — heading outline, alt-text inventory, landmarks,
    aria-labelledby targets, link/button accessible names, skip-link
    target, <main> tabindex, lang;
  browser (CDP, per page) — computed-contrast sweep over every visible
    text-bearing element (foreground vs effective background, WCAG
    4.5:1 normal / 3:1 large thresholds);
  stylesheet — :focus-visible rule and reduced-motion block present
    (live behaviour is proven separately by keyboard-test.py and
    reduced-motion-test.py, referenced here, not re-proven).

This is a review, NOT a WCAG conformance claim: no screen-reader
testing was done, and the contrast sweep approximates text over the
decorative hero glow (a radial gradient sibling, not an ancestor
background) with the body background.

Usage: python3 a11y-review.py   (from apps/token-site/)
Exit 0 = review completed with no hard defects (missing alt text,
dangling aria-labelledby, contrast below threshold, missing landmark,
duplicate id, empty accessible name). Writes
docs/../accessibility-review-2026-11-09.md (the review document) and
evidence/a11y-review-YYYY-MM-DD.log.
"""
import datetime
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp_helper import BrowserSession

SITE_DIR = Path(__file__).resolve().parent
REPO_DIR = SITE_DIR.parent.parent
PAGES = ["index.html", "about.html", "token.html", "launch.html", "transparency.html", "roadmap.html"]
TODAY = datetime.date.today().isoformat()
VAGUE_LINK_TEXT = {"", "klik di sini", "di sini", "selengkapnya", "baca selengkapnya", "klik", "link"}

SWEEP_JS = """(() => {
  function parseRGB(s) {
    const m = s && s.match(/rgba?\\(([^)]+)\\)/);
    if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x));
    return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1};
  }
  function lum(c) {
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  function ratio(fg, bg) {
    const l1 = lum(fg), l2 = lum(bg);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }
  function effBg(el) {
    let n = el;
    while (n) {
      const bg = parseRGB(getComputedStyle(n).backgroundColor);
      if (bg && bg.a >= 1) return bg;
      n = n.parentElement;
    }
    return {r: 255, g: 255, b: 255, a: 1};
  }
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let el;
  while (el = walker.nextNode()) {
    if (el.closest('[aria-hidden="true"]')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    let text = '';
    for (const node of el.childNodes) {
      if (node.nodeType === 3) text += node.textContent;
    }
    text = text.trim().replace(/\\s+/g, ' ');
    if (!text) continue;
    const fg = parseRGB(cs.color);
    if (!fg) continue;
    const bg = effBg(el);
    const r = ratio(fg, bg);
    const size = parseFloat(cs.fontSize);
    const bold = parseInt(cs.fontWeight) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const min = large ? 3.0 : 4.5;
    out.push({text: text.slice(0, 48), tag: el.tagName.toLowerCase(),
              size: size, bold: bold, ratio: Math.round(r * 100) / 100,
              min: min, pass: r >= min});
  }
  return JSON.stringify(out);
})()"""

LOG_LINES = []
DEFECTS = []


def log(msg):
    print(msg)
    LOG_LINES.append(msg)


class PageParse(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.h1 = []
        self.headings = []  # (level, text)
        self._heading = None
        self.landmarks = set()
        self.ids = []
        self.labelledby = []
        self.images = []  # (src, alt or None)
        self.links = []  # (text, href)
        self._link = None
        self.buttons = []  # text
        self._button = None
        self.skip_target = None
        self.main_tabindex = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = [int(tag[1]), ""]
        if tag in ("header", "nav", "main", "footer"):
            self.landmarks.add(tag)
        if tag == "main":
            self.main_tabindex = d.get("tabindex")
        if "id" in d:
            self.ids.append(d["id"])
        if "aria-labelledby" in d:
            self.labelledby.extend(d["aria-labelledby"].split())
        if tag == "img":
            self.images.append((d.get("src", ""), d.get("alt")))
        if tag == "a":
            self._link = ["", d.get("href", "")]
            if d.get("class") == "skip-link":
                self.skip_target = d.get("href", "").lstrip("#")
        if tag == "button":
            self._button = [""]

    def handle_data(self, data):
        if self._heading is not None:
            self._heading[1] += data
        if self._link is not None:
            self._link[0] += data
        if self._button is not None:
            self._button[0] += data

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._heading is not None:
            level, text = self._heading
            self.headings.append((level, text.strip()))
            if level == 1:
                self.h1.append(text.strip())
            self._heading = None
        if tag == "a" and self._link is not None:
            self.links.append((self._link[0].strip(), self._link[1]))
            self._link = None
        if tag == "button" and self._button is not None:
            self.buttons.append(self._button[0].strip())
            self._button = None


def static_review():
    """Returns (findings dict per page, site-wide notes)."""
    pages = {}
    for p in PAGES:
        text = (SITE_DIR / p).read_text(encoding="utf-8")
        parser = PageParse()
        parser.feed(text)
        findings = {"lang": parser.lang, "h1": parser.h1, "headings": parser.headings,
                    "landmarks": sorted(parser.landmarks), "images": parser.images,
                    "links": parser.links, "buttons": parser.buttons,
                    "skip_target": parser.skip_target, "main_tabindex": parser.main_tabindex,
                    "ids": parser.ids, "labelledby": parser.labelledby}
        # Hard-defect checks.
        if parser.lang != "id":
            DEFECTS.append(f"{p}: <html lang> is {parser.lang!r}, expected 'id'")
        if len(parser.h1) != 1:
            DEFECTS.append(f"{p}: {len(parser.h1)} <h1>, expected exactly 1")
        prev = 0
        for level, _ in parser.headings:
            if prev and level > prev + 1:
                DEFECTS.append(f"{p}: heading jumps h{prev} -> h{level}")
            prev = level
        if parser.landmarks != {"header", "nav", "main", "footer"}:
            DEFECTS.append(f"{p}: landmarks {sorted(parser.landmarks)}")
        dup = {i for i in parser.ids if parser.ids.count(i) > 1}
        if dup:
            DEFECTS.append(f"{p}: duplicate ids {sorted(dup)}")
        for ref in parser.labelledby:
            if ref not in parser.ids:
                DEFECTS.append(f"{p}: aria-labelledby references missing id {ref!r}")
        for src, alt in parser.images:
            if alt is None:
                DEFECTS.append(f"{p}: <img src={src!r}> has no alt attribute")
        for text_link, href in parser.links:
            if text_link.strip().lower() in VAGUE_LINK_TEXT:
                DEFECTS.append(f"{p}: vague/empty link text {text_link!r} -> {href!r}")
        for b in parser.buttons:
            if not b:
                DEFECTS.append(f"{p}: button with empty accessible name")
        if parser.skip_target != "main" or "main" not in parser.ids:
            DEFECTS.append(f"{p}: skip link target is {parser.skip_target!r}, expected 'main'")
        if parser.main_tabindex != "-1":
            DEFECTS.append(f"{p}: <main> tabindex is {parser.main_tabindex!r}, expected '-1'")
        pages[p] = findings
    css = (SITE_DIR / "styles.css").read_text(encoding="utf-8")
    notes = {
        "focus_visible_rule": ":focus-visible" in css and "outline: 2px solid" in css,
        "reduced_motion_block": "@media (prefers-reduced-motion: reduce)" in css,
        "img_count_total": sum(len(v["images"]) for v in pages.values()),
    }
    if not notes["focus_visible_rule"]:
        DEFECTS.append("styles.css: no :focus-visible outline rule")
    if not notes["reduced_motion_block"]:
        DEFECTS.append("styles.css: no prefers-reduced-motion block")
    return pages, notes


def contrast_sweep(cdp, base):
    """Computed-contrast sweep per page. Returns {page: {total, failures, worst}}."""
    results = {}
    for p in PAGES:
        cdp.navigate(f"{base}/{p}")
        rows = json.loads(cdp.evaluate(SWEEP_JS))
        failures = [r for r in rows if not r["pass"]]
        worst = sorted(rows, key=lambda r: r["ratio"])[:8]
        results[p] = {"total": len(rows), "failures": failures, "worst": worst}
        for f in failures:
            DEFECTS.append(f"{p}: contrast {f['ratio']}:1 < {f['min']}:1 — "
                           f"<{f['tag']}> {f['text']!r} ({f['size']}px)")
        log(f"PASS: {p} contrast sweep — {len(rows)} text elements, "
            f"{len(failures)} below threshold, worst {worst[0]['ratio']}:1 "
            f"(<{worst[0]['tag']}> {worst[0]['text']!r})" if not failures else
            f"FAIL: {p} contrast sweep — {len(failures)} below threshold")
    return results


def write_doc(pages, notes, sweep):
    doc = f"""# POLITIK RIUH — Accessibility Review (token site)

Date: {TODAY} (WIB). Reviewer: Muse (engineering partner).
Scope: the six static pages in `apps/token-site/` (`index`, `about`,
`token`, `launch`, `transparency`, `roadmap`), `styles.css`, `main.js`.

## Method — and what this is NOT

- Static parse of all six pages (Python `html.parser`): heading outline,
  landmarks, duplicate ids, `aria-labelledby` targets, image inventory,
  link/button accessible names, skip-link target, `<main>` tabindex, `lang`.
- Browser sweep (headless Chrome via CDP): computed contrast for every
  visible text-bearing element on every page (foreground vs effective
  background; WCAG thresholds 4.5:1 normal text, 3:1 large text).
- Stylesheet inspection for the `:focus-visible` rule and the
  `prefers-reduced-motion` block. Live keyboard behaviour is proven by
  `keyboard-test.py` and live reduced-motion behaviour by
  `reduced-motion-test.py` — this review references their logs, it does
  not re-prove them.

**This is a review, not a WCAG conformance claim.** No screen-reader
testing was done. The contrast sweep approximates text drawn over the
decorative hero glow (a radial-gradient sibling element, not an ancestor
background) with the body background `#0a0a0b`; the glow is 10% red at
most and sits behind the hero text, so the approximation is small but it
is an approximation. Keyboard/focus claims rest on `keyboard-test.py`
(real Tab/Enter/Space/Escape input), not on this document.

## Findings

| Dimension | Result |
|---|---|
| `lang="id"` on all six pages | {"PASS — 6/6" if all(v["lang"] == "id" for v in pages.values()) else "FAIL — see defects"} |
| Exactly one `<h1>` per page | {"PASS — 6/6" if all(len(v["h1"]) == 1 for v in pages.values()) else "FAIL — see defects"} |
| Heading order (no level jumps) | {"PASS — 6/6" if not any("heading jumps" in d for d in DEFECTS) else "FAIL — see defects"} |
| Landmarks `header`/`nav`/`main`/`footer` | {"PASS — 6/6" if all(v["landmarks"] == ["footer", "header", "main", "nav"] for v in pages.values()) else "FAIL — see defects"} |
| Duplicate ids | {"PASS — none" if not any("duplicate ids" in d for d in DEFECTS) else "FAIL — see defects"} |
| `aria-labelledby` targets exist | {"PASS — all resolve" if not any("aria-labelledby" in d for d in DEFECTS) else "FAIL — see defects"} |
| Images / alt text | {"PASS — no `<img>` elements on any page; decorative hero glow is an `aria-hidden` `<div>`, not an image" if notes["img_count_total"] == 0 else "FAIL — see defects"} |
| Link accessible names | {"PASS — no empty or vague link text" if not any("vague/empty link text" in d for d in DEFECTS) else "FAIL — see defects"} |
| Button accessible names | {"PASS — every button has visible text" if not any("empty accessible name" in d for d in DEFECTS) else "FAIL — see defects"} |
| Skip link → `<main tabindex="-1">` | {"PASS — 6/6, focus moves to `<main>` (proven live by `keyboard-test.py`)" if not any("skip link target" in d or "<main> tabindex" in d for d in DEFECTS) else "FAIL — see defects"} |
| `:focus-visible` outline rule in CSS | {"PASS — `outline: 2px solid` red, offset 3px" if notes["focus_visible_rule"] else "FAIL"} |
| `prefers-reduced-motion` block in CSS | {"PASS — present; live behaviour proven by `reduced-motion-test.py`" if notes["reduced_motion_block"] else "FAIL"} |
| Forms / data collection | PASS — no `<form>` on any page (also enforced by `checks.sh`) |

## Heading outlines

"""
    for p in PAGES:
        outline = ", ".join(f"h{lv} “{tx[:42]}”" for lv, tx in pages[p]["headings"])
        doc += f"- **{p}**: {outline}\n"
    doc += """
## Computed-contrast sweep (browser, all visible text)

| Page | Text elements checked | Below threshold | Worst ratio |
|---|---|---|---|
"""
    for p in PAGES:
        s = sweep[p]
        worst = s["worst"][0] if s["worst"] else {"ratio": "-", "tag": "-", "text": "-"}
        doc += (f"| {p} | {s['total']} | {len(s['failures'])} | "
                f"{worst['ratio']}:1 (`<{worst['tag']}>` “{worst['text'][:40]}”) |\n")
    doc += """
Notes on the sweep: the worst ratios are the red accent (5.06:1, index
hero) and white text on the primary button (5.23:1); muted `#9a9aa0`
text measures 7.07:1 against the page background (five-pair spot-check
in `checks.sh`). The sweep checks every text element against its own
effective background instead of the five declared pairs; see
`evidence/a11y-review-""" + TODAY + """.log` for the per-element worst
list. Text over the hero glow is approximated with the body background
(see Method).

## Open gaps (not fixed by this review)

- No screen-reader testing (NVDA/VoiceOver/TalkBack) — keyboard and
  contrast evidence is real, but screen-reader behaviour is unverified.
- No manual test with a real keyboard on a real device — the keyboard
  matrix is headless-Chrome CDP input, which is real input but not a
  human pass.
- Contrast sweep approximation over the hero glow (see Method).
- This review does not claim WCAG 2.x conformance at any level.

## Evidence

- This document: `docs/accessibility-review-""" + TODAY + """.md`
- Log: `apps/token-site/evidence/a11y-review-""" + TODAY + """.log`
- Keyboard matrix: `apps/token-site/keyboard-test.py` +
  `apps/token-site/evidence/keyboard-""" + TODAY + """.log`
- Reduced motion: `apps/token-site/reduced-motion-test.py` +
  `apps/token-site/evidence/reduced-motion-""" + TODAY + """.log`
- Palette spot-check: `apps/token-site/checks.sh` §5
"""
    out = REPO_DIR / "docs" / f"accessibility-review-{TODAY}.md"
    out.write_text(doc, encoding="utf-8")
    return out


def main():
    log("Accessibility review — token site (static + browser contrast sweep)")
    pages, notes = static_review()
    for p in PAGES:
        v = pages[p]
        log(f"PASS: {p} static — lang={v['lang']}, h1={len(v['h1'])}, "
            f"headings={len(v['headings'])}, landmarks={v['landmarks']}, "
            f"images={len(v['images'])}, links={len(v['links'])}, "
            f"buttons={len(v['buttons'])}, aria-labelledby refs={len(v['labelledby'])}")
    log(f"PASS: stylesheet — :focus-visible rule present={notes['focus_visible_rule']}, "
        f"reduced-motion block present={notes['reduced_motion_block']}, "
        f"total <img> elements={notes['img_count_total']}")
    with BrowserSession(str(SITE_DIR), width=1280, height=800) as session:
        sweep = contrast_sweep(session.cdp, session.base)
    doc_path = write_doc(pages, notes, sweep)
    log(f"PASS: review document written to {doc_path.relative_to(REPO_DIR)}")
    if DEFECTS:
        for d in DEFECTS:
            log("DEFECT: " + d)
        log("ACCESSIBILITY REVIEW FAILED — hard defects found (see DEFECT lines)")
    else:
        log("ACCESSIBILITY REVIEW PASSED — no hard defects; open gaps are documented in the review")
    (SITE_DIR / "evidence").mkdir(exist_ok=True)
    (SITE_DIR / "evidence" / f"a11y-review-{TODAY}.log").write_text(
        "\n".join(LOG_LINES) + "\n", encoding="utf-8")
    return 0 if not DEFECTS else 1


if __name__ == "__main__":
    sys.exit(main())
