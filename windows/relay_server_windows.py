#!/usr/bin/env python3
"""Server locale HEPscape! per il trigger KX-007 su Windows."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import serial
from serial.tools import list_ports

HTTP_HOST = "127.0.0.1"
HTTP_PORT = 5000
BAUD_RATE = 9600

trigger_lock = threading.Lock()


def find_trigger_port():
    """Trova automaticamente la porta COM del controller Prolific PL2303."""
    candidates = []
    for port in list_ports.comports():
        description = "{} {} {}".format(
            port.description or "", port.manufacturer or "", port.hwid or ""
        ).lower()
        if port.vid == 0x067B or "prolific" in description or "pl2303" in description:
            candidates.append(port.device)

    if not candidates:
        raise OSError(
            "Trigger USB non trovato. Controllare Gestione dispositivi e il driver PL2303."
        )
    return sorted(candidates)[0]


def open_drawer():
    """Invia il byte che fa generare al KX-007 l'impulso di apertura."""
    port = find_trigger_port()
    with serial.Serial(port, BAUD_RATE, timeout=1, write_timeout=1) as connection:
        connection.write(b"X")
        connection.flush()
    return port


class DrawerRequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(204, {})

    def do_GET(self):
        if self.path.rstrip("/") != "/open":
            self.send_json(404, {"ok": False, "error": "Endpoint non trovato"})
            return

        if not trigger_lock.acquire(False):
            self.send_json(409, {"ok": False, "error": "Trigger gia in uso"})
            return

        try:
            port = open_drawer()
            self.send_json(200, {"ok": True, "port": port})
        except (OSError, serial.SerialException) as error:
            self.send_json(503, {"ok": False, "error": str(error)})
        finally:
            trigger_lock.release()

    def log_message(self, format_string, *args):
        print("[{}] {}".format(self.log_date_time_string(), format_string % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HTTP_HOST, HTTP_PORT), DrawerRequestHandler)
    print("HEPscape! Cassetto 125 - Windows")
    print("Server pronto: http://localhost:{}/open".format(HTTP_PORT))
    print("Trigger KX-007 / PL2303 a {} baud".format(BAUD_RATE))
    print("Lascia aperta questa finestra. Premi Control-C per terminare.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer arrestato.")
    finally:
        server.server_close()
