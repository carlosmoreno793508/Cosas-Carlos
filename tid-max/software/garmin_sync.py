#!/usr/bin/env python3
"""
garmin_sync.py — Baja los datos de Garmin Connect (API PERSONAL) de cada cuenta conectada.
STUB listo para enchufar una key real (no probado en vivo; sin cuenta disponible al escribirlo).

Qué baja (pull-only, tier personal):
  • Actividades: resumen JSON + archivo **.FIT** (el .FIT puede traer R-R latido a latido → HVC).
  • Salud: JSON diario (FC reposo, HVC nocturna, sueño, estrés, etc. — según lo que exponga la API).
Guarda en datos/garmin/<cuenta>/ (o datos/atletas/<slug>/garmin/ en multiusuario, como polar_sync).

⚠️  POR VERIFICAR contra https://developer.garmin.com/gc-developer-program/overview/:
      - paths reales de los endpoints (los de abajo son placeholders documentados);
      - formato de autenticación (Bearer token vs otro);
      - si el .FIT personal viene completo (con R-R) o recortado;
      - ventanas/paginación y límites de rate.
    Mientras no se verifique, corre en modo --dry para ver qué HARÍA sin pegarle a la red.

Uso:
    python garmin_sync.py                 # baja lo nuevo de todas las cuentas
    python garmin_sync.py --account carlos --days 30
    python garmin_sync.py --dry           # no llama a la red: imprime el plan y sale

Ingesta posterior (cuando haya datos reales): tid_data leería datos/garmin/<cuenta>/*.fit con
garmin_fit.extrae_rr_ms() → hrv_rr.analiza_rr(), y el health JSON → fila diaria (hrv_ms/rhr_bpm/
sueño), con procedencia 'garmin'. Ese cableado se hace al confirmar el formato real.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con:  pip install -r requirements.txt")

from garmin_auth import load_store  # reutiliza el almacén de cuentas

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_BASE = os.path.join(os.environ.get("TID_DATA_DIR") or os.path.join(SCRIPT_DIR, "datos"), "garmin")

# --- Endpoints (POR VERIFICAR; placeholders del programa) ---
API_BASE = "https://apis.garmin.com"                              # VERIFICAR
EP_ACTIVITIES = API_BASE + "/activity-service/activities"          # VERIFICAR
EP_ACTIVITY_FIT = API_BASE + "/activity-service/activities/{id}/fit"   # VERIFICAR
EP_HEALTH = API_BASE + "/wellness-service/dailies"                 # VERIFICAR


def _hdr(token, accept="application/json"):
    return {"Authorization": f"Bearer {token}", "Accept": accept}


def _get(url, token, accept="application/json", dry=False, **params):
    if dry:
        print(f"    [dry] GET {url}  {params or ''}")
        return None
    r = requests.get(url, headers=_hdr(token, accept), params=params, timeout=45)
    if r.status_code == 401:
        raise PermissionError("401 — token inválido/expirado; reconecta con garmin_auth.py")
    r.raise_for_status()
    return r


def sync_cuenta(nombre, cuenta, days, dry=False):
    """Baja actividades (.FIT + JSON) y salud (JSON) de una cuenta. Devuelve nº de ítems bajados."""
    token = (cuenta or {}).get("access_token")
    if not token:
        print(f"[{nombre}] sin access_token — reconecta con garmin_auth.py")
        return 0
    out_dir = os.path.join(OUT_BASE, nombre)
    if not dry:
        os.makedirs(out_dir, exist_ok=True)
    desde = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    hasta = datetime.now(timezone.utc).date().isoformat()
    bajados = 0

    # 1) Actividades
    try:
        resp = _get(EP_ACTIVITIES, token, dry=dry, uploadStartTimeInSeconds=desde, uploadEndTimeInSeconds=hasta)
        actividades = resp.json() if resp is not None else []
        for a in actividades:
            aid = a.get("activityId") or a.get("id")
            if aid is None:
                continue
            if not dry:
                with open(os.path.join(out_dir, f"act_{aid}.json"), "w", encoding="utf-8") as f:
                    json.dump(a, f, ensure_ascii=False, indent=2)
                fit = _get(EP_ACTIVITY_FIT.format(id=aid), token, accept="application/octet-stream", dry=dry)
                if fit is not None:
                    with open(os.path.join(out_dir, f"act_{aid}.fit"), "wb") as f:
                        f.write(fit.content)
            bajados += 1
    except Exception as e:
        print(f"[{nombre}] actividades: {e}")

    # 2) Salud diaria
    try:
        resp = _get(EP_HEALTH, token, dry=dry, startDate=desde, endDate=hasta)
        dailies = resp.json() if resp is not None else []
        if not dry and dailies:
            with open(os.path.join(out_dir, f"health_{desde}_{hasta}.json"), "w", encoding="utf-8") as f:
                json.dump(dailies, f, ensure_ascii=False, indent=2)
            bajados += len(dailies) if isinstance(dailies, list) else 1
    except Exception as e:
        print(f"[{nombre}] salud: {e}")

    print(f"[{nombre}] {'(dry) ' if dry else ''}{bajados} ítems" + ("" if dry else f" → {out_dir}"))
    return bajados


def main():
    ap = argparse.ArgumentParser(description="Baja datos de Garmin Connect (API personal).")
    ap.add_argument("--account", help="solo esta cuenta (default: todas)")
    ap.add_argument("--days", type=int, default=30, help="ventana hacia atrás en días (default 30)")
    ap.add_argument("--dry", action="store_true", help="no llama a la red: imprime el plan y sale")
    args = ap.parse_args()

    store = load_store()
    if not store:
        sys.exit("No hay cuentas Garmin conectadas. Conecta una con:  python garmin_auth.py --account <n>")
    cuentas = {args.account: store[args.account]} if args.account else store
    if args.account and args.account not in store:
        sys.exit(f"Cuenta '{args.account}' no encontrada. Conéctala con garmin_auth.py.")

    total = 0
    for nombre, cuenta in cuentas.items():
        total += sync_cuenta(nombre, cuenta, args.days, dry=args.dry)
    print(f"\nListo. {total} ítems en total." + (" (modo dry — nada se bajó)" if args.dry else ""))


if __name__ == "__main__":
    main()
