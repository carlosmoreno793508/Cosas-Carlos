#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cruza la verificacion GRATIS de ZoomInfo (search_companies) contra la Tanda 1
de Fase 2. Agrega pais/estado/tamano/companyId y marca discrepancias de nombre."""
import csv, os, re, sys, difflib
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INV  = os.path.join(BASE, "02-Investigacion")
TSV  = sys.argv[1]

zi = {}
for l in open(TSV, encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) < 7: continue
    d = re.sub(r"^www\.", "", p[0].lower())
    zi[d] = dict(zi_nombre=p[1], pais=p[2], estado=p[3], ciudad=p[4],
                 empleados=p[5], zi_company_id=p[6])

def clave(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())

filas, hallado = [], 0
for r in csv.DictReader(open(os.path.join(INV, "Tsunami_Fase2_Tanda1.csv"), encoding="utf-8")):
    d = re.sub(r"^www\.", "", r["dominio"].lower())
    m = zi.get(d)
    r = dict(r)
    if m:
        hallado += 1
        r.update(m)
        a, b = clave(r["Nombre"]), clave(m["zi_nombre"])
        sim = difflib.SequenceMatcher(None, a, b).ratio()
        if a in b or b in a or sim > 0.72:
            r["match_entidad"] = "OK"
        else:
            r["match_entidad"] = "REVISAR - el nombre del CRM no coincide con la entidad del dominio"
        r["verificado"] = "SI"
    else:
        r["verificado"] = "NO - ZoomInfo no devolvio la empresa para ese dominio"
        r["match_entidad"] = ""
    filas.append(r)

COLS = ["tanda","Clave","Nombre","zi_nombre","match_entidad","verificado","tipo_final",
        "confianza_tipo","dominio","pais","estado","ciudad","empleados","zi_company_id",
        "presencia_mx","estado_mx","Notas"]
out = os.path.join(INV, "Tsunami_Fase2_Tanda1_VERIFICADA.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
    w.writeheader(); w.writerows(filas)

print("Tanda 1:", len(filas), "filas |", hallado, "verificadas gratis en ZoomInfo")
print()
print("PAIS REAL (el CRM no traia pais):")
for k, v in Counter(r.get("pais","") for r in filas if r["verificado"]=="SI").most_common():
    print("   %-22s %3d" % (k or "(sin dato)", v))
print()
mx = [r for r in filas if r.get("pais") == "Mexico"]
print("Planta en Mexico detectada por ZoomInfo:", len(mx))
for r in mx:
    print("   -", r["Nombre"], "->", r["zi_nombre"], "|", r["estado"], r["ciudad"],
          "|", r["empleados"], "empl. | marcada MX en CRM:", r["presencia_mx"] or "NO")
print()
rev = [r for r in filas if r["match_entidad"].startswith("REVISAR")]
print("Entidad que NO coincide con el nombre del CRM:", len(rev))
for r in rev[:20]:
    print("   - CRM '%s'  ->  ZoomInfo '%s'  (%s)" % (r["Nombre"], r["zi_nombre"], r.get("pais")))
print()
nf = [r for r in filas if r["verificado"].startswith("NO")]
print("Sin resultado en ZoomInfo:", len(nf), "->", ", ".join(sorted({r["dominio"] for r in nf})))
