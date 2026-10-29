# Cómo los nadadores de élite y olímpicos miden vueltas, brazadas, potencia y distancias en el entrenamiento

> Investigación recopilatoria (2026). Reúne cómo se mide el rendimiento en la natación de alto
> rendimiento: qué métricas se registran, con qué métodos y dispositivos, qué protocolos
> fisiológicos se usan, y dónde se discute todo esto (comunidades, publicaciones y fabricantes).

---

## 1. Las métricas clave que se miden

En el alto rendimiento la natación se descompone en un puñado de variables que, combinadas,
describen casi por completo el rendimiento. Las más importantes:

| Métrica | Qué es | Unidad típica | Para qué sirve |
|---|---|---|---|
| **Tiempo / Splits** | Tiempo por largo o por tramo (25/50 m) | segundos | Base de todo; ritmo y "pacing" |
| **Frecuencia de brazada (Stroke Rate, SR)** | Brazadas por minuto (o segundos por ciclo = "tempo") | brazadas/min ó s/ciclo | Cadencia; equilibrio velocidad-eficiencia |
| **Longitud/Distancia por brazada (DPS / Stroke Length)** | Metros avanzados por ciclo de brazada | m/brazada | Eficiencia técnica del "agarre" |
| **Conteo de brazadas** | Número de brazadas por largo | nº | Métrica manual clásica de eficiencia |
| **Velocidad** | Velocidad instantánea o media | m/s | Rendimiento puro |
| **SWOLF** | Tiempo del largo + nº de brazadas | puntos (menor = mejor) | Índice rápido de eficiencia |
| **Índice de brazada (Stroke Index)** | Velocidad × DPS (compuesto) | — | Eficiencia a una velocidad dada |
| **Fase subacuática** | Profundidad de empuje, tiempo/velocidad bajo el agua, % subacuático | m, s, m/s, % | Salidas, virajes y "breakouts" |
| **Fuerza / Potencia** | Fuerza propulsiva en el agua o potencia mecánica | N, W | Capacidad de generar propulsión |
| **Frecuencia cardíaca (FC)** | Pulsaciones | ppm | Carga interna / zonas |
| **Lactato en sangre** | Concentración de lactato | mmol/L | Umbrales e intensidad metabólica |

### La relación fundamental: Velocidad = SR × DPS

La velocidad de nado es el producto de la **frecuencia de brazada** por la **distancia por brazada**.
Existe un compromiso ("tradeoff"): si aceleras el brazo, baja el DPS; si alargas cada brazada,
baja la frecuencia. **Los nadadores de élite rara vez tienen el mejor valor en una sola métrica;
son maestros del equilibrio entre ambas.**

Referencias de élite (crol):
- **DPS**: ~2.0–2.5 m por brazada.
- **Frecuencia**: en 50 m libre los hombres de élite nadan a ~120–150 brazadas/min; en 200–800 m
  baja a ~70–100 según la técnica.

---

## 2. Segmentación de la carrera (cómo se "trocea" una prueba)

El análisis de competición y muchos test de entrenamiento dividen cada prueba en tramos fijos:

- **Salida (Start):** 0–15 m. Se mide el tiempo hasta que la cabeza llega a la marca de 15 m.
- **Viraje (Turn):** los ~15 m alrededor de la pared (habitualmente 5 m antes + 10 m después,
  o 7.5 + 7.5).
- **Nado limpio (Clean/Free swimming):** el resto del tramo, donde se calculan SR, DPS y velocidad.
- **Llegada (Finish):** los últimos 5 m.

Para cada tramo se obtienen: tiempo de salida, velocidad media, frecuencia media, longitud media
de brazada, nº de brazadas y tiempo de viraje.

---

## 3. Método "clásico" del entrenador (sin electrónica cara)

Antes (y todavía en paralelo) a los wearables, el entrenador mide con herramientas simples:

- **Reloj de pared / pace clock:** controla intervalos y tiempos de salida. Base del entrenamiento
  por series.
- **Cronómetro + conteo manual de brazadas por largo:** la métrica de eficiencia más antigua.
- **SWOLF a mano:** sumar tiempo del largo + brazadas de ese largo.
- **Metrónomo de natación (Tempo Trainer):** el más usado es el **FINIS Tempo Trainer Pro**, un
  dispositivo impermeable que va bajo el gorro y emite un "bip":
  - *Modo 1:* un bip por brazada (ajustable de 0.02 s a 99.99 s, en centésimas) → fija la cadencia.
  - *Modo 2:* triple bip por intervalo (1 s a 9:59) → sustituye el cálculo mental del pace clock
    (p. ej. bip cada 50 s para 100 m).
  - *Modo 3:* brazadas por minuto directamente.
  - Botón *Sync* para sincronizarlo con el reloj de pared.
- **Series de test de eficiencia:** por ejemplo, series descendentes donde se busca **bajar el
  tiempo manteniendo el conteo de brazadas** (mejora la velocidad sin perder eficiencia), o al revés,
  mantener el tempo fijo y descender el tiempo. Ajustes típicos del tempo de 0.02 s en 0.02 s.

Estas técnicas siguen siendo el "lenguaje" cotidiano de entrenadores incluso en equipos de élite,
porque son inmediatas y no dependen de sincronizar datos.

---

## 4. Wearables y sensores (medición automática)

Los wearables modernos usan **IMU (unidades de medición inercial: acelerómetro + giroscopio +
magnetómetro)** para detectar cada movimiento y convertirlo en métricas. La investigación valida
que estos sensores estiman de forma fiable: tiempo por largo, conteo y duración de brazada,
frecuencia instantánea y DPS. El acelerómetro triaxial se considera fiable para monitorizar el
entrenamiento diario de nadadores de élite.

### Plataformas orientadas a rendimiento / equipos

- **TritonWear** — Sensor que va bajo el gorro y transmite en tiempo real a la tablet del
  entrenador. Rastrea ~30 métricas: splits, SR, DPS, índice de brazada (su métrica compuesta
  *Stroke Index* = Velocidad × DPS × multiplicador de ciclo), tiempo en breakouts, virajes y fase
  subacuática (profundidad de empuje, tiempo/velocidad/% bajo el agua, profundidad máx.). Splits,
  conteo de brazadas y velocidad tienen alta fiabilidad; el "tiempo bajo el agua" es el más ruidoso
  (CV ~18–25 %). Muy usado por clubes competitivos.
- **FORM Smart Swim 2** — Gafas con **pantalla de realidad aumentada** que muestran las estadísticas
  en tiempo real delante del ojo (sin mirar la muñeca), con **sensor óptico de frecuencia cardíaca**,
  detección automática de brazada, biblioteca de entrenamientos guiados y ~16 h de batería. Se puede
  emparejar con reloj Apple/Garmin para ver distancia GPS en aguas abiertas dentro de las gafas.
- **MySwimEdge** — Sensor en un cinturón a la cintura que mide velocidad del cuerpo en tiempo real:
  DPS, velocidad mínima y máxima del cuerpo por brazada, timing y frecuencia de brazada. Enfocado a
  detalle técnico intra-ciclo.
- **Swimtraxx / otros trackers ligeros** — Trackers montados en las gafas, algunos tan ligeros como
  ~12.7 g, que registran FC, splits y frecuencia de brazada. Algunos son "World Aquatics Approved"
  y co-desarrollados con nadadores olímpicos.

### Relojes deportivos (el estándar de consumo/semi-pro)

- **Garmin** (Swim 2, Forerunner 965, etc.): identifican el estilo (4 estilos), registran tiempo,
  ritmo, distancia, brazadas, SWOLF, velocidad crítica de nado y tiempos de descanso, en piscina y
  aguas abiertas; los modelos altos muestran estadísticas en vivo en pantalla AMOLED.
- **Apple Watch, Polar, Suunto**: funciones equivalentes de conteo de largos, estilo y SWOLF.

Muchos entrenadores combinan sistemas a lo largo de la temporada: uno para feedback en tiempo real
en el entrenamiento y otro (vídeo) para la competición.

---

## 5. Sistemas de análisis de carrera por vídeo (cámaras)

Es la herramienta estándar en federaciones y campeonatos para el análisis fino:

- **Configuración típica:** una cámara fija cenital/lateral para la salida sobre el agua + una cámara
  de acción que se desplaza **bajo el agua** en paralelo al nadador, perpendicular a la calle.
- **Sistemas multicámara:** instalaciones de alto nivel usan hasta **10 cámaras** sincronizadas
  (p. ej. sistemas tipo Contemplas) para diagnóstico de rendimiento en 3D.
- **Velocity Meter (The Race Club):** sincroniza vídeo de alta velocidad con gráficas de velocidad,
  aceleración y **deceleración cada 0.04 s** dentro del ciclo de brazada, para ver exactamente dónde
  se genera propulsión y dónde se pierde velocidad.
- **Sistemas automatizados y con drones:** líneas de investigación recientes analizan el rendimiento
  con **vídeo aéreo desde dron** y con visión por computador para automatizar la detección de tramos.

De aquí salen los tiempos de salida (a 15 m), velocidades medias por tramo, SR, SL y tiempos de
viraje con validez y fiabilidad altas.

---

## 6. Medición de fuerza y potencia

Medir "potencia" en natación es más difícil que en ciclismo porque el medio es el agua. Enfoques:

### Nado atado (tethered swimming)
El método experimental más extendido para la fuerza en el agua:
- El nadador lleva un **cinturón unido a un cable de acero** (habitualmente ~5 m, con un ángulo de
  ~5.7° respecto a la superficie).
- Una **célula de carga (load cell)** conectada a un sistema de adquisición registra la fuerza,
  típicamente a **100 Hz**.
- Test **cortos** (10–30 s) para fuerza pico/media, o **largos** (~120 s) para impulso/resistencia.
- En élite, valores de fuerza pico rondan ~178–183 N en tests de 30 s (referencia orientativa).
- **Dato clave:** combinar potencia en seco + fuerza en nado atado explica hasta el **80 % de la
  variación del tiempo en 50 m**.

### Medidores de potencia "en el agua"
- **TraineSense SmartPaddle:** el medidor de potencia intra-acuático más citado; una paleta con
  sensores mide cómo fluye el agua a través de la mano para estimar fuerza/potencia propulsiva por
  brazada.
- **SwimOne:** dispositivo de investigación para determinar potencia instantánea y fuerzas
  propulsivas.

### Fuerza en seco (dry-land) como proxy
Se usan perfiles **fuerza-velocidad / carga-velocidad** (p. ej. en press de banca) para obtener la
fuerza teórica máxima, la velocidad teórica máxima y la potencia máxima, y así individualizar el
trabajo de gimnasio según las demandas aeróbicas/anaeróbicas del nadador. Correlaciona con el
rendimiento en sprint.

---

## 7. Métricas fisiológicas (carga interna)

### Frecuencia cardíaca
Se mide con sensores ópticos (gafas/relojes) o bandas, para controlar zonas y recuperación.

### Lactato en sangre y umbrales
El "gold standard" para fijar intensidades. Protocolos habituales:

- **Test incremental / escalonado (step test):** series como **7 × 200 m** a velocidad creciente,
  o incrementos de ~0.03 m/s cada 3 min, tomando muestra de lactato entre pasos. Sirve para hallar
  la velocidad a **4 mmol/L**, el umbral y las **zonas de entrenamiento** individuales. Se suele
  cortar al superar 7–8 mmol/L o por agotamiento; se recomiendan ~8–12 escalones.
- **T30:** test continuo de **30 minutos** a la intensidad del umbral de lactato (calculado antes con
  el test incremental). Durante el T30 se miden FC, frecuencia y longitud de brazada, lactato y VO₂.
- **MLSS (Máximo Estado Estable de Lactato):** referencia de precisión; requiere varios test de
  30 min en días distintos, por lo que el step test se prefiere en la práctica por ser más operativo.

### Velocidad crítica de nado (VCN / Critical Swim Speed)
Índice válido, fiable y **muy práctico** (no requiere pinchazos): es la máxima velocidad aeróbica
sostenible sin acumular lactato en exceso. Se estima a partir del rendimiento en varias distancias
(p. ej. 400 m y 50/100 m). Con el entrenamiento, la **velocidad crítica sube** mientras la
**frecuencia crítica de brazada baja** (mejora de eficiencia técnica). El **test T30** (Madsen &
Wilkie, años 80) correlaciona muy bien con las pruebas de lactato y es un clásico para triatletas
y nadadores.

---

## 8. Software y plataformas de análisis

- **TritonWear:** analítica con IA, dashboards de equipo, comparación entre nadadores y test sets,
  feedback en tiempo real a la tablet del entrenador.
- **App FORM:** análisis post-nado, planes y entrenamientos estructurados guiados en pantalla.
- **Athletica / MySwimEdge:** analítica de velocidad y técnica intra-brazada.
- **Contemplas y sistemas de federación:** diagnóstico de rendimiento multicámara.
- **Garmin Connect / Apple Health / Strava:** ecosistema de consumo para histórico y tendencias.

---

## 9. Dónde se investiga y se discute esto (comunidades y fuentes)

**Publicaciones científicas y agregadores:**
- **Swimming Science** (swimming.science) — traduce y resume estudios de biomecánica y fisiología.
- **PubMed / PMC, MDPI, ResearchGate, Sports (journal), Journal of Sports Sciences** — validaciones de
  IMU, tethered swimming, protocolos de lactato, análisis de carrera.
- **G-SE (Grupo Sobre Entrenamiento)** y **Alto Rendimiento** — en español, tests de campo (7×200,
  T30, velocidad crítica).

**Medios y blogs especializados:**
- **SwimSwam** — noticias, análisis técnico y de métricas ("tradeoffs", velocity meter).
- **Swimming World Magazine** — casos de uso de TritonWear en clubes.
- **Blogs de fabricantes:** TritonWear (blog.tritonwear.com), FORM, FINIS.
- **The Race Club** (theraceclub.com) — servicios de Velocity Meter y análisis de élite.
- **Total Immersion / Mediterra Swim** — metodología de tempo, DPS y series de eficiencia.
- **U.S. Masters Swimming, Outdoor Swimmer, 220 Triathlon** — guías prácticas de tempo trainer y
  wearables.

**Foros y grupos:**
- Comunidades como **r/Swimming** y **r/triathlon** (Reddit), foros de **SwimSwam**, grupos de
  Facebook de entrenadores/triatletas, y el newsletter/Substack **SwimEd (Parigi)** discuten uso
  real de TritonWear y wearables.

---

## 10. Resumen práctico: qué mide cada "capa"

| Nivel | Herramienta | Métricas que aporta |
|---|---|---|
| Entrenador clásico | Pace clock, cronómetro, conteo de brazadas, Tempo Trainer | Splits, SR/tempo, conteo, SWOLF |
| Wearable de equipo | TritonWear, FORM, MySwimEdge | SR, DPS, índice, velocidad, fase subacuática, FC en vivo |
| Reloj deportivo | Garmin/Apple/Polar | Largos, estilo, SWOLF, VCN, ritmo, FC |
| Análisis de carrera | Cámaras (1–10) + Velocity Meter | Salida a 15 m, velocidad/aceleración por 0.04 s, virajes |
| Fuerza/potencia | Nado atado + célula de carga, SmartPaddle, seco (F-V) | Fuerza pico/media, impulso, potencia propulsiva |
| Fisiología | Lactímetro, banda FC | Lactato, umbrales, zonas, VCN, T30, VO₂ |

**Idea central:** ningún dispositivo lo mide todo. El alto rendimiento **combina capas** —
el ojo y el cronómetro del entrenador, el wearable en tiempo real, el vídeo para el detalle
biomecánico, el nado atado para la fuerza y el lactato para la fisiología— y las cruza para
individualizar el entrenamiento.

---

## Fuentes

- Validation of Automatically Quantified Swim Stroke Mechanics Using an IMU (Paralympic) — https://pmc.ncbi.nlm.nih.gov/articles/PMC10813451/ · https://www.mdpi.com/2306-5354/11/1/15
- Using Tri-Axial Accelerometry in Daily Elite Swim Training — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5469343/
- Stroke rate–stroke length dynamics in elite freestyle — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12541611/
- The Secret to Swimming Metric Tradeoffs (SwimSwam) — https://swimswam.com/the-secret-to-metric-tradeoffs/
- Distance Per Stroke & Stroke Rate (Swim Like A Fish) — https://swimlikeafish.org/part-i-the-fine-line-between-distance-per-stroke-and-stroke-rate
- Smart sensors save swimmers seconds (The Conversation) — https://theconversation.com/smart-sensors-save-swimmers-seconds-1687
- Swimmer Wearable Sensor Technology (Wave DDS) — https://wavedds.com/blog/swimmer-wearable-sensor-technology
- Unlocking the Power of Sensor Technology (TritonWear) — https://blog.tritonwear.com/unlocking-the-power-of-sensor-technology-in-swimming
- TritonWear for Elite Swimming (SwimEd/Parigi) — https://swimed.substack.com/p/tritonwear-for-elite-swimming
- TritonWear — https://www.tritonwear.com/
- FORM Smart Swim 2 — https://www.formswim.com/products/smart-swim-2-goggles
- Best fitness trackers for swimming 2025 (Live Science) — https://www.livescience.com/health/exercise/best-fitness-trackers-for-swimming
- Best swimming watches 2026 (220 Triathlon) — https://www.220triathlon.com/gear/swim/training-kit/best-swimming-watches
- SwimOne: New Device for Instantaneous Power and Propulsive Forces — https://www.researchgate.net/publication/347634819
- Lifting the Hood on Swimming Power Meters (Triathlete) — https://www.triathlete.com/training/swimming-with-power/
- Association between force production and 100 m front crawl pacing — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10250633/
- The Race Club — Velocity Meter — https://theraceclub.com/specialized-services-velocity-meter/
- Why the Velocity Meter Matters (SwimSwam) — https://swimswam.com/velocity-meter-matters-swimming/
- MySwimEdge (Athletica) — https://athletica.ai/blog/unlocking-the-secrets-of-swimming-performance-with-myswimedge
- Comparison single vs multi-camera race analysis — https://www.researchgate.net/publication/259982206
- Validity and Reliability of In-Field Performance Analysis System — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11598412/
- Performance diagnostics with a 10 camera system (Contemplas) — https://contemplas.com/en/flemish-swimming-federation-antwerp/
- Analyzing Swimming Performance Using Drone Aerial Videos — https://arxiv.org/pdf/2503.12981
- How a Tempo Trainer Can Help (US Masters Swimming) — https://www.usms.org/fitness-and-training/articles-and-videos/articles/how-a-tempo-trainer-can-help-your-training
- FINIS Tempo Trainer Pro — https://www.finisswim.com/Tempo-Trainer-Pro
- Metrics 102: Tempo (Mediterra Swim) — https://mediterraswim.com/2014/03/23/metrics-102-tempo/
- Verifying Physiological/Biomechanical Parameters at Lactate Threshold (T30) — https://pmc.ncbi.nlm.nih.gov/articles/PMC7404638/
- Can an Incremental Step Test Determine MLSS in Swimming — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7826783/
- Complete Blood Lactate Testing Protocol (LaChart) — https://lachart.net/blog/lactate-testing-protocol-guide
- Test de la Velocidad Crítica (Alto Rendimiento) — https://altorendimiento.com/test-velocidad-critica-natacion/
- Test de 30 min en natación (G-SE) — https://g-se.com/es/test-de-30-min-de-natacion-como-medio-de-control-y-evaluacion-del-triatleta-ejemplo-practico-en-una-temporada
- Adaptaciones a 6 meses de entrenamiento aeróbico (Swimming Science) — https://swimming.science/es/adaptaciones-a-seis-meses-de-entrenamiento-de-natacion-aerobica-cambios-en-la-velocidad-frecuencia-de-brazada-longitud-de-brazada-y-lactato-en-sangre
