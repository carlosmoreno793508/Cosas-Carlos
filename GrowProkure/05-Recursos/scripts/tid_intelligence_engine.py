import openpyxl, re
from collections import defaultdict, Counter
U="/root/.claude/uploads/79b088b9-ecb6-5156-8b46-8be359f25fa8/"
SRC=U+"cf24ba7f-ContactosFoilTIDGLOBAL.xlsx"
OUT="05-Recursos/TID_Intelligence_Engine.xlsx"

def s(v): return str(v).strip() if v not in (None,"") else ""
def norm_email(e):
    e=str(e or "").strip().lower()
    if "@" not in e or " " in e or "." not in e.split("@")[-1]: return ""
    return e
def keyco(name):
    n=str(name or "").lower()
    n=re.sub(r'[^a-z0-9 ]',' ',n)
    n=re.sub(r'\b(s a de c v|sa de cv|s de rl de cv|s de rl|inc|corp|corporation|company|co|llc|ltd|de mexico|mexicana|mexico|group|grupo|the)\b',' ',n)
    return re.sub(r'\s+',' ',n).strip()

BAJIO={"queretaro","querétaro","guanajuato","san luis potosi","san luis potosí","aguascalientes","jalisco"}
def industry_fit(ind, seg):
    t=(ind+" "+seg).lower()
    if any(x in t for x in ("automotri","automotive","interior","cosmetic","cosmétic","medic","médic","farma","pharma")): return 20
    if any(x in t for x in ("electrodom","línea blanca","linea blanca","white","appliance","industrial")): return 18
    if any(x in t for x in ("grafic","gráfic","security","seguridad","packag","empaque","label")): return 12
    return 10

# ---- load verified (Agenda propia) ----
verified_emails=set(); verified_companies=set()
wb=openpyxl.load_workbook(SRC,read_only=True,data_only=True)
if "Agenda propia" in wb.sheetnames:
    ws=wb["Agenda propia"]; hdr=[str(c.value).strip().lower() if c.value else "" for c in ws[3]]
    def ci(n): return next((i for i,x in enumerate(hdr) if x==n or n in x),None)
    ei=ci("email"); epi=ci("empresa_actual") or ci("empresa_estudio")
    for r in ws.iter_rows(min_row=4,values_only=True):
        e=norm_email(r[ei]) if ei is not None and ei<len(r) else ""
        if e: verified_emails.add(e)
        if epi is not None and epi<len(r) and r[epi]: verified_companies.add(keyco(r[epi]))

# ---- load contacts (Prosp — Todos) ----
ws=wb["Prosp — Todos"]; hdr=[str(c.value).strip().lower() if c.value else "" for c in ws[3]]
def col(n): return next((i for i,x in enumerate(hdr) if x==n),None)
cols={k:col(k) for k in ["segmento","empresa","contacto","puesto","perfil","ciudad","estado","industria","linkedin","email","telefono","fuente","prioridad","confianza","notas"]}
def g(r,k):
    i=cols[k]; return s(r[i]) if (i is not None and i<len(r)) else ""

companies={}; comp_contacts=defaultdict(list); seen_email=set()
for r in ws.iter_rows(min_row=4,values_only=True):
    emp=g(r,"empresa"); nm=g(r,"contacto")
    if not emp and not nm: continue
    em=norm_email(g(r,"email"))
    if em and em in seen_email: continue
    if em: seen_email.add(em)
    k=keyco(emp)
    rec={"empresa":emp,"contacto":nm,"puesto":g(r,"puesto"),"perfil":g(r,"perfil"),
         "email":em,"tel":g(r,"telefono"),"ciudad":g(r,"ciudad"),"estado":g(r,"estado"),
         "industria":g(r,"industria"),"segmento":g(r,"segmento"),"prioridad":g(r,"prioridad"),
         "confianza":g(r,"confianza"),"linkedin":g(r,"linkedin"),"fuente":g(r,"fuente"),
         "verificado": em in verified_emails}
    comp_contacts[k].append(rec)
    if k not in companies:
        companies[k]={"key":k,"display":emp,"estado":g(r,"estado"),"ciudad":g(r,"ciudad"),
            "industria":g(r,"industria"),"segmento":g(r,"segmento"),"prioridad":g(r,"prioridad"),
            "confianza":g(r,"confianza")}
    else:
        c=companies[k]
        if len(emp)>len(c["display"]): c["display"]=emp
        for f in ["estado","ciudad","industria","segmento"]:
            if not c[f] and rec[f]: c[f]=rec[f]
        # keep highest priority
        if rec["prioridad"].lower()=="alta": c["prioridad"]="Alta"
wb.close()

def pri_rank(t):
    t=str(t or "").lower()
    if any(x in t for x in ("purchas","compra","sourc","procure","abasto","buyer","material")): return "A"
    if any(x in t for x in ("director","gerente","manager","chief","owner","dueñ","jefe")): return "B"
    if any(x in t for x in ("engineer","ingenier","calidad","quality","produc")): return "C"
    return "D"

rows=[]
for k,c in companies.items():
    lst=comp_contacts[k]
    best=None
    for pr in ["A","B","C","D"]:
        cand=[x for x in lst if pri_rank(x["puesto"])==pr and x["email"]]
        if cand:
            vc=[x for x in cand if x["verificado"]]
            best=(vc or cand)[0]; break
    if not best and lst: best=lst[0]
    bajio = c["estado"].lower() in BAJIO
    verified = any(x["verificado"] for x in lst)
    ind=industry_fit(c["industria"],c["segmento"])
    score=40+ind
    p=c["prioridad"].lower()
    score += 20 if p=="alta" else 10 if p=="media" else 0
    cf=c["confianza"].lower()
    score += 10 if cf=="alta" else 5 if cf=="media" else 0
    if best and best.get("email"): score+=5
    if bajio: score+=10
    if verified: score+=10
    score=min(score,100)
    tier="A+" if score>=90 else "A" if score>=80 else "B" if score>=70 else "C" if score>=60 else "Low"
    rows.append({**c,"n_contacts":len(lst),"bajio":bajio,"verified":verified,"ind":ind,
        "score":score,"tier":tier,"best_name":best["contacto"] if best else "",
        "best_title":best["puesto"] if best else "","best_email":best.get("email","") if best else "",
        "best_pri":pri_rank(best["puesto"]) if best else ""})
rows.sort(key=lambda x:(-x["score"], not x["bajio"]))

print("TID Master DB empresas:",len(rows))
print("Contactos:",sum(len(v) for v in comp_contacts.values()))
print("Tiers:",dict(Counter(r["tier"] for r in rows)))
print("Bajío:",sum(1 for r in rows if r["bajio"]),"| Verificados:",sum(1 for r in rows if r["verified"]))

wb=openpyxl.Workbook(); ws=wb.active; ws.title="Master Company DB"
cols_out=["MasterID","Empresa","Estado","Ciudad","Industria","Segmento","Prioridad","Confianza","Bajio","Verificado","#Contactos","Score","Tier","PrimaryContact","PrimaryTitle","PrimaryEmail","Pri"]
ws.append(cols_out)
for r in rows:
    ws.append([r["key"],r["display"],r["estado"],r["ciudad"],r["industria"],r["segmento"],r["prioridad"],r["confianza"],
        "Sí" if r["bajio"] else "","Sí" if r["verified"] else "",r["n_contacts"],r["score"],r["tier"],
        r["best_name"],r["best_title"],r["best_email"],r["best_pri"]])
# Top prospectos
top=[r for r in rows if r["best_email"]][:100]
ws2=wb.create_sheet("Top 100 Prospectos"); ws2.append(["Rank","Empresa","Estado","Industria","Score","Tier","Bajio","Contacto","Email","Angulo"])
for i,r in enumerate(top,1):
    ang="abasto local vs importar" if r["bajio"] else "segunda fuente / muestras"
    ws2.append([i,r["display"],r["estado"],r["industria"],r["score"],r["tier"],"Sí" if r["bajio"] else "",r["best_name"],r["best_email"],ang])
# Top 25 atacar ya (email + priority A/B, Bajío primero)
act=[r for r in rows if r["best_email"] and r["best_pri"] in ("A","B")]
act.sort(key=lambda x:(-x["score"], not x["bajio"]))
act=act[:25]
ws3=wb.create_sheet("Top 25 Atacar Ya"); ws3.append(["Rank","Empresa","Estado","Industria","Score","Bajio","Verif","Contacto","Rol","Email","Oportunidad","Next"])
for i,r in enumerate(act,1):
    ws3.append([i,r["display"],r["estado"],r["industria"],r["score"],"Sí" if r["bajio"] else "","Sí" if r["verified"] else "",
        r["best_name"],r["best_pri"],r["best_email"],"foil+tintas: abasto local, 2ª fuente, muestras","Email approach A/B/C + LinkedIn"])
# metodologia
ws5=wb.create_sheet("Metodologia")
for n in [
 ["TID Intelligence Engine — decoradores de plástico (foil hot stamping + tintas tampo/serigrafía)",""],
 ["Fecha","2026-08-29"],
 ["Fuente","ContactosFoilTIDGLOBAL (Prosp — Todos + Agenda propia verificada)"],
 ["Score (0-100)","base40 + industria(fit) + prioridad(estudio) + confianza + email + Bajío(+10 abasto local) + verificado(+10). Priorizacion, no hecho."],
 ["Bajío","Queretaro/Guanajuato/SLP/Aguascalientes/Jalisco = ventaja de abasto local vs importar (KURZ)."],
 ["Verificado","Contacto en 'Agenda propia' (verificado vs ZoomInfo/Wiza/Apollo)."],
 ["Angulo TID","A abasto local vs importar · B 2a fuente · C muestras. Pitch corto se manda tras respuesta."],
 ["Pendiente","Enriquecer comprador/ingenieria real (Apollo/Wiza/ZoomInfo) cuando permiso funcione."],
]: ws5.append(n)
for wsx in wb.worksheets:
    if wsx.max_row>1 and wsx.title!="Metodologia":
        wsx.auto_filter.ref=f"A1:{openpyxl.utils.get_column_letter(wsx.max_column)}{wsx.max_row}"
wb.save(OUT)
print("Guardado:",OUT,"| Top100:",len(top),"| Top25:",len(act))
print("\n--- TOP 15 TID ---")
for i,r in enumerate(top[:15],1):
    print(f"{i:2d}. [{r['score']}|{r['tier']}] {r['display'][:30]:30} {r['estado'][:12]:12} {'BAJIO' if r['bajio'] else '     '} {str(r['industria'])[:16]:16} {r['best_email'][:26]}")
