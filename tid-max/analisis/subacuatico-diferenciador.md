# El subacuático como DIFERENCIADOR de TID-MAX

> Cómo convertir la debilidad (una banda de brazo mide mal el subacuático y el dorso) en una
> ventaja competitiva para Gael y otros nadadores. Grounded en literatura; marcado por viabilidad.
> Fecha: 2026-08. Ver `modulo-natacion-tidmax.md`.

## El problema (recordatorio)
La patada de delfín subacuática es la **palanca #1** de velocistas/dorsistas (+1–2 m en virajes ≈
~1% en 200 m; el diferenciador de élite es la **velocidad** de patada, no la distancia). Pero una
banda en muñeca/bíceps la mide mal: el brazo va en streamline (quieto) mientras la patada nace en
cadera/piernas, y no hay GPS bajo el agua. Nadie en recovery-wearables lo resuelve (WHOOP no mide
nado; Garmin mide estilo pero no velocidad de patada; TritonWear no tiene recovery/HRV).

## Las 6 palancas de solución

**A) Medir bien lo que SÍ se puede (gana ya, sin hardware nuevo). ✅ Sólido**
Desde el IMM del pod se detecta con fiabilidad: **tiempo subacuático por viraje**, **timing del
breakout** (push-off→primera brazada), **cadencia de patada** (la ondulación viaja por el cuerpo
hasta el brazo) y —lo más valioso— **su DECAIMIENTO a lo largo de la prueba** (los 0.6–0.8 m que se
pierden por viraje al fatigarse). Eso ya supera a WHOOP y es 100% coachable.

**B) Sensor de PROFUNDIDAD en el pod (add-on barato). ✅ Sólido**
Un sensor de presión/profundidad (tipo MS58xx, ~USD 1–3) da el **perfil de profundidad** del
subacuático: profundidad de streamline, profundidad de breakout, y trayectoria. Ya existen wearables
PIMU (IMU + presión, 6.9 g, 100 Hz) probados para esto. **Ningún recovery-band lo trae** → hardware
diferenciador y de bajo costo. Encaja con nuestro 5 ATM + IP68.

**C) Colocación modular = "swim/underwater kit" (jugada de sistema). 🟡 Medio**
La patada se mide mejor en **cadera/tobillo** (donde nace). Como el pod TID-MAX es **magnético e
intercambiable** (muñeca/bíceps), se puede ofrecer un **clip a la cintura/tobillo** (o un 2º pod
IMU-only más barato) para capturar la patada en la fuente. Es un accesorio que **nadie ofrece** en
una banda de recuperación. Reusa el mismo pod → poco costo incremental.

**D) EL MOAT: IA que cruza subacuático × recuperación (nadie lo tiene). ⭐ Diferenciador central**
El valor único de TID-MAX no es medir el subacuático mejor que una cámara — es **correlacionarlo con
su propio dato de recovery/HRV/carga**: "tu patada subacuática **se degrada en días de recovery
baja**", "hoy con buena frescura toca **trabajar subacuáticos**". Esa **visión cruzada
fisiología×técnica** es imposible para Garmin (recovery/IA débil) y para TritonWear (sin HRV), y es
imposible para el vídeo. Es exactamente el posicionamiento predictivo de TID-MAX.

**E) ML específico para dorso. 🟡 Medio**
El estilo "más difícil para IMU" es un problema de algoritmo: clasificador entrenado para dorso +
placement en bíceps + fusión accel/giro/mag. Marketing honesto: "invertimos en el estilo que otros
dejan de lado".

**F) Híbrido con vídeo (integración, no competencia). ✅ Sólido**
Dejar que el entrenador **suba una sesión de vídeo/velocity meter** y TID-MAX la **fusione** con la
carga interna del día. Posicionamos la banda como el "cerebro" que integra todas las capas.

## Prioridad recomendada
1. **A + D** primero (software puro sobre el dato del EVK): tiempo/decaimiento subacuático + cadencia,
   cruzados con recovery. **Diferenciador inmediato, cero hardware extra.**
2. **B** (sensor de profundidad) en la spec del EVK/DVT — barato y muy vendible.
3. **C** (kit de cadera/tobillo) como accesorio de fase 2.
4. **E, F** en el roadmap de IA.

## Notas
- **IP:** es espacio con investigación pública pero poca protección en recovery-bands; **patentar**
  la correlación subacuático×recovery y el kit modular podría valer (consultar abogado de PI).
- **Alcance honesto:** seguimos sin dar velocidad intra-ciclo fina (eso es vídeo); damos **tendencia,
  timing, cadencia, profundidad y su relación con la fatiga** — que es lo accionable día a día.

## Fuentes
- Comparison of Video and IMU for Underwater Dolphin Kick — JHP (TAMUCC)
- Improving reliability of underwater gait with pressure + inertial sensors — PMC10956759
- PIMU wearable (IMU+presión, 6.9 g, 100 Hz) — systematic review / IEEE 8266113
- Kick frequency sync with metronome (cadencia coachable) — PMC5524309
- Ver `modulo-natacion-tidmax.md`, `metricas-nadadores-elite.md`, `aprendizajes-fr965.md`.
