# TID-MAX — Panorama competitivo (bandas de recuperación / rendimiento)

> **Fecha:** 2026-10-25 · **Estado:** vivo (actualizar al salir nuevos datos).
> Marco de referencia: TID-MAX es una banda de rendimiento para atletas de alto nivel, con
> **motor local**, **procedencia por dato**, scores **APROXIMADOS** (no diagnóstico) y señal de
> grado investigación (R-R crudo del Polar H10). Esta ficha nace del análisis de dos productos que
> aparecieron en redes (oct-2026): un **concepto** de banda Apple y **HIYD.ai** (real).
>
> Cifras de competidores = declaradas por ellos o por prensa; verificar en su fuente antes de citar
> en material externo.

---

## Resumen ejecutivo

- El **"Apple Loop" $299** que circula es un **render conceptual** (emkwan), **no un producto**.
  No hay fuente que confirme una banda sin pantalla de Apple. Señal útil: la categoría está tan
  caliente que el público *imagina* a Apple entrando → valida el mercado y marca el **riesgo #1**
  (un gigante con ecosistema que barra a las bandas genéricas).
- **HIYD.ai** sí es real (Kickstarter nov-2026, fundador ex-Apple, +16 k inscritos). Es el **espejo
  más cercano** de TID-MAX en promesa de features y en la bandera **"sin suscripción"**, pero
  compite en **conveniencia/amplitud**, no en profundidad.
- **"Sin suscripción"** ya es *table stakes* (todos atacan el talón de WHOOP). Nuestro diferenciador
  tiene que ser **profundidad verificada + honestidad + señal para alto rendimiento**, no la lista
  de features.

---

## 1 · "Apple Loop" / banda Apple — CONCEPTO (no real)

| Campo | Dato |
|---|---|
| Qué es | Render conceptual de **emkwan** (creador de contenido Apple): módulo de aluminio con logo Apple + LED verde + correas tipo Sport Loop de colores, *"ᐤLoop · Starting at $299"* |
| Realidad | **No anunciado por Apple. Sin fuente que lo confirme.** Contenido especulativo ("Apple could REALLY be coming…", encuesta con ~3,970 votos) |
| Relevancia | (a) valida que el nicho banda-sin-pantalla/recuperación está caliente; (b) marca el riesgo existencial de que Apple/Samsung entren con ecosistema y precio agresivo |
| Ancla | Estética (aluminio + Sport Loop) y precio imaginado ($299) como referencia de mercado |

**Implicación TID-MAX:** no es amenaza hoy, pero define el peor escenario. El foso **no puede ser
medir HR/HVC** (eso lo hará cualquiera, Apple incluido): tiene que ser el caso N-of-1, la honestidad
del dato y el coaching para alto rendimiento.

---

## 2 · HIYD.ai — REAL, competidor-patrón

| Campo | Dato |
|---|---|
| Forma | Disco de **7 g / 2,7 mm** que se pega por **microsucción a la parte trasera de un reloj normal** (sin imanes ni adhesivo) |
| Mide | FC, **HVC**, fases de sueño, movimiento, calorías, **VO₂max** (estimado), SpO₂, temp de piel |
| App / modelo | iOS + Android · **nutrición con IA** · **sin suscripción mensual** |
| Precio | **$199** early-bird (depósito VIP reembolsable ~$10 según un directorio) |
| Lanzamiento | **Kickstarter nov-2026**; envíos citados Q2-2027 (hay discrepancia entre fuentes) |
| Respaldo | Fundador **Salah Batroukh, ex-ingeniero de Apple**; **+16,000 inscritos** pre-lanzamiento |
| Fuentes | TechCrunch, NewsBytes, EcosistemaStartup, PCWelt, Netzwelt, TAAFT (ver abajo) |

**Fortalezas:** conveniencia (usa tu reloj de siempre), pedigree de fundador, demanda validada
(16 k), "sin suscripción" + nutrición IA, precio bajo de entrada.

**Debilidades / nuestra cuña:**
- **No controla el sensor ni la postura de medición** (depende del reloj, de la microsucción, de
  la posición). Para **HVC/DFA-α1** de calidad eso importa; nuestra banda dedicada + **R-R crudo del
  H10** da mejor señal para el atleta serio.
- **Features de bullet, sin verdad de ingeniería mostrada.** "VO₂max estimate / HVC / sleep" lo
  prometen todos. Nosotros lo **verificamos** (ver sección 4).

---

## 3 · Referencias del mercado (contexto)

| Producto | Forma | Modelo | Nota para TID-MAX |
|---|---|---|---|
| **WHOOP** | Banda sin pantalla | **Suscripción** (hardware "gratis") | Define la categoría; su suscripción es el talón que todos atacan. Day Strain es propietario |
| **Oura** | Anillo | Hardware + **suscripción** | Fuerte en sueño; forma distinta |
| **HIYD** | Adhiere a reloj | Sin suscripción + IA | Espejo más cercano (ver §2) |
| **Apple (concepto)** | Banda imaginada | Ecosistema | Riesgo existencial si se vuelve real |
| **TID-MAX** | Banda dedicada | **Motor local, sin cloud obligatorio**, coach BYOK | Profundidad + honestidad + alto rendimiento |

---

## 4 · Dónde nos diferencia el motor (verificado, no prometido)

Esto es lo que una ficha de features de competidor **no** puede decir, y nosotros sí, porque ya está
construido y **probado**:

- **Matemática de HVC correcta, demostrada.** RMSSD/SDNN/pNN50 coinciden con la referencia textbook
  Task Force (1996) **a 1e-9** (`software/valida_motor.py`), misma metodología que los *agreement
  tests* de NOOP. SDNN con ddof muestral (corregido en la validación).
- **R-R gap-aware + ventana por calidad** (`hrv_rr.py`), no un RMSSD ingenuo.
- **Carga (recuperación)** = z-score + logística HVC-dominante, **11 constantes pineadas** y
  semántica de nulos (cold-start → nada), con guard de saturación parasimpática detectado.
- **Esfuerzo propio desde HR** (Karvonen→Edwards→log) — no dependemos del Day Strain de WHOOP.
- **Readiness (Plews/Altini SWC)**, **Edad fitness/VO₂max (Nes 2011)** validado contra el ~59 real
  de Carlos, **alerta de enfermedad** con supresión por confusores.
- **Honestidad como producto:** "no disponible ≠ 0", procedencia por dato (3 ejes), scores marcados
  **APROXIMADO**, recomputamos lo nuestro (los scores ajenos quedan como referencia).
- **Privacidad / offline:** motor en el dispositivo, coach **BYOK** (tu clave, apuntable a modelo
  local), nada sale salvo bajo petición explícita.

---

## 5 · Lecturas accionables

1. **Posicionamiento:** no competir en "features de lista" (ahí HIYD/Apple empatan o ganan en
   conveniencia). Competir en **profundidad verificada + honestidad + grado investigación para
   alto rendimiento**. Es defendible y es lo que ya tenemos.
2. **"Sin suscripción" es table stakes** — comunicarlo, pero no como diferenciador único.
3. **GTM:** el patrón validado es **waitlist → crowdfunding → credibilidad**. Nuestra credibilidad
   no es un CV de Apple: es el **motor validado y el caso N-of-1 real**. Mostrarlo (la validación a
   1e-9, el VO₂max que cuadró, las correlaciones reales) en el lanzamiento.
4. **Precio de referencia:** HIYD $199, concepto Apple $299 → banda de precio del nicho.
5. **Vigilar:** campaña Kickstarter de HIYD (nov-2026) para specs/precio finales; cualquier señal
   real de Apple/Samsung/Google en banda sin pantalla.

---

## Fuentes

- HIYD — TechCrunch: https://techcrunch.com/?p=3170944
- HIYD — NewsBytes: https://www.newsbytesapp.com/news/science/hiyd-unveils-microsuction-watch-tracker-for-heart-rate-and-sleep/tldr
- HIYD — EcosistemaStartup (ES): https://ecosistemastartup.com/?p=117858
- HIYD — PCWelt (DE): https://www.pcwelt.de/article/3258776/
- HIYD — Netzwelt (DE): https://www.netzwelt.de/news/259594-neuer-sensor-macht-armbanduhr-smartwatch-haelt-laenger-galaxy-watch.html
- HIYD — There's An AI For That (directorio): https://theresanaiforthat.com/device/hiyd-sensor/
- "Apple Loop": sin fuente que confirme un producto real (render conceptual de emkwan).
  Conceptos Apple Watch no relacionados: https://9to5mac.com/2021/02/04/apple-watch-multi-color-braided-solo-loop/

> Nota: cifras de precio/envío/inscritos provienen de los propios fabricantes o de prensa; la fecha
> de envío de HIYD difiere entre fuentes. Verificar en el Kickstarter oficial antes de usar en
> material externo.
