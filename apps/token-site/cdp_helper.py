#!/usr/bin/env python3
"""Shared stdlib-only CDP client for token-site browser tests.

Zero dependencies: raw-socket WebSocket client (same proven approach as
nav-toggle-test.py, which predates this helper and keeps its own inline
copy so a passing test is never touched). Used by keyboard-test.py,
reduced-motion-test.py and a11y-review.py.

Conventions shared by all browser tests in this directory:
- Local HTTP server + headless Chrome on dynamically allocated free ports.
- The spawned server's PID is verified to own its listener (when `ss`
  exists) and the served page must contain its expected marker, so an
  unrelated process can never false-pass.
- Unique Chrome profile dir per session; server and Chrome are always
  terminated and the profile dir removed on exit.
- Chrome binary: $CHROME, else ~/chrome-extract/opt/google/chrome/chrome
  (Chrome 157). CI sets $CHROME via setup-chrome.
"""
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request

CHROME = os.environ.get("CHROME", os.path.expanduser("~/chrome-extract/opt/google/chrome/chrome"))


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def listener_pid(port):
    """PID owning the 127.0.0.1:port listener, via `ss` (None if unavailable)."""
    try:
        out = subprocess.run(["ss", "-ltnpH", f"sport = :{port}"],
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return None
    m = re.search(r"pid=(\d+)", out)
    return int(m.group(1)) if m else None


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
        header.append(0x80 | 126)
        header += struct.pack(">H", n)
    else:
        header.append(0x80 | 127)
        header += struct.pack(">Q", n)
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
            if not chunk:
                raise ConnectionError("ws closed")
            data += chunk
        fin = data[0] & 0x80
        op = data[0] & 0x0F
        ln = data[1] & 0x7F
        off = 2
        if ln == 126:
            while len(data) < 4:
                data += s.recv(4096)
            ln = struct.unpack(">H", data[2:4])[0]
            off = 4
        elif ln == 127:
            while len(data) < 10:
                data += s.recv(4096)
            ln = struct.unpack(">Q", data[2:10])[0]
            off = 10
        while len(data) < off + ln:
            data += s.recv(65536)
        payload = data[off:off + ln]
        data = data[off + ln:]
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


class CDP:
    """Minimal CDP session over one page target's WebSocket."""

    def __init__(self, ws):
        self.ws = ws
        self.mid = 0

    def call(self, method, params=None):
        self.mid += 1
        ws_send(self.ws, json.dumps({"id": self.mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(ws_recv_msg(self.ws))
            if msg.get("id") == self.mid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def evaluate(self, expression):
        """Runtime.evaluate with returnByValue; raises on page exceptions."""
        r = self.call("Runtime.evaluate",
                      {"expression": expression, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in r:
            raise RuntimeError("evaluate exception: " + json.dumps(r["exceptionDetails"])[:500])
        return r.get("result", {}).get("value")

    def key(self, key, code, vk, text=None, key_type="keyDown"):
        """One Input.dispatchKeyEvent. `text` only on keyDown (per protocol)."""
        params = {"type": key_type, "key": key, "code": code,
                  "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
        if text is not None:
            params["text"] = text
        return self.call("Input.dispatchKeyEvent", params)

    def press(self, key, code, vk, text=None):
        """A full key press: keyDown + keyUp, with settling pauses."""
        self.key(key, code, vk, text, "keyDown")
        time.sleep(0.05)
        self.key(key, code, vk, None, "keyUp")
        time.sleep(0.12)

    def press_tab(self):
        self.press("Tab", "Tab", 9)

    def press_enter(self):
        self.press("Enter", "Enter", 13, "\r")

    def press_space(self):
        self.press(" ", "Space", 32, " ")

    def press_escape(self):
        self.press("Escape", "Escape", 27)

    def wait_ready(self, timeout=15):
        for _ in range(int(timeout / 0.25)):
            try:
                if self.evaluate("document.readyState") == "complete":
                    return True
            except Exception:
                pass
            time.sleep(0.25)
        return False

    def navigate(self, url, timeout=15):
        self.call("Page.navigate", {"url": url})
        if not self.wait_ready(timeout):
            raise AssertionError(f"page did not reach readyState=complete at {url!r}")


class BrowserSession:
    """Local HTTP server + headless Chrome; cleans both up on exit.

    Usage:
        with BrowserSession(site_dir, width, height) as session:
            cdp = session.cdp          # CDP session on the first page
            base = session.base        # e.g. http://127.0.0.1:PORT
            cdp.navigate(base + "/about.html")
    """

    def __init__(self, site_dir, width=1280, height=800, extra_args=None, first_path="/index.html"):
        self.site_dir = site_dir
        self.width = width
        self.height = height
        self.extra_args = extra_args or []
        self.first_path = first_path
        self.server = None
        self.chrome = None
        self.profile_dir = None
        self.http_port = None
        self.cdp_port = None
        self.base = None
        self.cdp = None

    def __enter__(self):
        self.http_port = free_port()
        self.cdp_port = free_port()
        while self.cdp_port == self.http_port:
            self.cdp_port = free_port()
        self.base = f"http://127.0.0.1:{self.http_port}"
        first_url = self.base + self.first_path
        self.profile_dir = tempfile.mkdtemp(prefix="token-site-chrome-")
        self.server = subprocess.Popen(
            ["python3", "-m", "http.server", str(self.http_port), "--bind", "127.0.0.1"],
            cwd=self.site_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ready = False
        for _ in range(30):
            try:
                with urllib.request.urlopen(f"{self.base}/index.html", timeout=2) as r:
                    if r.status == 200 and b"REFORMASI" in r.read():
                        ready = True
                        break
            except Exception:
                time.sleep(0.5)
        if not ready:
            self._cleanup()
            raise AssertionError(f"server did not serve expected content on port {self.http_port} within 15s")
        owner = listener_pid(self.http_port)
        if owner is not None:
            if owner != self.server.pid:
                self._cleanup()
                raise AssertionError(f"port {self.http_port} owned by pid {owner}, not our server pid {self.server.pid}")
            print(f"PASS: spawned server pid {self.server.pid} owns listener on 127.0.0.1:{self.http_port} (CDP port {self.cdp_port})")
        else:
            print("INFO: 'ss' unavailable; listener ownership not verified "
                  f"(dynamic free port {self.http_port} + content check still apply)")
        self.chrome = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
             f"--user-data-dir={self.profile_dir}",
             f"--remote-debugging-port={self.cdp_port}",
             f"--window-size={self.width},{self.height}"] + self.extra_args + [first_url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        target = None
        for _ in range(30):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.cdp_port}/json/list", timeout=2))
                target = next((t for t in tabs if t.get("type") == "page" and t.get("url") == first_url), None)
                if target:
                    break
            except Exception:
                time.sleep(0.5)
        if not target:
            self._cleanup()
            raise AssertionError(f"no CDP page target matching {first_url!r}")
        ws = ws_connect(target["webSocketDebuggerUrl"])
        self.cdp = CDP(ws)
        self.cdp.call("Runtime.enable")
        self.cdp.call("Page.enable")
        if not self.cdp.wait_ready():
            self._cleanup()
            raise AssertionError(f"page did not reach readyState=complete at {first_url!r}")
        return self

    def _cleanup(self):
        for proc in (self.chrome, self.server):
            if proc is not None and proc.poll() is None:
                try:
                    proc.terminate()
                except ProcessLookupError:
                    pass
        for proc in (self.chrome, self.server):
            if proc is not None:
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
        if self.profile_dir:
            shutil.rmtree(self.profile_dir, ignore_errors=True)

    def __exit__(self, *exc):
        self._cleanup()
        return False
