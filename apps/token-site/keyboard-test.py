#!/usr/bin/env python3
"""Keyboard-only coverage for the token site (stdlib only, no deps).

Real keyboard input via CDP Input.dispatchKeyEvent against headless
Chrome -- NOT clicks through Runtime.evaluate. Covers, on all six pages:
  - Tab order (first stop, nav links in DOM order, full-set equality
    against the visible focusable elements in the DOM)
  - skip link (visible on focus, Enter moves focus to <main>)
  - visible focus indicator on every Tab stop (:focus-visible outline)
  - Enter/Space activation of the mobile nav toggle
  - Escape closes an open menu and returns focus to the toggle
  - Enter on a nav link navigates to the linked page
  - Shift+Tab moves focus backwards
Desktop viewport 1280x800 for Tab order; mobile viewport 390x844 for
the toggle (the toggle is display:none on desktop).

Usage: python3 keyboard-test.py   (from apps/token-site/)
Exit 0 = every check passes on every page. Writes the same output to
evidence/keyboard-YYYY-MM-DD.log.
"""
import datetime
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp_helper import BrowserSession

SITE_DIR = Path(__file__).resolve().parent
PAGES = ["index.html", "about.html", "token.html", "launch.html", "transparency.html", "roadmap.html"]
NAV_LABELS = ["Tentang", "Token", "Peluncuran", "Transparansi", "Peta Jalan"]
TODAY = datetime.date.today().isoformat()

DESCRIBE_ACTIVE = """(() => {
  const el = document.activeElement;
  if (!el || el === document.body) return 'BODY';
  const t = el.tagName.toLowerCase();
  const id = el.id ? '#' + el.id : '';
  const txt = (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 40);
  const href = el.getAttribute('href') || '';
  return t + id + ' :: ' + txt + (href ? ' -> ' + href : '');
})()"""

FOCUSABLE_LIST = """(() => {
  const desc = el => {
    const t = el.tagName.toLowerCase();
    const id = el.id ? '#' + el.id : '';
    const txt = (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 40);
    const href = el.getAttribute('href') || '';
    return t + id + ' :: ' + txt + (href ? ' -> ' + href : '');
  };
  return [...document.querySelectorAll('a[href], button, [tabindex]')]
    .filter(el => {
      if (el.tabIndex < 0) return false;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    })
    .map(desc);
})()"""

FOCUS_STYLE = """(() => {
  const el = document.activeElement;
  if (!el || el === document.body) return 'NONE';
  const cs = getComputedStyle(el);
  return cs.outlineStyle + '|' + cs.outlineWidth + '|' + cs.outlineColor;
})()"""

TOGGLE_STATE = """(() => {
  const t = document.querySelector('[data-nav-toggle]');
  const n = document.getElementById('site-nav');
  const cs = getComputedStyle(t);
  return JSON.stringify({
    visible: cs.display !== 'none',
    open: n.classList.contains('is-open'),
    expanded: t.getAttribute('aria-expanded'),
    label: t.textContent,
    focused: document.activeElement === t
  });
})()"""

LOG_LINES = []


def log(msg):
    print(msg)
    LOG_LINES.append(msg)


def check(name, ok, detail=""):
    log(("PASS: " if ok else "FAIL: ") + name + (f" — {detail}" if detail else ""))
    return ok


def tab_sweep(cdp, page):
    """Press Tab until focus cycles back to the first stop. Returns stops."""
    stops = []
    for _ in range(80):
        cdp.press_tab()
        d = cdp.evaluate(DESCRIBE_ACTIVE)
        if d == "BODY":
            break
        if stops and d == stops[0]:
            break
        stops.append(d)
    return stops


def desktop_page(cdp, base, page):
    """Tab order + skip link + focus visibility on one page (desktop)."""
    ok = True
    url = f"{base}/{page}"
    cdp.navigate(url)
    expected = cdp.evaluate(FOCUSABLE_LIST)
    stops = tab_sweep(cdp, page)
    ok &= check(f"{page} tab sweep reaches {len(expected)} focusable stops",
                len(stops) == len(expected),
                f"tabbed {len(stops)} stops, DOM lists {len(expected)}")
    if stops:
        ok &= check(f"{page} first Tab stop is the skip link",
                    stops[0].startswith("a :: Lewati ke konten"),
                    stops[0])
    # Header nav links are stops 3-7 (after skip link + wordmark). The
    # footer legitimately repeats the same labels, so only the header
    # run is asserted here; full-set equality above covers the rest.
    header_nav = [next((lb for lb in NAV_LABELS if f" :: {lb} -> " in s), "?")
                  for s in stops[2:7]]
    ok &= check(f"{page} header nav links in DOM order (stops 3-7)",
                header_nav == NAV_LABELS, " > ".join(header_nav))
    missing = [e for e in expected if e not in stops]
    extra = [s for s in stops if s not in expected]
    ok &= check(f"{page} tab set == DOM focusable set",
                not missing and not extra,
                f"missing={missing} extra={extra}")
    # Visible focus on every stop: re-walk and read the computed outline.
    cdp.navigate(url)
    bad_focus = []
    for i in range(len(stops)):
        cdp.press_tab()
        style = cdp.evaluate(FOCUS_STYLE)
        if style != "solid|2px|rgb(229, 72, 77)":
            bad_focus.append(f"stop {i + 1}: {style}")
    ok &= check(f"{page} visible focus (2px solid red outline) on every stop",
                not bad_focus, "; ".join(bad_focus[:3]))
    # Skip link: fresh load, one Tab, Enter moves focus to <main>.
    cdp.navigate(url)
    cdp.press_tab()
    top = cdp.evaluate("getComputedStyle(document.querySelector('.skip-link')).top")
    ok &= check(f"{page} skip link becomes visible on focus",
                top == "12px", f"top={top}")
    cdp.press_enter()
    import time
    time.sleep(0.5)
    active = cdp.evaluate(DESCRIBE_ACTIVE)
    href_hash = cdp.evaluate("location.hash")
    ok &= check(f"{page} skip-link Enter moves focus to <main>",
                active.startswith("main#main") and href_hash == "#main",
                f"active={active} hash={href_hash}")
    return ok


def desktop_extra(cdp, base):
    """Shift+Tab backwards + Enter on a nav link navigates (index.html)."""
    ok = True
    url = f"{base}/index.html"
    cdp.navigate(url)
    cdp.press_tab()  # skip link
    cdp.press_tab()  # wordmark
    cdp.press_tab()  # Tentang
    d = cdp.evaluate(DESCRIBE_ACTIVE)
    ok &= check("index Tab x3 lands on nav link Tentang",
                d.startswith("a :: Tentang"), d)
    # Shift+Tab: keyDown Tab with Shift modifier (8), then keyUp.
    cdp.call("Input.dispatchKeyEvent",
             {"type": "keyDown", "key": "Tab", "code": "Tab",
              "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9, "modifiers": 8})
    import time
    time.sleep(0.05)
    cdp.call("Input.dispatchKeyEvent",
             {"type": "keyUp", "key": "Tab", "code": "Tab",
              "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9, "modifiers": 8})
    time.sleep(0.12)
    d = cdp.evaluate(DESCRIBE_ACTIVE)
    ok &= check("index Shift+Tab moves focus back to the wordmark",
                d.startswith("a :: POLITIK RIUH"), d)
    # Enter on the Tentang nav link navigates to about.html.
    cdp.press_tab()  # back to Tentang
    d = cdp.evaluate(DESCRIBE_ACTIVE)
    ok &= check("index focus is on Tentang before Enter",
                d.startswith("a :: Tentang"), d)
    cdp.press_enter()
    arrived = False
    for _ in range(20):
        if cdp.evaluate("location.href").endswith("/about.html"):
            arrived = True
            break
        time.sleep(0.25)
    ok &= check("index Enter on nav link Tentang navigates to about.html",
                arrived, cdp.evaluate("location.href"))
    return ok


def mobile_page(cdp, base, page):
    """Toggle open/close/Escape/focus-return on one page (mobile width)."""
    ok = True
    url = f"{base}/{page}"
    cdp.navigate(url)
    import json
    state = json.loads(cdp.evaluate(TOGGLE_STATE))
    ok &= check(f"{page} nav toggle is visible at mobile width",
                state["visible"] is True, str(state))
    # Tab until the toggle is focused (skip link, wordmark, then toggle).
    for _ in range(10):
        if cdp.evaluate(DESCRIBE_ACTIVE).startswith("button :: Menu"):
            break
        cdp.press_tab()
    d = cdp.evaluate(DESCRIBE_ACTIVE)
    ok &= check(f"{page} Tab reaches the nav toggle",
                d.startswith("button :: Menu"), d)
    cdp.press_space()
    state = json.loads(cdp.evaluate(TOGGLE_STATE))
    ok &= check(f"{page} Space opens the menu",
                state["open"] is True and state["expanded"] == "true"
                and state["label"] == "Tutup menu", str(state))
    cdp.press_tab()
    d = cdp.evaluate(DESCRIBE_ACTIVE)
    ok &= check(f"{page} Tab from open toggle reaches first nav link",
                d.startswith("a :: Tentang"), d)
    cdp.press_escape()
    state = json.loads(cdp.evaluate(TOGGLE_STATE))
    ok &= check(f"{page} Escape closes the menu AND returns focus to toggle",
                state["open"] is False and state["expanded"] == "false"
                and state["label"] == "Menu" and state["focused"] is True,
                str(state))
    cdp.press_enter()
    state = json.loads(cdp.evaluate(TOGGLE_STATE))
    ok &= check(f"{page} Enter opens the menu",
                state["open"] is True and state["expanded"] == "true", str(state))
    cdp.press_enter()
    state = json.loads(cdp.evaluate(TOGGLE_STATE))
    ok &= check(f"{page} Enter closes the menu again",
                state["open"] is False and state["expanded"] == "false", str(state))
    return ok


def main():
    all_ok = True
    log("Keyboard-only test — token site, all six pages")
    with BrowserSession(str(SITE_DIR), width=1280, height=800) as session:
        cdp, base = session.cdp, session.base
        for page in PAGES:
            all_ok &= desktop_page(cdp, base, page)
        all_ok &= desktop_extra(cdp, base)
    with BrowserSession(str(SITE_DIR), width=390, height=844) as session:
        cdp, base = session.cdp, session.base
        for page in PAGES:
            all_ok &= mobile_page(cdp, base, page)
    log("KEYBOARD TEST PASSED (all pages, desktop + mobile)" if all_ok
        else "KEYBOARD TEST FAILED (see FAIL lines above)")
    (SITE_DIR / "evidence").mkdir(exist_ok=True)
    (SITE_DIR / "evidence" / f"keyboard-{TODAY}.log").write_text(
        "\n".join(LOG_LINES) + "\n", encoding="utf-8")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
