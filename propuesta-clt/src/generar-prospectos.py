# Genera el Excel interno de prospectos a partir de src/prospectos.json
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

d = json.load(open("src/prospectos.json", encoding="utf-8"))
ZONA = ["Estado de México y CDMX", "Jalisco", "Puebla y Tlaxcala", "Guanajuato", "Nuevo León", "Yucatán", "Querétaro", "La Laguna", "Aguascalientes"]
def zkey(z):
    for i, n in enumerate(ZONA):
        if n.split()[0].lower() in z.lower(): return i
    return 99
INK, PINK = "1B1F3B", "FCE4EC"
head = Font(bold=True, color="FFFFFF"); fill = PatternFill("solid", fgColor=INK)
wrap = Alignment(wrap_text=True, vertical="top")

wb = Workbook(); ws = wb.active; ws.title = "Prospectos"
cols = ["Prioridad", "Zona", "Empresa", "Ciudad", "Tipo", "Por qué es prospecto", "Sitio web", "Contacto publicado", "Fuente", "Estatus", "Responsable", "Próximo paso", "Notas"]
widths = [10, 22, 28, 24, 24, 60, 32, 24, 32, 16, 16, 24, 30]
ws.append(cols)
rows = sorted(d["prospects"], key=lambda p: ({"A": 0, "B": 1, "C": 2}.get(p["priority"], 3), zkey(p["zone"]), p["company"]))
for p in rows:
    ws.append([p["priority"], p["zone"], p["company"], p["city"], p["type"], p["why"], p["website"], p["phone_or_email"], p["source"], "Por contactar", "", "", ""])
for i, w in enumerate(widths, 1):
    ws.column_dimensions[ws.cell(1, i).column_letter].width = w
for c in ws[1]: c.font, c.fill = head, fill
for r in ws.iter_rows(min_row=2):
    for c in r: c.alignment = wrap
    if r[0].value == "A":
        for c in r[:9]: c.fill = PatternFill("solid", fgColor=PINK)
ws.freeze_panes = "D2"; ws.auto_filter.ref = ws.dimensions
dv = DataValidation(type="list", formula1='"Por contactar,Contactado,Visita agendada,Demo,Cotización,Ganado,Perdido"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"J2:J{ws.max_row}")

ws2 = wb.create_sheet("Resumen por zona")
ws2.append(["Zona", "Total", "A", "B", "C"])
zs = {}
for p in d["prospects"]:
    z = zs.setdefault(p["zone"], {"A": 0, "B": 0, "C": 0}); z[p["priority"]] = z.get(p["priority"], 0) + 1
for z in sorted(zs, key=zkey):
    v = zs[z]; ws2.append([z, sum(v.values()), v["A"], v["B"], v["C"]])
n = ws2.max_row
ws2.append(["Total", f"=SUM(B2:B{n})", f"=SUM(C2:C{n})", f"=SUM(D2:D{n})", f"=SUM(E2:E{n})"])
for c in ws2[1]: c.font, c.fill = head, fill
for c in ws2[ws2.max_row]: c.font = Font(bold=True)
ws2.column_dimensions["A"].width = 30

ws3 = wb.create_sheet("Competidores")
ws3.append(["Empresa", "Ciudad", "Qué vende", "Fuente"])
for c in d["competitors_seen"]: ws3.append([c["company"], c["city"], c["what"], c["source"]])
for c in ws3[1]: c.font, c.fill = head, fill
for col, w in zip("ABCD", [28, 20, 60, 40]): ws3.column_dimensions[col].width = w
for r in ws3.iter_rows(min_row=2):
    for c in r: c.alignment = wrap

ws4 = wb.create_sheet("Notas")
ws4.append(["Notas y advertencias"]); ws4["A1"].font = Font(bold=True)
for t in d.get("notes", []) + [
    "Prioridad A: estampado en volumen confirmado o fuerte; B: buen perfil; C: posible.",
    "Solo ADN Serigrafía y KW Puebla confirman pulpos automáticos en su propio sitio; el resto debe validarse por llamada.",
    "Uso interno de TID / VSP / CEB: no compartir con CLT.",
]:
    ws4.append([t])
ws4.column_dimensions["A"].width = 120
for r in ws4.iter_rows(min_row=2):
    for c in r: c.alignment = Alignment(wrap_text=True)

wb.save(sys.argv[1]); print("ok", sys.argv[1], len(rows))
