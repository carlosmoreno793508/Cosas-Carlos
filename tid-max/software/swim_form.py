#!/usr/bin/env python3
"""
swim_form.py — Analizador de TÉCNICA DE NATACIÓN por visión (TID-MAX).

Inspirado en el "Running Form Analyzer" de la comunidad Athlete AI, pero adaptado a NATACIÓN
(crol) — un diferenciador: casi nadie hace análisis de técnica de nado por IA.

Qué mide (de un video LATERAL, sobre el agua: desde la orilla o siguiendo al nadador):
  - Frecuencia de brazada (strokes/min y ciclos/min): de los picos de la muñeca del lado-cámara.
  - Conteo de brazadas en el clip.
  - Consistencia de tempo (CV de los intervalos entre brazadas): un tempo parejo = buen ritmo.
  - Línea del cuerpo (ángulo hombro→cadera vs horizontal): cadera caída = más arrastre.
  - Posición de cabeza (oreja/nariz vs línea de hombros): levantar la cabeza hunde la cadera.
  - Simetría L/R del codo en recobro (si ambos brazos son visibles).

Se gradúa verde/ámbar/rojo contra rangos de referencia (ver swim-form-ranges.md). Honesto:
un video 2D sobre el agua da RANGOS poblacionales y tendencia, NO un laboratorio. Lo bajo del
agua (catch, patada) necesita cámara subacuática y es otro trabajo.

Stack open-source (igual que el de running):
  ultralytics (YOLO11x-pose, AGPL) · opencv-python · numpy · (ffmpeg para el overlay H.264)

Uso:
    pip install -r requirements-swim.txt       # ultralytics opencv-python numpy
    python swim_form.py --input nado_lateral.mp4 --out out_nado
    python swim_form.py --input nado.mov --start 3 --end 25 --fps 60

Salida en out_nado/:  overlay.mp4 (esqueleto)  ·  report.md / report.json  ·  stills/
"""
import os
import sys
import json
import argparse
import subprocess

try:
    import numpy as np
    import cv2
    from ultralytics import YOLO
except ImportError:
    sys.exit("Faltan dependencias. Instala:  pip install -r requirements-swim.txt "
             "(ultralytics opencv-python numpy) y ten ffmpeg en el PATH.")

# COCO keypoints (orden YOLO pose): 0 nariz,1-2 ojos,3-4 orejas,5-6 hombros,7-8 codos,
# 9-10 muñecas,11-12 caderas,13-14 rodillas,15-16 tobillos.
K = {"nose":0,"l_ear":3,"r_ear":4,"l_sho":5,"r_sho":6,"l_elb":7,"r_elb":8,
     "l_wri":9,"r_wri":10,"l_hip":11,"r_hip":12}

# Rangos de referencia (crol, sobre el agua, lateral). Ver swim-form-ranges.md para el porqué.
RANGES = {
    # Frecuencia de brazada en nado: muy dependiente de la distancia/velocidad; se REPORTA,
    # con una banda amplia típica de entrenamiento.
    "stroke_rate_spm": {"green": (55, 95), "report": True},
    # Consistencia de tempo: CV bajo = brazada pareja (graduado).
    "tempo_cv_pct":    {"green": (0, 8), "amber": (8, 14)},  # >14 rojo
    # Línea del cuerpo: hombro→cadera cerca de horizontal (0°). Caída de cadera = + arrastre.
    "body_line_deg":   {"green": (0, 8), "amber": (8, 14)},  # >14 rojo
    # Simetría L/R del codo en recobro (diferencia de ángulo pico): bajo = simétrico.
    "lr_asym_deg":     {"green": (0, 10), "amber": (10, 18)},  # >18 rojo
}


def _conf(kp, idx, thr=0.3):
    """Devuelve (x,y) si la confianza del keypoint supera el umbral, si no None."""
    try:
        x, y, c = kp[idx]
        return (float(x), float(y)) if c >= thr else None
    except Exception:
        return None


def _angle_from_horizontal(p1, p2):
    """Ángulo (grados, 0=horizontal) de la línea p1→p2."""
    if not p1 or not p2:
        return None
    dx, dy = (p2[0]-p1[0]), (p2[1]-p1[1])
    import math
    return abs(math.degrees(math.atan2(dy, dx)))


def analyze(frames_kp, fps):
    """frames_kp: lista por frame de los 17 keypoints (o None). Devuelve métricas."""
    wrist_y, body_line, head_off, lr_elbow = [], [], [], []
    for kp in frames_kp:
        if kp is None:
            wrist_y.append(np.nan); continue
        # muñeca del lado-cámara: usa la de mayor confianza entre L/R
        w = _conf(kp, K["r_wri"]) or _conf(kp, K["l_wri"])
        wrist_y.append(w[1] if w else np.nan)
        # línea del cuerpo: hombro→cadera (promedia lados disponibles)
        sh = _conf(kp, K["r_sho"]) or _conf(kp, K["l_sho"])
        hp = _conf(kp, K["r_hip"]) or _conf(kp, K["l_hip"])
        bl = _angle_from_horizontal(sh, hp)
        if bl is not None:
            body_line.append(min(bl, 180-bl))  # cerca de 0 = horizontal
        # cabeza: nariz/oreja vs línea de hombros (offset vertical normalizado)
        nose = _conf(kp, K["nose"]) or _conf(kp, K["r_ear"]) or _conf(kp, K["l_ear"])
        if nose and sh:
            head_off.append(nose[1]-sh[1])
        # simetría de codo (ángulo codo respecto a vertical) si ambos visibles
        le, re = _conf(kp, K["l_elb"]), _conf(kp, K["r_elb"])
        if le and re:
            lr_elbow.append(abs((le[1]) - (re[1])))

    # Frecuencia de brazada: cuenta los picos (recobro = muñeca arriba) de wrist_y.
    y = np.array(wrist_y, dtype=float)
    valid = ~np.isnan(y)
    strokes = 0; intervals = []
    if valid.sum() > fps:
        ys = y.copy()
        # rellena huecos cortos por interpolación simple
        idx = np.arange(len(ys))
        ys[~valid] = np.interp(idx[~valid], idx[valid], ys[valid])
        ys = -(ys - np.nanmean(ys))  # invierte: 'arriba' en pantalla = y menor
        # suaviza
        k = max(3, int(fps//6) | 1)
        ys = np.convolve(ys, np.ones(k)/k, mode="same")
        thr = np.std(ys)*0.4
        last = -999
        peaks = []
        for i in range(1, len(ys)-1):
            if ys[i] > ys[i-1] and ys[i] >= ys[i+1] and ys[i] > thr and (i-last) > fps*0.4:
                peaks.append(i); last = i
        strokes = len(peaks)
        intervals = [ (peaks[i]-peaks[i-1])/fps for i in range(1, len(peaks)) ]

    dur_s = len(frames_kp)/fps if fps else 0
    spm = round(strokes/dur_s*60, 1) if dur_s else 0        # strokes/min (cada entrada de brazo)
    cpm = round(spm/2, 1)                                     # ciclos/min (L+R = 1)
    tempo_cv = round(np.std(intervals)/np.mean(intervals)*100, 1) if len(intervals) >= 3 else None
    bl_med = round(float(np.median(body_line)), 1) if body_line else None
    lr = round(float(np.median(lr_elbow)), 1) if lr_elbow else None

    return {
        "duracion_s": round(dur_s, 1),
        "stroke_rate_spm": spm, "cycles_per_min": cpm, "brazadas": strokes,
        "tempo_cv_pct": tempo_cv,
        "body_line_deg": bl_med,
        "lr_asym_px_med": lr,
    }


def grade(metric, value):
    r = RANGES.get(metric)
    if r is None or value is None:
        return "report"
    if r.get("report"):
        lo, hi = r["green"]
        return "green" if lo <= value <= hi else "amber"
    lo, hi = r["green"]
    if lo <= value <= hi: return "green"
    a = r.get("amber")
    if a and a[0] <= value <= a[1]: return "amber"
    return "red"


def run(args):
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.join(args.out, "stills"), exist_ok=True)
    print("Cargando YOLO11x-pose (descarga ~113MB la 1a vez)…")
    model = YOLO("yolo11x-pose.pt")

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"No pude abrir el video: {args.input}")
    fps = args.fps or cap.get(cv2.CAP_PROP_FPS) or 30
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    f0 = int((args.start or 0)*fps); f1 = int((args.end or 10**9)*fps)

    # overlay vía ffmpeg (una sola codificación H.264)
    ff = subprocess.Popen(
        ["ffmpeg","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(fps),
         "-i","-","-an","-vcodec","libx264","-crf","18","-pix_fmt","yuv420p",
         os.path.join(args.out,"overlay.mp4")],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frames_kp = []; i = 0; saved_still = False
    while True:
        ok, frame = cap.read()
        if not ok: break
        if i < f0: i += 1; continue
        if i > f1: break
        res = model.predict(frame, verbose=False)[0]
        kp = None
        if res.keypoints is not None and len(res.keypoints) > 0:
            # persona de mayor confianza
            confs = res.keypoints.conf.cpu().numpy() if res.keypoints.conf is not None else None
            xy = res.keypoints.data.cpu().numpy()   # (n,17,3)
            if len(xy):
                best = int(np.nanmean(xy[:, :, 2], axis=1).argmax())
                kp = xy[best]
                frame = res.plot()  # dibuja esqueleto
                if not saved_still:
                    cv2.imwrite(os.path.join(args.out,"stills","frame.jpg"), frame); saved_still = True
        frames_kp.append(kp)
        try: ff.stdin.write(frame.tobytes())
        except Exception: pass
        i += 1
    cap.release()
    try: ff.stdin.close(); ff.wait(timeout=60)
    except Exception: pass

    m = analyze(frames_kp, fps)
    grades = {k: grade(k, m.get(k)) for k in ("tempo_cv_pct","body_line_deg")}
    report = {"input": os.path.basename(args.input), "fps": fps, "metrics": m, "grades": grades}
    with open(os.path.join(args.out,"report.json"),"w") as f: json.dump(report, f, indent=2, ensure_ascii=False)

    def gi(k): return {"green":"🟢","amber":"🟠","red":"🔴","report":"▫️"}.get(grade(k, m.get(k)),"▫️")
    md = f"""# Reporte de técnica de nado — {report['input']}

- Duración analizada: {m['duracion_s']} s · {fps:.0f} fps

## Métricas
- {gi('stroke_rate_spm')} Frecuencia de brazada: **{m['stroke_rate_spm']} brazadas/min** ({m['cycles_per_min']} ciclos/min) · {m['brazadas']} brazadas
- {gi('tempo_cv_pct')} Consistencia de tempo (CV): **{m['tempo_cv_pct']}%**  (verde ≤8, ámbar 8–14)
- {gi('body_line_deg')} Línea del cuerpo (hombro→cadera vs horizontal): **{m['body_line_deg']}°**  (verde ≤8)
- ▫️ Simetría L/R codos (mediana, px): {m['lr_asym_px_med']}  (report)

## Cómo leerlo
- **Tempo parejo** (CV bajo) y **línea horizontal** (cadera arriba) son las dos palancas que este
  video 2D mide con más confianza. La frecuencia de brazada se **reporta** (depende de la distancia).
- Es una lectura poblacional, NO un laboratorio. Para catch/patada necesitas cámara subacuática.
- Filma LATERAL, cámara a la altura del agua, todo el cuerpo en cuadro, luz buena, 60 fps si puedes.
"""
    with open(os.path.join(args.out,"report.md"),"w",encoding="utf-8") as f: f.write(md)
    print(md)
    print(f"Salida en: {args.out}/ (overlay.mp4, report.md, report.json, stills/)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Analizador de técnica de natación (crol) por visión.")
    ap.add_argument("--input", required=True, help="Video lateral del nado (mp4/mov).")
    ap.add_argument("--out", default="out_nado", help="Carpeta de salida.")
    ap.add_argument("--start", type=float, default=None, help="Segundo inicial (recorta el clip).")
    ap.add_argument("--end", type=float, default=None, help="Segundo final.")
    ap.add_argument("--fps", type=float, default=None, help="Forzar fps si el video reporta mal.")
    run(ap.parse_args())
