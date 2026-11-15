#!/usr/bin/env python3
"""Reduced-motion verification for the token site (stdlib only, no deps).

Proves the `prefers-reduced-motion: reduce` media query in styles.css
actually changes browser behaviour, using CDP Emulation.setEmulatedMedia
-- not just a grep of the stylesheet. Control (no-preference) vs emulated
`reduce`, on the landing page:
  - matchMedia('(prefers-reduced-motion: reduce)').matches
  - computed scroll-behavior on <html> (smooth vs auto)
  - computed transition-duration on .skip-link (0.15s vs 0s)
    (.skip-link is the only element with a CSS transition)
Then restores no-preference and verifies behaviour flips back, proving
the change is driven by the emulation and not a static artifact.

Usage: python3 reduced-motion-test.py   (from apps/token-site/)
Exit 0 = every assertion passes. Writes the same output to
evidence/reduced-motion-YYYY-MM-DD.log.
"""
import datetime
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp_helper import BrowserSession

SITE_DIR = Path(__file__).resolve().parent
TODAY = datetime.date.today().isoformat()

PROBE = """(() => {
  const sl = document.querySelector('.skip-link');
  const cs = getComputedStyle(sl);
  return JSON.stringify({
    matchesReduce: matchMedia('(prefers-reduced-motion: reduce)').matches,
    scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
    skipTransitionDuration: cs.transitionDuration,
    skipTransitionProperty: cs.transitionProperty
  });
})()"""

LOG_LINES = []


def log(msg):
    print(msg)
    LOG_LINES.append(msg)


def check(name, ok, detail=""):
    log(("PASS: " if ok else "FAIL: ") + name + (f" — {detail}" if detail else ""))
    return ok


def main():
    all_ok = True
    log("Reduced-motion test — token site (CDP media emulation)")
    with BrowserSession(str(SITE_DIR), width=1280, height=800) as session:
        cdp = session.cdp
        control = json.loads(cdp.evaluate(PROBE))
        all_ok &= check("control (no-preference): reduce does not match",
                        control["matchesReduce"] is False, str(control))
        all_ok &= check("control: html scroll-behavior is smooth",
                        control["scrollBehavior"] == "smooth", str(control))
        all_ok &= check("control: skip-link transition is 0.15s",
                        control["skipTransitionDuration"] == "0.15s", str(control))
        cdp.call("Emulation.setEmulatedMedia", {
            "features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        time.sleep(0.3)
        reduced = json.loads(cdp.evaluate(PROBE))
        all_ok &= check("emulated reduce: media query matches",
                        reduced["matchesReduce"] is True, str(reduced))
        all_ok &= check("emulated reduce: html scroll-behavior becomes auto",
                        reduced["scrollBehavior"] == "auto", str(reduced))
        all_ok &= check("emulated reduce: skip-link transition becomes 0s (none)",
                        reduced["skipTransitionDuration"] == "0s"
                        and reduced["skipTransitionProperty"] == "none",
                        str(reduced))
        cdp.call("Emulation.setEmulatedMedia", {
            "features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
        time.sleep(0.3)
        restored = json.loads(cdp.evaluate(PROBE))
        all_ok &= check("restored no-preference: behaviour flips back",
                        restored["matchesReduce"] is False
                        and restored["scrollBehavior"] == "smooth"
                        and restored["skipTransitionDuration"] == "0.15s",
                        str(restored))
    log("REDUCED-MOTION TEST PASSED" if all_ok
        else "REDUCED-MOTION TEST FAILED (see FAIL lines above)")
    (SITE_DIR / "evidence").mkdir(exist_ok=True)
    (SITE_DIR / "evidence" / f"reduced-motion-{TODAY}.log").write_text(
        "\n".join(LOG_LINES) + "\n", encoding="utf-8")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
