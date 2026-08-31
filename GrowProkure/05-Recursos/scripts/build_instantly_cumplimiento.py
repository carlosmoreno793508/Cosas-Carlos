#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arma los CSV de Instantly aplicando los filtros de cumplimiento de
04-GoToMarket/ESTADO-ENRIQUECIMIENTO.md y las reglas R2/R3/R9 de REGLAS.md.

No envia nada. Solo escribe archivos y una hoja de auditoria con el motivo
de cada exclusion.
"""
import csv, os, re, unicodedata
from collections import Counter, OrderedDict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INV  = os.path.join(BASE, "02-Investigacion")
GTM  = os.path.join(BASE, "04-GoToMarket")

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def leer(p):
    with open(p, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

# ---------- listas de bloqueo ----------
riesgo = leer(os.path.join(INV, "Estudios_Correos_En_Riesgo.csv"))
BLOQUEO_ALTA = {r["email"].strip().lower() for r in riesgo if r["severidad"] == "ALTA"}
RIESGO_MEDIA = {r["email"].strip().lower() for r in riesgo if r["severidad"] == "MEDIA"}
# los "(inferido)" traen sufijo: guardamos tambien la parte antes del parentesis
BLOQUEO_ALTA |= {e.split("(")[0].strip() for e in list(BLOQUEO_ALTA) if "(" in e}
RIESGO_MEDIA |= {e.split("(")[0].strip() for e in list(RIESGO_MEDIA) if "(" in e}

crm = leer(os.path.join(INV, "Tsunami_Prospectos_CLASIFICADO.csv"))
NO_CONTACTAR = {norm(r["Nombre"]) for r in crm if r["no_contactar"] == "SI"}
MOTIVO_NC    = {norm(r["Nombre"]): r["motivo_no_contactar"] for r in crm if r["no_contactar"] == "SI"}
DUP_INACTIVO = {norm(r["Nombre"]) for r in crm if r["tipo_final"] == "DUP/Inactivo"}

GRATUITOS = {"gmail.com","outlook.com","outlook.es","hotmail.com","hotmail.es","hotmail.com.mx",
             "yahoo.com","yahoo.com.mx","live.com","prodigy.net.mx","icloud.com","aol.com"}
GENERICOS = {"info","ventas","compras","contacto","sales","admin","purchasing","procurement",
             "contact","hello","marketing","rh","recursoshumanos","atencion"}
EDUCATIVO = re.compile(r"\.(edu|edu\.mx|ac\.[a-z]{2})$")

RE_EMAIL = re.compile(r"^[^@\s,;()<>]+@[^@\s,;()<>]+\.[a-z]{2,}$", re.I)

def evaluar(email, empresa):
    """Devuelve (motivo_exclusion|None, bandera_riesgo)."""
    e = (email or "").strip().lower()
    emp = norm(empresa)
    if not e:
        return "sin email (R3)", ""
    if "(" in e or " " in e or "inferido" in e:
        return "email construido/inferido, no verificado (R3)", ""
    if not RE_EMAIL.match(e):
        return "email malformado (R3)", ""
    if e in BLOQUEO_ALTA:
        return "riesgo ALTA de rebote (filtro 3, R12)", ""
    dom  = e.split("@")[1]
    user = e.split("@")[0]
    if emp in NO_CONTACTAR:
        return "no_contactar=SI: %s (filtro 1, R9)" % MOTIVO_NC.get(emp, ""), ""
    if emp in DUP_INACTIVO:
        return "tipo_final=DUP/Inactivo (filtro 2)", ""
    if dom in GRATUITOS:
        return "dominio personal/gratuito, no corporativo (R9)", ""
    if EDUCATIVO.search(dom):
        return "dominio educativo, no es la empresa", ""
    if user in GENERICOS:
        return "buzon generico, no nominal (R3)", ""
    return None, ("MEDIA" if e in RIESGO_MEDIA else "")

# ---------- fuentes ----------
filas, excluidos = [], []
vistos = set()

def agregar(email, first, last, empresa, estado, pais, prioridad, arquetipo, idioma, fuente):
    motivo, riesgo_f = evaluar(email, empresa)
    reg = OrderedDict(email=(email or "").strip().lower(), first_name=first or "", last_name=last or "",
                      company_name=empresa or "", estado=estado or "", pais=pais or "",
                      prioridad=prioridad or "", arquetipo=arquetipo or "", idioma_copy=idioma or "",
                      riesgo=riesgo_f, fuente=fuente)
    if motivo:
        reg["motivo_exclusion"] = motivo
        excluidos.append(reg); return
    if reg["email"] in vistos:                      # R2
        reg["motivo_exclusion"] = "duplicado por email (R2)"
        excluidos.append(reg); return
    vistos.add(reg["email"]); filas.append(reg)

# 1) Astute (estudios propios, ya con prioridad/tier)
for r in leer(os.path.join(GTM, "Astute_Instantly_LISTO.csv")):
    agregar(r["email"], r["first_name"], r["last_name"], r["company_name"],
            r["estado"], "MX", r["prioridad"], "", "", "Astute_Instantly_LISTO")

# 2) Tsunami Top100 comprado
def partir(nombre):
    p = (nombre or "").strip().split()
    return (p[0] if p else "", " ".join(p[1:]) if len(p) > 1 else "")

for r in leer(os.path.join(INV, "Tsunami_Top100_ENRIQUECIDO.csv")):
    f, l = partir(r.get("comprador"))
    agregar(r.get("email"), f, l, r.get("Nombre"), "", r.get("region"),
            "2 - Decisor compras", r.get("tipo_final"), "", "Tsunami_Top100_ENRIQUECIDO")

# 3) Hueco Mexico comprado
for r in leer(os.path.join(INV, "Tsunami_MX_Hueco_ENRIQUECIDO.csv")):
    f, l = partir(r.get("comprador"))
    agregar(r.get("email"), f, l, r.get("Nombre_CRM"), r.get("estado_mx"), "MX",
            "2 - Decisor compras", r.get("tipo_final"), "ES", "Tsunami_MX_Hueco_ENRIQUECIDO")

# 4) CRM Tsunami: contactos que ya venian gratis en el CRM
for r in crm:
    if not (r.get("email_contacto") or "").strip():
        continue
    f, l = partir(r.get("contacto"))
    agregar(r["email_contacto"], f, l, r["Nombre"], "", "",
            "4 - Directorio ampliado", r.get("tipo_final"), "", "Tsunami_CRM_gratis")

# ---------- salidas ----------
COLS = ["email","first_name","last_name","company_name","estado","pais",
        "prioridad","arquetipo","idioma_copy","riesgo","fuente"]

def escribir(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

orden = {"1 - Clave electrónicos": 0, "2 - Decisor compras": 1,
         "3 - Comprador": 2, "4 - Directorio ampliado": 3}
filas.sort(key=lambda r: (orden.get(r["prioridad"], 9), r["company_name"]))

escribir(os.path.join(GTM, "Instantly_FILTRADO_COMPLETO.csv"), filas, COLS)

tanda1 = [r for r in filas if orden.get(r["prioridad"], 9) <= 1 and r["riesgo"] != "MEDIA"]
escribir(os.path.join(GTM, "Instantly_TANDA1_LIMPIA.csv"), tanda1, COLS)

escribir(os.path.join(GTM, "_Instantly_EXCLUIDOS_auditoria.csv"), excluidos,
         COLS + ["motivo_exclusion"])

print("ENVIABLES        :", len(filas))
print("  tanda 1 limpia :", len(tanda1))
print("  con riesgo MEDIA:", sum(1 for r in filas if r["riesgo"] == "MEDIA"))
print("EXCLUIDOS        :", len(excluidos))
for m, n in Counter(r["motivo_exclusion"].split(":")[0] for r in excluidos).most_common():
    print("   %-55s %4d" % (m, n))
print()
print("por fuente (enviables):")
for m, n in Counter(r["fuente"] for r in filas).most_common():
    print("   %-32s %4d" % (m, n))
