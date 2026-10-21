#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte el archivo enviable en tandas semanales listas para subir a Instantly.

Tres cosas que no se pueden dejar al criterio del momento:
  1. Excluir a quien YA recibio la secuencia (la tanda 1 de Astute, 28 jul).
     Repetir un ciclo de 4 correos a la misma persona quema la cuenta.
  2. Separar por idioma: ES / EN / PT necesitan campanas distintas en Instantly
     porque el copy es distinto.
  3. Respetar el ritmo: 7 buzones calentados. La rampa la define el rebote de
     la tanda anterior, no el tamano del archivo.
"""
import csv, os
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTM  = os.path.join(BASE, "04-GoToMarket")
OUT  = os.path.join(GTM, "tandas-envio")
os.makedirs(OUT, exist_ok=True)

def leer(p):
    with open(p, encoding="utf-8-sig") as f: return list(csv.DictReader(f))

# 1) quien ya recibio la secuencia
ya = {r["email"].strip().lower()
      for r in leer(os.path.join(GTM, "Astute_Tier1_Clave_Instantly.csv"))}

env = leer(os.path.join(GTM, "Instantly_FILTRADO_COMPLETO.csv"))
antes = len(env)
env = [r for r in env if r["email"] not in ya]
print("enviables            :", antes)
print("ya contactados (28 jul), excluidos:", antes - len(env))
print("disponibles          :", len(env))
print()

ORDEN = {"1 - Clave electrónicos":0, "2 - Decisor compras":1,
         "3 - Comprador":2, "4 - Directorio ampliado":3}
env.sort(key=lambda r: (ORDEN.get(r["prioridad"], 9), r["company_name"]))

# 2) por idioma (campanas distintas) y 3) en tandas de una semana
POR_SEMANA = 500          # 100/dia x 5 dias habiles = 20/buzon/dia con 7 buzones
COLS = ["email","first_name","last_name","company_name","estado","pais",
        "prioridad","arquetipo","idioma_copy","riesgo","fuente"]

por_idioma = defaultdict(list)
for r in env:
    por_idioma[r["idioma_copy"] or "SIN_IDIOMA"].append(r)

plan = []
for idioma, filas in sorted(por_idioma.items(), key=lambda kv: -len(kv[1])):
    for i in range(0, len(filas), POR_SEMANA):
        lote = filas[i:i+POR_SEMANA]
        n = i // POR_SEMANA + 1
        nom = "Astute_%s_S%d.csv" % (idioma, n)
        with open(os.path.join(OUT, nom), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
            w.writeheader(); w.writerows(lote)
        plan.append((idioma, n, nom, len(lote), Counter(x["prioridad"] for x in lote)))

print("%-8s %-28s %6s  %s" % ("IDIOMA","ARCHIVO","FILAS","REPARTO POR PRIORIDAD"))
for idioma, n, nom, cnt, pri in plan:
    top = ", ".join("%s:%d" % (k.split(" - ")[0], v) for k, v in sorted(pri.items()))
    print("%-8s %-28s %6d  %s" % (idioma, nom, cnt, top))
print()
print("semanas de envio a 500/semana:", len(plan))
print("total a enviar               :", sum(x[3] for x in plan))
