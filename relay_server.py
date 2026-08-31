#!/usr/bin/env python3
"""Local HTTP bridge for the HEPscape USB cash-drawer trigger."""

import glob
import json
import os
import termios
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERIAL_PORT_PATTERN = "/dev/cu.PL2303G-USBtoUART*"
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 5000

relay_lock = threading.Lock()


def find_trigger_port() -> str:
    """Return the Prolific virtual serial port created by the USB trigger."""
    ports = sorted(glob.glob(SERIAL_PORT_PATTERN))
    if not ports:
        raise OSError("Trigger USB non trovato")
    return ports[0]


def open_drawer() -> str:
    """Send one byte; the trigger converts it into the drawer-opening pulse."""
    port = find_trigger_port()
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    try:
        settings = termios.tcgetattr(fd)
        settings[4] = termios.B9600
        settings[5] = termios.B9600
        settings[2] = (settings[2] & ~(termios.CSIZE | termios.PARENB | termios.CSTOPB)) | termios.CS8
        termios.tcsetattr(fd, termios.TCSANOW, settings)
        os.write(fd, b"X")
        termios.tcdrain(fd)
    finally:
        os.close(fd)
    return port


class RelayRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._send_json(204, {})

    def do_GET(self) -> None:
        if self.path.rstrip("/") != "/open":
            self._send_json(404, {"ok": False, "error": "Endpoint non trovato"})
            return

        if not relay_lock.acquire(blocking=False):
            self._send_json(409, {"ok": False, "error": "Relay già in uso"})
            return

        try:
            port = open_drawer()
            self._send_json(200, {"ok": True, "port": port})
        except OSError as exc:
            self._send_json(503, {"ok": False, "error": str(exc)})
        finally:
            relay_lock.release()

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HTTP_HOST, HTTP_PORT), RelayRequestHandler)
    print(f"HEPscape drawer server: http://localhost:{HTTP_PORT}/open")
    print(f"Trigger: {SERIAL_PORT_PATTERN} @ 9600 baud")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer arrestato.")
    finally:
        server.server_close()
