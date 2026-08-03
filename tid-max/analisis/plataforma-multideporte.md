# TID-MAX → Plataforma de Rendimiento Humano (estrategia multideporte)

> Síntesis de tres revisiones externas (CPO/inversionista, Director de Ingeniería, CPO/Director) más la
> postura de TID. Decisión de fondo: **TID-MAX no es "una pulsera para nadadores", es el nodo de captura
> de una plataforma de inteligencia deportiva.** Carlos quiere el sensor de profundidad — y este documento
> muestra por qué eso **es compatible** con el enfoque de plataforma, no contrario. Fecha: 2026-08.
> Ver `subacuatico-diferenciador.md`, `especificacion-pulsera-rfq.md` (v2.1), `agentes-ai.md`.

## 0. Veredicto (qué nos conviene)

1. **Adoptar la tesis de plataforma.** El activo de la empresa es el **motor de IA**, no el hardware.
   Reposicionar: *"An AI-Powered Human Performance Platform"*; la banda es el **nodo de captura**.
2. **SÍ construimos el sensor de profundidad — pero como EDICIÓN, no como core.** El PCB universal lo
   soporta (RFQ v2.1, opcional [DURO] sin crecer case ni romper sellado); se **puebla** solo en la
   variante acuática **TID-MAX Aqua**. Así Carlos tiene su sensor **y** el core sigue universal. **No hay
   contradicción**: "opcional" nunca significó "no se hace", significa "no obliga a todos".
3. **Congelar el hardware core** (PPG + IMU) para el beta; que el 90% del valor venga de software/IA.
4. **Beachhead enfocado** (no "todos los deportes a la vez"): **Natación** (Gael, el diferenciador de
   profundidad, design partner) + **Running/Triatlón** (misma fisiología, cero hardware nuevo).
5. **Acelerar la IA de Rendimiento** (pico de forma): es el eslabón que conecta natación, running y
   triatlón — y aplica ya al *tapering* de Gael rumbo a Vancouver.
6. **NO perseguir ahora** el mercado ocupacional (bomberos/policía/militar/choferes). Es TAM real pero
   otra bestia regulatoria y otra venta; distrae y roza el guardrail "no medicina". Fase 3+.

## 1. En qué coinciden las tres opiniones (lo aceptamos)

- **Plataforma > producto.** Mismo hardware, IA especializada por deporte. Correcto y **barato**: es
  arquitectura de software, no fierro nuevo.
- **Sensor de profundidad opcional = buena arquitectura.** Protege BOM, tamaño, sellado, pool de
  proveedores y tiempo. (Ya ejecutado en RFQ v2.1.)
- **Pensar en CAPACIDADES, no en sensores** (recuperación, carga, estrés, sueño, ritmo circadiano).
- **Reencuadre de posicionamiento** a plataforma de inteligencia para atleta/coach/club/federación.
- **Prioridad #1 de prototipo: validar la señal en BÍCEPS** (auto-gain / corriente LED dinámica /
  off-body / piel oscura / sudor). Sin buena PPG en bíceps, la ventaja multideporte se cae. Es el
  **gate** de toda la tesis (encaja con EVK H1, §9.2 del RFQ).
- **Acelerar la IA de Rendimiento** de "planeada" a "en desarrollo".

## 2. Lo que CORREGIMOS de las opiniones (integridad de datos)

Dos opiniones atribuyeron al sensor de presión cosas que **no hace**. Lo fijamos aquí para no arrastrar
el error al cliente (ethos del AUDITOR; ver `subacuatico-diferenciador.md`):

| Afirmación externa | Realidad |
|---|---|
| "Sensor de profundidad para **conteo de vueltas**" | El conteo de largos es del **IMU**, no de la presión. |
| "...**tiempo por brazada / distancia subacuática**" | Brazada = IMU. Distancia/**velocidad** subacuática fina = **vídeo**. |
| "eficiencia de brazada **por profundidad**" | La presión da la **dimensión vertical** (profundidad de streamline/breakout y trayectoria del viraje), no la brazada. |

**Lo que el sensor de profundidad SÍ aporta (y es único):** el **perfil vertical** del subacuático +,
sobre todo, la **correlación IA subacuático × recovery/HRV** (palanca D, el moat). Ese es el valor —
no reemplazar a la cámara. Y "PPG grado médico" / "temperatura obligatoria": en nuestro spec la
**temperatura es opcional** (§4.3) y **no** reclamamos grado médico (roza COFEPRIS). Precisión importa.

## 3. Arquitectura que adoptamos (mapea a lo que YA tenemos)

```
  Capa 1  Sensores          PPG · IMU            (+ opcionales: profundidad, temp, SpO2)
  Capa 2  Motor fisiológico FC · HRV · sueño · carga (ACWR) · recuperación · estrés   ← ya existe (motor determinista)
  Capa 3  IA deportiva      Running · Natación · Ciclismo · Fútbol · Básquet ...       ← módulos = system prompt + contexto
  Capa 4  Usuario           Atleta · Coach · Club · Universidad · Federación
```

Clave: la **Capa 3 no son IAs nuevas desde cero.** Son **especializaciones** del patrón que ya corre
(`tid_agent.py`): mismo motor, distinto system prompt + distinto recorte de contexto por deporte. El
usuario elige su deporte en el perfil y eso activa el módulo. Barato de extender, difícil de copiar.

## 4. Decisión de producto: Core universal + ediciones

| Producto | Sensores | Mercado | Estado |
|---|---|---|---|
| **TID-MAX Core** | PPG + IMU (obligatorios) | Running, triatlón, fútbol, básquet, ciclismo, fuerza… | Beta H3 |
| **TID-MAX Aqua** | Core **+ profundidad** | Natación, apnea, tri (segmento nado) | Post-validación EVK |

Mismo PCB, misma carcasa, mismo ensamble; la Aqua solo **puebla** el sensor y abre el puerto de presión.
**Gael es el design partner** de la Aqua — el caso de uso perfecto para el diferenciador subacuático.

## 5. Por deporte, con el hardware ACTUAL (sin fierro nuevo)

- **Fútbol/Básquet:** IMU = carga mecánica (saltos, aceleraciones, cambios de dirección); PPG bíceps =
  carga fisiológica. **IA Preventiva** cruza mecánica×HRV → riesgo de lesión. Fatiga neuromuscular.
- **Running/Maratón:** economía aeróbica (HR/ritmo), cadencia; **IA Rendimiento** define el pico
  (tapering); **Nutriólogo** ajusta carga de glucógeno para los long runs.
- **Ciclismo:** PPG bíceps evita el ruido del manubrio; sincroniza power meter/cadencia; Nutriólogo
  para rutas largas.
- **Fuerza/CrossFit:** PPG bíceps lee FC aunque la mano apriete la barra; **Preventiva** vigila el SNC
  por HRV matutina (heavy vs recovery).
- **Natación:** todo lo anterior (carga/eficiencia/recuperación) **+ Aqua** para el subacuático.

## 6. Lo que NO hacemos ahora (trampas de foco)

- **Mercado ocupacional/seguridad** (microsueño, estrés térmico): otra venta (B2B/gobierno), otra
  regulación (posible dispositivo de seguridad/médico), y choca con el guardrail "no medicina". **Fase 3+**,
  con su propio análisis regulatorio.
- **"Todos los deportes a la vez":** dispersa el beta. Enfocar el beachhead (natación + running/triatlón)
  y expandir con evidencia.
- **Sensores futuros** (ECG, EDA, bioimpedancia, NFC, UWB): a evaluar por edición; ojo, el MAX86141 **no**
  hace ECG (requiere AFE aparte). No comprometer nada de esto en el beta.

## 7. Acciones concretas

1. **Posicionamiento:** actualizar narrativa a "Human Performance Platform" (nodo de captura + motor IA).
2. **RFQ:** ya soporta el core universal + profundidad opcional (v2.1). Sin cambios; validar en EVK.
3. **Prototipo H1 — gate #1:** validar señal PPG en **bíceps** (auto-gain/off-body/piel oscura/sudor).
   Es la condición de toda la tesis multideporte.
4. **IA de Rendimiento:** mover a *en desarrollo* (nutre de la HRV que ya capturamos; sirve al tapering
   de Gael ya).
5. **Roadmap de módulos deportivos:** definir orden — Natación (Gael) → Running/Triatlón → equipo.
6. **Registrar** esta decisión en `PROJECT-TRACKER.md`.

## Fuentes / relacionados
- `subacuatico-diferenciador.md` (qué mide de verdad el subacuático; palancas A–F).
- `especificacion-pulsera-rfq.md` v2.1 (§4.3 sensor de profundidad opcional [DURO] sin crecer case).
- `agentes-ai.md` (motor común + módulos; regla "el LLM no inventa números").
- `modulo-natacion-tidmax.md`, `metricas-nadadores-elite.md`, `aprendizajes-fr965.md`.
- Tres revisiones externas (CPO/inversionista · Director de Ingeniería · CPO/Director), 2026-08.
