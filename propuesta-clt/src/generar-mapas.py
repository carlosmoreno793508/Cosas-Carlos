# Mapas de prospectos (México + Centroamérica y Caribe): uno de OEM y otro de estampadores/fabricantes.
# Estrella dorada numerada = cuenta 80/20 (México) o prioridad A (Centroamérica y Caribe); estrella chica = resto.
# Uso: python3 src/generar-mapas.py <carpeta_salida>
# Fuente de mapas: Natural Earth (dominio público). Coordenadas aproximadas a nivel ciudad.
import json, math, os, subprocess, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SRC = os.path.dirname(os.path.abspath(__file__))
INK, MAG, CYAN, GOLD, GREY = "#1B1F3B", "#C2185B", "#0089C2", "#F2B705", "#7A8299"
LAND, LAND_MX, SEA = "#EEF2F7", "#E1E7F0", "#FFFFFF"

# Coordenadas por ciudad (lat, lon); la llave se busca como subcadena del campo "city"
CITY = [
    ("Acajete", 19.10, -97.95), ("Aguascalientes", 21.88, -102.29), ("Atizapán", 19.56, -99.25), ("Baca", 21.11, -89.40),
    ("Celaya", 20.52, -100.81), ("Contla", 19.33, -98.17), ("Ensenada", 31.87, -116.60), ("Zapopan", 20.72, -103.39),
    ("Zapotlanejo", 20.62, -103.07), ("Guadalajara", 20.67, -103.35), ("Guadalupe, N.L.", 25.68, -100.26), ("Gómez Palacio", 25.57, -103.50),
    ("Irapuato", 20.68, -101.35), ("Purísima", 21.04, -101.88), ("León", 21.12, -101.68), ("Linares", 24.86, -99.57),
    ("Monterrey", 25.69, -100.32), ("Moroleón", 20.13, -101.19), ("Motul", 21.10, -89.28), ("Mérida", 20.97, -89.62),
    ("Naucalpan", 19.48, -99.24), ("Nazareno", 25.53, -103.52), ("San Andrés Cholula", 19.05, -98.30), ("San Pedro Cholula", 19.06, -98.30),
    ("Santa Isabel Cholula", 18.99, -98.37), ("Zacatepec", 19.10, -98.38), ("Tepanco", 18.55, -97.57), ("Puebla", 19.04, -98.21),
    ("Querétaro", 20.59, -100.39), ("Reynosa", 26.09, -98.28), ("San Bartolo Morelos", 19.78, -99.67), ("Tecate", 32.57, -116.63),
    ("Tijuana", 32.51, -117.04), ("Tlalnepantla", 19.54, -99.19), ("Tlaxcala", 19.32, -98.24), ("Toluca", 19.29, -99.66),
    ("Torreón", 25.54, -103.41), ("Tulancingo", 20.08, -98.37), ("Xalapa", 19.54, -96.91), ("Ciudad de México", 19.43, -99.13),
    ("Yucatán", 20.97, -89.62),
    ("San José", 9.93, -84.08), ("Costa Rica", 9.93, -84.08), ("Antiguo Cuscatlán", 13.67, -89.25), ("Apopa", 13.81, -89.18),
    ("Chalchuapa", 13.98, -89.68), ("Ciudad Arce", 13.84, -89.45), ("Ilopango", 13.70, -89.11), ("Lourdes Colón", 13.72, -89.37),
    ("Olocuilta", 13.57, -89.12), ("San Juan Opico", 13.88, -89.36), ("San Marcos", 13.66, -89.18), ("Soyapango", 13.71, -89.14),
    ("El Salvador", 13.69, -89.22), ("Mixco", 14.63, -90.61), ("Quetzaltenango", 14.84, -91.52), ("Guatemala", 14.63, -90.51),
    ("Caracol", 19.69, -72.02), ("Croix-des-Bouquets", 18.58, -72.23), ("Ouanaminthe", 19.55, -71.72), ("Port-au-Prince", 18.54, -72.34),
    ("Choloma", 15.61, -87.95), ("Naco", 15.33, -88.40), ("San Pedro Sula", 15.50, -88.03), ("Villanueva", 15.32, -88.00),
    ("Kingston", 17.97, -76.79), ("Managua", 12.13, -86.25), ("Panamá", 8.98, -79.52), ("Caguas", 18.23, -66.04),
    ("Guaynabo", 18.36, -66.11), ("Puerto Rico", 18.40, -66.06), ("Barahona", 18.21, -71.10), ("Moca", 19.39, -70.52),
    ("Navarrete", 19.56, -70.87), ("San Cristóbal", 18.42, -70.11), ("Villa González", 19.53, -70.79), ("Santo Domingo", 18.49, -69.93),
    ("Santiago", 19.45, -70.70),
]

# Sudamérica (se busca primero cuando el país es sudamericano; evita confundir Santiago de Chile con Santiago, R. D.)
SA_CITY = [
    ("Lima", -12.05, -77.04), ("Chincha", -13.42, -76.13), ("Envigado", 6.17, -75.59), ("Yumbo", 3.58, -76.49),
    ("Bello", 6.34, -75.56), ("Itagüí", 6.17, -75.61), ("Medellín", 6.25, -75.56), ("Tebaida", 4.45, -75.79),
    ("Bogotá", 4.71, -74.07), ("Barranquilla", 10.96, -74.80), ("Dosquebradas", 4.84, -75.67), ("Antioquia", 6.25, -75.56),
    ("Cuenca", -2.90, -79.00), ("Guayaquil", -2.19, -79.89), ("Santiago", -33.45, -70.67), ("Blumenau", -26.92, -49.07),
    ("Luján", -34.57, -59.11), ("Villa Lynch", -34.58, -58.53), ("San Martín", -34.58, -58.54), ("Buenos Aires", -34.60, -58.38),
]
SA = {"Perú", "Colombia", "Ecuador", "Chile", "Argentina", "Brasil"}

def locate(city, country=None):
    if country in SA:
        for k, la, lo in SA_CITY:
            if k.lower() in city.lower():
                return la, lo
        raise KeyError(city)
    for k, la, lo in CITY:
        if k.lower() in city.lower():
            return la, lo
    raise KeyError(city)

def node(mod):
    return json.loads(subprocess.check_output(["node", "-e", f"console.log(JSON.stringify(require('{SRC}/{mod}')))"]))

mx = json.load(open(f"{SRC}/prospectos.json", encoding="utf-8"))["prospects"]
la = [x for f in ["latam_centroamerica", "latam_caribe"] for x in json.load(open(f"{SRC}/{f}.json", encoding="utf-8"))["prospects"]]
sa = json.load(open(f"{SRC}/latam_sudamerica.json", encoding="utf-8"))["prospects"]
top = node("top8020")
top_p = [r[0] for r in top["prospects"]]
top_o = [r[0] for r in top["oems"]]

def is_top(company, names):
    key = company.lower()
    for n in names:
        base = n.split(" (")[0].lower()
        if key.startswith(base) or base.startswith(key.split(" (")[0].split(",")[0]):
            return n
    return None

def draw_geo(ax, extent):
    for path, color in [(f"{SRC}/geo/paises.geojson", LAND), (f"{SRC}/geo/mexico_estados.geojson", LAND_MX)]:
        for f in json.load(open(path))["features"]:
            g = f["geometry"]
            polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
            for poly in polys:
                ax.add_patch(Polygon(poly[0], closed=True, facecolor=color, edgecolor="#B8C2D1", linewidth=0.4, zorder=1))
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3])
    ax.set_facecolor(SEA); ax.set_aspect(1 / math.cos(math.radians((extent[2] + extent[3]) / 2)))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_edgecolor("#C9D1DC")

def spread(points):
    """Separa estrellas que caen en la misma ciudad (pequeño círculo alrededor del punto)."""
    groups = {}
    for p in points: groups.setdefault((round(p["lat"], 2), round(p["lon"], 2)), []).append(p)
    for (lat, lon), g in groups.items():
        if len(g) == 1: continue
        r = (0.35 if any(p["top"] for p in g) else 0.22) + 0.05 * len(g)
        tops = [p for p in g if p["top"]] + [p for p in g if not p["top"]]
        for i, p in enumerate(tops):
            a = 2 * math.pi * i / len(g) + 0.4
            p["lat"], p["lon"], p["ang"] = lat + r * math.sin(a), lon + r * math.cos(a), a
    return points

def build(kind):
    oem = kind == "oem"
    title = "Prospectos OEM — maquila de exportación" if oem else "Prospectos estampadores y fabricantes"
    sel_mx = [x for x in mx if (x.get("segment") == "OEM") == oem]
    sel_la = [x for x in la if (x.get("segment") == "OEM") == oem]
    names = top_o if oem else top_p
    pts, key, n = [], [], 0
    for x in sorted(sel_mx, key=lambda x: x["company"]):
        lat, lon = locate(x["city"])
        t = is_top(x["company"], names)
        if t:
            n += 1; key.append(("MX", n, t, x["city"]))
        pts.append({"lat": lat, "lon": lon, "top": bool(t), "num": n if t else None, "mx": True})
    nla = 0
    for x in sorted(sel_la, key=lambda x: (x["country"], x["company"])):
        lat, lon = locate(x["city"])
        top_a = x["priority"] == "A"
        if top_a:
            nla += 1; key.append(("LA", nla, x["company"].split(" (")[0].replace(", S.A. de C.V.", "").replace(" S.A.", "").replace(", S.A.", ""), f'{x["city"].split(",")[0].split(" (")[0]}, {x["country"].replace("República Dominicana", "Rep. Dominicana")}' + (" — cerró 2024" if "Hanes Ink" in x["company"] else "")))
        pts.append({"lat": lat, "lon": lon, "top": top_a, "num": nla if top_a else None, "mx": False})
    spread(pts)

    fig = plt.figure(figsize=(16, 10.2), dpi=150, facecolor="white")
    fig.text(0.03, 0.955, title, fontsize=22, fontweight="bold", color=INK)
    fig.text(0.03, 0.925, f"México: {len(sel_mx)} empresas ({sum(1 for k in key if k[0]=='MX')} del 80/20)   ·   Centroamérica y Caribe: {len(sel_la)} empresas ({nla} de prioridad A)",
             fontsize=12, color=GREY)
    axm = fig.add_axes([0.02, 0.33, 0.55, 0.54]); draw_geo(axm, (-118.5, -86, 14, 34))
    axc = fig.add_axes([0.58, 0.33, 0.40, 0.54]); draw_geo(axc, (-93, -64, 7.5, 21.5))
    axm.set_title("México", loc="left", fontsize=13, fontweight="bold", color=INK)
    axc.set_title("Centroamérica y Caribe", loc="left", fontsize=13, fontweight="bold", color=INK)
    for ax, mxflag in [(axm, True), (axc, False)]:
        for p in pts:
            if p["mx"] != mxflag: continue
            if p["top"]:
                ax.plot(p["lon"], p["lat"], marker="*", markersize=20, color=GOLD, markeredgecolor=INK, markeredgewidth=0.8, zorder=5)
                a = p.get("ang", 0.6)
                ax.annotate(str(p["num"]), (p["lon"], p["lat"]), xytext=(13 * math.cos(a), 11 * math.sin(a)), ha="center", va="center", textcoords="offset points", fontsize=9, fontweight="bold",
                            color=INK, zorder=6, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=INK, lw=0.5))
            else:
                ax.plot(p["lon"], p["lat"], marker="*", markersize=9, color=MAG if oem else CYAN, markeredgecolor="white", markeredgewidth=0.4, zorder=4)
    leg = [Line2D([], [], marker="*", ls="", markersize=16, color=GOLD, markeredgecolor=INK, label="Cuenta 80/20 (México) o prioridad A (Centroamérica y Caribe)"),
           Line2D([], [], marker="*", ls="", markersize=10, color=MAG if oem else CYAN, label="Otros prospectos")]
    axm.legend(handles=leg, loc="lower left", fontsize=9, frameon=True, framealpha=0.95)
    # Claves numeradas
    kx = [k for k in key if k[0] == "MX"]; kl = [k for k in key if k[0] == "LA"]
    fig.text(0.03, 0.295, "México — cuentas 80/20", fontsize=12, fontweight="bold", color=MAG)
    for i, (_, num, name, city) in enumerate(kx):
        fig.text(0.03, 0.27 - i * 0.024, f"{num}. {name} — {city}", fontsize=9.5, color=INK)
    fig.text(0.44, 0.295, "Centroamérica y Caribe — prioridad A", fontsize=12, fontweight="bold", color=MAG)
    cols = 2; per = math.ceil(len(kl) / cols) if kl else 0
    for i, (_, num, name, city) in enumerate(kl):
        c, r = divmod(i, per) if per else (0, i)
        fig.text(0.44 + c * 0.27, 0.27 - r * 0.024, f"{num}. {name[:28].rstrip(', .')} — {city}", fontsize=9, color=INK)
    fig.text(0.03, 0.015, "Fuente: estudio de prospectos TID · VSP · CEB (oct. 2026). Ubicación aproximada por ciudad. Mapa base: Natural Earth.", fontsize=8.5, color=GREY)
    f = os.path.join(OUT, f"Mapa_Prospectos_{'OEM' if oem else 'Estampadores_Fabricantes'}.png")
    fig.savefig(f, dpi=150); plt.close(fig)
    print("ok", f, len(sel_mx), len(sel_la), len(kx), len(kl))

def build_latam(kind):
    """Escenario LATAM completo: México + Centroamérica y Caribe + Sudamérica en un solo mapa por tipo."""
    oem = kind == "oem"
    title = ("Escenario LATAM — prospectos OEM (maquila de exportación)" if oem else "Escenario LATAM — prospectos estampadores y fabricantes")
    color = MAG if oem else CYAN
    names = top_o if oem else top_p
    regions = [
        ("México", [x for x in mx if (x.get("segment") == "OEM") == oem], "80/20"),
        ("Centroamérica y Caribe", [x for x in la if (x.get("segment") == "OEM") == oem], "A"),
        ("Sudamérica", [x for x in sa if (x.get("segment") == "OEM") == oem], "A"),
    ]
    pts, keys = [], {}
    for reg, items, mode in regions:
        keys[reg] = []
        for x in sorted(items, key=lambda x: (x.get("country", ""), x["company"])):
            lat, lon = locate(x["city"], x.get("country"))
            if mode == "80/20":
                t = is_top(x["company"], names); label = t; place = x["city"]
            else:
                t = x["priority"] == "A"; label = x["company"].split(" (")[0]
                place = f'{x["city"].split(",")[0].split(" (")[0]}, {x["country"].replace("República Dominicana", "Rep. Dominicana")}'
                if "Hanes Ink" in x["company"]: place += " — cerró 2024"
            num = None
            if t:
                keys[reg].append((len(keys[reg]) + 1, label, place)); num = len(keys[reg])
            pts.append({"lat": lat, "lon": lon, "top": bool(t), "num": num, "reg": reg})
    spread(pts)
    counts = {reg: len(items) for reg, items, _ in regions}

    fig = plt.figure(figsize=(18, 14), dpi=140, facecolor="white")
    fig.text(0.03, 0.965, title, fontsize=22, fontweight="bold", color=INK)
    fig.text(0.03, 0.942, f"{sum(counts.values())} empresas en {len(regions)} regiones  ·  México {counts['México']} ({len(keys['México'])} del 80/20)  ·  "
             f"Centroamérica y Caribe {counts['Centroamérica y Caribe']} ({len(keys['Centroamérica y Caribe'])} prioridad A)  ·  "
             f"Sudamérica {counts['Sudamérica']} ({len(keys['Sudamérica'])} prioridad A)", fontsize=12, color=GREY)
    panels = [
        ("México", (-118.5, -86, 14, 34), [0.02, 0.60, 0.50, 0.32]),
        ("Centroamérica y Caribe", (-93, -64, 7.5, 21.5), [0.02, 0.30, 0.50, 0.27]),
        ("Sudamérica", (-84, -34, -42, 13), [0.54, 0.30, 0.44, 0.62]),
    ]
    for reg, ext, rect in panels:
        ax = fig.add_axes(rect); draw_geo(ax, ext)
        n = counts[reg]
        ax.set_title(f"{reg} — {n} empresas", loc="left", fontsize=13, fontweight="bold", color=INK)
        for p in pts:
            if p["reg"] != reg: continue
            if p["top"]:
                ax.plot(p["lon"], p["lat"], marker="*", markersize=18, color=GOLD, markeredgecolor=INK, markeredgewidth=0.8, zorder=5)
                a = p.get("ang", 0.6)
                ax.annotate(str(p["num"]), (p["lon"], p["lat"]), xytext=(12 * math.cos(a), 10 * math.sin(a)), textcoords="offset points",
                            ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK, zorder=6,
                            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=INK, lw=0.5))
            else:
                ax.plot(p["lon"], p["lat"], marker="*", markersize=8, color=color, markeredgecolor="white", markeredgewidth=0.4, zorder=4)
        if reg == "Sudamérica":
            leg = [Line2D([], [], marker="*", ls="", markersize=15, color=GOLD, markeredgecolor=INK, label="80/20 (México) o prioridad A (resto de LATAM)"),
                   Line2D([], [], marker="*", ls="", markersize=10, color=color, label="Otros prospectos")]
            ax.legend(handles=leg, loc="lower right", fontsize=9, frameon=True, framealpha=0.95)
    heads = [("México — 80/20", "México"), ("Centroamérica y Caribe — prioridad A", "Centroamérica y Caribe"), ("Sudamérica — prioridad A", "Sudamérica")]
    for i, (h, reg) in enumerate(heads):
        x0 = 0.03 + i * 0.32
        fig.text(x0, 0.265, h, fontsize=12, fontweight="bold", color=MAG)
        for j, (num, name, place) in enumerate(keys[reg]):
            fig.text(x0, 0.243 - j * 0.0165, f"{num}. {name[:30].rstrip(', .')} — {place[:34]}", fontsize=8.8, color=INK)
    fig.text(0.03, 0.012, "Fuente: estudio de prospectos TID · VSP · CEB (oct. 2026). Ubicación aproximada por ciudad. Mapa base: Natural Earth.", fontsize=8.5, color=GREY)
    f = os.path.join(OUT, f"Mapa_LATAM_{'OEM' if oem else 'Estampadores_Fabricantes'}.png")
    fig.savefig(f, dpi=140); plt.close(fig)
    print("ok", f, counts, {k: len(v) for k, v in keys.items()})

for k in ("oem", "fab"):
    build(k)
    build_latam(k)
