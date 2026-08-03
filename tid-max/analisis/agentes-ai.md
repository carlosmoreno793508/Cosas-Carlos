# Agentes AI — TID-MAX (arquitectura v0)

Cómo TID-MAX usa la **Claude API** para volver los números en **consejo conversacional** que Gael y su
entrenador entienden. Es la Capa 2 del producto (coach) sobre la Capa 1 (motor determinista).

> Cubre los ítems **2.1** (integración LLM), **2.2** (plan 5 pilares) y **2.4** (guardrails) del tracker.

---

## Regla de oro: el LLM NO inventa números

La división más importante del diseño, y la que hace al producto confiable (y defendible ante COFEPRIS):

```
  dataset.json  ──►  MOTOR determinista (código)  ──►  hechos + semáforo  ──►  AGENTE (Claude)  ──►  texto
   (esquema           ACWR, HRV vs base, FC vs        números duros,          interpreta,
    canónico)         base, sueño, volumen de nado    ya calculados           explica, conversa
```

- **El código calcula** Recovery vs base, desviación de HRV, ACWR (agudo:crónico), volumen de nado, semáforo.
  Esos números son **auditables y reproducibles** — no dependen del humor del modelo.
- **El agente interpreta**: toma esos hechos ya calculados y los explica, prioriza, y responde preguntas en
  lenguaje natural. Nunca se le pide "calcula el ACWR"; se le pasa "ACWR = 1.42 (zona de spike)".
- Si el modelo alucinara un número, no rompe nada crítico: la decisión (verde/amarillo/rojo) ya la tomó el motor.

Esto también nos deja **degradar con gracia**: sin `ANTHROPIC_API_KEY`, el agente cae al texto por reglas de
`tid_coach.py`. El producto sigue funcionando; solo pierde la conversación.

---

## Los agentes (roles)

Arrancamos con **un** agente coach y separamos por rol conforme crezca. Todos leen el **mismo** `dataset.json`.

| Agente | Qué hace | Entradas (del motor) | Estado |
|---|---|---|---|
| **Coach** | Reporte diario en lenguaje natural: veredicto + plan de 5 pilares, tono humano y personalizado a Gael. **Salida estructurada** (`coach-hoy.json`) que alimenta el dashboard. | semáforo, recovery, HRV/FC vs base, sueño, ACWR, km nado | 🟡 v0 (`tid_agent.py`) |
| **Preventivo** | Vigila señales tempranas de fatiga/sobreentrenamiento y escala **vigilar → descarga → fisio**. | tendencia HRV 7d, FC reposo 7d, días de recovery baja seguidos, ACWR | 🟡 v0 (`tid_agent.py --preventivo`) |
| **Q&A** | Responde preguntas libres del entrenador ("¿por qué bajó la HRV esta semana?") sobre el dataset. | hechos del atleta | 🟡 v0 (`tid_agent.py --pregunta`) |
| **Nutriólogo** | Estima el consumo desde **foto o texto** (kcal + macros), lo suma a "consumido vs meta" del día y arma el plan de comidas. **Con MEMORIA**: aprende los platillos recurrentes de Gael para autocompletar cuando falten detalles. | plantilla nutricional, meta del día, plan de nado, **memoria de alimentos** | 🟡 v0 (`tid_nutricion.py`) |
| **Rendimiento** | Lee la carga (ACWR / forma) y dice si el plan progresa y cuándo llega el pico rumbo al evento. | CTL/ATL/TSB, volumen, workouts | ⬜ |

> No sobre-ingenierizamos: **un** agente coach bien hecho cubre el 80%. Los demás son especializaciones del
> mismo patrón (mismo dataset, distinto system prompt + distinto recorte de contexto).

> ⚠️ **El Nutriólogo es el único que ESTIMA números nuevos** (kcal/macros de una foto), no solo interpreta
> lo ya calculado por el motor. Por eso es donde el **AUDITOR** más aplica: una mala estimación se va directo
> a la tarjeta de la familia. Mitigaciones: rango + confianza explícitos, y la memoria (abajo) que ancla la
> estimación a lo que Gael realmente suele comer.

### El Nutriólogo y su MEMORIA (aprendizaje sin reentrenar)

Carlos pidió que "la IA vaya aprendiendo de las fotos por si el usuario no tiene tiempo de subir todos los
detalles". La forma correcta **no es reentrenar el modelo** (caro, arriesga guardrails), sino **memoria +
reconocimiento** — el mismo principio de "el LLM no inventa, se le da contexto":

```
  cada comida  ──►  historial-alimentos.json  ──►  construir_memoria()  ──►  contexto del agente
   (foto/texto)      bitácora acumulada          platillos recurrentes      "esto es el desayuno
                     (tope 800, acotada)          + macros típicos           de siempre" → autocompleta
```

- **Guarda** cada estimación en `datos/procesado/historial-alimentos.json` (`guardar_historial`).
- **Aprende**: `construir_memoria()` agrupa por platillo, saca **macros típicos** (mediana), frecuencia y
  alimentos más vistos → los N más recurrentes.
- **Usa lo aprendido**: esa memoria entra en el contexto. Si la foto/el texto vienen **sin detalles** y
  coinciden con un platillo conocido, el agente **autocompleta porciones** y **baja la confianza a 'media'**
  (honestidad: no finge precisión que no tiene). Si no se parece a nada, estima normal.
- Ver lo aprendido: `python tid_nutricion.py --memoria`.
- **Privacidad:** la memoria es **por atleta** y local (vive en `datos/`, ya protegido por `.gitignore`).
  No se comparte entre clientes.

---

## Cómo se llama a Claude (referencia técnica)

Siguiendo la guía oficial de la Claude API:

- **SDK oficial de Python** (`anthropic`), nunca HTTP crudo ni shims de otros proveedores.
- **Modelo por defecto:** `claude-opus-5` (el más capaz de uso general). `claude-haiku-4-5` si queremos abaratar
  el reporte diario a escala.
- **Pensamiento adaptativo:** `thinking={"type": "adaptive"}` para el razonamiento del coach (no `budget_tokens`,
  que ya está deprecado / da 400 en los modelos nuevos).
- **Salida estructurada** (`client.messages.parse()` con un esquema Pydantic) para el veredicto diario: fuerza
  al modelo a devolver `{semaforo, veredicto, pilares{...}, alertas[]}` validado — cero parseo frágil.
- **Streaming** para el Q&A conversacional (respuestas largas sin timeouts).
- **Auth:** variable de entorno `ANTHROPIC_API_KEY` (o `ant auth login`). Nunca se hardcodea la llave.

Contexto que se le pasa al agente = **hechos del motor** (JSON compacto) + system prompt con la persona y los
guardrails. NO se le vuelca el dataset crudo entero: se le da el resumen ya calculado.

---

## Guardrails (ítem 2.4 — COFEPRIS)

Van en el **system prompt** de cada agente y se prueban:

1. **Rendimiento y bienestar, no medicina.** Nunca diagnostica, ni nombra enfermedades, ni sugiere fármacos.
   Ante señal de alarma real (p. ej. FC reposo disparada varios días), la acción es *"consulta a un profesional"*,
   no una interpretación clínica.
2. **No inventa datos.** Solo habla de los números que el motor le pasó. Si falta un dato, lo dice.
3. **Menor de edad.** El consejo va al entrenador/tutor, con tono responsable; nada de restricción calórica
   agresiva ni sobrecarga.
4. **Trazable.** Cada recomendación se apoya en una señal concreta y auditable (el semáforo del motor).

---

## Roadmap

- **v0 (hecho):** `tid_agent.py` — 3 agentes vía Claude API con fallback por reglas, leyendo `dataset.json`:
  Coach del día (**salida estructurada Pydantic** → `coach-hoy.json` para el dashboard), Preventivo
  (escalón vigilar→descarga→fisio) y Q&A conversacional (streaming). **+ Nutriólogo** (`tid_nutricion.py`):
  estimación por visión/texto, consumo vs meta, plan de comidas y **memoria de alimentos** (aprende los
  platillos recurrentes para autocompletar sin detalles).
- **v1:** persona nombrada del asistente (ítem 2.5); que el dashboard lea `coach-hoy.json`.
- **v2:** agente Rendimiento (forma/pico); memoria de conversación (histórico) cuando exista la BD (0.4).
- **v2-nutri:** verificación de rango en el Nutriólogo (auditar plausibilidad kcal/macros antes de mostrar);
  captura de correcciones del usuario como aprendizaje ("los frijoles llevan 1 cda de aceite").
- **v3:** cuando llegue el dato crudo (Polar Etapa 2 / EVK), sumar zonas de FC, TRIMP y DFA-α1 al contexto.
