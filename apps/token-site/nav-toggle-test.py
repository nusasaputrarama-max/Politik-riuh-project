#!/usr/bin/env python3
"""Minimal CDP nav-toggle test for the token site (stdlib only, no deps).
Starts a local server + headless Chrome on dynamically allocated free ports,
verifies the spawned server owns its listener and serves the expected page,
clicks the mobile nav toggle via Runtime.evaluate, and prints NAV-OPEN /
ARIA / LABEL. Exit 0 on pass.
Usage: python3 nav-toggle-test.py [url]  (default http://127.0.0.1:<free-port>/index.html)
"""
import base64, hashlib, json, os, re, shutil, socket, struct, subprocess, sys, tempfile, time, urllib.request

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]; s.close(); return port

def listener_pid(port):
    """PID owning the 127.0.0.1:port listener, via `ss` (None if unavailable)."""
    try:
        out = subprocess.run(["ss", "-ltnpH", f"sport = :{port}"],
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return None
    m = re.search(r"pid=(\d+)", out)
    return int(m.group(1)) if m else None

CHROME = os.environ.get("CHROME", os.path.expanduser("~/chrome-extract/opt/google/chrome/chrome"))
HTTP_PORT = free_port()
CDP_PORT = free_port()
while CDP_PORT == HTTP_PORT:
    CDP_PORT = free_port()
URL = sys.argv[1] if len(sys.argv) > 1 else f"http://127.0.0.1:{HTTP_PORT}/index.html"

_WS_LEFTOVER = {}

def ws_connect(ws_url):
    # ws://127.0.0.1:<cdp-port>/devtools/page/<id>
    assert ws_url.startswith("ws://")
    rest = ws_url[5:]
    hostport, path = rest.split("/", 1)
    host, port = hostport.split(":")
    key = base64.b64encode(os.urandom(16)).decode()
    s = socket.create_connection((host, int(port)), timeout=30)
    req = (f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        buf += s.recv(4096)
    assert b"101" in buf.split(b"\r\n")[0], buf[:200]
    # Keep any bytes already received past the HTTP headers: the first
    # WebSocket frame may arrive coalesced with the handshake response,
    # and dropping it would hang the first CDP call until socket timeout.
    _WS_LEFTOVER[id(s)] = buf.split(b"\r\n\r\n", 1)[1]
    return s

def ws_send(s, text):
    payload = text.encode()
    header = bytearray([0x81])
    n = len(payload)
    if n < 126:
        header.append(0x80 | n)
    elif n < 65536:
        header.append(0x80 | 126); header += struct.pack(">H", n)
    else:
        header.append(0x80 | 127); header += struct.pack(">Q", n)
    mask = os.urandom(4)
    header += mask
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    s.sendall(bytes(header) + masked)

def ws_recv_msg(s):
    data = _WS_LEFTOVER.pop(id(s), b"")
    while True:
        # read 2-byte header
        while len(data) < 2:
            chunk = s.recv(4096)
            if not chunk: raise ConnectionError("ws closed")
            data += chunk
        fin = data[0] & 0x80; op = data[0] & 0x0F
        ln = data[1] & 0x7F; off = 2
        if ln == 126:
            while len(data) < 4: data += s.recv(4096)
            ln = struct.unpack(">H", data[2:4])[0]; off = 4
        elif ln == 127:
            while len(data) < 10: data += s.recv(4096)
            ln = struct.unpack(">Q", data[2:10])[0]; off = 10
        while len(data) < off + ln:
            data += s.recv(65536)
        payload = data[off:off+ln]; data = data[off+ln:]
        if op == 9:  # ping -> pong
            s.sendall(bytes([0x8A, 0x80]) + os.urandom(4))
            continue
        if op == 1:
            # Preserve any trailing bytes: Chrome may coalesce several
            # frames into one TCP segment, and the next message is already
            # in `data`. Dropping it would hang the next recv until timeout.
            _WS_LEFTOVER[id(s)] = data
            return payload.decode()
        if op == 8:
            raise ConnectionError("ws closed by peer")
        if op == 0:
            continue

def cdp(s, mid, method, params=None):
    ws_send(s, json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws_recv_msg(s))
        if msg.get("id") == mid:
            if "error" in msg: raise RuntimeError(msg["error"])
            return msg.get("result", {})

# Unique profile dir per run: a stale/shared default profile can make a
# second Chrome instance attach to (or block on) another process.
PROFILE_DIR = tempfile.mkdtemp(prefix="token-site-chrome-")
server = None
chrome = None
try:
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(HTTP_PORT), "--bind", "127.0.0.1"],
                              cwd=os.getcwd(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Readiness polling with timeout (15 s) + content check: the server must
    # answer with OUR page, not just any HTTP 200 on a colliding port.
    ready = False
    for _ in range(30):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{HTTP_PORT}/index.html", timeout=2) as r:
                if r.status == 200 and b"REFORMASI" in r.read():
                    ready = True; break
        except Exception:
            time.sleep(0.5)
    assert ready, f"server did not serve expected content on port {HTTP_PORT} within 15s"
    owner = listener_pid(HTTP_PORT)
    if owner is not None:
        assert owner == server.pid, f"port {HTTP_PORT} owned by pid {owner}, not our server pid {server.pid}"
        print(f"PASS: spawned server pid {server.pid} owns listener on 127.0.0.1:{HTTP_PORT} (CDP port {CDP_PORT})")
    else:
        print(f"INFO: 'ss' unavailable; listener ownership not verified (dynamic free port {HTTP_PORT} + content check still apply)")
    chrome = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                               f"--user-data-dir={PROFILE_DIR}",
                               f"--remote-debugging-port={CDP_PORT}", "--window-size=390,844", URL],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    target = None
    for _ in range(30):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=2))
            target = next((t for t in tabs if t.get("type") == "page" and t.get("url") == URL), None)
            if target:
                break
        except Exception:
            time.sleep(0.5)
    assert target, f"no CDP page target matching {URL!r}"
    s = ws_connect(target["webSocketDebuggerUrl"])
    cdp(s, 1, "Runtime.enable")
    page_ready = False
    for _ in range(20):
        r = cdp(s, 9, "Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True})
        if r.get("result", {}).get("value") == "complete":
            page_ready = True
            break
        time.sleep(0.5)
    assert page_ready, f"page did not reach readyState=complete at {URL!r}"
    controls_ready = False
    for _ in range(20):
        r = cdp(s, 10, "Runtime.evaluate", {
            "expression": "!!document.querySelector('[data-nav-toggle]') && !!document.getElementById('site-nav')",
            "returnByValue": True
        })
        if r.get("result", {}).get("value") is True:
            controls_ready = True
            break
        time.sleep(0.25)
    assert controls_ready, f"nav controls not found at {URL!r}"
    expr = ("(()=>{const t=document.querySelector('[data-nav-toggle]');"
            "const n=document.getElementById('site-nav');"
            "if(!t||!n)return 'FAIL:missing nav controls';"
            "const initial=t.getAttribute('aria-expanded')==='false'&&t.getAttribute('aria-controls')==='site-nav'&&t.textContent==='Menu';"
            "t.click();"
            "const opened=n.classList.contains('is-open')&&t.getAttribute('aria-expanded')==='true'&&t.textContent==='Tutup menu';"
            "t.click();"
            "const closed=!n.classList.contains('is-open')&&t.getAttribute('aria-expanded')==='false'&&t.textContent==='Menu';"
            "return 'INITIAL='+initial+' OPEN='+opened+' CLOSED='+closed;})()")
    r = cdp(s, 2, "Runtime.evaluate", {"expression": expr, "returnByValue": True})
    if "exceptionDetails" in r:
        print("FAIL: evaluate exception:", json.dumps(r["exceptionDetails"])[:500]); sys.exit(1)
    out = r["result"]["value"]
    print(out)
    ok = out == "INITIAL=true OPEN=true CLOSED=true"
    print("PASS: nav toggle initial/open/close states and ARIA labels are correct" if ok else "FAIL: unexpected toggle state")
    sys.exit(0 if ok else 1)
finally:
    for proc in (chrome, server):
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
            except ProcessLookupError:
                pass
    for proc in (chrome, server):
        if proc is not None:
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
    shutil.rmtree(PROFILE_DIR, ignore_errors=True)
