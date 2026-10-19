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
