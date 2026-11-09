#!/usr/bin/env bash
# POLITIK RIUH — token-site reproducible local checks (PR-013).
# Zero dependencies beyond python3, curl, node (all already on the machine).
# Usage: bash checks.sh (from apps/token-site/)
# Exit code 0 = all checks pass. Any failure prints FAIL and exits non-zero.
# Screenshots are NOT produced here; see screenshots.sh.
# Server port: allocated dynamically from a free port (never a fixed 8000);
# the spawned server's PID is verified to own the listener before any
# HTTP result is accepted, so an unrelated process can never false-pass.
set -u
cd "$(dirname "$0")"

FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=1; }

free_port() {
  python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()'
}

# --- 1. Serve the site locally on a dynamically allocated port -----------
PORT="$(free_port)"
echo "INFO: allocated free port $PORT"
python3 -m http.server "$PORT" --bind 127.0.0.1 >/tmp/token-site-server.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
BASE="http://127.0.0.1:${PORT}"

# Readiness polling with timeout (15 s): wait until OUR server answers.
READY=0
for _ in $(seq 1 30); do
  if curl -fs -o /dev/null "$BASE/index.html" 2>/dev/null; then READY=1; break; fi
  sleep 0.5
done
[ "$READY" = 1 ] || { fail "server did not become ready on port $PORT within 15s"; echo "CHECKS FAILED (see FAIL lines above)"; exit 1; }

# Verify the spawned server PID owns the listener on $PORT (when `ss` exists).
# A collision with an unrelated process is a hard FAIL, not a silent pass.
if command -v ss >/dev/null 2>&1; then
  LISTENER_PID="$(ss -ltnpH "sport = :$PORT" 2>/dev/null | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2)"
  if [ -z "$LISTENER_PID" ]; then
    fail "no listener found on port $PORT (ss)"
  elif [ "$LISTENER_PID" != "$SERVER_PID" ]; then
    fail "port $PORT is owned by pid $LISTENER_PID, not our server pid $SERVER_PID"
  else
    pass "spawned server pid $SERVER_PID owns listener on 127.0.0.1:$PORT"
  fi
else
  echo "INFO: 'ss' not available; listener ownership not verified (dynamic free port + content checks still apply)"
fi

# --- 2. Route smoke test: 8/8 HTTP 200 + expected content -----------------
# HTTP 200 alone is not proof: each route must also contain its expected
# marker text, so a wrong server answering 200 still fails.
declare -A EXPECTED=(
  ["index.html"]="Belum diluncurkan"
  ["about.html"]="bukan portal berita"
  ["token.html"]="Token belum dibuat"
  ["launch.html"]="Nama token disetujui"
  ["transparency.html"]="belum difinalisasi"
  ["roadmap.html"]="Nama token REFORMASI disetujui"
  ["styles.css"]="--"
  ["main.js"]="data-nav-toggle"
)
OK=0
for r in "index.html" "about.html" "token.html" "launch.html" "transparency.html" "roadmap.html" "styles.css" "main.js"; do
  BODY="$(curl -fs "$BASE/$r" 2>/dev/null)" || { fail "route /$r did not return HTTP 200"; continue; }
  MARKER="${EXPECTED[$r]}"
  case "$BODY" in
    *"$MARKER"*) OK=$((OK+1)) ;;
    *) fail "route /$r returned 200 but lacks expected content: $MARKER" ;;
  esac
done
[ "$OK" = 8 ] && pass "route smoke test 8/8 HTTP 200 with expected page content"

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
        self.h1 = 0; self.headings = []; self.ids = []; self.landmarks = set()
        self.links = []; self.lang = None; self.in_html = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html": self.lang = d.get("lang")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"): self.headings.append(int(tag[1]))
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
    previous_heading = 0
    for level in parser.headings:
        if previous_heading and level > previous_heading + 1:
            fails.append(f"{p}: heading level jumps from h{previous_heading} to h{level}")
        previous_heading = level
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

# Negative regression assertions (PR-013 acceptance criteria 1-5):
# these exact regressions must fail the run if they ever return.
if re.search(r"\bRama\b", all_text):
    fails.append("founder's personal name 'Rama' present in public copy (team is anonymous)")
if re.search(r"0[,.]02\s*SOL", all_text):
    fails.append("unverified launch-cost estimate '0,02 SOL' present in public copy")
# Present-tense newsroom capability claims: news monitoring / source
# verification must only ever appear as explicitly future/planned scope.
for pat in (r"memantau\s+berita", r"pemantauan\s+berita", r"memverifikasi\s+sumber",
            r"verifikasi\s+sumber", r"memantau\s+isu", r"portal\s+berita\s+kami"):
    if re.search(pat, all_text, re.IGNORECASE):
        fails.append(f"present-tense newsroom claim present in public copy: {pat}")
# Gate 01 must be narrowed to the approved token NAME only.
if "Konsep disetujui" in all_text or "Keputusan konsep token" in all_text:
    fails.append("Gate 01 still claims the whole token concept is approved (only the name is)")
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
print("PASS: negative regressions — no .wallet-status, no founder name, no 0,02 SOL estimate, no present-tense newsroom claims, Gate 01 narrowed to token name")
print("PASS: no forms, fetch/XHR/storage, wallet signing, or secret patterns in site source")
PYEOF
[ $? -ne 0 ] && FAIL=1

# --- 4. JS syntax ----------------------------------------------------------
node --check main.js && pass "node --check main.js" || fail "node --check main.js"

# --- 5. Contrast: five-pair palette spot-check (NOT a full WCAG audit) -----
# This checks five declared foreground/background pairs only. It does not
# establish full-page WCAG AA compliance or keyboard/focus behaviour; do not
# describe it as a complete audit. Manual keyboard/focus matrix: Tab through
# each page, toggle opens/closes with Enter/Space, focus ring visible on
# every link/button (see README "Keterbatasan yang diketahui").
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
