#!/usr/bin/env python3
"""Minimal CDP nav-toggle test for the token site (stdlib only, no deps).
Starts a local server + headless Chrome, clicks the mobile nav toggle via
Runtime.evaluate, and prints NAV-OPEN / ARIA / LABEL. Exit 0 on pass.
Usage: python3 nav-toggle-test.py [url]  (default http://127.0.0.1:8000/index.html)
"""
import base64, hashlib, json, os, socket, struct, subprocess, sys, time, urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/index.html"
CHROME = os.environ.get("CHROME", os.path.expanduser("~/chrome-extract/opt/google/chrome/chrome"))
PORT = 9222

def ws_connect(ws_url):
    # ws://127.0.0.1:9222/devtools/page/<id>
    assert ws_url.startswith("ws://")
    rest = ws_url[5:]
    hostport, path = rest.split("/", 1)
    host, port = hostport.split(":")
    key = base64.b64encode(os.urandom(16)).decode()
    s = socket.create_connection((host, int(port)), timeout=10)
    req = (f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        buf += s.recv(4096)
    assert b"101" in buf.split(b"\r\n")[0], buf[:200]
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
    data = b""
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
            return payload.decode()
        if op == 0:
            continue

def cdp(s, mid, method, params=None):
    ws_send(s, json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws_recv_msg(s))
        if msg.get("id") == mid:
            if "error" in msg: raise RuntimeError(msg["error"])
            return msg.get("result", {})

server = subprocess.Popen([sys.executable, "-m", "http.server", "8000", "--bind", "127.0.0.1"],
                          cwd=os.getcwd(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
chrome = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                           f"--remote-debugging-port={PORT}", "--window-size=390,844", URL],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    target = None
    for _ in range(30):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=2))
            target = next(t for t in tabs if t["type"] == "page")
            break
        except Exception:
            time.sleep(0.5)
    assert target, "no CDP page target"
    s = ws_connect(target["webSocketDebuggerUrl"])
    cdp(s, 1, "Runtime.enable")
    for _ in range(20):
        r = cdp(s, 9, "Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True})
        if r.get("result", {}).get("value") == "complete":
            break
        time.sleep(0.5)
    expr = ("(()=>{const t=document.querySelector('[data-nav-toggle]');"
            "const n=document.getElementById('site-nav');"
            "t.click();"
            "return 'NAV-OPEN='+n.classList.contains('is-open')"
            " + ' ARIA='+t.getAttribute('aria-expanded')"
            " + ' LABEL='+t.textContent;})()")
    r = cdp(s, 2, "Runtime.evaluate", {"expression": expr, "returnByValue": True})
    if "exceptionDetails" in r:
        print("FAIL: evaluate exception:", json.dumps(r["exceptionDetails"])[:500]); sys.exit(1)
    out = r["result"]["value"]
    print(out)
    ok = out == "NAV-OPEN=true ARIA=true LABEL=Tutup menu"
    print("PASS: nav toggle opens, aria-expanded=true, label=Tutup menu" if ok else "FAIL: unexpected toggle state")
    sys.exit(0 if ok else 1)
finally:
    chrome.terminate(); server.terminate()
