#!/usr/bin/env python3
"""
live_session.py — "Guardián silencioso": loop de esfuerzo-objetivo en vivo.

Port del `LiveSessionEngine` de NOOP (código abierto, PolyForm Noncommercial; ver dossier
`analisis/noop-ipa-teardown.md`). Puro, determinista, sin BLE ni reloj: el tiempo se pasa en
cada `update(now, bpm)`, así una sesión se reproduce desde una traza sintética de HR.

Vigila la FC en vivo contra una **banda objetivo condicionada por la Carga de hoy** y emite
como mucho dos cues hápticos: un empujón suave (PUSH) cuando vas demasiado fácil para hoy, y
un "afloja" firme (EASE_OFF) cuando aprietas más de lo que tu recuperación de hoy puede pagar.
**El silencio significa que vas bien** — ese es el punto del diseño.

Dos reglas dominan: (1) un buzz EQUIVOCADO es imperdonable, uno OMITIDO está bien → sesgo
fuerte hacia el silencio (dwell, cooldown, histéresis). (2) Nunca fabricar: muestras imposibles
se rechazan; un stream viejo pausa el coaching en vez de adivinar.

Banda desde Carga (confirmado con datos reales: Charge 66 → zona 136–158 bpm en el iPhone de
Carlos): techo %HRR interpola 0.60 (Carga 0) → 0.82 (Carga 100); piso = techo − 0.15, nunca
bajo 0.40; bpm = RHR + %HRR·(FCmáx − RHR).

NOTA: se portan la banda y el núcleo del coaching (warmup/stale/dwell/cooldown/histéresis +
acumulado dentro/debajo/encima). Refinamientos de NOOP omitidos aquí (atribución de "climb"
para EASE_OFF, deriva del techo en días fuertes) quedan documentados para una iteración.

Sin dependencias externas (sólo stdlib).
"""

# ------------------------------------------------------------------ constantes (LiveSessionEngine)

CEILING_PCT_AT_LOW_CHARGE = 0.60
CEILING_PCT_AT_HIGH_CHARGE = 0.82
BAND_WIDTH_PCT_HRR = 0.15
MIN_FLOOR_PCT_HRR = 0.40
DEFAULT_CHARGE_FRACTION = 0.5

SMOOTHING_WINDOW_SEC = 12
STALE_AFTER_SEC = 8
WARMUP_SEC = 60
DWELL_SEC = 25
COOLDOWN_SEC = 50
HYSTERESIS_MARGIN_BPM = 2.0
MAX_ACCRUAL_DT_SEC = 5

MIN_PLAUSIBLE_BPM = 25.0
ABOVE_HRMAX_REJECT_BPM = 5.0
MAX_JUMP_BPM = 45.0


def _mediana(xs):
    ys = sorted(xs)
    n = len(ys)
    if n == 0:
        return None
    mid = n // 2
    return ys[mid] if n % 2 else (ys[mid - 1] + ys[mid]) / 2.0


def banda(rhr, hrmax, charge=None):
    """
    Banda objetivo de FC desde la Carga de hoy (0..100; None → punto medio conservador 0.5).
    Devuelve {floor_bpm, ceiling_bpm, floor_pct, ceiling_pct}.
    """
    cn = DEFAULT_CHARGE_FRACTION if charge is None else min(max(charge / 100.0, 0.0), 1.0)
    ceiling_pct = CEILING_PCT_AT_LOW_CHARGE + (CEILING_PCT_AT_HIGH_CHARGE - CEILING_PCT_AT_LOW_CHARGE) * cn
    floor_pct = max(ceiling_pct - BAND_WIDTH_PCT_HRR, MIN_FLOOR_PCT_HRR)
    reserve = max(hrmax - rhr, 1.0)
    return {
        "floor_bpm": round(rhr + floor_pct * reserve, 1),
        "ceiling_bpm": round(rhr + ceiling_pct * reserve, 1),
        "floor_pct": round(floor_pct, 4),
        "ceiling_pct": round(ceiling_pct, 4),
    }


class LiveSession:
    """Motor de sesión en vivo. Alimentar con update(now_s, bpm); leer totales al final."""

    def __init__(self, rhr, hrmax, charge, start_ts):
        self.rhr = rhr
        self.hrmax = hrmax
        self.band = banda(rhr, hrmax, charge)
        self.start_ts = start_ts
        self.last_update_ts = start_ts
        self.last_valid_ts = None
        self.last_accepted_bpm = None
        self.position = "in_band"
        self._buffer = []          # (ts, bpm) dentro de la ventana de suavizado
        self.in_band_s = 0.0
        self.below_s = 0.0
        self.above_s = 0.0
        self._below_since = None
        self._above_since = None
        self._last_push_ts = None
        self._last_ease_ts = None
        self.cues_push = 0
        self.cues_ease = 0

    def _acepta(self, now, bpm):
        if bpm < MIN_PLAUSIBLE_BPM:
            return False
        if bpm > self.hrmax + ABOVE_HRMAX_REJECT_BPM:
            return False
        if self.last_accepted_bpm is not None and abs(bpm - self.last_accepted_bpm) > MAX_JUMP_BPM:
            return False
        return True

    def _posicion(self, smoothed):
        """Posición con histéresis: sólo cambia al cruzar el borde ± margen."""
        f, c, m = self.band["floor_bpm"], self.band["ceiling_bpm"], HYSTERESIS_MARGIN_BPM
        if smoothed >= c + m:
            return "above"
        if smoothed <= f - m:
            return "below"
        if f + m <= smoothed <= c - m:
            return "in_band"
        return self.position  # zona de histéresis → mantiene

    def update(self, now, bpm):
        """Un tick. Devuelve {status, position, smoothed_bpm, cue, in_band_s, below_s, above_s}."""
        sample_ok = self._acepta(now, bpm)
        if sample_ok:
            self.last_valid_ts = now
            self.last_accepted_bpm = bpm
            self._buffer.append((now, bpm))
            self._buffer = [(t, b) for (t, b) in self._buffer if now - t <= SMOOTHING_WINDOW_SEC]

        # Stale: sin muestra válida reciente → coaching en pausa.
        stale = self.last_valid_ts is None or (now - self.last_valid_ts) > STALE_AFTER_SEC
        smoothed = _mediana([b for _, b in self._buffer]) if self._buffer and not stale else None

        # Acumular tiempo por posición (dt acotado para que un stall no infle).
        dt = min(now - self.last_update_ts, MAX_ACCRUAL_DT_SEC)
        if dt < 0:
            dt = 0
        self.last_update_ts = now

        warmup = (now - self.start_ts) < WARMUP_SEC
        cue = None

        if stale or smoothed is None:
            status = "stale"
        else:
            self.position = self._posicion(smoothed)
            if self.position == "in_band":
                self.in_band_s += dt
                self._below_since = None
                self._above_since = None
            elif self.position == "below":
                self.below_s += dt
                self._above_since = None
                if self._below_since is None:
                    self._below_since = now
            else:  # above
                self.above_s += dt
                self._below_since = None
                if self._above_since is None:
                    self._above_since = now

            status = "warmup" if warmup else "active"

            # Cues sólo fuera de warmup, tras dwell continuo y respetando cooldown.
            if not warmup:
                if (self.position == "below" and self._below_since is not None
                        and now - self._below_since >= DWELL_SEC
                        and (self._last_push_ts is None or now - self._last_push_ts >= COOLDOWN_SEC)):
                    cue = "push_nudge"
                    self._last_push_ts = now
                    self.cues_push += 1
                elif (self.position == "above" and self._above_since is not None
                        and now - self._above_since >= DWELL_SEC
                        and (self._last_ease_ts is None or now - self._last_ease_ts >= COOLDOWN_SEC)):
                    cue = "ease_off"
                    self._last_ease_ts = now
                    self.cues_ease += 1

        return {
            "status": status,
            "position": self.position,
            "smoothed_bpm": round(smoothed, 1) if smoothed is not None else None,
            "cue": cue,
            "in_band_s": round(self.in_band_s, 1),
            "below_s": round(self.below_s, 1),
            "above_s": round(self.above_s, 1),
            "sample_arrived": sample_ok,
        }

    def resumen(self):
        """Resumen de la sesión (como la pantalla 'Resumen de la sesión' de NOOP)."""
        total = self.in_band_s + self.below_s + self.above_s
        return {
            "zona_bpm": f"{int(self.band['floor_bpm'])}-{int(self.band['ceiling_bpm'])}",
            "dentro_s": round(self.in_band_s, 1),
            "debajo_s": round(self.below_s, 1),
            "encima_s": round(self.above_s, 1),
            "avisos_push": self.cues_push,
            "avisos_ease": self.cues_ease,
            "demasiado_corto": total < 120,  # la zona necesita unos minutos para significar algo
        }


# ------------------------------------------------------------------ autoprueba

if __name__ == "__main__":
    # 1) Banda: datos reales de Carlos (RHR 50, FCmáx Tanaka 18a=195.4, Charge 66) → 136–158 bpm.
    b = banda(rhr=50.0, hrmax=195.4, charge=66)
    print("Banda (Charge 66):", b["floor_bpm"], "–", b["ceiling_bpm"], "bpm")
    assert 135 <= b["floor_bpm"] <= 137 and 157 <= b["ceiling_bpm"] <= 159  # coincide con la app

    # Carga baja estrecha/baja la zona; Carga alta la sube.
    bl = banda(50.0, 195.4, charge=10)
    bh = banda(50.0, 195.4, charge=95)
    assert bh["ceiling_bpm"] > b["ceiling_bpm"] > bl["ceiling_bpm"]
    assert bl["floor_pct"] >= MIN_FLOOR_PCT_HRR  # el piso nunca baja de 0.40 (clamp de seguridad)

    # 2) Sesión: 10 min dentro de zona → mayormente silencio, tiempo acumulado dentro.
    s = LiveSession(rhr=50.0, hrmax=195.4, charge=66, start_ts=0)
    centro = (b["floor_bpm"] + b["ceiling_bpm"]) / 2.0
    out = None
    for t in range(0, 600):  # 10 min @1Hz dentro de zona
        out = s.update(t, centro)
    print("Tras 10min en zona:", out["status"], out["position"], "· dentro",
          s.resumen()["dentro_s"], "s · avisos", s.cues_push + s.cues_ease)
    assert out["position"] == "in_band" and s.in_band_s > 500
    assert s.cues_push == 0 and s.cues_ease == 0  # silencio = vas bien

    # 3) Caer bajo zona sostenido → PUSH tras dwell.
    s2 = LiveSession(rhr=50.0, hrmax=195.4, charge=66, start_ts=0)
    bajo = b["floor_bpm"] - 20
    push_visto = False
    for t in range(0, 200):
        o = s2.update(t, bajo if t >= 70 else centro)  # warmup primero, luego bajo
        if o["cue"] == "push_nudge":
            push_visto = True
    print("Demasiado fácil sostenido → PUSH:", push_visto, "· debajo", round(s2.below_s), "s")
    assert push_visto and s2.below_s > 0

    # 4) Apretar sobre zona → EASE_OFF.
    s3 = LiveSession(rhr=50.0, hrmax=195.4, charge=66, start_ts=0)
    alto = b["ceiling_bpm"] + 15
    ease_visto = any(s3.update(t, alto if t >= 70 else centro)["cue"] == "ease_off"
                     for t in range(0, 200))
    print("Demasiado duro sostenido → EASE_OFF:", ease_visto)
    assert ease_visto

    # 5) Resumen muy corto → "demasiado corto para juzgar".
    s4 = LiveSession(rhr=50.0, hrmax=195.4, charge=66, start_ts=0)
    for t in range(0, 30):
        s4.update(t, centro)
    assert s4.resumen()["demasiado_corto"] is True

    print("\nOK — loop esfuerzo-objetivo funcional (zona por Carga, silencio=ok, PUSH/EASE_OFF).")
