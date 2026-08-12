#!/usr/bin/env python3
"""
tid_multi.py — Pipeline MULTIUSUARIO de TID-MAX.

Recorre el registro de atletas (atletas.json) y, POR CADA UNO, corre el pipeline
completo (sync de su fuente -> normalizar -> coach -> reporte) de forma AISLADA:
cada atleta tiene su propia carpeta de datos, para que el reporte de uno nunca
arrastre los workouts de otro.

Reusa los scripts que ya existen (whoop_sync / polar_sync / agregador_sync /
tid_data / tid_agent / tid_web) pasándoles overrides por variable de entorno:
  TID_DATA_DIR  — carpeta de datos crudos del atleta (aísla WHOOP/Polar/agregador).
  TID_CONFIG    — su archivo de perfil/config (nutricion-gael.json, perfil-carlos.json…).
  TID_PROC_DIR  — su carpeta 'procesado' (dataset.json + coach-hoy.json).
  TID_REPORT_OUT— dónde escribe su reporte PRIVADO (reportes/<slug>.json).

Salida: reportes/<slug>.json por atleta (privado; el login de la Fase 2 lo sirve).
El atleta 'público' (el primero activo, o --publico <slug>) ADEMÁS refresca el
dashboard público actual (web/data.json + app/data.json) para no romper lo que ya vive.

Uso:
    python tid_multi.py                 # todos los atletas activos
    python tid_multi.py --solo carlos-moreno
    python tid_multi.py --sin-sync      # no baja datos; solo re-genera reportes
    python tid_multi.py --publico gael-moreno
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER = os.path.join(SCRIPT_DIR, "atletas.json")
ATLETAS_BASE = os.path.join(SCRIPT_DIR, "datos", "atletas")
REPORTES_DIR = os.path.join(SCRIPT_DIR, "reportes")
WEB_DATA = os.path.join(SCRIPT_DIR, "..", "web", "data.json")
APP_DATA = os.path.join(SCRIPT_DIR, "..", "app", "data.json")


def cargar_roster():
    with open(ROSTER, encoding="utf-8") as f:
        data = json.load(f)
    atletas = data.get("atletas") if isinstance(data, dict) else data
    return [a for a in (atletas or []) if isinstance(a, dict) and a.get("slug")]


def correr(script, env, args=None, fatal=False):
    """Corre un script del pipeline con env override. Devuelve True si salió 0.
    fatal=False: un fallo NO tumba al atleta (se sigue con lo que haya)."""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script)] + (args or [])
    full_env = {**os.environ, **env}
    r = subprocess.run(cmd, env=full_env, cwd=SCRIPT_DIR,
                       capture_output=True, text=True)
    salida = (r.stdout or "") + (r.stderr or "")
    # Ecoa la salida indentada para que se lea en el log del atleta.
    for linea in salida.rstrip().splitlines():
        print("    " + linea)
    if r.returncode != 0 and fatal:
        raise RuntimeError(f"{script} salió {r.returncode}")
    return r.returncode == 0


def sync_fuente(atleta, base, env):
    """Baja el crudo de la fuente del atleta a SU carpeta. Defensivo: si falla
    (p. ej. sin tokens en la nube), se sigue con lo que ya exista en disco."""
    fuente = (atleta.get("fuente") or "").lower()
    slug = atleta["slug"]
    try:
        if fuente == "whoop":
            print(f"    → sync WHOOP → {base}")
            correr("whoop_sync.py", env)
        elif fuente == "agregador":
            # 'agregador_atleta' = la carpeta del usuario en Junction (por defecto el slug;
            # se alinea cuando el atleta reconecta su fuente desde la app con su nombre).
            ja = atleta.get("agregador_atleta") or slug
            print(f"    → sync agregador (Junction, atleta '{ja}') → {base}")
            correr("agregador_sync.py", env, ["--atleta", ja])
        elif fuente == "polar":
            print(f"    → sync Polar Flow → {base}")
            correr("polar_sync.py", env)
        else:
            print(f"    (fuente '{fuente}' desconocida; sin sync)")
    except Exception as e:  # noqa: BLE001 — nunca tumbamos el pipeline por un sync
        print(f"    (sync {fuente} no fatal: {e})")


def procesar_atleta(atleta, do_sync=True):
    slug = atleta["slug"]
    base = os.path.join(ATLETAS_BASE, slug)
    proc = os.path.join(base, "procesado")
    os.makedirs(proc, exist_ok=True)
    os.makedirs(REPORTES_DIR, exist_ok=True)
    reporte = os.path.join(REPORTES_DIR, f"{slug}.json")

    # Env base del atleta: aísla datos + elige su config/perfil.
    env = {"TID_DATA_DIR": base, "TID_PROC_DIR": proc}
    # Config/perfil del atleta. Si no tiene uno propio, usamos perfil-<slug>.json
    # (probablemente inexistente aún) para NO caer al config por defecto de otro atleta.
    env["TID_CONFIG"] = atleta.get("perfil") or f"perfil-{slug}.json"
    if atleta.get("nombre"):
        env["TID_ATLETA"] = atleta["nombre"]
    if atleta.get("deporte"):
        env["TID_DEPORTE"] = atleta["deporte"]

    # Copia los archivos de planificación de ESTE atleta a su carpeta aislada. En modo
    # multiusuario tid_data NO cae al SCRIPT_DIR compartido (para no filtrar el plan de
    # uno al reporte de otro), así que cada atleta trae los suyos aquí.
    for nombre in (atleta.get("planes") or []):
        origen = os.path.join(SCRIPT_DIR, nombre)
        if os.path.exists(origen):
            shutil.copyfile(origen, os.path.join(base, nombre))

    print(f"\n═══ {atleta.get('nombre', slug)}  ({slug} · {atleta.get('fuente')} · {atleta.get('deporte')}) ═══")

    if do_sync:
        sync_fuente(atleta, base, env)

    # Normalizar: tid_data lee de 'base' y escribe en 'proc'. Si NO hay datos, sale
    # !=0; lo tomamos como 'sin datos aún' y no generamos reporte este run.
    ok = correr("tid_data.py", env, [base, proc])
    if not ok:
        print(f"    (sin datos aún para {slug}; su reporte aparecerá cuando fluya su fuente)")
        return None

    # Coach: usa IA si hay ANTHROPIC_API_KEY; si no, cae a reglas solo (tid_agent decide).
    correr("tid_agent.py", env)

    # Reporte PRIVADO del atleta.
    env_rep = {**env, "TID_REPORT_OUT": reporte}
    if not correr("tid_web.py", env_rep):
        print(f"    (no se pudo escribir el reporte de {slug})")
        return None
    print(f"    ✓ reporte privado → {os.path.relpath(reporte, SCRIPT_DIR)}")
    return reporte


def escribir_indice(atletas, generados):
    """Índice NO secreto de atletas (para login/app): quién existe y si tiene reporte."""
    idx = {
        "_uso": "Índice de atletas del ecosistema (no secreto). Lo consume el login/app "
                "para saber quién existe. Los datos privados van en reportes/<slug>.json, "
                "servidos solo tras autenticar.",
        "atletas": [
            {"slug": a["slug"], "nombre": a.get("nombre"), "deporte": a.get("deporte"),
             "fuente": a.get("fuente"), "tiene_reporte": a["slug"] in generados}
            for a in atletas
        ],
    }
    os.makedirs(REPORTES_DIR, exist_ok=True)
    with open(os.path.join(REPORTES_DIR, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description="Pipeline multiusuario de TID-MAX.")
    ap.add_argument("--solo", default=None, help="Procesar solo ese slug.")
    ap.add_argument("--publico", default=None,
                    help="Slug cuyo reporte ADEMÁS refresca el dashboard público (default: 1º activo).")
    ap.add_argument("--sin-sync", action="store_true", help="No bajar datos; solo re-generar reportes.")
    args = ap.parse_args()

    roster = cargar_roster()
    activos = [a for a in roster if a.get("activo", True)]
    if args.solo:
        activos = [a for a in activos if a["slug"] == args.solo]
        if not activos:
            sys.exit(f"No encuentro al atleta activo '{args.solo}' en atletas.json.")

    publico = args.publico or (activos[0]["slug"] if activos else None)

    print("═══════════ TID-MAX · PIPELINE MULTIUSUARIO ═══════════")
    print(f"Atletas activos: {', '.join(a['slug'] for a in activos) or '(ninguno)'}")
    print(f"Dashboard público lo refresca: {publico}")

    generados = {}
    for atleta in activos:
        try:
            reporte = procesar_atleta(atleta, do_sync=not args.sin_sync)
        except Exception as e:  # noqa: BLE001 — un atleta no tumba a los demás
            print(f"    ✗ error procesando {atleta['slug']}: {e}")
            reporte = None
        if reporte:
            generados[atleta["slug"]] = reporte

    # El atleta 'público' refresca el dashboard actual (web + app) para no romperlo.
    if publico and publico in generados:
        for destino in (WEB_DATA, APP_DATA):
            out = os.path.abspath(destino)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copyfile(generados[publico], out)
        print(f"\nDashboard público actualizado desde '{publico}' → web/data.json + app/data.json")

    escribir_indice(roster, generados)

    print("\n─────────────────────── Resumen ───────────────────────")
    for a in activos:
        estado = "✓ reporte" if a["slug"] in generados else "· sin datos aún"
        print(f"  {estado:16} {a['slug']}")
    print(f"\nReportes privados en: {os.path.relpath(REPORTES_DIR, SCRIPT_DIR)}/")
    if not generados:
        print("(Ningún atleta generó reporte todavía — falta que fluya su fuente de datos.)")


if __name__ == "__main__":
    main()
