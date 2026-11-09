#!/usr/bin/env bash
# POLITIK RIUH — token-site reproducible local checks (PR-013).
# Zero dependencies beyond python3, curl, node (all already on the machine).
# Usage:  bash checks.sh            (from apps/token-site/)
# Usage: bash checks.sh
# Exit code 0 = all checks pass. Any failure prints FAIL and exits non-zero.
# Screenshots are NOT produced here; see screenshots.sh.
set -u
cd "$(dirname "$0")"

PORT="${PORT:-8000}"
BASE="http://127.0.0.1:${PORT}"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=1; }

# --- 1. Serve the site locally -------------------------------------------
python3 -m http.server "$PORT" --bind 127.0.0.1 >/tmp/token-site-server.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
sleep 1

# --- 2. Route smoke test: 8/8 HTTP 200 ------------------------------------
ROUTES=( "/" "index.html" "about.html" "token.html" "launch.html" "transparency.html" "roadmap.html" "styles.css" "main.js" )
# "/" and "index.html" are the same resource; count distinct URLs served = 8
OK=0
for r in "index.html" "about.html" "token.html" "launch.html" "transparency.html" "roadmap.html" "styles.css" "main.js"; do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/$r")
  if [ "$CODE" = "200" ]; then OK=$((OK+1)); else fail "route /$r returned HTTP $CODE"; fi
done
[ "$OK" = 8 ] && pass "route smoke test 8/8 HTTP 200"

# --- 3. HTML + copy checks (python stdlib only) ---------------------------
python3 - <<'PYEOF'
import re, sys
from html.parser import HTMLParser
from pathlib import Path

pages = ["index.html", "about.html", "token.html", "launch.html", "transparency.html", "roadmap.html"]
fails = []

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0; self.ids = []; self.landmarks = set()
        self.links = []; self.lang = None; self.in_html = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html": self.lang = d.get("lang")
        if tag == "h1": self.h1 += 1
        if tag in ("header", "nav", "main", "footer"): self.landmarks.add(tag)
        if "id" in d: self.ids.append(d["id"])
        for a in ("href", "src"):
            if a in d: self.links.append(d[a])

for p in pages:
    text = Path(p).read_text(encoding="utf-8")
    parser = P(); parser.feed(text)
    if parser.lang != "id":
        fails.append(f"{p}: <html lang> is {parser.lang!r}, expected 'id'")
    if parser.h1 != 1:
        fails.append(f"{p}: {parser.h1} <h1> elements, expected exactly 1")
    if parser.landmarks != {"header", "nav", "main", "footer"}:
        fails.append(f"{p}: landmarks {sorted(parser.landmarks)}, expected header/nav/main/footer")
    dup = {i for i in parser.ids if parser.ids.count(i) > 1}
    if dup:
        fails.append(f"{p}: duplicate ids {sorted(dup)}")
    for link in parser.links:
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = link.split("#")[0].split("?")[0]
        if target and not Path(target).exists():
            fails.append(f"{p}: unresolved local link {link!r}")
    if "<form" in text.lower():
        fails.append(f"{p}: contains a <form> (static site must not collect data)")
    if re.search(r'class=["\'][^"\']*\bwallet-status\b', text) or "Koneksi baca-saja direncanakan" in text:
        fails.append(f"{p}: wallet-status UI is outside Phase 1 and must be absent")
    if re.search(r"\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage", text):
        fails.append(f"{p}: contains fetch/XHR/storage calls")
    if 'lang="en"' in text:
        fails.append(f"{p}: leftover lang=\"en\" attribute")

# Site-wide copy discipline
all_text = "\n".join(Path(p).read_text(encoding="utf-8") for p in pages)
for name in ("NENGOK", "GORENG", "DER"):
    # DER as a standalone word only; do not flag substrings.
    if re.search(rf"\b{name}\b", all_text):
        fails.append(f"stale candidate name {name} still present in public copy")
for phrase in ("To be decided", "Not launched", "Skip to content", "Read-only connect planned", "Koneksi baca-saja direncanakan"):
    if phrase in all_text:
        fails.append(f"leftover English participant copy: {phrase!r}")
if "REFORMASI" not in all_text:
    fails.append("token name REFORMASI missing from public copy")
if "Belum diluncurkan" not in all_text:
    fails.append("launch status 'Belum diluncurkan' missing")
if "belum dibuka" not in Path("launch.html").read_text(encoding="utf-8").lower():
    fails.append("launch.html does not state the whitelist is not yet open")
# No wallet/signing/transaction code anywhere in the site tree
site = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in Path(".").rglob("*") if p.is_file() and p.suffix in (".html", ".js", ".css") and "evidence" not in p.parts)
for pat in (r"signTransaction", r"signMessage", r"sendTransaction", r"connect\(\)", r"window\.solana", r"@solana/", r"api_key", r"sk-[A-Za-z0-9]{20,}"):
    if re.search(pat, site):
        fails.append(f"forbidden code/secret pattern in site source: {pat}")

if fails:
    for f in fails:
        print("FAIL:", f)
    sys.exit(1)
print("PASS: HTML parse 6/6 — lang=id, one <h1>, landmarks, no duplicate ids, links resolve")
print("PASS: copy discipline — no stale candidate names, no leftover English participant copy, REFORMASI identity present")
print("PASS: no forms, fetch/XHR/storage, wallet signing, or secret patterns in site source")
PYEOF
[ $? -ne 0 ] && FAIL=1

# --- 4. JS syntax ----------------------------------------------------------
node --check main.js && pass "node --check main.js" || fail "node --check main.js"

# --- 5. WCAG contrast spot-check (five declared palette pairs only) --------
python3 - <<'PYEOF'
def lum(hexs):
    r, g, b = (int(hexs[i:i+2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
pairs = [
    ("muted #9a9aa0 on bg #0a0a0b", "#9a9aa0", "#0a0a0b"),
    ("headline #fafafa on bg #0a0a0b", "#fafafa", "#0a0a0b"),
    ("red accent #e5484d on bg #0a0a0b", "#e5484d", "#0a0a0b"),
    ("white on primary button #c93338", "#ffffff", "#c93338"),
    ("white on primary button hover #be2e33", "#ffffff", "#be2e33"),
]
bad = False
for name, fg, bg in pairs:
    r = ratio(fg, bg)
    print(f"  contrast {name}: {r:.2f}:1")
    if r < 4.5:
        print(f"FAIL: contrast {name} below AA 4.5:1"); bad = True
import sys
sys.exit(1 if bad else 0)
PYEOF
[ $? -eq 0 ] && pass "contrast: five-pair palette spot-check passes WCAG AA; not a full page audit" || fail "contrast spot-check"

# --- 6. Summary ------------------------------------------------------------
if [ "$FAIL" = 0 ]; then
  echo "ALL CHECKS PASSED"
  exit 0
else
  echo "CHECKS FAILED (see FAIL lines above)"
  exit 1
fi
