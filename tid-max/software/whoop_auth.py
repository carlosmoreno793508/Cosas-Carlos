#!/usr/bin/env python3
"""
whoop_auth.py — Paso 1 (una sola vez): obtener el REFRESH TOKEN de WHOOP.

Qué hace:
  1. Abre tu navegador en la pantalla de login de WHOOP.
  2. Inicias sesion con la cuenta de WHOOP de Gael y das "Autorizar".
  3. WHOOP regresa a http://localhost:8765/callback (este script lo escucha).
  4. Canjea el codigo por tokens e imprime + guarda el REFRESH TOKEN en .env.

Uso:
    python whoop_auth.py

Requisitos previos (en el archivo .env de esta carpeta):
    WHOOP_CLIENT_ID=...        (del portal developer-dashboard.whoop.com)
    WHOOP_CLIENT_SECRET=...    (del portal, tratalo como contrasena)
    WHOOP_REDIRECT_URI=http://localhost:8765/callback   (opcional; este es el default)
"""
import os
import sys
import secrets
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

try:
    from dotenv import load_dotenv, set_key
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

# --- Endpoints oficiales de WHOOP (OAuth 2.0) ---
AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"

# 'offline' es lo que hace que WHOOP entregue un refresh_token (acceso permanente).
SCOPES = (
    "offline "
    "read:recovery read:cycles read:sleep read:workout "
    "read:profile read:body_measurement"
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")


def main():
    load_dotenv(ENV_PATH)

    client_id = os.getenv("WHOOP_CLIENT_ID", "").strip()
    client_secret = os.getenv("WHOOP_CLIENT_SECRET", "").strip()
    redirect_uri = os.getenv(
        "WHOOP_REDIRECT_URI", "http://localhost:8765/callback"
    ).strip()

    if not client_id or not client_secret:
        sys.exit(
            "\nFaltan credenciales. Crea el archivo .env (copia de .env.example) con:\n"
            "  WHOOP_CLIENT_ID=...\n"
            "  WHOOP_CLIENT_SECRET=...\n"
        )

    parsed = urllib.parse.urlparse(redirect_uri)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8765
    callback_path = parsed.path or "/callback"

    state = secrets.token_urlsafe(24)  # WHOOP exige 'state' (min 8 chars)
    result = {}  # aqui guardamos el 'code' o el 'error' que llegue

    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "state": state,
    }
    auth_link = AUTH_URL + "?" + urllib.parse.urlencode(auth_params)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_req = urllib.parse.urlparse(self.path)
            if parsed_req.path != callback_path:
                self.send_response(404)
                self.end_headers()
                return
            qs = urllib.parse.parse_qs(parsed_req.query)
            result["code"] = qs.get("code", [None])[0]
            result["state"] = qs.get("state", [None])[0]
            result["error"] = qs.get("error", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if result.get("error"):
                msg = f"Error de WHOOP: {result['error']}. Puedes cerrar esta pestana."
            else:
                msg = "Listo. WHOOP autorizado. Ya puedes cerrar esta pestana y volver a la terminal."
            self.wfile.write(
                f"<html><body style='font-family:sans-serif;padding:40px'>"
                f"<h2>TID-MAX &times; WHOOP</h2><p>{msg}</p></body></html>".encode("utf-8")
            )

        def log_message(self, *args):
            pass  # silenciar los logs del servidor

    try:
        server = HTTPServer((host, port), Handler)
    except OSError as e:
        sys.exit(
            f"\nNo pude abrir el puerto {port} ({e}).\n"
            f"Cierra lo que este usando ese puerto o cambia WHOOP_REDIRECT_URI en .env\n"
            f"(y en el portal de WHOOP debe coincidir exactamente)."
        )

    print("\n=== WHOOP — Autorizacion (paso unico) ===")
    print("Se abrira tu navegador. Inicia sesion con la cuenta de WHOOP de Gael y da 'Autorizar'.")
    print("Si no se abre solo, copia y pega esta URL:\n")
    print(auth_link + "\n")

    threading.Thread(target=lambda: webbrowser.open(auth_link), daemon=True).start()
    print(f"Esperando el callback en {redirect_uri} ...")
    server.handle_request()  # atiende exactamente 1 request (el callback) y sigue
    server.server_close()

    if result.get("error"):
        sys.exit(f"\nWHOOP devolvio un error: {result['error']}")
    if not result.get("code"):
        sys.exit("\nNo llego el codigo de autorizacion. Intenta de nuevo.")
    if result.get("state") != state:
        sys.exit("\nEl 'state' no coincide (posible problema de seguridad). Intenta de nuevo.")

    print("Codigo recibido. Canjeando por tokens...")
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": result["code"],
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )

    if resp.status_code != 200:
        sys.exit(
            f"\nFallo el intercambio de tokens ({resp.status_code}):\n{resp.text}\n"
            "Revisa que el Client Secret y el Redirect URI sean correctos."
        )

    tokens = resp.json()
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        sys.exit(
            "\nWHOOP no devolvio refresh_token. Verifica que el scope 'offline' este incluido."
        )

    # Guardar en .env para que whoop_sync.py lo use.
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, "a").close()
    set_key(ENV_PATH, "WHOOP_REFRESH_TOKEN", refresh_token)

    print("\n===================== LISTO =====================")
    print("REFRESH TOKEN obtenido y guardado en .env como WHOOP_REFRESH_TOKEN.")
    print("(No lo compartas ni lo pegues en chats: es como una contrasena.)")
    print("\nSiguiente paso:")
    print("    python whoop_sync.py")
    print("=================================================\n")


if __name__ == "__main__":
    main()
