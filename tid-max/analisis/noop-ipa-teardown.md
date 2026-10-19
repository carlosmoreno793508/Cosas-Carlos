# NOOP — teardown del .ipa  ·  comparativa vs TID-MAX

> Análisis forense del binario `NOOP-ios-unsigned-v12.0.0.ipa` (20.9 MB, iOS ≥ 17.0).
> Qué trae por dentro y cómo se compara con TID-MAX en **gráficos, estructura y métricas**.
> Hermano de `noop-metricas.md` (ese es el dossier de métricas; éste es lo que revela el binario).

---

## 0. TL;DR (lo que vi y el veredicto)

- **NOOP es una app madura, local-first, de una sola persona** — y aun así nos pasa en
  profundidad de métricas, idiomas y "honestidad" de la UI. No nos gana en lo que TID-MAX
  hace único: **coach con contexto del atleta real, plan de entrenamiento, nutrición y
  reporte diario automático en la nube**.
- Lo que sí debemos copiarle ya: **el pipeline de R-R crudo** (filtro de ectópicos →
  DFA-α1, Poincaré, monotonía) y la **escritura de vuelta a Apple Health**. Nosotros ya
  **capturamos** R-R crudo del Polar (`build_polar` lo guarda) pero **no lo procesamos**:
  sólo contamos muestras y tomamos el RMSSD *ya calculado por WHOOP*.
- Lo que NO debemos copiar: su modelo "trae-tu-propia-API-key" para el coach. Nosotros
  corremos el coach en la nube con contexto del atleta; es nuestra ventaja, no la tiremos.

---

## 1. Qué es el archivo y cómo lo abrí

Un `.ipa` es un **ZIP**. Dentro: `Payload/NOOP Staging.app/` (el bundle de la app).
Los `.strings` de cada idioma **no son texto UTF-16**, son *binary property lists* de Apple
— se leen con `plistlib`, no con un editor. Así saqué los **4,173 textos** de `es.lproj`.

```
Payload/NOOP Staging.app/
├── NOOP Staging                  ← binario Mach-O (el ejecutable)
├── Info.plist                    ← permisos y capacidades
├── Assets.car                    ← gráficos compilados (no PNGs sueltos)
├── Frameworks/                   ← GRDB, StrandDesign, WhoopProtocol, ZIPFoundation…
├── PlugIns/NOOPWidgets.appex     ← widgets de pantalla de inicio / bloqueo
├── lift-step-silence.caf         ← audio en silencio (truco para BLE en segundo plano)
└── {de,en,es,fr,it,pl,pt-PT,ru,zh-Hans,zh-Hant}.lproj  ← 11 idiomas
```

**Dato duro:** es una app **"Staging"** (build de pruebas), sin firmar (`unsigned`), v12.0.0.
Para instalarla hay que firmarla (Sideloadly) — que es justo lo que ya hicimos.

---

## 2. Permisos y capacidades (Info.plist) — qué toca del teléfono

| Permiso | Para qué | ¿TID-MAX lo tiene? |
|---|---|---|
| `NSBluetoothAlwaysUsageDescription` | Leer FC, **R-R, batería** y datos del sensor **localmente** | No (dependemos de WHOOP/Polar en la nube) |
| `NSHealthShare` **+ `NSHealthUpdate`** | **Lee y ESCRIBE** en Apple Health | No |
| `NSMicrophone` + `NSSpeechRecognition` | Coach por voz, transcripción **en el dispositivo** | No |
| `NSMotion` | Pasos / actividad | No |
| `UIBackgroundModes`: `bluetooth-central`, `location`, `fetch`, `processing` | Seguir leyendo el sensor con la app en segundo plano | No |

**Lo clave:** NOOP **escribe de vuelta a Apple Health** (grupo
`com.noopapp.noop.healthwriteback`). Eso significa que sus métricas calculadas (HRV, sueño,
esfuerzo) **aparecen en la app Salud del iPhone** y quedan disponibles para cualquier otra
app. Es un movimiento de integración muy fuerte y barato de copiar.

El `lift-step-silence.caf` (audio mudo) es el truco clásico para que iOS **no mate la
conexión BLE** cuando la pantalla se apaga. Es exactamente la razón técnica por la que NOOP
"no se cae" del sensor — algo que preguntaste. No es magia WHOOP; es un keep-alive de iOS.

---

## 3. Gráficos / diseño

| | NOOP | TID-MAX |
|---|---|---|
| **Sistema de diseño** | Framework propio **`StrandDesign`** (componentes reutilizables) | CSS a mano en `index.html` + `reporte.html` |
| **Assets** | `Assets.car` **compilado** (Xcode optimiza y escala) | PNGs sueltos (`icon-192/512`, iconos) |
| **Estética** | Oscura, acentos verde/titanio (`NavyTitanium` = color de la banda WHOOP) | Oscura, tarjetas; ya la comparamos y quedó pareja en estructura |
| **Nativo vs web** | 100% SwiftUI nativo | PWA (web) envuelta en Capacitor |
| **Widgets** | Sí — `NOOPWidgets.appex` (inicio + bloqueo) | No |
| **Heros** | `SleepNightHero.heic` y gráficos a pantalla completa | Tarjetas compactas |

**Lectura honesta:** NOOP se ve "más app" porque **es** nativa y tiene un *design system*.
Nosotros, siendo PWA, ganamos en **velocidad de iteración** (empujamos a Cloudflare y el
iPhone lo ve al instante, sin recompilar en Xcode) y en que **el reporte diario se genera
solo en la nube**. Su ventaja es visual/widgets; la nuestra es operativa.

---

## 4. Estructura (pantallas)

**NOOP — 13+ secciones:** Hoy · Tendencias · Sueño · En vivo · Vitalidad · Salud ·
Respira · Mente · Intervalos · Explorar · Comparar · Dispositivos · Fuentes de datos.

**TID-MAX — 4 pestañas:** Hoy · Entrenar · Datos · Perfil.

NOOP tiene mucha más superficie, pero gran parte es **exploración de datos del propio
usuario** (comparar días, ver correlaciones). TID-MAX concentra todo en un **reporte diario
dirigido** + coach. No necesitamos 13 pestañas; sí nos faltan 3 ideas concretas de su
estructura:

1. **"En vivo"** — ver FC/R-R del sensor en tiempo real (hoy no lo tenemos; con el Polar
   conectado sería directo).
2. **"Comparar"** — poner dos días lado a lado con días de traslape.
3. **"Respira"** — sesiones de respiración guiada (presets tipo *box breathing*).

---

## 5. Métricas (lo que confirmé en el binario)

Conté las ocurrencias de cada método en el ejecutable Mach-O (señal de que **sí están
implementados**, no sólo nombrados):

| Método | NOOP (ocurrencias) | TID-MAX (hoy) |
|---|---|---|
| **Poincaré** (SD1/SD2) | ~200 | ❌ |
| **RMSSD** | ~190 | ✅ *pero tomado de WHOOP ya calculado* |
| **DFA / DFA-α1** | ~163 | ❌ (planeado) |
| **VO₂máx** | ~80 | parcial |
| **Banister** (fitness/fatiga) | ~40 | mencionado |
| **SDNN** | ~30 | ❌ |
| **TRIMP / Edwards** | 23 / 11 | ✅ (zonas FC) |
| **Ectópicos** (filtro de latidos raros) | 27 | ❌ |
| **ACWR** (agudo:crónico) | 7 | ✅ (muy presente) |
| **pNN50** | 9 | ❌ |
| **Plews** (umbral DFA-α1) | 6 | ❌ |
| **Karvonen** (%reserva FC) | 3 | ✅ (zonas) |

### El hueco que más importa
NOOP parte de **R-R crudo** → filtra **ectópicos** (Malik) → de ahí saca RMSSD/SDNN/pNN50,
Poincaré y **DFA-α1** (el marcador de umbral aeróbico de Plews). Nosotros en
`tid_data.build_polar()` **ya guardamos el R-R crudo del Polar** (`rr_ms`), pero sólo hacemos
`rr_muestras = len(rrs)` — **lo contamos y lo tiramos**. Y nuestro HRV del día
(`hrv_rmssd_milli`) viene **precalculado por WHOOP**, sin control de ectópicos.

Esto es exactamente lo documentado en `noop-metricas.md`. El teardown lo **confirma**: no es
teoría, NOOP lo trae compilado.

### Lo que NOOP hace y es "producto", no sólo ciencia
- **Coach con IA de "trae tu API-key":** soporta Gemini y endpoints OpenAI-compatibles
  (Ollama, LM Studio, llama.cpp). Puede **mandar imágenes de las gráficas a Gemini**. La
  llave se guarda en el **Keychain**. → Nosotros corremos el coach en la nube **con el
  contexto real del atleta** (perfil, plan, umbrales). Ventaja nuestra; no la perdamos.
- **Ingeniería inversa de Oura** (`OURA_PROTOCOL.md`, `SetFeatureMode`, muestreo PPG) y de
  WHOOP — lee varias bandas, no una.
- **Etiquetado honesto** en toda la UI: *"estimación en el dispositivo, no es un
  diagnóstico"*, *"importa un CSV de WHOOP para un % real"*. Buen tono; copiémoslo.
- **Hidratación** con meta ajustada por esfuerzo, y **correlaciones** entre métricas con
  conteo de días de traslape (para no mentir con n pequeña).

---

## 6. Qué nos llevamos (acción concreta)

**Copiar ya (alto valor, bajo costo):**
1. **Pipeline de R-R crudo** → filtro de ectópicos (Malik) → DFA-α1 (Plews), Poincaré,
   SDNN/pNN50, monotonía (Foster). Ya tenemos el insumo capturado del Polar.
2. **Escribir a Apple Health** desde la app nativa (HealthKit write-back).
3. **Keep-alive BLE** (audio mudo / background modes) para el modo "En vivo" sin caídas.
4. **Etiquetado honesto** de cada estimación.

**Evaluar (medio plazo):**
5. Pestaña **"En vivo"** (FC/R-R del sensor en tiempo real).
6. **Widgets** de pantalla de inicio/bloqueo.
7. Vista **"Comparar"** días con traslape.

**NO copiar:**
8. El modelo "trae-tu-API-key" del coach. Nuestro coach en la nube con contexto del atleta
   es la diferencia de producto; mantenerlo servido por nosotros.

---

## 7. Nota de método
Binario analizado con `unzip` + `plistlib` (strings) + conteo de símbolos en el Mach-O.
Las "ocurrencias" indican presencia de implementación, no exactitud clínica. Para validar
los números reales de NOOP haría falta correr la app con R-R conocido y comparar — que es el
siguiente paso con tu **Polar Verity Sense** (sensor óptico de brazo; su R-R es más ruidoso
que el ECG del **H10**, así que la prueba de DFA-α1 conviene hacerla en reposo/quieto).

---

## Anexo A — UI en vivo (capturas del iPhone de Carlos, 2026-10-19)

> Lo que el teardown del binario no muestra: la app corriendo con datos reales.
> Carlos la tiene cargada con **WHOOP (CSV importado, 90 días) + Mi Band (BLE) +
> Apple Health**, fusionados en el teléfono. Esto confirma el camino "WHOOP CSV →
> métricas" del teardown y revela que **NOOP es, de facto, un agregador multi-fuente**.

### A.1 Pantalla "Tendencias"
- **Anillos CHARGE / EFFORT / REST** (66 / — / 85) con **chip de delta** (`↗ +<1%`,
  `↘ −4%`): estado + tendencia de un vistazo.
- **Resumen de la semana**: Carga 54 · Esfuerzo 48 · Descanso 76, con barras de puntos.
- **Selector de rango** M / L / 3M / 6M / 1A / TODO + subtítulo honesto *"90 lecturas ·
  3 meses"* (dice cuántos datos respaldan el número).
- **Gráfica de área con gradiente por valor** (CARGA 90 días): la línea va de **rojo
  (bajo) a verde (alto)** — codifica nivel por color *y* por altura. Pie de stats
  `PROM 54 · PICO 98 · BAJO 4 · DÍAS 90 · TENDENCIA +11`.
- **Señales diarias**: HRV (MEDIA 95 ms, MÍN 13, MÁX 149, tend −4), FC reposo (52 bpm,
  45–75), Esfuerzo (48.2/100).
- **Etiquetado honesto en vivo**: *"Only 1 day into this week… too early to call a
  trend yet."* — **bug de QA: esa nota sale en inglés** con el resto de la UI en
  español (señal de app de una persona que empuja rápido).

### A.2 Pantalla "Explorar" — el modelo de datos completo
Catálogo navegable de **~60 señales en 7 categorías**, cada una con su **fuente
etiquetada**. Cuando una señal existe en dos fuentes (p. ej. FC reposo de Whoop *y* Mi
Band), **las muestra separadas con su origen — no hace merge ciego**. Arriba de todo:
**"Cronología profunda — cada segundo de tu día, con zoom"** (timeline a resolución de
segundos).

| Categoría | # | Señales (fuente) |
|---|---|---|
| **Heart** | 12 | FC media, FC máxima, Calorías (Whoop + Mi Band); VO₂ Máx (Apple Health); Edad fitness, Edad corporal (Whoop); Vitalidad (Mi Band) |
| **Carga** | 8 | Carga %, HRV ms, Frec. respiratoria rpm, Temp. piel °C (Whoop); FC reposo, Oxígeno en sangre % (Whoop + Mi Band) |
| **Descanso** | 18 | Descanso %, Tiempo en cama, Horas vs Horas Necesarias, Consistencia, Sueño reparador (% y min), Eficiencia, **Sueño necesario**, **Deuda de sueño**, SWS/REM/ligero (Whoop + Mi Band); Puntuación de sueño (Mi Band) |
| **Esfuerzo** | 11 | Esfuerzo /100 (Whoop); Pasos (Apple Health + Whoop + Whoop estimados + Mi Band); HR Zones 1-3, 4-5, todas, Tiempo de fuerza (Whoop); Energía activa (Apple Health); Minutos de intensidad (Mi Band) |
| **Salud** | 6 | Peso, Grasa corporal, Masa magra, BMI (Apple Health); Estrés del día /3 (Whoop); Estrés /100 (Mi Band) |
| **Nutrición** | 4 | Calorías ingeridas, Proteína, Carbohidratos, Grasa (entrada manual) |
| **Mente** | 1 | **Ánimo /5** (auto-reporte subjetivo) |

### A.3 Lecturas nuevas para TID-MAX
1. **Badge de procedencia por métrica.** Ya guardamos la fuente (`mark(r, src)` en
   `tid_data.py`); falta **mostrarla** en la UI ("HRV · WHOOP", "FC · Polar"). Resuelve
   el "¿de dónde salió este número?" y da confianza.
2. **Fusión multi-fuente sin pisar datos.** Mantener fuentes paralelas y dejar que el
   usuario/coach elija la primaria por métrica, en vez de un merge ciego. Es justo el
   problema de `esquema-canonico.md`.
3. **"Explorar" = catálogo navegable** por categoría con conteo. Barato y hace la app
   sentirse profunda.
4. **Objetivo + subjetivo:** la categoría **Mente → Ánimo /5** mezcla auto-reporte con
   los datos del sensor. Barato de añadir y mejora el coach (contexto que el sensor no ve).
5. **Nutrición manual** (kcal/proteína/carbos/grasa) — ya lo tenemos en `comida.js`;
   NOOP valida que es parte esperada del modelo.
6. **Métricas de sueño que nos faltan:** *Deuda de sueño*, *Horas vs Horas Necesarias*,
   *Consistencia* — todas derivables de lo que ya baja WHOOP.

### A.4 Pantalla "Cronología profunda" — el pipeline de R-R expuesto
La pantalla más relevante para TID-MAX. Subtítulo: *"Cada segundo de tu día, con zoom."*
**7 streams** en pestañas: **Frecuencia cardíaca · rMSSD por ventanas · SpO2 · Temp. de
piel · Respiración · Movimiento · Band Sleep State**, con timeline interactivo
(*"Pinch to zoom · drag to pan · hold to read"*) y toggle de procedencia **"En propiedad /
Todo"** sobre la fuente (WHOOP).

**Estados vacíos "capability-aware" (gran patrón de honestidad):** NOOP sabe qué puede
físicamente cada sensor y lo dice, distinguiendo tres casos:
- *"This strap doesn't send SpO₂ over Bluetooth. Import a WHOOP export or Health Connect
  to see it."* → la banda **no puede** por BLE, con el fallback de importación.
- *"This strap sends no raw respiration stream. Your estimated respiratory rate appears on
  the Health screen."* → distingue **stream crudo vs métrica estimada/derivada**.
- *"Aún no se ha descargado nada para esta ventana."* → simplemente **no hay dato** aún.

Lección para TID-MAX: nuestro caso multi-sensor es idéntico — el **H10** da R-R limpio
(ECG), el **Verity Sense** da R-R más ruidoso (óptico), y WHOOP **no** expone R-R crudo por
API. Un estado que diga qué da cada fuente evita prometer métricas que el sensor no puede
sostener.

- **"rMSSD por ventanas"** es el hallazgo clave: NOOP calcula **RMSSD rodante (por
  ventanas) sobre el R-R crudo**, no un solo número diario. Ése es **el eslabón
  intermedio que a TID-MAX le falta**: hoy tomamos un RMSSD/día ya calculado por WHOOP;
  deberíamos calcular RMSSD por ventanas desde el R-R del Polar que ya capturamos. Es el
  paso natural *antes* de DFA-α1 (que también se computa por ventanas).
- **Estado vacío honesto** (*"No hay frecuencia cardíaca aquí — Aún no se ha descargado
  nada para esta ventana"*): "Hoy" sale vacío porque los datos de Carlos son **CSV de
  WHOOP importado (histórico)**, no un stream en vivo. Confirma el camino de ingesta.

Esto refuerza la recomendación #1 del dossier: **pipeline de R-R crudo → RMSSD por
ventanas → DFA-α1 (Plews) / Poincaré**. NOOP demuestra que es viable y lo enseña en UI.

### A.5 Drill-down de una métrica (ej. "Frecuencia cardíaca media")
Al tocar cualquier señal se abre su detalle, con un layout reusable:
- **Selector de rango fino**: M · 2S · 3S · L · 3M · 6M · 1A · TODO (día → 2–3 semanas →
  mes → …).
- Valor grande + fecha + *"30 lecturas · mes"* (cuántos datos respaldan el número).
- Gráfica de área con puntos + footer **VENTANA / PUNTOS / MÁS RECIENTE**.
- Tarjetas: **PROMEDIO con sparkline de 30 días**, **MÍN**, **MÁX**, **Δ vs período
  anterior** (`+1 bpm vs mes ant.` con chip de tendencia), **Más reciente**.
- **Tabla "LECTURAS" con columna `Fuente` por fila** (Fecha · Valor · WHOOP): la
  procedencia llevada **al nivel de cada lectura**, no sólo de la métrica. Es la
  confirmación más fuerte de la filosofía "cada dato sabe de dónde viene".

Para TID-MAX: este detalle (Δ-vs-período, sparkline, tabla con fuente por fila) es un
**componente reusable** — se define una vez y sirve para cualquier métrica. Encaja con el
badge de procedencia ya recomendado, llevándolo a nivel de fila.

### A.6 Pantalla "Sueño", "Carga de entrenamiento" y "Exportar"
Más pantallas capturadas, con 4 patrones de producto nuevos:

- **Badge de fuente BAJO la métrica hero.** El score de sueño (80/100 "Bien") lleva el
  chip **`WHOOP`** justo debajo del anillo. La procedencia no es un detalle escondido:
  está al lado del número principal. Es la validación más fuerte de la recomendación del
  *badge de procedencia* — y a nivel hero, no sólo en tablas.
- **"¿Por qué este sueño?"** — enlace de **explicabilidad** sobre una métrica derivada
  (por qué la app decidió esa ventana de sueño). Transparencia que genera confianza; TID-MAX
  puede hacer lo mismo con el coach ("por qué este número").
- **Exportar informe en PDF de 1 página** — *"recuperación, sueño, VFC, FC en reposo y
  esfuerzo en un rango, guardado en tu iPhone."* TID-MAX ya genera reportes; un **PDF
  compartible de una página** es una feature directa (para mandar al entrenador/médico).
- **Calendario heatmap + ACWR con gating honesto.** Calendario tipo GitHub de 247 días
  (Agotado→En su pico, rojo→verde). La tarjeta de **Carga de entrenamiento (crónica vs
  aguda = ACWR)** dice *"Necesita 14+ días consecutivos de Esfuerzo para empezar. 0 hasta
  ahora."* — no inventa un número sin datos suficientes. TID-MAX ya calcula ACWR; copiar
  ese gating honesto evita falsos positivos.

Detalle de sueño confirmado: desglose de fases (Despierto/REM/Ligero/Profundo con
timeline), eficiencia %, *"compara con tu típico de 30 días"* (contexto vs baseline
personal), siestas manuales y **Deuda de sueño** — todo lo que ya vimos en el catálogo
"Explorar", ahora renderizado.

### A.7 Pantalla "Entrenador" (el coach) — cierra el panorama
La última pantalla. Confirma al pie de la letra lo que vio el teardown del binario:
*"El coach usa tu propia clave de API. Elige un proveedor, pega una clave y selecciona un
modelo. Tu clave se guarda de forma segura en el Llavero y nunca sale de este iPhone salvo
en la solicitud que tú haces."*

- **Proveedores:** OpenAI · Anthropic · Google Gemini · **Custom (OpenAI-compatible)**
  (Ollama/LM Studio/llama.cpp). Modelo seleccionable (ej. `gpt-5-mini`).
- *"Esta es la única función que sale de este iPhone."* → NOOP es local-first; el coach es
  la **única** salida a la nube, y con la llave del usuario.

**Veredicto (refuerza la recomendación "NO copiar" #8):** el modelo "trae-tu-API-key" es
lo que hace a NOOP 100% local/privado, pero traslada al usuario la fricción (conseguir y
pagar su propia API key) y **no conoce el contexto del atleta**. La ventaja de TID-MAX es
exactamente la contraria: **coach servido por nosotros, con el perfil/plan/umbrales del
atleta cargados**. No lo cambiemos.

### A.8 "vs lo típico" en todo (patrón de contextualización)
El detalle de sueño muestra CADA métrica contra la **línea base personal de 30 días**, no
contra un promedio poblacional: Descanso 80% (+9% vs típico), Eficiencia 86% (−3%),
Consistencia 81% (+17%), Horas vs Necesarias 75% (+7%), Reparador 56% (−2%), Respiración
16.1 (−0.6 rpm). Fases "vs lo habitual" (Profundo +10m, REM −3m, Ligero +14m).

- **Modelo de Deuda de sueño explicado:** *"Meeting that complete sleep need clears the
  displayed debt; recent shortfalls carry forward at a reduced weight."* (Balance −1h4m,
  necesidad 8h/noche, ventana 14 noches). Algoritmo concreto y copiable.
- **Para TID-MAX:** comparar siempre contra el baseline personal del atleta (no contra la
  población) hace el número accionable — es más honesto y más útil para el coach.
- **Otro bug i18n:** esa tarjeta de deuda sale en inglés (como la nota de Tendencias).

> **Dossier NOOP completo** — binario + las 5 pestañas (Hoy/Tendencias/Sueño/Entrenador/Más)
> y sus detalles. Sin capturas pendientes.
