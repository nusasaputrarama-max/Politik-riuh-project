#!/usr/bin/env bash
# POLITIK RIUH — token-site screenshot refresh (PR-013).
# Usage: bash screenshots.sh   (from apps/token-site/)
# Serves the site locally, captures headless-Chrome screenshots into evidence/,
# then stops the server. Exit code 0 = all screenshots produced.
# Chrome: ~/chrome-extract/opt/google/chrome/chrome (Chrome 157, extracted .deb).
set -u
cd "$(dirname "$0")"

CHROME="${CHROME:-$HOME/chrome-extract/opt/google/chrome/chrome}"
PORT="${PORT:-8000}"
FAIL=0
[ -x "$CHROME" ] || { echo "FAIL: Chrome not found at $CHROME"; exit 1; }

python3 -m http.server "$PORT" --bind 127.0.0.1 >/tmp/token-site-server-shots.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
sleep 1
BASE="http://127.0.0.1:${PORT}"

shot() { # $1=url $2=outfile $3=width $4=height
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size="$3,$4" --screenshot="evidence/$2" "$1" \
    >/tmp/token-site-chrome.log 2>&1
  if [ -s "evidence/$2" ]; then echo "PASS: evidence/$2 ($3x$4)"; else echo "FAIL: evidence/$2"; FAIL=1; fi
}

shot "$BASE/index.html" landing-desktop.png 1280 2600
shot "$BASE/index.html" landing-mobile.png 390 3800
shot "$BASE/about.html" about-desktop.png 1280 1000
shot "$BASE/token.html" token-desktop.png 1280 1000
shot "$BASE/launch.html" launch-desktop.png 1280 1000
shot "$BASE/transparency.html" transparency-desktop.png 1280 1000
shot "$BASE/roadmap.html" roadmap-desktop.png 1280 1000

exit "$FAIL"
