#!/usr/bin/env python3
"""Every homepage header link stays fully inside the viewport."""
from __future__ import annotations

import base64
import json
import os
import shutil
import signal
import socket
import struct
import subprocess
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (320, 360, 375, 390, 414, 480, 481, 520, 640, 700, 766, 767, 900, 1024, 1280)
_CHROME = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
)

_MEASURE = r"""
(async () => {
  if (document.fonts && document.fonts.ready) {
    await Promise.race([
      document.fonts.ready,
      new Promise((resolve) => setTimeout(resolve, 2500))
    ]);
  }
  const animations = document.getAnimations ? document.getAnimations() : [];
  await Promise.race([
    Promise.all(animations.map((animation) => animation.finished.catch(() => {}))),
    new Promise((resolve) => setTimeout(resolve, 2000))
  ]);
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const width = Math.min(window.innerWidth, document.documentElement.clientWidth);
  const links = [];
  for (const el of document.querySelectorAll("header.global-nav a")) {
    const style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") continue;
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) continue;
    links.push({
      text: (el.textContent || "").replace(/\s+/g, " ").trim(),
      left: rect.left,
      right: rect.right,
      top: rect.top,
      bottom: rect.bottom
    });
  }
  const tops = links.map((link) => link.top);
  const bottoms = links.map((link) => link.bottom);
  const header = document.querySelector("header.global-nav");
  return {
    width,
    scroll: document.documentElement.scrollWidth,
    client: document.documentElement.clientWidth,
    inner: window.innerWidth,
    headerHeight: header ? header.getBoundingClientRect().height : 0,
    oneRow: tops.length ? Math.max(...tops) < Math.min(...bottoms) : false,
    links
  };
})()
"""


def _chrome_bin() -> str:
    for name in _CHROME:
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Chrome is not installed; the homepage header fit test cannot run")


class _Ws:
    """Small client for Chrome's debugger socket. Server frames are unmasked."""

    def __init__(self, url: str) -> None:
        parsed = urlparse(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=20)
        key = base64.b64encode(os.urandom(16)).decode()
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        host = f"{parsed.hostname}:{parsed.port}"
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise SystemExit("Chrome closed the debugger handshake")
            data += chunk
        head, self._buf = data.split(b"\r\n\r\n", 1)
        if b" 101 " not in head.split(b"\r\n", 1)[0]:
            raise SystemExit("debugger handshake failed")
        self._id = 0

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    def call(self, method: str, params: dict | None = None, timeout: float = 20) -> dict:
        self._id += 1
        ident = self._id
        self._send(json.dumps({"id": ident, "method": method, "params": params or {}}))
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SystemExit(f"timed out waiting for {method}")
            self.sock.settimeout(remaining)
            message = json.loads(self._recv())
            if message.get("id") != ident:
                continue
            if "error" in message:
                raise SystemExit(f"{method} failed: {message['error']}")
            return message.get("result") or {}

    def _send(self, text: str) -> None:
        payload = text.encode()
        mask = os.urandom(4)
        length = len(payload)
        if length < 126:
            header = struct.pack("!BB", 0x81, 0x80 | length)
        elif length < 65536:
            header = struct.pack("!BBH", 0x81, 0x80 | 126, length)
        else:
            header = struct.pack("!BBQ", 0x81, 0x80 | 127, length)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def _recv(self) -> str:
        while True:
            opcode, payload = self._frame()
            if opcode == 0x1:
                return payload.decode()
            if opcode == 0x8:
                raise SystemExit("Chrome closed the debugger socket")
            if opcode == 0x9:
                self._pong(payload)

    def _pong(self, payload: bytes) -> None:
        mask = os.urandom(4)
        header = struct.pack("!BB", 0x8A, 0x80 | len(payload))
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def _exact(self, size: int) -> bytes:
        while len(self._buf) < size:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise SystemExit("Chrome closed the debugger socket")
            self._buf += chunk
        out, self._buf = self._buf[:size], self._buf[size:]
        return out

    def _frame(self) -> tuple[int, bytes]:
        header = self._exact(2)
        opcode = header[0] & 0x0F
        masked = header[1] & 0x80
        length = header[1] & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._exact(8))[0]
        mask = self._exact(4) if masked else b""
        payload = self._exact(length)
        if masked:
            payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        return opcode, payload


def _serve() -> tuple[ThreadingHTTPServer, int]:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def log_message(self, fmt: str, *args) -> None:
            return

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, int(httpd.server_address[1])


def _start_chrome(profile: str) -> tuple[subprocess.Popen, int]:
    proc = subprocess.Popen(
        [
            _chrome_bin(),
            "--headless=new",
            "--remote-debugging-port=0",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            f"--user-data-dir={profile}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    found: dict[str, int] = {}
    lines: list[str] = []

    def read() -> None:
        assert proc.stderr is not None
        for line in proc.stderr:
            lines.append(line)
            if "DevTools listening on " in line:
                url = line.split("DevTools listening on ", 1)[1].strip()
                port = urlparse(url).port
                if port:
                    found["port"] = port
                return

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    reader.join(20)
    if "port" not in found:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            proc.kill()
        proc.wait(timeout=5)
        raise SystemExit("Chrome did not open a debugger port:\n" + "".join(lines))
    return proc, found["port"]


def _page_socket(port: int) -> str:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2) as response:
                targets = json.load(response)
        except (OSError, json.JSONDecodeError):
            time.sleep(0.1)
            continue
        for target in targets:
            if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
                return str(target["webSocketDebuggerUrl"])
        time.sleep(0.1)
    raise SystemExit("Chrome did not expose a page target")


def _measure(ws: _Ws, width: int) -> dict:
    ws.call(
        "Emulation.setDeviceMetricsOverride",
        {
            "width": width,
            "height": 800,
            "deviceScaleFactor": 1,
            "mobile": False,
        },
    )
    ws.call("Page.navigate", {"url": f"http://127.0.0.1:{_PORT}/"})
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        result = ws.call(
            "Runtime.evaluate",
            {"expression": "document.readyState", "returnByValue": True},
        )
        if (result.get("result") or {}).get("value") == "complete":
            break
        time.sleep(0.05)
    else:
        raise SystemExit(f"homepage did not finish loading at {width}px")
    measured = ws.call(
        "Runtime.evaluate",
        {"expression": _MEASURE, "awaitPromise": True, "returnByValue": True},
        timeout=15,
    )
    value = (measured.get("result") or {}).get("value")
    if not isinstance(value, dict):
        detail = measured.get("exceptionDetails") or measured
        raise SystemExit(f"could not measure the homepage header at {width}px: {detail}")
    return value


_STUB_MEASURE = r"""
(() => {
  const heading = document.querySelector("h1");
  const body = document.querySelector(".article-shell p");
  const button = document.querySelector(".stub-fallback");
  const box = (el) => el ? el.getBoundingClientRect().left : -1;
  return { headingLeft: box(heading), bodyLeft: box(body), buttonLeft: box(button) };
})()
"""


def _measure_stub(ws: _Ws, width: int) -> dict:
    ws.call(
        "Emulation.setDeviceMetricsOverride",
        {"width": width, "height": 800, "deviceScaleFactor": 1, "mobile": False},
    )
    # A real stub meta-refreshes away before layout can be read. Paint the same
    # markup in the already-styled homepage document.
    ws.call(
        "Runtime.evaluate",
        {
            "expression": """
            document.body.innerHTML = '<main><section class="scene scene-light"><div class="article-shell"><h1>You.com review</h1><p>This page has moved. The current page keeps the dated evidence and the affiliate disclosure.</p><p><a class="button button-blue stub-fallback" href="/tools/you-com/">Open the current page</a></p></div></section></main>';
            """,
            "returnByValue": True,
        },
    )
    measured = ws.call(
        "Runtime.evaluate",
        {"expression": _STUB_MEASURE, "returnByValue": True},
        timeout=15,
    )
    value = (measured.get("result") or {}).get("value")
    if not isinstance(value, dict):
        detail = measured.get("exceptionDetails") or measured
        raise SystemExit(f"could not measure the stub page at {width}px: {detail}")
    return value


_PORT = 0


def _stop_chrome(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        proc.kill()
    proc.wait(timeout=5)


def _remove_profile(profile: str) -> None:
    for _ in range(5):
        shutil.rmtree(profile, ignore_errors=True)
        if not os.path.exists(profile):
            return
        time.sleep(0.1)
    shutil.rmtree(profile)


def main() -> None:
    global _PORT
    errors: list[str] = []
    httpd, _PORT = _serve()
    profile = tempfile.mkdtemp(prefix="home-header-")
    proc = None
    ws = None
    try:
        proc, debug_port = _start_chrome(profile)
        ws = _Ws(_page_socket(debug_port))
        ws.call("Page.enable")
        for width in WIDTHS:
            layout = _measure(ws, width)
            viewport = float(layout["width"])
            if abs(viewport - width) > 1:
                errors.append(f"{width}px viewport measured {viewport}")
            if float(layout["scroll"]) > float(layout["client"]) + 1:
                errors.append(
                    f"{width}px page is {layout['scroll']}px wide in a {layout['client']}px viewport"
                )
            labels = []
            tops = []
            for link in layout["links"]:
                labels.append(link["text"])
                tops.append(float(link["top"]))
                if float(link["left"]) < -0.5 or float(link["right"]) > viewport + 0.5:
                    errors.append(
                        f"{width}px {link['text']!r} sits at {link['left']:.1f}–{link['right']:.1f}"
                        f" outside 0–{viewport:.0f}"
                    )
            if "Sponsor us" not in labels:
                errors.append(f"{width}px hides Sponsor us")
            if not layout["oneRow"] or float(layout["headerHeight"]) > 72:
                errors.append(
                    f"{width}px homepage header wrapped onto a second row"
                    f" (height {layout['headerHeight']})"
                )
        stub = _measure_stub(ws, 375)
        if stub.get("headingLeft", 0) < 15 or stub.get("bodyLeft", 0) < 15:
            errors.append(
                f"stub text is flush: heading {stub.get('headingLeft')} body {stub.get('bodyLeft')}"
            )
        if abs(float(stub.get("headingLeft", 0)) - float(stub.get("buttonLeft", -1))) > 2:
            errors.append(
                f"stub heading inset {stub.get('headingLeft')} differs from button {stub.get('buttonLeft')}"
            )
        if abs(float(stub.get("bodyLeft", 0)) - float(stub.get("buttonLeft", -1))) > 2:
            errors.append(
                f"stub body inset {stub.get('bodyLeft')} differs from button {stub.get('buttonLeft')}"
            )
    finally:
        if ws is not None:
            try:
                ws.close()
            except Exception:
                pass
        if proc is not None:
            try:
                _stop_chrome(proc)
            except Exception:
                pass
        try:
            httpd.shutdown()
        except Exception:
            pass
        _remove_profile(profile)
    if os.path.exists(profile):
        errors.append(f"Chrome profile was left at {profile}")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
