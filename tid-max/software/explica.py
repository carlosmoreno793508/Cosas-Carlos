#!/usr/bin/env python3
"""
explica.py — Explicabilidad "¿por qué este número?" para los scores de TID-MAX.

Traduce la traza interna de un score (los términos ponderados que ya devuelven `recovery_score`
y `sleep_score`) a frases legibles: qué término movió el score y en qué dirección. Es el patrón
"¿por qué este sueño?" / "ver qué término lo movió" que vimos en NOOP (transparencia por
decisión), pero sobre NUESTROS scores.

No recalcula nada: consume el dict que ya produce cada scorer, así la explicación NO PUEDE
divergir del número. Puro, determinista, sin dependencias.
"""

# Etiquetas legibles por término de Carga (recovery_score).
_CARGA_LABEL = {
    "hrv": "VFC (variabilidad de la FC)",
    "rhr": "FC en reposo",
    "resp": "respiración",
    "sueno": "calidad del sueño",
    "temp_piel": "temperatura de la piel",
    "recovery_index": "caída de FC nocturna",
    "activity_balance": "esfuerzo del día previo",
}

# Etiquetas por término de Descanso (sleep_score).
_DESCANSO_LABEL = {
    "duracion": "horas vs necesarias",
    "eficiencia": "eficiencia de sueño",
    "reparador": "sueño reparador (profundo+REM)",
    "consistencia": "consistencia de horario",
}


def _signo_frase(contrib):
    return "subió" if contrib > 0 else "bajó"


def explica_carga(carga, top=3):
    """
    Explica una salida de `recovery_score.carga`. Devuelve {score, banda, por_que:[frases],
    detalle:[{termino, contribucion}]}. La contribución de cada término es z·w (su aporte al z
    compuesto); se ordenan por magnitud. Cold-start (carga None) → None.
    """
    if carga is None:
        return None
    terminos = carga.get("terminos", [])
    detalle = []
    for t in terminos:
        contrib = t["z"] * t["w"]
        detalle.append({"termino": t["nombre"], "contribucion": round(contrib, 4),
                        "z": t["z"], "w": t["w"]})
    detalle.sort(key=lambda d: abs(d["contribucion"]), reverse=True)

    frases = []
    for d in detalle[:top]:
        if abs(d["contribucion"]) < 1e-6:
            continue
        label = _CARGA_LABEL.get(d["termino"], d["termino"])
        frases.append(f"Tu {label} {_signo_frase(d['contribucion'])} la Carga "
                      f"({'+' if d['z'] >= 0 else ''}{d['z']:.2f}σ vs tu base).")
    if carga.get("saturacion_parasimpatica_detectada"):
        frases.append("⚠ Posible saturación parasimpática (VFC baja con FC en reposo baja): "
                      "la penalización por VFC NO se aplicó (detectada, no corregida).")
    return {"score": carga["score"], "banda": carga["banda"], "por_que": frases, "detalle": detalle}


def explica_descanso(descanso, top=3):
    """
    Explica una salida de `sleep_score.descanso`/`descanso_de_noche`. Compara cada término
    contra el ideal (1.0) y ordena por cuánto le faltó/sobró, ponderado por su peso. None → None.
    """
    if descanso is None:
        return None
    import sleep_score as _ss
    pesos = {"duracion": _ss.W_DURATION, "eficiencia": _ss.W_EFFICIENCY,
             "reparador": _ss.W_RESTORATIVE, "consistencia": _ss.W_CONSISTENCY}
    terminos = descanso.get("terminos", {})
    detalle = []
    for nombre, peso in pesos.items():
        val = terminos.get(nombre)
        if val is None:
            continue
        # Déficit ponderado contra el ideal (1.0): negativo = arrastró el score hacia abajo.
        contrib = (val - 1.0) * peso
        detalle.append({"termino": nombre, "valor": val, "deficit_ponderado": round(contrib, 4)})
    detalle.sort(key=lambda d: d["deficit_ponderado"])  # los que más restan, primero

    frases = []
    for d in detalle[:top]:
        label = _DESCANSO_LABEL.get(d["termino"], d["termino"])
        if d["deficit_ponderado"] < -0.02:
            frases.append(f"Lo que más bajó el Descanso: {label} ({d['valor']*100:.0f}% del ideal).")
        else:
            frases.append(f"{label.capitalize()} estuvo bien ({d['valor']*100:.0f}% del ideal).")
    return {"score": descanso["score"], "banda": descanso["banda"],
            "por_que": frases, "detalle": detalle}


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    import recovery_score
    import sleep_score

    base_hrv = {"mean": 60.0, "spread": 8.0, "usable": True, "status": "confiable"}
    base_rhr = {"mean": 52.0, "spread": 3.0, "usable": True, "status": "confiable"}

    # Noche mala: HRV baja + RHR alta → Carga baja; la explicación debe señalar VFC/RHR.
    c = recovery_score.carga(hrv=40.0, rhr=60.0, hrv_baseline=base_hrv, rhr_baseline=base_rhr,
                             sueno_calidad=0.70, temp_piel_dev=1.0)
    ec = explica_carga(c)
    print("Carga:", ec["score"], ec["banda"])
    for f in ec["por_que"]:
        print("  ·", f)
    assert ec["detalle"][0]["termino"] == "hrv"           # VFC domina (peso 0.55)
    assert any("VFC" in f for f in ec["por_que"])

    # Cold-start → None.
    base_cal = {"mean": 60.0, "spread": 8.0, "usable": False, "status": "calibrando"}
    assert explica_carga(recovery_score.carga(hrv=60, rhr=52, hrv_baseline=base_cal)) is None

    # Descanso con sueño corto → "horas vs necesarias" debe salir como lo que más baja.
    d = sleep_score.descanso_de_noche(total_sleep_min=5 * 60, efficiency=0.90, need_hours=8.0,
                                      deep_min=90, rem_min=80, consistency=0.85)
    ed = explica_descanso(d)
    print("Descanso:", ed["score"], ed["banda"])
    for f in ed["por_que"]:
        print("  ·", f)
    assert ed["detalle"][0]["termino"] == "duracion"       # la duración corta es lo que más resta
    assert any("horas vs necesarias" in f for f in ed["por_que"])

    print("\nOK — explicabilidad '¿por qué este número?' funcional (no recalcula, consume la traza).")
