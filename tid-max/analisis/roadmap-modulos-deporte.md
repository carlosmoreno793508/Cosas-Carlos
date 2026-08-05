# Roadmap de módulos de IA por deporte + pressure-test de la tesis de plataforma

> Encargo de Carlos (2026-08-03): (1) romper la estrategia de plataforma multideporte para ver qué
> aguanta, y (2) definir el orden de construcción de los módulos de IA por deporte. Grounded en el
> hardware **real** (RFQ v2.1: PPG bíceps MAX86141 + IMU; profundidad/temperatura **opcionales**; sin
> GPS, sin potencia, sin ECG) y en la arquitectura ya decidida (motor determinista + LLM que **no
> inventa números**; los módulos = system prompt + recorte de contexto, no IAs nuevas).
> Ver `plataforma-multideporte.md`, `agentes-ai.md`, `subacuatico-diferenciador.md`,
> `especificacion-pulsera-rfq.md` (v2.1), `PROJECT-TRACKER.md` (E1–E6, ítems 2.6, 4.2, H1.6, R0.7).
> Autor: NORTE. Este documento **no** modifica decisiones aprobadas; propone un matiz de secuencia.

---

## 0. Veredicto (léelo primero)

**La tesis de plataforma es correcta y barata de ejecutar — pero descansa sobre un gate no
resuelto y sobre un moat que aún no existe (se construye con datos en el tiempo).** Dos cosas que hay
que decir sin adornos:

1. **Todo cuelga de H1.6.** Si la PPG en bíceps no da RR-intervals grado-referencia bajo movimiento,
   sudor y piel oscura, la métrica insignia (DFA-α1) y la "carga fisiológica" por deporte se
   debilitan. Hoy eso es una **hipótesis a validar**, no un resultado. La estrategia está redactada
   como si el gate ya hubiera pasado. No lo ha pasado.

2. **El moat "IA predictiva por deporte" todavía no es un moat.** El motor determinista (ACWR,
   CTL/ATL/TSB, TRIMP, DFA-α1) es ciencia del deporte **pública y no propietaria**. La capa LLM es un
   moat de **UX/idioma/flujo con el coach**, no de datos — hasta que acumulemos resultados y lesiones
   etiquetadas por deporte. Con N=1 (Gael) + beta chico no se entrena ni valida un modelo predictivo
   de lesión por deporte. El moat **compone con el tiempo**; al arranque somos copiables por un
   incumbente con más datos. Hay que ser honestos con esto ante inversionistas.

**Sobre el orden del beachhead — mi veredicto es un "sí, pero con un matiz de secuencia":**

- **Natación debe seguir siendo el diferenciador central y el track de I+D desde YA** (Gael design
  partner, subacuático × recovery = el moat más fuerte y el más difícil de copiar). Eso **no cambia**.
- **Pero el rollout COMERCIAL del software (Etapa 1, software-first) debe LIDERAR con Running/Triatlón,
  no con Natación.** Tres razones duras:
  - **Dato de terceros:** en Etapa 1 ingerimos de WHOOP/Garmin/Samsung vía Terra/Vital. El dato de
    **running es rico**; el de **natación es pobre** (WHOOP no mide distancia de nado, sin GPS en
    alberca — ya documentado en 0.2 del tracker). El dato de nado *bueno* exige **nuestro** hardware
    (Aqua), que es Etapa 2 y aún no validado.
  - **PPG limpia:** running/ciclismo/triatlón son esfuerzo aeróbico estable → mejor caso para DFA-α1.
    Es donde el producto se ve mejor primero.
  - **Hardware listo:** running/triatlón = **cero fierro nuevo**; natación completa = **Aqua**
    (post-EVK, sin validar). Lanzar comercialmente con tu hardware menos listo es un autogol.

  → **Secuencia comercial recomendada: Running/Maratón → Triatlón (+ Ciclismo) → Natación (Aqua) →
  Fuerza → Fútbol/Básquet.** Natación corre en **paralelo como I+D con Gael desde el día 1** y sale a
  producción cuando Aqua valide. Esto honra que natación es el moat **y** arregla la secuencia de
  ingreso comercial. No es rechazar E3; es separar "flagship de I+D" de "primer producto que cobra".

- **Equipo (fútbol/básquet) va al final, y con expectativas recortadas:** un IMU en el **brazo** no
  es un sustituto validado de la carga mecánica de centro de masa (eso es un sensor de **tronco**,
  tipo Catapult). Ahí damos readiness fisiológica, no "PlayerLoad". Ver §2.

---

## 1. Pressure-test: los 5 supuestos más frágiles

### R1 — El gate del bíceps es más frágil en deportes de contacto/intermitentes que en aeróbicos
El bíceps es mejor que la muñeca para HRV bajo movimiento, cierto. Pero **DFA-α1 es brutalmente
sensible a artefacto de RR** (un par de latidos perdidos/ectópicos lo corrompen). En running/nado/
ciclismo el esfuerzo es rítmico y estable → caso amable. En **fútbol/básquet/CrossFit** hay impacto,
choques, cambios de dirección y contracción del brazo → artefacto de movimiento justo cuando más
quieres el dato. Conclusión honesta: **"carga fisiológica por PPG bíceps" es sólida en aeróbicos y
dudosa en contacto/intermitente.** Esto por sí solo dicta que los deportes de equipo van tarde.
- **Mitigación:** en H1.6/H1.4 validar el bíceps **por tipo de esfuerzo**, no solo "en movimiento":
  protocolo separado para estable (running) vs. intermitente/impacto (sprints, saltos, contacto). Si
  el intermitente no pasa, el módulo de equipo se limita a readiness matutina + sesión aeróbica, y se
  comunica así (no prometer HRV intra-partido).

### R2 — DFA-α1 óptica es una apuesta, no un hecho
El diferenciador "predictivo" se apoya en parte en DFA-α1 (umbrales aeróbicos personalizados sin
lactato). La literatura muestra que DFA-α1 derivada de PPG óptica **se degrada** frente a RR de ECG de
pecho. Es exactamente lo que H1.3/H1.4 deben medir contra el Polar H10. **Hoy la tesis lo da por
ganado.**
- **Mitigación:** tener un **plan B de producto** si la DFA-α1 óptica no llega a grado-referencia bajo
  esfuerzo: el producto sigue en pie con HRV en reposo (ráfaga 24/7, caso amable), TRIMP, ACWR,
  CTL/ATL/TSB, tendencias y el coach — todo eso **no** depende de DFA-α1 intra-esfuerzo. Marketing y
  claims deben poder degradar con gracia (alinea con R0.7). No amarrar el pitch entero a DFA-α1.

### R3 — La "IA por deporte" necesita datos que aún no tenemos (cold-start del moat)
La arquitectura (prompt + contexto sobre el mismo motor) es elegante y **barata** — eso es una
fortaleza real. Pero los claims de moat ("tu patada se degrada en recovery baja", "riesgo de lesión",
"tu pico será el día X") requieren **datos longitudinales etiquetados con resultados** (lesiones,
marcas, PBs) **por deporte**. Con Gael (N=1) y un beta chico no se valida un modelo predictivo. Al
principio el motor es **ciencia del deporte estándar** (copiable) + interpretación LLM (buena UX, no
moat de datos).
- **Mitigación:** ser explícitos: **Fase 3/4 es donde nace el moat de datos** (4.1 requiere el dataset
  acumulado del beta — ya está así en el tracker). Al arranque vendemos **claridad, idioma, coach-in-
  loop y agnosticismo**, no "IA que predice tu lesión". Instrumentar desde el día 1 la captura de
  **outcomes** (lesiones, resultados de competencia) para que el dataset valga; sin esos labels, nunca
  hay modelo predictivo. Este es el activo estratégico a construir, no la arquitectura de prompts.

### R4 — El IMU de brazo NO mide carga mecánica de equipo (y la estrategia lo insinúa)
`plataforma-multideporte.md` §5 dice "IMU = carga mecánica (saltos, aceleraciones, cambios de
dirección)" para fútbol/básquet. **Científicamente débil desde el brazo:** el estándar validado de
carga externa (PlayerLoad) es un sensor en el **tronco** (entre escápulas). Un IMU en bíceps/muñeca
mide el **brazo**, no el centro de masa; estima mal altura de salto, desaceleración y carga de cambio
de dirección. Sirve para cadencia, brazadas, conteo genérico y actividad — **no** como sustituto de
carga externa de equipo.
- **Mitigación:** recortar el claim de equipo a lo defendible (**carga interna fisiológica + readiness
  + actividad**), y si algún día se quiere carga mecánica de verdad, es una **edición con clip de
  tronco/cadera** (parienta del kit de cadera/tobillo del §C del subacuático), no el pod de brazo.

### R5 — Beachhead: liderar comercialmente con natación concentra riesgo en el caso menos listo
Natación es simultáneamente el **mejor moat** y el **peor caso operativo** de arranque: BLE no
atraviesa agua (store-and-forward), sin GPS, clasificador de estilo IMU no trivial (dorso difícil,
§E), dato de terceros pobre, y el diferenciador completo (profundidad) exige **Aqua** aún sin
validar. Además el mercado de nado competitivo es **nicho** vs. el de running/endurance. Liderar el
ingreso comercial ahí = máxima fricción, mínimo TAM temprano.
- **Mitigación = el matiz de secuencia del veredicto:** natación como **flagship de I+D con Gael desde
  ya** (construye el moat y la narrativa), pero **primer producto que cobra = Running/Triatlón**.

### Qué podría matar la ventaja vs WHOOP/Garmin — y cómo lo defendemos
| Amenaza | Realidad | Defensa durable |
|---|---|---|
| **WHOOP Coach (LLM) ya existe** y tienen millones de usuarios | Pueden localizar a español y añadir coaching | No abrirán su ingesta a wearables ajenos (canibaliza su hardware). **Nuestro agnosticismo + coach-in-loop B2B es lo que ellos no pueden copiar sin romper su modelo.** |
| **Garmin** tiene datos multideporte enormes + métricas on-device + potencia | Ecosistema maduro (TrainingPeaks/WKO) | Garmin no hace **recovery/IA predictiva fuerte** ni español-LATAM ni venta B2B a club/uni/federación. Ese es el hueco. |
| Localización a español es **copiable** | Sí, individualmente | El moat NO es una feature suelta; es el **combo**: agnóstico + predictivo + coach-in-loop + B2B LATAM + precio. Y el **dato de outcomes** que acumulemos (R3). |
| El motor determinista es **público** | Sí | Por eso el moat real es **datos de resultados por deporte** (Fase 3/4) + el **subacuático×recovery** (patentar, ver §natación) + el flujo con el entrenador. |

**Traducción sin rodeos:** hoy nuestro moat es **de modelo de negocio y GTM** (agnóstico, coach-in-
loop, B2B, LATAM/idioma/precio), no de tecnología. El moat **tecnológico** (predictivo por deporte +
subacuático×recovery) se construye con datos en Fase 3/4. Vender el segundo como si ya existiera es el
mayor riesgo de credibilidad.

---

## 2. Roadmap de módulos por deporte

Recordatorio de arquitectura: cada módulo = **misma** capa 1 (PPG+IMU) + **mismo** motor determinista
(capa 2) + **especialización** de capa 3 (system prompt + recorte de contexto). Las 6 IAs base:
**Coach** (orquestador), **Preventivo** (riesgo/fatiga), **Salud** (HRV/sueño/SpO2/temp/VO2max),
**Rendimiento** (carga/pico/tapering), **Q&A** (preguntas libres del coach), **Nutriólogo** (kcal/
macros, única que estima números nuevos). "Esfuerzo" es de software (extender el patrón), no de fierro.

### Tabla maestra

| Deporte | Qué entrega con HW ACTUAL (PPG bíceps + IMU), sin inventar | IAs base reutilizadas | Esfuerzo | Qué necesita | Moat (por qué cuesta copiar) |
|---|---|---|---|---|---|
| **Running / Maratón** | HRV/FC continua limpia (esfuerzo estable); carga interna TRIMP/ACWR/CTL-ATL-TSB; cadencia (IMU); DFA-α1 → umbral aeróbico **si H1.4 valida**. Ritmo/distancia/GPS = **wearable externo/teléfono**, no TID. | Rendimiento, Preventivo, Coach, Salud, Nutriólogo | **Bajo** | Solo prompt+contexto. Dato ya llega por agregador. | Tapering/pico predictivo + DFA-α1 personalizado, en español, con coach-in-loop. Barato de operar. Moat = UX/idioma al arranque. |
| **Triatlón** | **Carga integrada de 3 disciplinas** en un solo TSB + periodización/pico. Nado en beta = dato pobre de wearable; bici = potencia externa. El valor único = una carga combinada + tapering. | Rendimiento, Coach, Preventivo, Nutriólogo, Salud | **Bajo-Medio** | Prompt+contexto **+ modelo de carga multideporte** (sumar TSS de 3 fuentes). | Carga integrada tri + tapering en español; incumbentes lo hacen fragmentado. Encaja con el tapering de Gael a Vancouver. |
| **Ciclismo** | HRV/FC **limpia en bíceps** (evita ruido del manubrio — ventaja real vs muñeca); carga interna; CTL/ATL/TSB con TSS de **potencia externa** (Garmin/Wahoo/Zwift vía Terra). No damos potencia propia. | Rendimiento, Coach, Preventivo, Nutriólogo, Salud | **Bajo-Medio** | Prompt+contexto + **ingesta de potencia externa** (ya cubierta por agregador). | HRV limpia sobre la bici + readiness; el ecosistema (TrainingPeaks/WKO) es fuerte → moat medio (idioma + coach). |
| **Natación** | **Sin Aqua:** largos/lap por IMU, cadencia de brazada, **tiempo subacuático por viraje + su decaimiento** (IMU), FC bajo agua (store-and-forward), HRV en reposo. **NO** da profundidad (→Aqua), **NO** velocidad subacuática fina (→vídeo), **NO** distancia por GPS. **Con Aqua:** perfil de profundidad de streamline/breakout + trayectoria de viraje. | Coach, Rendimiento, Preventivo, Salud, Nutriólogo (+ módulo natación) | **Medio-Alto** | Prompt+contexto **+ clasificador de estilo/lap IMU** (dorso difícil, §E) **+ Aqua (hardware, post-EVK)** para el moat completo **+ kit cadera/tobillo (fase 2)**. | ⭐ **El más fuerte:** subacuático × recovery/HRV. Imposible para WHOOP (no mide nado), Garmin (recovery débil), TritonWear (sin HRV) y el vídeo (sin fisiología). Gael design partner + **patentable** (consultar PI). |
| **Fuerza / CrossFit** | **Readiness por HRV matutina** (heavy vs recovery) = el valor central; FC bíceps lee aunque la mano apriete la barra (**ventaja real** vs muñeca). Conteo de reps por IMU de brazo = **poco fiable** en barra (el brazo no sigue la barra). **NO** da velocidad de barra (VBT=encoder) ni 1RM. | Preventivo (SNC/HRV), Coach, Salud, Rendimiento | **Bajo** | Solo prompt+contexto. El valor es la capa readiness, no in-session. | Bajo-medio: readiness HRV es genérico; ventaja = FC fiable con manos ocupadas + idioma. |
| **Fútbol** | Carga interna fisiológica (FC/HRV) **con caveat de artefacto en contacto/intermitente** (R1); readiness matutina. IMU de brazo = actividad del brazo, **NO** PlayerLoad de tronco (R4). **NO** GPS/distancia/sprints (externo). | Preventivo (riesgo), Coach, Salud, Rendimiento | **Medio** | Prompt+contexto **+ validar PPG bajo contacto (peor caso de H1.6)**. Carga mecánica real = **edición clip de tronco** (no el pod de brazo). | Débil-medio con HW actual: la carga mecánica desde el brazo no compite con chalecos (Catapult). Ángulo = B2B equipo/uni + readiness, y el **moat de lesión llega con datos de beta** (R3). |
| **Básquet** | Igual que fútbol: readiness fisiológica sí; saltos/aterrizajes (clave de lesión) **mal estimados** desde el brazo (mejor en cadera). Intermitente → artefacto (R1). | Preventivo, Coach, Salud, Rendimiento | **Medio** | Igual que fútbol. Salto/aterrizaje fiable = accesorio de cadera. | Igual que fútbol: moat de lesión = datos de beta, no HW actual. |

### Lo que NO se puede con el hardware actual (marcado honesto)
- **Profundidad de nado / perfil subacuático** → requiere **Aqua** (sensor de presión poblado; edición
  post-EVK). No lo da el Core.
- **Velocidad subacuática/intra-ciclo fina** → **vídeo** (integración, no el pod). Ya aclarado en
  `subacuatico-diferenciador.md`.
- **Distancia/ritmo/GPS** (running, ciclismo, nado en aguas abiertas) → **wearable externo/teléfono**;
  el pod no lleva GPS (decisión [DURO] del RFQ).
- **Potencia de ciclismo** → **power meter externo** ingerido por agregador. No lo genera TID.
- **Potencia/dinámica de carrera** (tipo Stryd/Garmin Running Dynamics) → wearable externo.
- **Carga mecánica de equipo (PlayerLoad), altura de salto, aterrizaje** → **sensor de tronco/cadera**
  (edición/accesorio futuro), no el pod de brazo.
- **Velocidad de barra (VBT), 1RM** → encoder de fuerza externo. Fuera de alcance.
- **ECG/EDA/bioimpedancia** → el MAX86141 no hace ECG (AFE aparte). Fuera del beta.

---

## 3. Orden recomendado de implementación (y por qué)

Ordenado por **(esfuerzo bajo × dato ya disponible × PPG limpia × TAM temprano)**, con el moat
construyéndose en paralelo:

1. **Running / Maratón** — esfuerzo **bajo**, dato de terceros **rico**, PPG en su mejor caso, TAM
   endurance grande, y la **IA de Rendimiento (E4, ítem 4.2)** aplica de inmediato. Es el módulo que
   mejor exhibe el producto primero. **Empezar aquí.**
2. **Triatlón** — reutiliza running + añade la **carga integrada de 3 deportes** (el valor único),
   atletas de alto LTV, y conecta directo con el tapering de Gael. Esfuerzo bajo-medio.
3. **Ciclismo** — add barato (potencia externa ya ingerida), completa la familia endurance, HRV limpia
   en bici es una ventaja real. Cierra el "trío aeróbico".
4. **Natación (Aqua)** — **el moat más fuerte, pero gated en Aqua + clasificador IMU.** Corre como
   **I+D con Gael desde el día 1** (construye moat y narrativa); **sale a producción cuando Aqua
   valide** (post-EVK, tras H1.5). No liderar el ingreso comercial aquí (R5), pero **nunca soltarlo
   como diferenciador**: es lo único verdaderamente no-copiable. Iniciar el trámite de **patente**
   (subacuático×recovery + kit modular) en paralelo.
5. **Fuerza / CrossFit** — barato de sumar (prompt+contexto), valor = capa readiness; moat modesto.
   Buen "long-tail" para ampliar retención sin gran inversión.
6. **Fútbol / Básquet (equipo)** — **al final.** Depende del peor caso de H1.6 (PPG en contacto) y el
   moat de lesión necesita el **dataset del beta** (R3). El ángulo es **B2B (equipo/universidad)** con
   claim recortado a readiness + carga interna, no PlayerLoad. Si se valida el clip de tronco, se
   reabre el caso de carga mecánica como edición.

**Relación con E3:** E3 dice "Natación → Running/Triatlón → equipo". Este roadmap **mantiene natación
como el diferenciador y el track de I+D con Gael desde ya**, pero recomienda que el **rollout comercial
del software lidere con Running/Triatlón** por readiness de dato/PPG/hardware, y que natación entre a
producción con Aqua. Es un matiz de **secuencia de ingreso comercial**, no un cambio de fondo de la
estrategia. Si Carlos prefiere mantener el orden literal de E3, la condición para liderar con natación
es tener Aqua validada y el clasificador de estilo IMU listo — lo cual mueve el primer ingreso comercial
más tarde. Mi recomendación es no esperar a eso para empezar a cobrar.

---

## 4. Próximos pasos accionables
1. **Ítem 2.6 (tracker):** arrancar el módulo **Running** como primera especialización de
   `tid_agent.py` (system prompt + recorte de contexto de running). Es el de menor esfuerzo y ya hay
   dato real de Gael/WHOOP para probarlo.
2. **Ítem 4.2 (Rendimiento):** priorizar el motor de **CTL/ATL/TSB + pico/tapering**; es prerequisito
   de los módulos endurance (running, tri, ciclismo) y sirve ya a Gael.
3. **H1.4/H1.6:** validar el bíceps **separando esfuerzo estable vs intermitente/contacto** (R1); ese
   resultado decide qué tan pronto (y con qué claim) entran fútbol/básquet.
4. **Instrumentar captura de OUTCOMES desde el día 1** (lesiones, marcas, resultados): es el activo que
   convierte la arquitectura en moat de datos (R3). Sin labels no hay modelo predictivo en Fase 4.
5. **Patente natación:** preparar requisitos para el abogado de PI (subacuático×recovery + kit modular)
   en paralelo al I+D con Gael.
6. **Claims (R0.7):** que el marketing pueda degradar con gracia si DFA-α1 óptica no llega a
   grado-referencia (R2). No amarrar el pitch entero a DFA-α1.

## Fuentes / relacionados
- `plataforma-multideporte.md` (estrategia E1–E6), `agentes-ai.md` (6 IAs, motor + módulos),
  `subacuatico-diferenciador.md` (palancas A–F; qué mide el subacuático de verdad),
  `especificacion-pulsera-rfq.md` v2.1 (HW real; profundidad/temp opcionales; sin GPS/potencia),
  `PROJECT-TRACKER.md` (ítems 2.6, 4.2, H1.4, H1.6, R0.7; regla de gasto go/no-go H1.5).
