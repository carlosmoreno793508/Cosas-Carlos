#!/usr/bin/env python3
"""
polar_auth.py — Paso 1 (una sola vez): autorizar TID-MAX con tu cuenta Polar Flow.

Qué hace:
  1. Abre el navegador en el login de Polar Flow.
  2. Inicias sesión con tu cuenta Polar y das "Aceptar".
  3. Polar regresa a http://localhost:8765/callback (este script lo escucha).
  4. Canjea el código por el ACCESS TOKEN + tu user-id, registra al usuario en
     AccessLink y guarda ambos en .env.

Uso:
    python polar_auth.py

Requisitos previos en .env (de admin.polaraccesslink.com > tu app):
    POLAR_CLIENT_ID=...
    POLAR_CLIENT_SECRET=...     (trátalo como contraseña)
    POLAR_REDIRECT_URI=http://localhost:8765/callback   (debe coincidir EXACTO en el portal)
"""
import os
import sys
import base64
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

# --- Endpoints oficiales de Polar AccessLink (OAuth 2.0) ---
AUTH_URL = "https://flow.polar.com/oauth2/authorization"
TOKEN_URL = "https://polarremote.com/v2/oauth2/token"
API_BASE = "https://www.polaraccesslink.com/v3"
SCOPE = "accesslink.read_all"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")


def main():
    load_dotenv(ENV_PATH)
    client_id = os.getenv("POLAR_CLIENT_ID", "").strip()
    client_secret = os.getenv("POLAR_CLIENT_SECRET", "").strip()
    redirect_uri = os.getenv("POLAR_REDIRECT_URI", "http://localhost:8765/callback").strip()

    if not client_id or not client_secret:
        sys.exit(
            "\nFaltan credenciales. Copia .env.example a .env y rellena:\n"
            "  POLAR_CLIENT_ID=...\n  POLAR_CLIENT_SECRET=...\n"
        )

    parsed = urllib.parse.urlparse(redirect_uri)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8765
    callback_path = parsed.path or "/callback"
    state = secrets.token_urlsafe(24)
    result = {}

    auth_link = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPE,
        "state": state,
    })

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            req = urllib.parse.urlparse(self.path)
            if req.path != callback_path:
                self.send_response(404)
                self.end_headers()
                return
            qs = urllib.parse.parse_qs(req.query)
            result["code"] = qs.get("code", [None])[0]
            result["state"] = qs.get("state", [None])[0]
            result["error"] = qs.get("error", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = ("Error de Polar: " + result["error"]) if result.get("error") \
                else "Listo. Polar autorizado. Ya puedes cerrar esta pestana."
            self.wfile.write(
                f"<html><body style='font-family:sans-serif;padding:40px'>"
                f"<h2>TID-MAX &times; Polar</h2><p>{msg}</p></body></html>".encode("utf-8"))

        def log_message(self, *a):
            pass

    try:
        server = HTTPServer((host, port), Handler)
    except OSError as e:
        sys.exit(
            f"\nNo pude abrir el puerto {port} ({e}).\n"
            f"Cierra lo que lo use o cambia POLAR_REDIRECT_URI en .env\n"
            f"(y en el portal de Polar debe coincidir exactamente)."
        )

    print("\n=== Polar — Autorizacion (paso unico) ===")
    print("Se abrira tu navegador. Inicia sesion en Polar Flow y da 'Aceptar'.")
    print("Si no se abre solo, copia esta URL:\n\n" + auth_link + "\n")
    threading.Thread(target=lambda: webbrowser.open(auth_link), daemon=True).start()
    print(f"Esperando el callback en {redirect_uri} ...")
    server.handle_request()
    server.server_close()

    if result.get("error"):
        sys.exit(f"\nPolar devolvio un error: {result['error']}")
    if not result.get("code"):
        sys.exit("\nNo llego el codigo de autorizacion. Intenta de nuevo.")
    if result.get("state") != state:
        sys.exit("\nEl 'state' no coincide (posible problema de seguridad). Intenta de nuevo.")

    # Canje del codigo -> access token (Polar usa Basic auth con client_id:client_secret)
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    print("Codigo recibido. Canjeando por access token...")
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": result["code"],
            "redirect_uri": redirect_uri,
        },
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(
            f"\nFallo el intercambio de tokens ({resp.status_code}):\n{resp.text}\n"
            "Revisa que el Client Secret y el Redirect URI sean correctos."
        )

    tok = resp.json()
    access_token = tok.get("access_token")
    user_id = str(tok.get("x_user_id", ""))
    if not access_token or not user_id:
        sys.exit(f"\nRespuesta inesperada de Polar:\n{tok}")

    # Registro del usuario en AccessLink (una sola vez; 409 = ya estaba registrado, ok)
    reg = requests.post(
        f"{API_BASE}/users",
        json={"member-id": f"tidmax-{user_id}"},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=30,
    )
    if reg.status_code not in (200, 201, 409):
        print(f"Aviso: el registro del usuario devolvio {reg.status_code}: {reg.text}")

    # Los tokens de Polar son de larga duracion -> guardamos token + user_id (sin refresh).
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, "a").close()
    set_key(ENV_PATH, "POLAR_ACCESS_TOKEN", access_token)
    set_key(ENV_PATH, "POLAR_USER_ID", user_id)

    print("\n===================== LISTO =====================")
    print("ACCESS TOKEN y USER_ID obtenidos y guardados en .env.")
    print("(No los compartas ni los pegues en chats: son como una contrasena.)")
    print("\nSiguiente paso, despues de cada corrida:")
    print("    python polar_sync.py")
    print("=================================================\n")


if __name__ == "__main__":
    main()
