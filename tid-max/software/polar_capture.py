#!/usr/bin/env python3
"""
polar_capture.py — Conecta el Polar (Verity Sense / H10) por Bluetooth a tu Mac y captura datos.

ETAPA 1: registra FRECUENCIA CARDIACA + intervalos RR (latido a latido) en tiempo real y los
guarda en datos/polar_<fecha>.csv. Los RR/IBI son la base de HRV / DFA-alfa1.
(La señal PPG/acelerometro cruda es la ETAPA 2 — protocolo PMD de Polar.)

Uso:
    python polar_capture.py --scan            # lista los dispositivos Bluetooth cercanos
    python polar_capture.py                   # busca "Polar", conecta y captura 120 s
    python polar_capture.py --seconds 300     # captura 5 minutos
    python polar_capture.py --address <ID>    # conectar a uno especifico (copiado de --scan)

Requisitos:  pip install -r requirements.txt   (incluye 'bleak')
macOS: da permiso de Bluetooth a la Terminal en
  Ajustes del Sistema  >  Privacidad y seguridad  >  Bluetooth  >  activa "Terminal".
"""
import asyncio
import argparse
import os
import sys
import csv
from datetime import datetime, timezone

try:
    from bleak import BleakScanner, BleakClient
except ImportError:
    sys.exit("Falta 'bleak'. Instala con:  pip install -r requirements.txt")

# Heart Rate Measurement (perfil Bluetooth estandar 0x2A37)
HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "datos")


def parse_hr(data):
    """Decodifica el paquete de Heart Rate Measurement -> (hr_bpm, [rr_ms, ...])."""
    flags = data[0]
    idx = 1
    if flags & 0x01:  # HR en 16 bits
        hr = int.from_bytes(data[1:3], "little")
        idx = 3
    else:
        hr = data[1]
        idx = 2
    if flags & 0x08:  # energia gastada presente -> saltar 2 bytes
        idx += 2
    rr = []
    if flags & 0x10:  # intervalos RR presentes
        while idx + 1 < len(data):
            val = int.from_bytes(data[idx:idx + 2], "little")
            rr.append(round(val / 1024 * 1000, 1))  # unidades 1/1024 s -> ms
            idx += 2
    return hr, rr


async def scan():
    print("Buscando dispositivos Bluetooth (6 s)... (enciende el Polar)")
    devs = await BleakScanner.discover(timeout=6.0)
    if not devs:
        print("No se vio ningun dispositivo. Revisa el permiso de Bluetooth de la Terminal.")
        return
    for d in devs:
        marca = "  <-- POLAR?" if (d.name or "").lower().find("polar") >= 0 else ""
        print(f"  {d.name or '(sin nombre)':32}  {d.address}{marca}")
    print("\nSi ves tu Polar arriba, corre:  python polar_capture.py")


async def find_polar(name):
    print(f"Buscando '{name}' (12 s)... asegurate que el Polar este ENCENDIDO y cerca.")
    return await BleakScanner.find_device_by_filter(
        lambda d, ad: (d.name or "").lower().find(name.lower()) >= 0, timeout=12.0
    )


async def capture(address, seconds, name):
    if not address:
        dev = await find_polar(name)
        if not dev:
            sys.exit(f"\nNo encontre un dispositivo '{name}'. Enciendelo y prueba:  python polar_capture.py --scan")
        address = dev.address
        print(f"Encontrado: {dev.name} ({address})")

    os.makedirs(DATA_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(DATA_DIR, f"polar_{stamp}.csv")
    f = open(path, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(["t_iso", "hr_bpm", "rr_ms"])
    count = {"muestras": 0, "rr": 0}

    def cb(_, data):
        hr, rr = parse_hr(bytearray(data))
        t = datetime.now(timezone.utc).isoformat()
        if rr:
            for r in rr:
                writer.writerow([t, hr, r])
                count["rr"] += 1
        else:
            writer.writerow([t, hr, ""])
        count["muestras"] += 1
        f.flush()
        extra = f"   RR {', '.join(str(x) for x in rr)} ms" if rr else ""
        print(f"  HR {hr:3d} bpm{extra}        ", end="\r", flush=True)

    print(f"Conectando a {address} ...")
    async with BleakClient(address) as client:
        print("Conectado ✅  Capturando... (Ctrl+C para parar)\n")
        await client.start_notify(HR_UUID, cb)
        try:
            await asyncio.sleep(seconds)
        finally:
            try:
                await client.stop_notify(HR_UUID)
            except Exception:
                pass
    f.close()
    print(f"\n\nListo. {count['muestras']} muestras, {count['rr']} intervalos RR.")
    print(f"Guardado en: {path}")
    if count["rr"] == 0:
        print("Nota: este dispositivo no envio RR por el perfil estandar (normal en el Verity Sense).")
        print("      Los RR/PPG/ACC crudos vienen en la ETAPA 2 (protocolo PMD de Polar).")


def main():
    ap = argparse.ArgumentParser(description="Captura FC/RR del Polar por Bluetooth.")
    ap.add_argument("--scan", action="store_true", help="listar dispositivos cercanos")
    ap.add_argument("--address", help="ID/UUID del dispositivo (de --scan)")
    ap.add_argument("--name", default="Polar", help="nombre a buscar (default: Polar)")
    ap.add_argument("--seconds", type=int, default=120, help="duracion de captura (default 120)")
    args = ap.parse_args()
    try:
        if args.scan:
            asyncio.run(scan())
        else:
            asyncio.run(capture(args.address, args.seconds, args.name))
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")


if __name__ == "__main__":
    main()
