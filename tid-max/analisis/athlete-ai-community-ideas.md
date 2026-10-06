# Ideas para TID-MAX — minería de la "Athlete AI Community" (Kevin Rudd)

**Fecha:** 2026-10-06 · **Fuente:** classroom de la comunidad Athlete AI (Skool) de @krudd.jr.
**Objetivo:** qué robar/adaptar para mejorar TID-MAX. Esta comunidad es la **versión DIY** de TID-MAX
(wearables + Claude Code); su temario es, en la práctica, la receta abierta de lo que hacemos.

> Diferenciación de TID-MAX frente a este crowd: **producto hágalo-por-mí** (sin sideload ni Claude Code),
> **profundidad de ciencia deportiva** (zonas de lab, natación) y, a futuro, **hardware propio**.
> La jugada: robar sus mejores integraciones gratis + sumar lo que ellos no tienen (natación, producto pulido).

---

## 🥇 TIER 1 — máxima palanca (resuelven dolores reales nuestros)

### 1. intervals.icu como AGREGADOR GRATIS ⭐ (replantea todo el debate de Junction)
De su guía de APIs: **intervals.icu** ya jala **Garmin, Strava, WHOOP, Oura, Polar y COROS con UNA sola
API key, en el tier GRATIS**. Maneja el OAuth/refresh de todas esas fuentes por ti.
- **Impacto directo para Carlos (Polar):** es el **pipe automático y gratis** que buscábamos — en vez de
  exportar TCX a mano, intervals.icu lee Polar Flow y nosotros leemos su API. Cero costo, cero plomería frágil.
- **Reencuadre del hilo de Junction:** concluimos que "no hay agregador gratis"; resulta que **sí lo hay
  para Garmin/Strava/Oura/Polar/COROS → intervals.icu**. Junction a $300/mes queda aún más innecesario.
- **Caveat honesto:** WHOOP vía intervals.icu **sí requiere membresía WHOOP activa**. Para WHOOP **gratis**,
  la vía es **NOOP (BLE)** (ver §2). Pero el Polar de Carlos y cualquier Garmin/Oura entran gratis ya.
- Bonus: su guía documenta los gotchas (usuario literal `API_KEY`, User-Agent para pasar Cloudflare, `oldest`
  requerido, athlete id `0`).

### 2. NOOP (BLE) para WHOOP gratis — Gael
Ya analizado aparte: lee el strap WHOOP por Bluetooth (incl. **R-R crudo**), SQLite local, export `.noopbak`
y una tool `noop-local-access` (CLI/MCP). Revive a Gael a $0 + desbloquea HRV/DFA-α1. (Caveat: sideload que
expira cada 7 días; ToS-gray → uso personal OK, no cimiento comercial.)

### 3. Analizador de FORMA por visión (YOLO11 pose) — y aquí está el diferenciador: NATACIÓN
Su "Running Form Analyzer": video lateral → **YOLO11-pose (17 keypoints)** → cadencia, overstride, inclinación
de tronco, graduado verde/ámbar/rojo contra rangos de investigación, con esqueleto de color + cue exacto.
Stack open-source (YOLO11 AGPL, supervision MIT, OpenCV).
- **La oportunidad grande:** el mismo enfoque de *pose estimation* aplicado a **técnica de NATACIÓN de Gael**
  (frecuencia de brazada, posición del cuerpo, catch, simetría). **Nadie en el panorama que revisamos hace
  natación** — es un feature premium y diferenciado, perfecto para un nadador de élite.
- También existen Bike Fit / Squat Form / Jump Height → una familia de análisis por CV.

---

## 🥈 TIER 2 — upgrades fuertes de producto

### 4. Coach de dos vías por Telegram/WhatsApp ("coach en el bolsillo")
Hoy TID-MAX manda avisos de UNA vía. Ellos texean al coach: "cambia sábado y domingo", "dormí mal, ajusta hoy",
"acabé un 16", y el bot lee la data y responde/ajusta. El brief matutino (sesión + readiness + cuenta al evento)
llega antes de levantarte. Empezar por la mitad fácil: **brief matutino saliente** (una sola salida, sin servidor).

### 5. Memoria persistente / "Brain" del atleta
Su "Brain" (LLM wiki tipo Obsidian): una nota por entreno/día, enlazadas, que el coach lee ANTES de responder y
actualiza DESPUÉS → se vuelve más listo cada semana. Nuestro agente de nutrición ya tiene `memoria`; extenderla a
**memoria de todo el atleta** haría al coach citar patrones ("la última vez que subiste volumen rápido, pasó X").

### 6. Review diario que juzga EJECUCIÓN, no asistencia
Su lente de coaching: *"¿los días fáciles se quedaron fáciles? ¿los duros pegaron el objetivo?"* — más filoso que
"entrenaste o no". Fácil de meter a nuestro agente de rendimiento (ya tenemos zonas por sesión).

### 7. Empujar la sesión estructurada DE VUELTA al reloj
Vía intervals.icu puedes **mandar el workout planeado al reloj** (Garmin/COROS/Polar) con objetivos de FC/ritmo.
TID-MAX genera el plan pero no lo pone en el dispositivo. Enorme win de UX: la sesión aparece en la muñeca.

---

## 🥉 TIER 3 — adiciones ricas y baratas

- **Entrevista de onboarding que calcula metas** (BMR/TDEE/macros con Mifflin-St Jeor + multiplicadores; zonas),
  **etiquetando cada número MEASURED / ESTIMATED / UNKNOWN**. Encaja con nuestro ethos de integridad de datos
  (agente auditor) y de una vez cierra las metas de nutrición de Carlos que quedaron estimadas.
  *(Anécdota suya: una FCmax de 195 "fantasma" sin respaldo en 180 días volvió "fácil" en realidad tempo meses.)*
- **Agua / hidratación** en el agente de nutrición (no la trackeamos; add fácil).
- **Web-lookup para alimentos empacados/restaurante** (USDA/marca) en el agente de nutrición → sube precisión
  de lo que la foto sola no estima bien (ya lo hacen ellos).
- **Modo "solo observar" las primeras 2 semanas** con un wearable nuevo (los scores de recovery no son confiables
  mientras el aparato te "aprende"). Buen guardrail.

---

## Resumen de prioridades

| # | Idea | Para quién | Costo | Por qué |
|---|---|---|---|---|
| 1 | **intervals.icu (agregador gratis)** | Carlos (Polar) + futuros | $0 | Pipe automático gratis; mata Junction para no-WHOOP |
| 2 | **NOOP (BLE)** | Gael (WHOOP) | $0 | WHOOP gratis + R-R crudo |
| 3 | **Form analyzer → NATACIÓN** | Gael | $0 (open-source) | Feature premium diferenciado; nadie hace natación |
| 4 | Coach 2-vías (Telegram/WhatsApp) | todos | bajo | "coach en el bolsillo" |
| 5 | Memoria/Brain del atleta | todos | bajo | coach que aprende y cita patrones |
| 6 | Review por ejecución | todos | bajo | coaching más filoso |
| 7 | Empujar workout al reloj | todos | bajo (intervals.icu) | la sesión en la muñeca |

**Veredicto:** robar **intervals.icu + NOOP** (dato gratis para Carlos y Gael) y construir el **analizador de
forma de natación** (diferenciador real). Lo demás es roadmap de producto. Y Kevin Rudd sigue siendo un
contacto valioso: ya tiene resuelto medio stack que a nosotros nos costó semanas.

### Fuentes (classroom Athlete AI Community)
- My Exact Fitness Agent Stack · September 2026 Wearable API Guides · Claude Macros & Nutrition Tracker ·
  Running Form Analyzer · 4 Ways I Run My Entire Training with AI · Connecting Noop to Your Athlete OS.
