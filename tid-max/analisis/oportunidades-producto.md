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
