#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arma las tandas de 150 de la Fase 2 de Tsunami.

Criterio de orden (por que importa): el rebote de SIIX y el falso positivo de
Selex (selex.com = Selex Electricals, Dubai; NO Selex ES de Leonardo) muestran
que sin dominio no se puede verificar que la entidad de ZoomInfo sea la correcta.
Comprar un contacto de la entidad equivocada quema el credito Y la reputacion
del dominio de envio. Por eso: primero los que traen dominio completo.
"""
import csv, os, re, unicodedata
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INV  = os.path.join(BASE, "02-Investigacion")

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def leer(p):
    with open(p, encoding="utf-8-sig") as f: return list(csv.DictReader(f))

crm = leer(os.path.join(INV, "Tsunami_Prospectos_CLASIFICADO.csv"))

ya = set()
for f, c in [("Tsunami_Top100_ENRIQUECIDO.csv", "Nombre"),
             ("Tsunami_MX_Hueco_ENRIQUECIDO.csv", "Nombre_CRM")]:
    for r in leer(os.path.join(INV, f)): ya.add(norm(r[c]))

# presencia MX conocida -> prioridad, segun la vista mexicana ya construida
mx = {}
for r in leer(os.path.join(INV, "Tsunami_x_Mexico.csv")):
    if (r.get("presencia_mx") or "").strip().upper() in ("SI", "SÍ"):
        mx[norm(r["Nombre_CRM"])] = r.get("estado_mx", "")

def dominio(u):
    u = (u or "").strip()
    if not u or u.endswith("..."): return ""
    u = re.sub(r"^https?://", "", u).split("/")[0]
    return u if "." in u else ""

objetivo = []
for r in crm:
    if r["tipo_final"] not in ("OEM", "EMS/CM"): continue
    if r["no_contactar"] == "SI": continue
    n = norm(r["Nombre"])
    if n in ya or r["email_contacto"].strip(): continue
    d = dominio(r["URL"])
    objetivo.append({
        "Clave": r["Clave"], "Nombre": r["Nombre"], "tipo_final": r["tipo_final"],
        "confianza_tipo": r["confianza_tipo"], "dominio": d,
        "URL_cruda": r["URL"], "presencia_mx": "SI" if n in mx else "",
        "estado_mx": mx.get(n, ""), "Notas": (r["Notas"] or "")[:160],
        "listo_para_comprar": "SI" if d else "NO - URL truncada, re-exportar CRM primero",
    })

# orden: dominio primero, luego MX, luego confianza Alta, luego nombre
objetivo.sort(key=lambda r: (0 if r["dominio"] else 1,
                            0 if r["presencia_mx"] else 1,
                            0 if r["confianza_tipo"] == "Alta" else 1,
                            r["Nombre"]))

COLS = ["tanda","Clave","Nombre","tipo_final","confianza_tipo","dominio","URL_cruda",
        "presencia_mx","estado_mx","listo_para_comprar","Notas"]
for i, r in enumerate(objetivo):
    r["tanda"] = i // 150 + 1

for t in range(1, (len(objetivo) - 1) // 150 + 2):
    filas = [r for r in objetivo if r["tanda"] == t]
    p = os.path.join(INV, "Tsunami_Fase2_Tanda%d.csv" % t)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader(); w.writerows(filas)
    listos = sum(1 for r in filas if r["dominio"])
    print("Tanda %d: %3d cuentas | %3d con dominio verificable | %3d con planta MX"
          % (t, len(filas), listos, sum(1 for r in filas if r["presencia_mx"])))

print()
print("TOTAL Fase 2:", len(objetivo))
print("  con dominio (comprables con verificacion):",
      sum(1 for r in objetivo if r["dominio"]))
print("  sin dominio (esperar re-export del CRM)  :",
      sum(1 for r in objetivo if not r["dominio"]))
# lista de dominios de la tanda 1 para la verificacion gratis
d1 = [r["dominio"] for r in objetivo if r["tanda"] == 1 and r["dominio"]]
with open(os.path.join(INV, "_fase2_tanda1_dominios.txt"), "w") as f:
    f.write("\n".join(d1))
print("\nDominios tanda 1 escritos:", len(d1))
