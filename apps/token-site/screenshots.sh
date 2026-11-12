#!/usr/bin/env bash
# POLITIK RIUH — token-site screenshot refresh (PR-013).
# Usage: bash screenshots.sh   (from apps/token-site/)
# Serves the site locally on a dynamically allocated port, captures
# extended-height headless-Chrome viewport screenshots into evidence/ (6 desktop + 6 mobile),
# then stops the server. Exit code 0 = all screenshots produced fresh.
# A capture FAILS unless: the old file was deleted first, Chrome exits 0,
# the new file is non-empty, and it is a valid PNG with expected dimensions.
# Stale screenshots can therefore never be reported as a fresh PASS.
# Chrome: ~/chrome-extract/opt/google/chrome/chrome (Chrome 157, extracted .deb),
# or $CHROME when set (CI uses the setup-chrome binary).
set -u
cd "$(dirname "$0")"

CHROME="${CHROME:-$HOME/chrome-extract/opt/google/chrome/chrome}"
FAIL=0
[ -x "$CHROME" ] || { echo "FAIL: Chrome not found at $CHROME"; exit 1; }
command -v file >/dev/null 2>&1 || { echo "FAIL: 'file' command not found (needed to validate PNG dimensions)"; exit 1; }

free_port() {
  python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()'
}

PORT="$(free_port)"
echo "INFO: allocated free port $PORT"
python3 -m http.server "$PORT" --bind 127.0.0.1 >/tmp/token-site-server-shots.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
BASE="http://127.0.0.1:${PORT}"

# Readiness polling with timeout (15 s).
READY=0
for _ in $(seq 1 30); do
  if curl -fs -o /dev/null "$BASE/index.html" 2>/dev/null; then READY=1; break; fi
  sleep 0.5
done
[ "$READY" = 1 ] || { echo "FAIL: server did not become ready on port $PORT within 15s"; exit 1; }

# Verify the spawned server PID owns the listener on $PORT (when `ss` exists).
if command -v ss >/dev/null 2>&1; then
  LISTENER_PID="$(ss -ltnpH "sport = :$PORT" 2>/dev/null | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2)"
  if [ "$LISTENER_PID" != "$SERVER_PID" ]; then
    echo "FAIL: port $PORT listener pid is '${LISTENER_PID:-none}', not our server pid $SERVER_PID"
    exit 1
  fi
  echo "PASS: spawned server pid $SERVER_PID owns listener on 127.0.0.1:$PORT"
else
  echo "INFO: 'ss' not available; listener ownership not verified (dynamic free port still applies)"
fi

shot() { # $1=url $2=outfile $3=width $4=height
  rm -f "evidence/$2"
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=5000 \
    --window-size="$3,$4" --screenshot="evidence/$2" "$1" \
    >/tmp/token-site-chrome.log 2>&1
  CHROME_RC=$?
  if [ "$CHROME_RC" -ne 0 ]; then
    echo "FAIL: evidence/$2 — Chrome exited $CHROME_RC"; FAIL=1; return
  fi
  if [ ! -s "evidence/$2" ]; then
    echo "FAIL: evidence/$2 — missing or empty after Chrome exit 0"; FAIL=1; return
  fi
  DIMS="$(file "evidence/$2")"
  case "$DIMS" in
    *"PNG image data, $3 x $4"*) echo "PASS: evidence/$2 (${3}x${4})" ;;
    *) echo "FAIL: evidence/$2 — unexpected image: $DIMS"; FAIL=1 ;;
  esac
}

shot "$BASE/index.html" landing-desktop.png 1280 3000
shot "$BASE/index.html" landing-mobile.png 390 4500
shot "$BASE/about.html" about-desktop.png 1280 3000
shot "$BASE/about.html" about-mobile.png 390 4500
shot "$BASE/token.html" token-desktop.png 1280 3000
shot "$BASE/token.html" token-mobile.png 390 4500
shot "$BASE/launch.html" launch-desktop.png 1280 3000
shot "$BASE/launch.html" launch-mobile.png 390 4500
shot "$BASE/transparency.html" transparency-desktop.png 1280 3000
shot "$BASE/transparency.html" transparency-mobile.png 390 4500
shot "$BASE/roadmap.html" roadmap-desktop.png 1280 3000
shot "$BASE/roadmap.html" roadmap-mobile.png 390 4500

if [ "$FAIL" = 0 ]; then echo "ALL SCREENSHOTS PASSED (12/12)"; else echo "SCREENSHOTS FAILED (see FAIL lines above)"; fi
exit "$FAIL"
