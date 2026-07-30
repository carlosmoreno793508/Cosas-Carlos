# Guía — Conectar el Polar Verity Sense a la Mac (dato crudo)

**Objetivo:** conectar el **Polar Verity Sense** (Model 4J) por Bluetooth a la Mac y capturar señal
para el banco de pruebas de TID-MAX (ítem H1). Código: `software/polar_capture.py`.

> Por qué importa: el Verity Sense entrega FC latido a latido y (Etapa 2) **PPG + acelerómetro
> crudos** por el Polar BLE SDK — el óptico de brazo más parecido a TID-MAX. Ver
> `analisis/oportunidades-producto.md` (OPP-01) y `analisis/bandas-dato-crudo.md`.

## Etapas
- **Etapa 1 (esta guía):** FC + intervalos RR en vivo → CSV. Confirma la conexión.
- **Etapa 2 (siguiente):** PPG/ACC crudos (protocolo PMD) para DFA-α1 y conteo de vueltas.

## Antes de empezar
1. **Carga** el Verity Sense.
2. **Enciéndelo:** mantén el botón hasta que prenda el LED. Con toques cortos cambia de **modo**
   (los iconos: ♥ = frecuencia cardiaca, 〜 = natación/grabar). Para esta prueba, modo **♥ (HR)**.
3. **Bluetooth de la Mac** encendido y el sensor **cerca**.

## Permiso de Bluetooth para la Terminal (macOS) — clave
Ajustes del Sistema → **Privacidad y seguridad** → **Bluetooth** → activa **Terminal**.
(Sin esto, el escaneo no ve nada.)

## Pasos
```bash
cd ~/Cosas-Carlos/tid-max/software
source .venv/bin/activate
pip install -r requirements.txt        # instala bleak

python polar_capture.py --scan         # 1) ver que aparezca tu Polar
python polar_capture.py                # 2) conectar y capturar 120 s de FC
```
Verás la **FC en vivo** y al final `Guardado en: datos/polar_<fecha>.csv`.

> Si `--scan` no muestra el Polar: revisa el permiso de Bluetooth de la Terminal, que el sensor esté
> encendido en modo ♥ y que no esté ya conectado a otra app (Polar Flow/teléfono) — ciérrala.

## Qué sigue
Con la conexión confirmada, pasamos a la **Etapa 2** (PPG/ACC crudos) para arrancar la validación
del pipeline contra el Polar H10.
