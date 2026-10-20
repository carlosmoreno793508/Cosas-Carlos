#!/usr/bin/env python3
"""
illness_signal.py — Alerta temprana de enfermedad (señal multiparámetro).

Port fiel del `IllnessSignalEngine` de NOOP (código abierto; ver dossier). PURO, determinista.
APROXIMADO — estimación en el dispositivo, NO un diagnóstico.

Idea (literatura de wearables): al incubar una infección, la FC en reposo ↑, la temperatura de
la piel ↑, la HRV (RMSSD) ↓ y la respiración ↑ tienden a moverse JUNTAS. En vez de una regla
tosca "2 de 4", se calcula:
  • un score compuesto 0–100 (para distinguir "leve" de "fuerte"),
  • con corroboración (≥2 señales disparadas) y un gate de magnitud,
  • y SUPRESIÓN por confusores (alcohol, estrés, sauna, entreno duro/tardío, viaje) que explican
    mejor el patrón → amortigua el score y lo baja de nivel.

Cada señal llega ya z-scoreada contra el baseline PERSONAL, con el signo "illness-ward" (positivo
= más parecido a enfermedad): RHR↑, temp↑, resp↑ pasan su z crudo; la HVC va NEGADA (una caída es
illness-ward). Honestidad: si el baseline no es confiable (<14 noches) NO se alerta (gate 0).

Sin dependencias externas (sólo stdlib).
"""

# ------------------------------------------------------------------ constantes (mirror NOOP)

RAISE_THRESHOLD = 50.0        # score ≥ esto → aviso ELEVADO
MILD_THRESHOLD = 25.0         # score ≥ esto (con corroboración) → leve
MIN_CORROBORATING = 2         # señales disparadas mínimas
SIGNAL_Z_THRESHOLD = 2.0      # |z| para que una señal "dispare" (~p95 personal)
K_Z_TO_SCORE = 22.0           # sub-score = k·(z − umbral)
PER_SIGNAL_CAP = 40.0         # tope por señal
CONFOUNDER_DAMPEN = 0.45      # factor de amortiguación si hay confusor

DISCLAIMER = "Estimación en el dispositivo, no es un diagnóstico."

# Orden fijo → señales disparadas deterministas.
_ORDEN = ["rhr", "temp_piel", "hvc", "respiracion"]
_ETIQUETA = {"rhr": "FC reposo ↑", "temp_piel": "temp piel ↑", "hvc": "HVC ↓", "respiracion": "respiración ↑"}


def evaluate(senales, baseline_confiable, ya_enfermo=False, confusores=None):
    """
    `senales`: dict con z illness-ward por señal (positivo = más parecido a enfermedad):
        {"rhr": z, "temp_piel": z, "hvc": z, "respiracion": z}  (cualquiera puede faltar / None).
        Recuerda: la HVC debe entrar ya NEGADA (caída de HVC = z positivo).
    `baseline_confiable`: True sólo si el baseline tiene ≥14 noches válidas y no está stale.
    `ya_enfermo`: el usuario registró sentirse mal (su log manda).
    `confusores`: lista de tags presentes que explican el patrón:
        de {"alcohol","estres","sauna","entreno_duro","viaje"}.

    Devuelve {score, nivel, senales_disparadas, suprimido_por, n_senales, mensaje}.
    Niveles: tranquilo · ya_enfermo · suprimido · leve · elevado.
    """
    senales = senales or {}
    confusores = confusores or []

    raw = 0.0
    disparadas = []
    for k in _ORDEN:
        z = senales.get(k)
        if z is None:
            continue
        over = z - SIGNAL_Z_THRESHOLD
        if over <= 0:
            continue
        disparadas.append(k)
        raw += min(PER_SIGNAL_CAP, K_Z_TO_SCORE * over)
    score = min(100.0, raw)
    n = len(disparadas)
    etiquetas = [_ETIQUETA[k] for k in disparadas]

    def res(sc, nivel, msg, sup=None):
        return {"score": round(sc, 1), "nivel": nivel, "senales_disparadas": etiquetas,
                "suprimido_por": sup or [], "n_senales": n, "mensaje": msg, "aprox": True}

    # Gate 0: baseline no confiable → nunca alertar (cold-start). Score se reporta, nivel tranquilo.
    if not baseline_confiable:
        return res(score, "tranquilo", "Aún aprendiendo tu baseline — pendiente, sin alertar.")

    # El usuario registró sentirse mal: su log es la verdad. "Descansa", nunca asustar.
    if ya_enfermo:
        de_acuerdo = score >= MILD_THRESHOLD and n >= 1
        msg = ("Descansa — registraste sentirte mal y tus números coinciden. " + DISCLAIMER) if de_acuerdo \
              else ("Descansa — registraste sentirte mal. Tómalo con calma hoy. " + DISCLAIMER)
        return res(score, "ya_enfermo", msg)

    # Corroboración + magnitud: ≥2 señales y score ≥ leve, si no → tranquilo.
    if n < MIN_CORROBORATING or score < MILD_THRESHOLD:
        return res(score, "tranquilo", "Nada notable — tus señales están en tu rango normal.")

    # Supresión por confusores (la parte diferenciadora): si hay alguno, amortigua y baja de nivel.
    presentes = [c for c in ["alcohol", "estres", "sauna", "entreno_duro", "viaje"] if c in confusores]
    if presentes:
        dampened = score * CONFOUNDER_DAMPEN
        sp = ", ".join(etiquetas) or "Algunas señales subieron"
        return res(dampened, "suprimido",
                   f"Algunas señales subieron ({sp}), pero registraste {', '.join(presentes)} — "
                   f"probablemente eso, no enfermedad. " + DISCLAIMER, sup=presentes)

    # Sin confusor: leve se queda en el detalle; un compuesto fuerte se eleva.
    sp = ", ".join(etiquetas)
    if score < RAISE_THRESHOLD:
        return res(score, "leve", f"Unas señales ligeramente elevadas ({sp}). Nada alarmante — "
                   f"vale un día más tranquilo. " + DISCLAIMER)
    return res(score, "elevado", f"Varios signos elevados ({sp}) que suelen preceder a una infección. "
               f"Prioriza descanso e hidratación. " + DISCLAIMER)


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # 1) Baseline no confiable → tranquilo pase lo que pase.
    r = evaluate({"rhr": 5, "hvc": 5}, baseline_confiable=False)
    assert r["nivel"] == "tranquilo"
    print("Baseline no confiable:", r["nivel"], "✓")

    # 2) Sin señales / una sola → tranquilo (necesita corroboración ≥2).
    assert evaluate({"rhr": 4}, True)["nivel"] == "tranquilo"
    assert evaluate({}, True)["nivel"] == "tranquilo"
    print("Una sola señal: tranquilo (corroboración) ✓")

    # 3) Dos señales fuertes (z=4 → sub 40 c/u = 80), baseline ok, sin confusor → ELEVADO.
    r3 = evaluate({"rhr": 4, "hvc": 4}, True)
    print("Fuerte:", r3["nivel"], "· score", r3["score"], "·", r3["senales_disparadas"])
    assert r3["nivel"] == "elevado" and r3["score"] == 80.0 and r3["n_senales"] == 2

    # 4) Dos señales leves (z≈3 → sub ~22-24 = ~46) → LEVE.
    r4 = evaluate({"rhr": 3.1, "temp_piel": 3.0}, True)
    print("Leve:", r4["nivel"], "· score", r4["score"])
    assert r4["nivel"] == "leve" and MILD_THRESHOLD <= r4["score"] < RAISE_THRESHOLD

    # 5) Mismo patrón fuerte PERO con confusor (alcohol) → SUPRIMIDO, score ×0.45.
    r5 = evaluate({"rhr": 4, "hvc": 4}, True, confusores=["alcohol"])
    print("Con alcohol:", r5["nivel"], "· score", r5["score"], "· por", r5["suprimido_por"])
    assert r5["nivel"] == "suprimido" and abs(r5["score"] - 80 * CONFOUNDER_DAMPEN) < 1e-6

    # 6) Usuario registró sentirse mal → ya_enfermo.
    r6 = evaluate({"rhr": 4, "hvc": 4}, True, ya_enfermo=True)
    assert r6["nivel"] == "ya_enfermo"
    print("Ya enfermo:", r6["nivel"], "✓")

    # 7) Umbral de disparo: z justo en 2.0 NO dispara (necesita > umbral).
    assert evaluate({"rhr": 2.0, "hvc": 2.0}, True)["n_senales"] == 0
    print("z=2.0 no dispara (necesita > umbral) ✓")

    print("\nOK — alerta temprana de enfermedad funcional (score 0-100, corroboración, supresión).")
