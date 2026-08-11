#!/usr/bin/env python3
"""
agregador_connect.py — Conecta a un atleta con TID-MAX vía Junction (ex-Vital).

Junction es un AGREGADOR: una sola integracion cubre WHOOP + Polar + Garmin +
Oura + Fitbit + Strava + Apple + ... (300+ dispositivos). El atleta elige su
marca en un widget que hospeda Junction (con logos), hace login en SU marca, y
a partir de ahi sus entrenos llegan ya normalizados a nuestra API.

Que hace este script (una vez por atleta):
  1. Crea (o reutiliza) el usuario del atleta en Junction.
  2. Genera un "link token" y arma la URL del widget "Conectate".
  3. Te imprime esa URL (mandasela al atleta por WhatsApp: la abre en SU cel y
     conecta su reloj/banda). Tambien intenta abrirla aqui por si conectas tu.
  4. Guarda el mapeo atleta -> user_id en datos/agregador_users.json.

Uso:
    python agregador_connect.py --atleta gael
    python agregador_connect.py --atleta carlos --provider polar   # salta directo a Polar

Requisitos previos en .env (de tu dashboard de Junction, https://app.junction.com):
    JUNCTION_API_KEY=...            (trátalo como contraseña)
    JUNCTION_API_BASE=https://api.sandbox.us.junction.com   (COPIA el de tu dashboard)
    JUNCTION_ENV=sandbox           (sandbox | production)
    JUNCTION_REGION=us             (us | eu)

Nota: 'sandbox' te deja probar gratis con datos simulados. Para datos reales de un
reloj, pon el atleta en 'production' (mismo codigo, otras llaves y base).

Siguiente paso, una vez que el atleta conecto su marca:
    python agregador_sync.py
"""
import os
import sys
import json
import argparse
import webbrowser

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Falta 'python-dotenv'. Instala con:  pip install -r requirements.txt")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
STORE_PATH = os.path.join(SCRIPT_DIR, "datos", "agregador_users.json")

# Base por defecto (sandbox US). Se sobreescribe con JUNCTION_API_BASE del .env.
DEFAULT_API_BASE = "https://api.sandbox.us.junction.com"
DEFAULT_LINK_BASE = "https://link.tryvital.io"


def load_store():
    """Almacen de atletas: { "atleta": {"user_id","client_user_id","env"} }."""
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_store(store):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def _cfg():
    load_dotenv(ENV_PATH)
    api_key = os.getenv("JUNCTION_API_KEY", "").strip()
    api_base = os.getenv("JUNCTION_API_BASE", DEFAULT_API_BASE).strip().rstrip("/")
    link_base = os.getenv("JUNCTION_LINK_BASE", DEFAULT_LINK_BASE).strip().rstrip("/")
    env = os.getenv("JUNCTION_ENV", "sandbox").strip() or "sandbox"
    region = os.getenv("JUNCTION_REGION", "us").strip() or "us"
    if not api_key:
        sys.exit(
            "\nFalta JUNCTION_API_KEY en .env.\n"
            "Sacala de tu dashboard de Junction (https://app.junction.com) > API Keys.\n"
            "Y confirma JUNCTION_API_BASE con la base que te muestra tu dashboard."
        )
    return api_key, api_base, link_base, env, region


def _hdr(api_key):
    return {"x-vital-api-key": api_key, "Content-Type": "application/json",
            "Accept": "application/json"}


def crear_o_reusar_usuario(api_key, api_base, atleta, store):
    """Devuelve el user_id de Junction para 'atleta' (lo crea si no existe)."""
    client_user_id = f"tidmax-{atleta}"

    # Si ya lo tenemos guardado, lo reusamos.
    if atleta in store and store[atleta].get("user_id"):
        return store[atleta]["user_id"]

    # Crear usuario. Si ya existia (409/400 con conflicto), lo resolvemos por client_user_id.
    r = requests.post(f"{api_base}/v2/user",
                      headers=_hdr(api_key),
                      json={"client_user_id": client_user_id},
                      timeout=30)
    if r.status_code in (200, 201):
        return r.json().get("user_id")

    if r.status_code in (400, 409):
        # Ya existe: lo buscamos por client_user_id.
        g = requests.get(f"{api_base}/v2/user/resolve/{client_user_id}",
                         headers=_hdr(api_key), timeout=30)
        if g.status_code == 200:
            return g.json().get("user_id")

    sys.exit(f"\nNo pude crear/resolver el usuario en Junction ({r.status_code}):\n{r.text}\n"
             "Revisa que JUNCTION_API_KEY y JUNCTION_API_BASE sean correctos.")


def crear_link_token(api_key, api_base, user_id, provider=None):
    """Genera el link token para abrir el widget 'Conectate'."""
    body = {"user_id": user_id}
    if provider:
        body["provider"] = provider  # p.ej. 'polar', 'whoop', 'garmin', 'oura'
    r = requests.post(f"{api_base}/v2/link/token",
                      headers=_hdr(api_key), json=body, timeout=30)
    if r.status_code not in (200, 201):
        sys.exit(f"\nNo pude crear el link token ({r.status_code}):\n{r.text}")
    return r.json().get("link_token")


def main():
    parser = argparse.ArgumentParser(description="Conectar un atleta via Junction (agregador).")
    parser.add_argument("--atleta", required=True,
                        help="Nombre corto del atleta (ej. gael, carlos).")
    parser.add_argument("--provider", default=None,
                        help="Opcional: salta directo a una marca (polar, whoop, garmin, oura, fitbit).")
    args = parser.parse_args()
    atleta = args.atleta.strip().lower()

    api_key, api_base, link_base, env, region = _cfg()
    store = load_store()

    print(f"\n=== Junction — Conectar al atleta '{atleta}' ({env}/{region}) ===")
    user_id = crear_o_reusar_usuario(api_key, api_base, atleta, store)
    link_token = crear_link_token(api_key, api_base, user_id, args.provider)

    # URL del widget hospedado por Junction (el atleta elige su marca y hace login ahi).
    widget_url = f"{link_base}/?token={link_token}&env={env}&region={region}"

    store[atleta] = {"user_id": user_id, "client_user_id": f"tidmax-{atleta}", "env": env}
    save_store(store)

    print("\n===================== LISTO =====================")
    print(f"Atleta '{atleta}' registrado en Junction (user_id: {user_id}).")
    print("Mandale ESTE link para que conecte su reloj/banda desde su celular:\n")
    print("   " + widget_url + "\n")
    print("(El link es de un solo uso y caduca. Vuelve a correr este script para uno nuevo.)")
    print("Guardado el mapeo en datos/agregador_users.json (no lo compartas).")
    print("\nCuando el atleta ya conecto su marca, baja sus datos con:")
    print("    python agregador_sync.py")
    print("=================================================\n")

    # Intenta abrirlo aqui tambien (util si eres tu quien conecta).
    try:
        webbrowser.open(widget_url)
    except Exception:
        pass


if __name__ == "__main__":
    main()
