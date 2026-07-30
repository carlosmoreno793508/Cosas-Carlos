# Oportunidades de producto (Quick Wins) — aprendizajes de usar la competencia

Bitácora viva de **gaps detectados al usar wearables existentes con un atleta real (Gael, nadador
de fondo)**. Cada gap de la competencia es un **requisito o diferenciador** para la banda TID-MAX.

> Regla: cuando un dispositivo de referencia (WHOOP, Samsung, etc.) **falla en algo que le importa
> al atleta**, se documenta aquí como (a) *Quick Win* de software que podemos resolver ya, y
> (b) *oportunidad de hardware/firmware* para nuestra propia pulsera.

---

## OPP-01 · Distancia y volumen de natación en alberca

**Estado:** 🟢 Quick Win de software implementado · 🔵 oportunidad de hardware documentada

### El hallazgo (evidencia real)
Gael nada **6–8 km al día** (y en doble sesión **8–10 km**). Al revisar sus datos por la API de
WHOOP, la distancia reportada en sus nados fue de **0.04 a 1.44 km** — es decir, **basura**.

### Causa raíz
WHOOP es una banda de **muñeca óptica + GPS**. En alberca:
- **No hay GPS** (señal no penetra el agua / techo).
- **No cuenta vueltas** (no tiene modo de natación con detección de largos por IMU).
WHOOP mide bien la **carga fisiológica** (FC, strain, kcal, recuperación) pero **no la distancia**.
Para un nadador, eso deja fuera **su métrica más importante: el volumen**.

### Impacto de negocio
El nado, triatlón y aguas abiertas son un **segmento desatendido** por los "recovery bands"
mainstream. Resolver bien el volumen de nado es un **gancho de adquisición** claro en LATAM.

### (a) Quick Win — software (YA hecho)
En el dashboard (`software/whoop_dashboard.py`):
- **Registro manual** `datos/registro-natacion.csv` (km, sesiones, min pesas por día).
- Banda **"NATACIÓN · volumen real"** con KM último día, KM 7 días, sesiones y pesas.
- El **Km de WHOOP se marca como "no confiable"** en la hoja Workouts.
- Cruce del volumen real con el **strain/FC de WHOOP** → esfuerzo por km.

### (b) Oportunidad de hardware/firmware — banda TID-MAX
**Modo natación en alberca con conteo de largos por IMU** (acelerómetro/giroscopio 6–9 ejes):
- Detección de vueltas por patrón de brazada + giro en pared → **distancia sin GPS**.
- Métricas de nado: distancia, ritmo por 100 m, largos, **SWOLF**, detección de estilo.
- Ya está en spec: **5 ATM (ISO 22810)** y carga sellada → la banda puede vivir en alberca.
- Diferenciador directo vs WHOOP/Oura para el mercado acuático.

### Puente que YA tenemos: Polar Verity Sense (Model 4J, WR50)
Confirmado en inventario (foto). Sirve para **dos cosas** hoy, sin esperar al EVK:
1. **Dato de nado interino (opción 3):** se clipa a los goggles, mide **FC bajo el agua** (WR50 =
   50 m) y registra la sesión vía **Polar Flow**. Fuente de FC de nado confiable mientras la banda
   propia no existe.
2. **Banco de pruebas del algoritmo (lo más valioso):** expone **PPG crudo + acelerómetro** por el
   **Polar BLE SDK** ("SDK mode"). Es el óptico de brazo **más parecido a TID-MAX** → con él se puede:
   - Validar el pipeline **PPG→IBI / DFA-α1** contra la referencia ECG (Polar H10).
   - **Prototipar el algoritmo de conteo de largos** con su acelerómetro (el mismo enfoque IMU que
     usará la banda), grabando sesiones reales de Gael en alberca.

**Siguiente paso sugerido:** capturar 1–2 sesiones de Gael con el Verity Sense en "SDK mode"
(PPG+ACC) y en Polar Flow (FC+distancia por largos), y compararlas contra el registro manual.
Eso alimenta el ítem H1 (banco de pruebas) y valida la viabilidad del modo natación.

---

## OPP-02 · Auto-detección y clasificación de entrenamientos

**Estado:** 🔵 capacidad de producto documentada (algoritmo/firmware a desarrollar)

### El hallazgo
WHOOP **detecta solo** el inicio/fin y la duración de cada sesión (los nados de Gael de ~2h26m,
las pesas de ~1h16m) sin que el atleta apunte nada. Lo hace combinando **FC sostenida (PPG)** +
**movimiento (acelerómetro)**. Pero **falla al nombrar el deporte** (a veces lo marca genérico:
"activity", "walking") y **no mide distancia de nado** (ver OPP-01).

### Cómo lo hace (para replicarlo)
- **FC sube y se mantiene** → marca inicio; **baja y se estabiliza** → marca fin (de ahí duración
  y strain, que **sí son confiables**).
- **Patrón de acelerómetro** → intenta clasificar el tipo de actividad.

### Oportunidad de producto — banda TID-MAX
Es una **funcionalidad central**, no un extra. Con los sensores que ya trae el spec (**PPG + IMU**)
TID-MAX puede:
- **Auto-detectar** inicio/fin/duración (paridad con WHOOP).
- **Clasificar mejor el deporte** por patrón de movimiento (brazada, cadencia, reps) — superando el
  "activity" genérico de WHOOP.
- **Contar vueltas → distancia de nado** (el diferenciador de OPP-01, que WHOOP no tiene).

### Puente de desarrollo
El **Polar Verity Sense** (PPG+ACC crudo por BLE SDK) es el banco para **entrenar y validar** estos
algoritmos con sesiones reales de Gael, antes del hardware propio. Ver OPP-01.

### (a) Quick Win — software (YA hecho)
El dashboard ahora muestra **hora local de inicio/fin y duración** de cada sesión (hoja Workouts),
igualando el resumen que ya se comparte.

---

## Nota de arquitectura · Conectividad de la banda

**Cómo se comunica la banda TID-MAX con el ecosistema:**

```
Banda TID-MAX  --(Bluetooth LE)-->  App del celular  --(WiFi/celular / internet)-->  Nube TID-MAX  -->  Dashboard + Coach
```

- **Banda ↔ Celular: Bluetooth Low Energy (BLE).** Enlace principal. Es de **bajísimo consumo**
  (clave para la autonomía de 7–14 días), universal y lo que usan WHOOP/Garmin/Polar. El chip del
  plan (nRF52840/nRF5340) ya trae BLE integrado.
- **Celular ↔ Nube:** el teléfono actúa de **puente** y sube los datos por internet a la tubería
  de datos que estamos construyendo.
- **Por qué NO WiFi/celular en la banda:** matarían la batería, suben costo/tamaño y disparan el
  peso regulatorio (IFT). Se descartan para el beta.

**Clave para natación:** el BLE (2.4 GHz) **no atraviesa el agua**. Por eso la banda **debe grabar
en memoria interna (store-and-forward)** durante el nado y **sincronizar por BLE al salir** — igual
que el Verity Sense. Esto ya está como decisión de firmware en el spec, y es **imprescindible** para
el caso de uso de nadador de Gael.

---

## Plantilla para nuevas oportunidades

```
## OPP-0X · <título>
Estado: ...
### El hallazgo (evidencia real)
### Causa raíz
### Impacto de negocio
### (a) Quick Win — software
### (b) Oportunidad de hardware/firmware — banda TID-MAX
```
