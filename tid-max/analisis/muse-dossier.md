# Dossier de inteligencia competitiva — "Muse" / "Meta Muse"

**Fecha:** 2026-10-06 · **Autor:** NORTE (copiloto TID-MAX) para Carlos
**Encargo:** entender qué es el "Muse" que suena en la comunidad *Athlete AI* (@krudd.jr) y decidir la
jugada de TID-MAX (coach de IA + wearable para nadador de élite y corredores).
**Método:** WebSearch + WebFetch. Lo no verificable va marcado **[NO VERIFICADO]**. Separo hecho de marketing.

---

## 0. TL;DR — la conclusión que importa

El "Muse" del que habla la comunidad **NO es un producto de fitness ni un wearable**. Es **Muse from Meta**:
un **agente de IA de propósito general** (el "do-everything assistant" de Meta, lanzado el 8-sep-2026),
que la comunidad DIY **conecta a Garmin/health data** para automatizar su entrenamiento. Es el mismo
tipo de bestia que **Grok Bot (xAI)** y **Dots (OpenAI)** — los tres agentes horizontales del otoño 2026.
El fitness es **una de sus muchas capacidades**, no su identidad.

Para TID-MAX esto cambia el encuadre: Muse **no compite con nuestro posicionamiento de alto rendimiento
con ciencia de lab**; compite por la atención del *early adopter techie* que prefiere ensamblar su propio
coach. **Veredicto: VIGILAR + DIFERENCIARSE** (no ignorar, no aliarse todavía). Detalle en §9.

---

## 1. Qué es exactamente

**Muse from Meta** es el asistente/agente personal de IA de Meta, lanzado **8-sep-2026** en EE. UU. y
Canadá, para iOS, Android y web ([TechCrunch](https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/),
[App Store](https://apps.apple.com/us/app/muse-from-meta/id6760173601),
[Google Play](https://play.google.com/store/apps/details?id=com.facebook.aura)). Es un **agente
agéntico**: no solo chatea, sino que **ejecuta tareas de varios pasos** con un navegador real que puedes
ver trabajar en vivo — inicia sesión en sitios, investiga, llena formularios, compra y puede **hacer
pagos** con permiso ([TechCrunch](https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/),
[Khaleej Times](https://www.khaleejtimes.com/business/tech/meta-muse-ai-agent-rollout)).

**El ángulo fitness (marketing de Meta):** "Muse es tu *AI fitness coach*: construye un plan de
entrenamiento o de comidas a partir de los datos que elijas compartir, cuenta calorías y nutrición,
monitorea sueño y bienestar, y ajusta tu entrenamiento día a día" ([The Neuron](https://theneuron.ai/explainer-articles/how-to-get-started-with-meta-muse/),
[AARP](https://www.aarp.org/personal-technology/tech-guru-meta-muse-ai/)). **Esto es claim de marketing,
no profundidad demostrada** (ver §8 — en pruebas independientes dio consejo de salud pobre).

**Desambiguación (confirmada):** NO es la diadema EEG Muse (meditación), NO es la banda de rock, NO es
"Amuse". Es el agente de Meta de 2026. El nombre técnico del modelo es **Muse Spark 1.3**.

**En la comunidad Athlete AI:** los posts ("Meta Muse is Actually Legit", "Garmin + Muse Setup Guide",
"Muse vs Grok Bot vs Dots") reflejan a entusiastas **apuntando el agente general de Meta a sus datos de
Garmin** para armarse un coach casero — exactamente la **versión DIY** de lo que hace TID-MAX
([Athlete AI Community / Skool](https://www.skool.com/athlete-ai-community/about)). La comunidad es "no
code": conecta wearables + agentes de IA sin programar ([Skool](https://www.skool.com/athlete-ai-community/4-ways-i-am-using-ai-to-further-my-training)).

---

## 2. Cómo funciona técnicamente

- **Arquitectura:** corre en la **nube de Meta** sobre el modelo **Muse Spark 1.3** (enfocado en coding,
  uso de herramientas y tareas multi-paso). Una capa de permisos/credenciales separada llamada
  **Sentinel** gestiona las conexiones externas; las credenciales se guardan aparte del agente y las
  compras requieren aprobación ([The Neuron](https://theneuron.ai/explainer-articles/how-to-get-started-with-meta-muse/)).
- **Lee y escribe** en servicios conectados, con permisos granulares (p. ej. correo "solo lectura" vs.
  "enviar"). Categorías de conexión: **email, calendario, pagos/finanzas, shopping, smart home y
  "health & fitness"** ([The Neuron](https://theneuron.ai/explainer-articles/how-to-get-started-with-meta-muse/),
  [CNN vía snippet](https://www.cnn.com/2026/09/28/tech/meta-muse-ai-agents-amazon)).
- **Conexión a wearables:** Muse se conecta a **datos de salud/fitness** (vía Apple Health / Health
  Connect y las apps que el usuario enlace). **Que lea Garmin/Whoop/Strava/Oura directamente por API
  nativa — [NO VERIFICADO].** Lo documentado es que accede a "health & fitness data" con permiso; la
  comunidad escribe sus propias **guías de setup Garmin+Muse** para cablearlo ([Skool](https://www.skool.com/athlete-ai-community/about)).
- **¿Escribe workouts de vuelta al reloj?** **[NO VERIFICADO].** No hay evidencia de que Muse empuje
  sesiones estructuradas al Garmin. (Ojo: en la propia comunidad, "mandar el workout al reloj" se resuelve
  con **intervals.icu**, no con Muse — ver `athlete-ai-community-ideas.md` §7.)
- **No es MCP/Claude:** Muse **no** usa Claude ni MCP. Es stack propietario de Meta (Spark). Esto lo
  distingue del otro camino de la comunidad (Claude Code + MCP de Garmin), que es la receta que ya
  conocemos.

---

## 3. Plataformas y IA por detrás

- **Plataformas:** **iOS, Android y web**; soporte para gafas Meta (Ray-Ban/Oakley) y "computer use" en
  Mac anunciados como *próximos* ([TechCrunch](https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/)).
- **Disponibilidad:** solo **EE. UU. y Canadá** por ahora. **Esto es relevante para TID-MAX: Muse aún NO
  está en LATAM/México en español** — es una ventana.
- **IA detrás:** modelo propio de Meta, **Muse Spark 1.3**. No requiere ChatGPT ni Claude; es cerrado.

---

## 4. Precio y modelo de negocio

Freemium con tope por consumo de tokens ([The Neuron](https://theneuron.ai/explainer-articles/how-to-get-started-with-meta-muse/),
[MENA Startup Digest](https://menastartupdigest.com/?p=51131)):

| Plan | Precio | Notas |
|---|---|---|
| **Free** | $0/mes | Allowance semanal de tokens (las fuentes difieren: ~1M–100M tokens/sem **[NO VERIFICADO el número exacto]**). "Suficiente para la mayoría de los usos diarios" según Meta. |
| **Power** | $20/mes | Más consumo. |
| **Maximum** | $100/mes | Tope más alto. |

- **Todas las features están en todos los planes**; solo cambia *cuánto* puedes usarlas (no hay paywall
  por capacidad).
- **Sin anuncios** en la app y, según Meta, las conversaciones no entran a su sistema publicitario
  (afirmación de Meta, no auditada independientemente).
- Requiere **tarjeta de pago incluso en el tier gratis** ([The Neuron](https://theneuron.ai/explainer-articles/how-to-get-started-with-meta-muse/)).
- **Etapa:** NO es indie ni startup. Es **Big Tech con todo el músculo de Meta detrás** (distribución
  vía Facebook/Instagram/WhatsApp, Meta Connect). Esto es a la vez su mayor fuerza y, para el nicho de
  élite, parte de su debilidad (es masivo y genérico).

---

## 5. Quién está detrás

**Meta Platforms** (Zuckerberg). No es un emprendedor de fitness; es el producto bandera de IA de consumo
de Meta para 2026, promovido en **Meta Connect** ([TechCrunch](https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/)).
El "Muse" de la comunidad Athlete AI lo populariza **Kevin Rudd (@krudd.jr)** como *caso de uso*, pero
Rudd no es el creador — solo enseña a cablearlo a Garmin ([Skool](https://www.skool.com/athlete-ai-community/about)).

---

## 6. Tracción / adopción

Tracción **brutal, pero como app generalista, no como coach de fitness**:
- **3.4M+ descargas** a fines de sep-2026 (Sensor Tower); estimaciones alternas 4.3M (Apptopia) y 2.3M
  (Appfigures) ([TechCrunch](https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/)).
- **#1 en App Store (18-sep) y Google Play (19-sep)** en EE. UU.
- Crecimiento ~**55% día-a-día** en las primeras dos semanas (vs. ~24% del ChatGPT inicial).
- En la **comunidad Athlete AI** sí genera hilos ("Actually Legit", setup guides, comparativas vs. Grok
  Bot/Dots) — es tema caliente entre los DIYers, pero ése es un público de **nicho techie**, no de
  atletas de élite ([Skool](https://www.skool.com/athlete-ai-community/4-ways-i-am-using-ai-to-further-my-training)).

**El campo competitivo que la comunidad compara** (los tres agentes horizontales del otoño 2026):

| Agente | Dueño | Modelo | Entrada de precio | Notas |
|---|---|---|---|---|
| **Muse** | Meta | Spark 1.3 | **Gratis** | Errands, shopping, mensajería; navegador visible |
| **Grok Bot** | xAI | Grok | ~$20 (vía Cursor Pro) | Varios "bots" con tareas separadas |
| **Dots** | OpenAI | GPT‑6 Astra | ~$100 (ChatGPT Pro) | Un agente con su "computadora" en la nube; 4,000+ apps vía plugins |

Fuentes: [laozhang comparison](https://blog.laozhang.ai/en/posts/chatgpt-dots-vs-meta-muse-vs-grok-bot),
[Capital & Compute](https://capitalandcompute.net/blog/dots-vs-muse-vs-grok-bot/),
[efficient.app](https://efficient.app/compare/muse-vs-grok-bot). **Lectura clave:** los tres son
**horizontales**. Ninguno es un coach deportivo con ciencia de lab ni tiene wearable propio. El fitness es
un *use case* que los entusiastas les montan encima.

---

## 7. Comparación directa con TID-MAX

| Dimensión | Muse (Meta) | TID-MAX |
|---|---|---|
| **Naturaleza** | Agente de IA **generalista** (todo-en-uno) | **Vertical** de alto rendimiento deportivo |
| **Hardware** | Ninguno (usa el wearable que ya tengas) | **Banda propia** (etapa 2): PPG crudo ≥100 Hz, IBI/RR, bíceps |
| **Dato crudo** | Lee métricas cocinadas de apps de salud | **Onda PPG + RR crudo** → DFA‑α1, HRV reales |
| **Ciencia deportiva** | LLM genérico; consejo de salud **flojo en pruebas** (§8) | Zonas de lab, CTL/ATL/TSB, umbrales, modelos por deporte |
| **Natación** | No (nadie en el panorama la hace) | **Diferenciador** (módulo natación + análisis de técnica) |
| **Predicción** | Reactivo ("ajusta día a día") | IA **predictiva**: riesgo de lesión, sobreentreno, pico |
| **Entrenador en el ciclo** | No | Sí (coach dentro del flujo) |
| **Localización LATAM/ES** | Solo EE. UU./Canadá, inglés | **Español, LATAM-first** |
| **Producto** | Hágalo-usted-mismo (conectar/permisos) | **Hágalo-por-mí** (pulido, sin sideload) |
| **Privacidad/claims** | Banderas rojas serias (§8) | Claims acotados, sin diagnóstico; ethos de integridad de dato |
| **Distribución/escala** | Enorme (Meta) | Nicho, incipiente |
| **Precio** | $0 / $20 / $100 | SaaS 2 caras (B2C freemium + B2B licencia/atleta) |

**¿Competidor, adyacente o aliado?** **Adyacente con solape parcial.** Compite por el *early adopter
techie* que arma su propio coach, pero **no** por el atleta de élite que quiere ciencia de natación,
dato crudo y producto pulido en español. **No es aliado hoy** (Meta es cerrado, sin API para montarnos
encima, y sus banderas de privacidad chocan con nuestro ethos). Es, sobre todo, **validación de mercado**:
confirma que "coach de IA sobre tus wearables" es una categoría con demanda masiva.

**Dónde Muse gana:** distribución, gratis, UX agéntica (navegador que actúa), amplitud (email/compras/
calendario), velocidad de iteración de Big Tech.
**Dónde TID-MAX gana:** dato crudo y ciencia real, natación, IA predictiva, entrenador en el ciclo,
español/LATAM, producto hágalo-por-mí, claims responsables.

---

## 8. Riesgos y banderas (escéptico)

De Muse (sus debilidades = nuestras oportunidades):
- **Consejo de salud pobre en prueba independiente:** un test reportó que Muse ofreció analizar datos
  crudos de salud/labs y dio **guía médica muy por debajo de la de un médico**, con presentación
  "confiada" pero floja ([ainauten](https://news.ainauten.com/en/story/metas-new-ai-asked-for-my-raw-health-dataand-gave-me-terrible-advice)).
  **Esto valida nuestra tesis:** LLM genérico ≠ ciencia deportiva; el dato crudo mal interpretado es peor
  que no tenerlo.
- **Privacidad/seguridad — banderas serias:** acusado de **leer mensajes privados sin consentimiento**
  (un usuario reportó ~187,000 líneas sincronizadas pese a negar acceso), de intentar enlazar cuentas
  bancarias y escanear correos; **Amazon prohibió a Muse** en su plataforma por disclosure inadecuado y
  riesgo de *credential harvesting* ([KuCoin](https://kucoin.com/news/flash/meta-ai-agent-muse-accused-of-reading-private-messages-and-misleading-users),
  [The Week](https://www.theweek.in/news/sci-tech/2026/09/09/meta-says-its-muse-personal-ai-assistant-which-can-spend-your-money-is-safe-and-secure-is-it.html),
  [Global News](https://globalnews.ca/news/12077192/metas-ai-agent-muse-privacy/)).
- **Dependencia de permisos amplios:** su utilidad exige entregar email, calendario, salud, finanzas — a
  **Meta**. Para un atleta/coach que cuida datos, es fricción y riesgo reputacional.
- **Genérico por diseño:** optimizado para "errands/shopping/mensajería", no para periodización ni
  natación. Sin wearable, depende del reloj ajeno y del dato cocinado.

Banderas de la narrativa/hype general:
- Mucho del "fitness coach" es **marketing de Meta**, no capacidad demostrada en deporte de élite.
- El furor "Muse vs Grok vs Dots" es **moda de agentes 2026**; la vida real de estos flujos DIY
  (sideload, permisos, mantenimiento) es frágil.

---

## 9. Veredicto para TID-MAX

**VIGILAR + DIFERENCIARSE.** (No ignorar, no aliarse hoy.)

**Por qué:**
1. **No es nuestro competidor frontal.** Muse es horizontal y generalista; TID-MAX es vertical de alto
   rendimiento con dato crudo, ciencia de lab, natación e IA predictiva. Sus propias pruebas muestran
   consejo de salud flojo — justo el hueco que llenamos.
2. **Pero marca el mercado.** 3.4M+ descargas confirman apetito masivo por "coach de IA sobre mis
   wearables". Eso nos favorece: educa al mercado; nosotros llegamos con profundidad y producto pulido.
3. **Ventana geográfica:** Muse está en EE. UU./Canadá y en inglés. **LATAM/español sigue abierto** —
   nuestra cancha. Moverse rápido ahí es ventaja real.
4. **No aliarse aún:** Meta es cerrado (sin API para construir encima), y sus banderas de privacidad
   chocan con nuestro ethos de integridad y claims responsables. Aliarse diluiría el posicionamiento.

**Siguientes pasos accionables:**
- **Mensaje de posicionamiento** que use a Muse como contraste: *"Un agente generalista no sabe de
  umbrales de natación ni de DFA‑α1 con tu onda cruda. TID-MAX sí."* (sin nombrarlo en copy legal).
- **Alerta de competencia:** monitorear si Meta lanza Muse en México/español o firma integración nativa
  con Garmin/Whoop (eso cambiaría el cálculo). Revisar trimestralmente.
- **Doblar en los dos fosos que Muse no puede copiar barato:** (a) **natación + dato crudo PPG** (hardware
  propio, etapa 2) y (b) **confianza/privacidad** como feature de marca (lo opuesto a las banderas de Muse).

### Tabla resumen

| Pregunta | Respuesta corta |
|---|---|
| ¿Qué es? | Agente de IA **generalista** de Meta (no fitness, no wearable); la comunidad lo apunta a Garmin |
| ¿Fitness? | Capacidad secundaria; coach genérico, **consejo de salud flojo en prueba** |
| ¿Técnica? | Nube Meta, modelo **Spark 1.3**, lee/escribe apps con permisos; **no Claude/MCP** |
| ¿Garmin nativo? | **[NO VERIFICADO]**; accede a "health data", comunidad arma el setup |
| ¿Plataformas? | iOS/Android/web, **solo EE. UU./Canadá**, inglés |
| ¿Precio? | **Free** / $20 Power / $100 Maximum |
| ¿Quién? | **Meta** (no indie); Kevin Rudd solo lo populariza como use case |
| ¿Tracción? | 3.4M+ descargas, #1 app stores (como app general) |
| ¿Vs. TID-MAX? | **Adyacente**; gana en distribución/gratis, pierde en ciencia/natación/dato crudo/ES |
| ¿Riesgos de Muse? | Privacidad (Amazon lo baneó), consejo médico débil, genérico, cerrado |
| **Veredicto** | **VIGILAR + DIFERENCIARSE** (no ignorar, no aliarse) |

### 3 cosas que TID-MAX puede aprender/robar de Muse

1. **UX agéntica visible y de dos vías.** Muse deja *ver* al agente trabajar y ejecuta tareas multi-paso.
   Nuestro Coach debe sentirse igual de "vivo": brief matutino proactivo + chat de dos vías
   ("ajústame el sábado"), no solo avisos de una vía (encaja con `athlete-ai-community-ideas.md` §4).
2. **Onboarding de permisos granular y transparente.** Su layer "Sentinel" (credenciales aparte,
   permisos por acción, aprobación de pagos) es buen patrón — y **podemos ganarle por contraste**
   convirtiendo privacidad/consentimiento en bandera de marca donde Muse sangra.
3. **Freemium con tope por uso, todas las features en todos los planes.** Modelo simple y sin paywall por
   capacidad; baja fricción de entrada. Útil para nuestro B2C freemium (que el premium sea *cuánto/qué tan
   profundo*, no *si puedes o no*).

---

### Fuentes
- [TechCrunch — Meta pone su músculo detrás de Muse (25‑sep‑2026)](https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/)
- [CNN — agentes de IA y el baneo de Amazon (28‑sep‑2026)](https://www.cnn.com/2026/09/28/tech/meta-muse-ai-agents-amazon) *(HTTP 451 al fetch; citado vía snippet de búsqueda)*
- [The Neuron — cómo empezar con Meta Muse (setup, pricing, Spark 1.3)](https://theneuron.ai/explainer-articles/how-to-get-started-with-meta-muse/)
- [MENA Startup Digest — pricing desde $20](https://menastartupdigest.com/?p=51131)
- [AARP — Muse maneja tareas por ti (claim de fitness coach)](https://www.aarp.org/personal-technology/tech-guru-meta-muse-ai/)
- [Khaleej Times — Muse accede a apps, envía correos, hace pagos](https://www.khaleejtimes.com/business/tech/meta-muse-ai-agent-rollout)
- [ainauten — "pidió mis datos crudos de salud y dio mal consejo"](https://news.ainauten.com/en/story/metas-new-ai-asked-for-my-raw-health-dataand-gave-me-terrible-advice)
- [KuCoin — acusado de leer mensajes privados / engañar](https://kucoin.com/news/flash/meta-ai-agent-muse-accused-of-reading-private-messages-and-misleading-users)
- [The Week — ¿es seguro un asistente que gasta tu dinero?](https://www.theweek.in/news/sci-tech/2026/09/09/meta-says-its-muse-personal-ai-assistant-which-can-spend-your-money-is-safe-and-secure-is-it.html)
- [Global News — preocupaciones de privacidad de Muse](https://globalnews.ca/news/12077192/metas-ai-agent-muse-privacy/)
- [App Store — Muse from Meta](https://apps.apple.com/us/app/muse-from-meta/id6760173601) · [Google Play — Muse from Meta](https://play.google.com/store/apps/details?id=com.facebook.aura)
- Comparativas Muse/Grok Bot/Dots: [laozhang](https://blog.laozhang.ai/en/posts/chatgpt-dots-vs-meta-muse-vs-grok-bot) · [Capital & Compute](https://capitalandcompute.net/blog/dots-vs-muse-vs-grok-bot/) · [efficient.app](https://efficient.app/compare/muse-vs-grok-bot)
- Comunidad: [Athlete AI Community (Skool) — about](https://www.skool.com/athlete-ai-community/about) · [4 Ways I am Using AI](https://www.skool.com/athlete-ai-community/4-ways-i-am-using-ai-to-further-my-training) · [Connect Garmin to Claude Code](https://www.skool.com/athlete-ai-community/connect-garmin-to-claude-code)
