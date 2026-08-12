#!/usr/bin/env python3
"""
tid_web.py — Puente entre el pipeline y el dashboard WEB (Vercel).

Lee la salida del coach (datos/procesado/coach-hoy.json) + el consumo del día y escribe
tid-max/web/data.json, que es lo que consume la página estática (tid-max/web/index.html).
Así la web NO tiene lógica: el motor determinista + agentes viven en Python, y la web solo
PINTA el data.json. Para actualizar el tablero, se regenera este data.json (a mano hoy, o con
un cron en la nube mañana) y Vercel lo sirve con dirección fija 24/7.

Uso:
    python tid_agent.py          # genera coach-hoy.json (con IA)
    python tid_web.py            # escribe tid-max/web/data.json
    (git commit + push  →  Vercel redepliega solo la web con el dato nuevo)
"""
import os
import json
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# TID_PROC_DIR: carpeta 'procesado' de origen (per-atleta en el pipeline multiusuario).
PROC = os.environ.get("TID_PROC_DIR") or os.path.join(SCRIPT_DIR, "datos", "procesado")
COACH_JSON = os.path.join(PROC, "coach-hoy.json")
CONSUMO_JSON = os.path.join(PROC, "consumo-hoy.json")
WEB_DATA = os.path.join(SCRIPT_DIR, "..", "web", "data.json")
APP_DATA = os.path.join(SCRIPT_DIR, "..", "app", "data.json")
# TID_REPORT_OUT: si está, escribe el reporte a ESA sola ruta (privada, por atleta)
# en vez de a web/ y app/. El login (Fase 2) sirve estos reportes por atleta autenticado.
REPORT_OUT = os.environ.get("TID_REPORT_OUT") or None

_MESES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
_DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
SEM_TITULO = {"verde": "Listo para entrenar", "amarillo": "Recovery media", "rojo": "Cuidado — recovery baja"}


def _fecha_texto(iso):
    try:
        d = datetime.date.fromisoformat(iso[:10])
        return f"{_DIAS[d.weekday()]} {d.day} {_MESES[d.month]} {d.year}"
    except Exception:
        return iso[:10] if iso else ""


def _load(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _nivel_alerta(txt):
    t = (txt or "").lower()
    if any(k in t for k in ("rebot", "recuper", "mejor", "buen", "cerrada", "ya está")):
        return "good"
    return "med"


def build_data():
    p = _load(COACH_JSON)
    if not p:
        raise SystemExit("No hay coach-hoy.json. Corre primero:  python tid_agent.py")
    f = p.get("hechos", {})
    sd = f.get("sueno_detalle") or {}
    forma = f.get("forma") or {}
    rend = p.get("rendimiento") or {}
    fecha_iso = (p.get("generado_utc") or "")[:10] or datetime.date.today().isoformat()

    # Nutrición: consumo real del día si existe; si no, solo la meta.
    consumo = _load(CONSUMO_JSON)
    hoy = datetime.date.today().isoformat()
    macros = f.get("macros_hoy") or {}
    meta_k = f.get("kcal_objetivo_hoy")
    nutricion = {
        "consumido": 0, "meta": meta_k or 0,
        "c": macros.get("C"), "p": macros.get("P"), "g": macros.get("G"),
        "comidas": [], "pendiente": None,
    }
    if consumo and consumo.get("fecha") == hoy:
        tot = consumo.get("totales", {})
        meta = consumo.get("meta", {})
        nutricion.update({
            "consumido": tot.get("kcal", 0),
            "meta": meta.get("kcal") or meta_k or 0,
            "c": tot.get("carb_g"), "p": tot.get("prot_g"), "g": tot.get("grasa_g"),
            "comidas": [{"hora": c.get("hora", ""), "nombre": c.get("platillo", ""),
                         "kcal": c.get("kcal", 0)} for c in consumo.get("comidas", [])],
        })

    # Preserva las comidas YA publicadas en data.json (p. ej. subidas por API/foto, o por un
    # sync previo del mismo día). Si este re-sync no trae consumo propio pero el data.json del
    # MISMO día ya tenía comidas, no las borres: un re-sync de la tarde (para atrapar la siesta)
    # no debe tirar lo que la familia ya cargó. En un día nuevo la fecha no coincide → limpio.
    if not nutricion["comidas"]:
        prev = _load(os.path.abspath(REPORT_OUT or WEB_DATA))
        prev_nu = (prev or {}).get("nutricion") or {}
        if prev and prev.get("fecha") == fecha_iso and prev_nu.get("comidas"):
            nutricion.update({
                "consumido": prev_nu.get("consumido", 0),
                "meta": nutricion["meta"] or prev_nu.get("meta") or 0,
                "c": prev_nu.get("c"), "p": prev_nu.get("p"), "g": prev_nu.get("g"),
                "comidas": prev_nu.get("comidas"),
                "pendiente": prev_nu.get("pendiente"),
            })

    razones = f.get("razones") or []
    data = {
        "fecha": fecha_iso,
        "fecha_texto": _fecha_texto(fecha_iso),
        "atleta": p.get("atleta") or f.get("atleta") or "Atleta",
        "dias_datos": f.get("dias_de_datos"),
        "deporte": f.get("deporte_nombre") or "Natación",
        "fase": f.get("fase") or f.get("fase_plan_semana") or "—",
        "evento": f.get("evento") or "el evento",
        "dias_al_evento": f.get("dias_al_evento"),
        "dias_al_viaje": f.get("dias_al_viaje"),
        "semaforo": p.get("semaforo") or "amarillo",
        "semaforo_titulo": (razones[0] if razones else SEM_TITULO.get(p.get("semaforo"), "")),
        "semaforo_desc": p.get("veredicto") or "; ".join(razones),
        "recovery": f.get("recovery_pct"),
        "hrv": {"ms": f.get("hrv_ms"), "vs_base_pct": f.get("hrv_vs_base_pct"), "base": f.get("hrv_base_ms")},
        "rhr": {"lpm": f.get("fc_reposo_lpm"), "vs_base_pct": f.get("fc_reposo_vs_base_pct"),
                "base": f.get("fc_reposo_base_lpm")},
        "sueno": {
            "total_h": sd.get("horas_anoche"), "noche_h": sd.get("horas_noche"),
            "siesta_h": sd.get("siesta_h") or 0, "n_siestas": sd.get("n_siestas") or 0,
            "perf": f.get("sueno_pct"), "efic": sd.get("eficiencia_pct"),
            "deep_pct": sd.get("profundo_pct"), "rem_pct": sd.get("rem_pct"),
            "consist": sd.get("consistencia_pct"), "despertares": sd.get("despertares"),
            "deuda_min": sd.get("deuda_min"), "acostado": sd.get("acostado"),
            "despertar": sd.get("despertar"), "prom_7d": sd.get("horas_prom_7d"),
            "perf_prom_7d": sd.get("perf_prom_7d"),
        },
        "forma": {
            "ctl": forma.get("fitness_ctl"), "atl": forma.get("fatiga_atl"),
            "tsb": forma.get("forma_tsb"), "tsb_previa": forma.get("forma_tsb_previa"),
            "estado_pico": rend.get("estado") or "sin_datos",
            "lectura": rend.get("lectura") or "",
        },
        "alertas": [{"nivel": _nivel_alerta(a), "tag": "Preventivo", "texto": a}
                    for a in (p.get("alertas") or []) if isinstance(a, str)],
        "nutricion": nutricion,
        "nota_datos": "Fuente: WHOOP + motor determinista + agentes Claude. El sueño suma las siestas. "
                      "“Forma” es un proxy sobre el strain de WHOOP: lee la tendencia, no el número absoluto.",
    }
    return data


def main():
    data = build_data()
    # Multiusuario: si TID_REPORT_OUT está, el reporte va a UNA ruta privada por atleta.
    # (El login de la Fase 2 lo sirve; NO se publica como data.json estático.)
    destinos = (REPORT_OUT,) if REPORT_OUT else (WEB_DATA, APP_DATA)
    salidas = []
    for destino in destinos:
        out = os.path.abspath(destino)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        salidas.append(out)
    print(f"data.json actualizado ({data['fecha']} · {data['semaforo'].upper()} · "
          f"recovery {data.get('recovery')}%).")
    for out in salidas:
        print(f"  → {out}")
    print("Sube el cambio (git add web/data.json app/data.json && git commit && git push) "
          "y Vercel redepliega web + app.")


if __name__ == "__main__":
    main()
