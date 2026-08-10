#!/usr/bin/env python3
"""
agregador_webhook.py — Receptor de webhooks de Junction (FASE 2: el "push").

Hoy (Fase 1) bajamos con "pull": corres agregador_sync.py y trae lo nuevo.
Esto es el UPGRADE: Junction EMPUJA cada evento (workout nuevo, sueno, etc.)
apenas lo descubre, y este servidor lo recibe y lo guarda al instante. Asi la
data cae minutos despues de que el atleta termina, sin correr nada a mano.

Requiere una URL PUBLICA (no localhost). Dos formas:
  - Dev/prueba:  un tunel ->  cloudflared tunnel --url http://localhost:8770
                 (o ngrok http 8770) y registras esa URL en el dashboard de Junction.
  - Produccion:  despliega esto en un host siempre-encendido (Render/Railway/Fly/VPS).

Junction firma los webhooks con Svix. Pon el secreto en .env como
JUNCTION_WEBHOOK_SECRET para verificar la firma (recomendado). Sin el, el server
acepta todo (solo para pruebas locales).

Guarda cada evento crudo en datos/agregador/<atleta>/webhook_<tipo>_<ts>.json,
que el normalizador (tid_data.py) ya sabe leer.

Uso:
    python agregador_webhook.py            # escucha en el puerto 8770
    python agregador_webhook.py --port 9000
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
STORE_PATH = os.path.join(SCRIPT_DIR, "datos", "agregador_users.json")
OUT_BASE = os.path.join(SCRIPT_DIR, "datos", "agregador")


def _users_por_id():
    """Mapa user_id -> atleta, para archivar el evento en la carpeta correcta."""
    if not os.path.exists(STORE_PATH):
        return {}
    with open(STORE_PATH, encoding="utf-8") as f:
        store = json.load(f)
    return {v.get("user_id"): a for a, v in store.items() if v.get("user_id")}


def _verificar_firma(secret, headers, body):
    """Verifica la firma Svix si hay secreto y libreria. Devuelve True/False."""
    if not secret:
        return True  # sin secreto configurado: modo prueba, acepta todo
    try:
        from svix.webhooks import Webhook, WebhookVerificationError
    except ImportError:
        print("(aviso: instala 'svix' para verificar la firma:  pip install svix)")
        return True
    try:
        Webhook(secret).verify(body, {
            "svix-id": headers.get("svix-id", ""),
            "svix-timestamp": headers.get("svix-timestamp", ""),
            "svix-signature": headers.get("svix-signature", ""),
        })
        return True
    except WebhookVerificationError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Receptor de webhooks de Junction.")
    parser.add_argument("--port", type=int, default=8770)
    args = parser.parse_args()

    load_dotenv(ENV_PATH)
    secret = os.getenv("JUNCTION_WEBHOOK_SECRET", "").strip()
    users = _users_por_id()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Endpoint de salud (para probar que el server responde).
            if self.path in ("/", "/health"):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true,"servicio":"tidmax-agregador-webhook"}')
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            hdrs = {k.lower(): v for k, v in self.headers.items()}

            if not _verificar_firma(secret, hdrs, body):
                self.send_response(401)
                self.end_headers()
                print("Webhook RECHAZADO: firma invalida.")
                return

            try:
                evento = json.loads(body)
            except ValueError:
                self.send_response(400)
                self.end_headers()
                return

            tipo = evento.get("event_type") or evento.get("type") or "evento"
            data = evento.get("data") or {}
            user_id = data.get("user_id") or evento.get("user_id")
            atleta = users.get(user_id, "desconocido")

            out_dir = os.path.join(OUT_BASE, atleta)
            os.makedirs(out_dir, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
            safe_tipo = str(tipo).replace(".", "_").replace("/", "_")
            path = os.path.join(out_dir, f"webhook_{safe_tipo}_{ts}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(evento, f, ensure_ascii=False, indent=2)

            print(f"Webhook OK  [{atleta}]  {tipo}  -> {os.path.relpath(path, SCRIPT_DIR)}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"received":true}')

        def log_message(self, *a):
            pass

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    print(f"\n=== TID-MAX · Receptor de webhooks de Junction ===")
    print(f"Escuchando en http://0.0.0.0:{args.port}  (salud: /health)")
    print(f"Firma Svix: {'ACTIVA' if secret else 'sin verificar (modo prueba)'}")
    print("Expon este puerto con un tunel (cloudflared/ngrok) y registra la URL "
          "en tu dashboard de Junction.\nCtrl+C para parar.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDetenido.")
        server.server_close()


if __name__ == "__main__":
    main()
