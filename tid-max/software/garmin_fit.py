#!/usr/bin/env python3
"""
garmin_fit.py — Extrae R-R latido a latido de un archivo .FIT de Garmin → ms, para alimentar
hrv_rr.analiza_rr() igual que el R-R del Polar H10. STUB (no probado con un .FIT real).

Por qué esto importa: si el .FIT de la API personal trae los mensajes HRV, Garmin deja de ser
"otro import de scores ajenos" y se vuelve FUENTE DE SEÑAL para nuestro motor (RMSSD gap-aware,
SDNN, DFA-α1), reutilizando TODO hrv_rr.py sin cambios.

Formato FIT (perfil oficial): los intervalos latido a latido van en el mensaje **'hrv'**
(global message num 78), campo **'time'**: un arreglo de intervalos R-R en SEGUNDOS con
resolución 1/1000 s. El valor 0xFFFF (65535 → 65.535 s) es "inválido/relleno" y se descarta.
Convertimos a ms (×1000). Fuente: perfil FIT SDK de Garmin. ⚠️ VERIFICAR que la API personal
incluya estos mensajes (puede entregar un .FIT recortado sin HRV).

Dependencia OPCIONAL: 'fitdecode' (parser .FIT puro-Python). Es la capa de ADQUISICIÓN, no el
motor — igual que 'bleak' para el Polar. El motor (hrv_rr/recovery_score/…) sigue siendo stdlib.
Instala sólo si usas Garmin:  pip install fitdecode
"""
import sys

RR_INVALIDO_S = 65.535   # 0xFFFF en resolución 1/1000 s = relleno FIT
RR_MIN_MS, RR_MAX_MS = 300.0, 2000.0   # rango fisiológico (30–200 lpm); fuera = artefacto


def extrae_rr_ms(fit_path):
    """
    Devuelve la lista de intervalos R-R (ms) de los mensajes 'hrv' del .FIT, en orden. Descarta
    el relleno 0xFFFF y los valores fuera de rango fisiológico. Lista vacía si el .FIT no trae HRV.

    Requiere 'fitdecode' (opcional). La limpieza fina (ectópicos, segmentos) la hace hrv_rr.
    """
    try:
        import fitdecode
    except ImportError:
        raise ImportError(
            "Falta 'fitdecode' (parser .FIT, dependencia opcional de la capa Garmin). "
            "Instala con:  pip install fitdecode"
        )

    rr_ms = []
    with fitdecode.FitReader(fit_path) as fit:
        for frame in fit:
            if not isinstance(frame, fitdecode.FitDataMessage) or frame.name != "hrv":
                continue
            # El campo 'time' puede venir como escalar o lista (según el SDK).
            try:
                val = frame.get_value("time")
            except KeyError:
                continue
            valores = val if isinstance(val, (list, tuple)) else [val]
            for s in valores:
                if s is None:
                    continue
                if abs(s - RR_INVALIDO_S) < 1e-6:   # relleno
                    continue
                ms = float(s) * 1000.0
                if RR_MIN_MS <= ms <= RR_MAX_MS:
                    rr_ms.append(round(ms, 1))
    return rr_ms


# ------------------------------------------------------------------ prueba manual (con un .FIT real)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:  python garmin_fit.py <archivo.fit>\n"
              "Extrae el R-R de los mensajes HRV y lo pasa por hrv_rr para un resumen rápido.")
        sys.exit(0)
    rr = extrae_rr_ms(sys.argv[1])
    print(f"Intervalos R-R extraídos: {len(rr)}")
    if rr:
        import hrv_rr
        res = hrv_rr.analiza_rr(rr)
        print(f"  RMSSD gap: {res.get('rmssd_gap_ms')} ms · SDNN: {res.get('sdnn_ms')} ms · "
              f"segmentos: {res.get('n_segmentos')} · calidad: "
              f"{(res.get('hrv_calidad') or {}).get('rmssd_mediana_ms')}")
    else:
        print("  (Sin mensajes HRV en el .FIT — ¿la API personal entregó un .FIT recortado?)")
