# Análisis de mercado — Wearables con dato crudo (banco de pruebas TID-MAX)

Objetivo: identificar dispositivos con API/SDK y **dato crudo** (PPG y/o RR/IBI) para montar un
banco de pruebas que valide el pipeline HRV / DFA-α1 antes/junto con el EVK (nRF52840 + MAX86141).

## El punto clave: el "RR gratis" por BLE estándar
El perfil Bluetooth **Heart Rate Service (0x180D)**, característica **0x2A37**, incluye el campo
**RR-Interval**. Cualquier dispositivo que lo implemente (correas baratas incluidas) **transmite los
intervalos RR sin SDK ni nube** — se leen con `bleak` (Python) o nRF Connect.

- Para HRV/DFA-α1 lo que necesitas son **RR/IBI limpios** → gratis de casi cualquier correa.
- **PERO** el RR ya es resultado de que el dispositivo detectó los picos internamente = **valida la
  SALIDA, no la ENTRADA**. TID-MAX hace justo eso (PPG crudo → IBI), así que el banco necesita: (a)
  una **verdad de referencia** RR grado ECG, y (b) dispositivos con **PPG crudo** para comparar
  nuestro extractor de picos contra uno serio (Polar SDK, Samsung Sensor SDK, Ultrahuman, Corsano).

## Comparativa (resumen)

Leyenda: RR/IBI = latido a latido · PPG = onda óptica cruda · ECG = electro crudo · ACC = acelerómetro.

### Correas de pecho (referencia)
| Dispositivo | Crudo | API/SDK | Precio | Rol |
|---|---|---|---|---|
| **Polar H10** | RR/IBI, ECG 130 Hz, ACC | Sí (SDK público) | ~$105 | **Verdad de referencia (gold standard HRV)** |
| Wahoo TICKR / X | RR/IBI (ACC en X) | Parcial (BLE estándar) | ~$50–80 | RR barato |
| Garmin HRM-Pro | RR/IBI | Parcial (SDK con vetting) | ~$120 | — |
| Movesense | ECG, IMU, HR/RR | Sí (SDK programable) | ~$180–350 | Sandbox de firmware |

### Brazaletes ópticos (lo más parecido a TID-MAX)
| Dispositivo | Crudo | API/SDK | Precio | Cercanía |
|---|---|---|---|---|
| **Polar Verity Sense** | **PPG crudo, ACC, PPI** | Sí (SDK "SDK-mode") | ~$105 | **La más alta: óptico de brazo, PPG crudo** |
| **Scosche Rhythm24** | RR/IBI (modo HRV), ACC | Parcial (BLE estándar) | ~$100 | Alta (bíceps/antebrazo) |
| Wahoo TICKR FIT | RR/IBI | Parcial | ~$80 | Alta |
| Biostrap EVO / Wavelet | PPG (bajo acuerdo) | Parcial (nube) | ~$175+ | Media |

### Consumo / anillos / médico (extracto)
| Dispositivo | Crudo | API/SDK | Precio | Nota |
|---|---|---|---|---|
| Samsung Galaxy Watch | PPG/ECG/IBI crudo | Sí (Sensor SDK, on-device, Android) | ~$200–300 | Encaja con ruta Health Connect del beta |
| Apple Watch | PPG crudo (SensorKit, entitlement) | Restringido | ~$250–400 | No plug-and-play |
| WHOOP / Fitbit / Oura | **NO crudo** (métricas nube) | Parcial | — | Sirven para integración, **no para validar pipeline** |
| Ultrahuman Ring AIR + UltraSignal | PPG crudo, ACC, temp | Sí (programa dev) | ~$350 | PPG en dedo |
| Corsano CardioWatch 287 | PPG, ACC, BioZ crudo | Sí (API/SDK) | ~$250–500 | Grado médico CE |

## Lista de compra recomendada (banco de pruebas)

**Núcleo (~$415, comprar ya):**
1. **Polar H10 — ~$105.** LA verdad de referencia (ECG). Todo error del pipeline se mide contra él. Innegociable.
2. **Polar Verity Sense ×2 — ~$210.** Gemelo funcional de TID-MAX (óptico de brazo, PPG crudo + PPI por SDK). 2 unidades para muñeca vs. bíceps. **Nota: el sensor Polar de natación con clip a goggles ya es un Verity Sense (o su antecesor OH1) → puede que ya tengamos 1.**
3. **Scosche Rhythm24 — ~$100.** Segundo óptico de otra marca + demo del "RR gratis" por BLE.

**I+D (si el presupuesto permite):**
4. **Movesense dev kit — ~$180–350.** Firmware custom on-device; prototipar store-and-forward antes del EVK.
5. **Ultrahuman Ring AIR + UltraSignal — ~$350.** PPG crudo en otra anatomía (generalización del algoritmo).

**Opcional (benchmark médico):** Corsano CardioWatch 287 (~$250–500).

**NO comprar para esto:** WHOOP, Fitbit, Amazfit/Zepp, Oura, RingConn — no dan crudo utilizable para validar.

## Cómo encaja
Este banco es el paso previo/paralelo al EVK. El H10 da la vara de medir; el Verity Sense dice si
nuestro firmware PPG→IBI está a la altura de un fabricante serio, **con el mismo tipo de señal óptica
de brazo que usará TID-MAX**. Siguiente paso: comprar H10 + 2× Verity Sense + Rhythm24, montar captura
BLE (`bleak`/Polar SDK) y definir protocolo (reposo, esfuerzo, sudor/movimiento) con RR del H10 como
verdad → métricas de error de DFA-α1 antes de que llegue el EVK.

**Experto a llamar:** un fisiólogo del ejercicio o bioestadístico para firmar el protocolo de
validación (Bland-Altman, criterios de aceptación de DFA-α1). NORTE prepara el protocolo; ellos validan.

## Fuentes
Bluetooth HRS spec · Polar BLE SDK (H10, Verity Sense) · Scosche Rhythm24 · Movesense dev kit ·
Samsung Health Sensor SDK · Apple SensorKit · Garmin Health SDK · WHOOP API · Fitbit intraday ·
Oura API · Ultrahuman UltraSignal · Corsano. (Precios retail 2026, confirmar en checkout; dev kits
requieren cotización/aplicación.)
