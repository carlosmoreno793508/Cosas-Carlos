#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segunda pasada GRATIS sobre los 3,262 'Otro/Por clasificar' del CRM Tsunami.
Solo usa senal ya presente en el archivo (Notas / Nombre). No consulta APIs.
Respeta R6: si no hay senal, no se adivina; se manda a una cubeta de revision.
"""
import csv, os, re
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INV  = os.path.join(BASE, "02-Investigacion")
SRC  = os.path.join(INV, "Tsunami_Prospectos_CLASIFICADO.csv")

with open(SRC, encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f)); COLS = list(rows[0].keys())

def m(pat, t): return re.search(pat, t, re.I)

# (regex sobre Notas, tipo_final, metodo). Orden = prioridad.
REGLAS_NOTAS = [
    (r"\bdo not (call|use|email)\b|\bdnu\b|\bblacklist",      None,            "nota: prohibicion explicita -> no_contactar"),
    (r"out of business|no longer|closed|ceased|bankrupt|liquidat", "DUP/Inactivo", "nota: empresa cerrada/inactiva"),
    (r"sales office\s*[-–]\s*no purchasing|no purchasing (here|at)", "Sin compras", "nota: oficina de ventas, no compra"),
    (r"government agency|\bnasa\b|air force|\bus army\b|\bnavy\b|department of defense",
                                                              "Gobierno/Institucional", "nota: agencia de gobierno"),
    (r"universit|\bcollege\b|research institute|laborator(y|io) nacional",
                                                              "Gobierno/Institucional", "nota: academia/instituto"),
    (r"contract manufactur|\bems\b|pcb assembl|pcba|turnkey assembl|box build",
                                                              "EMS/CM",        "nota: manufactura por contrato"),
    (r"distribut|reseller|stocking|franchise line|broker",     "Broker/Trader", "nota: distribucion/reventa"),
    (r"\boem\b|manufactures its own|own product|builds (its|their) own",
                                                              "OEM",           "nota: fabricante de producto propio"),
]
# Estos NO reclasifican: marcan para revision humana (R6).
REGLAS_REVISION = [
    (r"\bsee\b\s+[A-Z]|\buse\b\s+[A-Z]{2,}|apunta a|remite a", "posible duplicado: la nota remite a otro registro"),
    (r"acquired|acquisition|merged|now part of|subsidiary of|renamed|formerly",
                                                               "cambio corporativo: verificar si la planta sigue comprando"),
]

nuevos, revision, sin_senal = [], [], 0
for r in rows:
    if r["tipo_final"] != "Otro/Por clasificar":
        continue
    notas = (r["Notas"] or "").strip()
    if not notas:
        sin_senal += 1; continue
    hecho = False
    for pat, tipo, metodo in REGLAS_NOTAS:
        if m(pat, notas):
            n = dict(r)
            if tipo is None:
                n["no_contactar"] = "SI"; n["motivo_no_contactar"] = "prohibicion explicita en notas del CRM"
            else:
                n["tipo_final"] = tipo
            n["metodo_clasificacion"] = metodo
            n["confianza_tipo"] = "Media"
            nuevos.append(n); hecho = True; break
    if hecho: continue
    for pat, motivo in REGLAS_REVISION:
        if m(pat, notas):
            n = dict(r); n["metodo_clasificacion"] = motivo
            revision.append(n); hecho = True; break
    if not hecho:
        sin_senal += 1

def esc(p, rows_, cols):
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows_)

esc(os.path.join(INV, "Tsunami_Pendientes_RECLASIFICADOS.csv"), nuevos, COLS)
esc(os.path.join(INV, "Tsunami_Pendientes_REVISION_HUMANA.csv"), revision, COLS)

print("De los 3,262 pendientes:")
print("  reclasificados con senal del propio archivo :", len(nuevos))
for k, v in Counter(x["metodo_clasificacion"] for x in nuevos).most_common():
    print("      %-52s %4d" % (k, v))
print("  marcados para revision humana               :", len(revision))
for k, v in Counter(x["metodo_clasificacion"] for x in revision).most_common():
    print("      %-52s %4d" % (k, v))
print("  siguen sin senal suficiente (R6)            :", sin_senal)
