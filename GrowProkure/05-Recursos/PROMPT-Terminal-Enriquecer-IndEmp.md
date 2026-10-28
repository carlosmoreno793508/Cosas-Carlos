# Prompt terminal — Enriquecer contactos de COMPRAS (Industrial+Empresarial) por vertical

> Copiar/pegar en la **terminal Claude** (interactiva), donde sí funciona el login de ZoomInfo y el botón de permiso.
> Objetivo: jalar **teléfono directo + celular + LinkedIn** de los contactos de compras ya **filtrados por las dos
> verticales de GrowProkure** (electrónica para Astute, plásticos/empaque para TID), con match por **email** (confiable).
> Solo se enriquece la lista filtrada `ZoomInfo_Upload_Verticales.csv` (112 contactos) para **ahorrar créditos** —
> la lista completa (`ZoomInfo_Upload_IndEmp.csv`, 1,995) queda intacta por si acaso.

## Setup (una sola vez, antes del prompt)
```
cd Cosas-Carlos
git pull origin claude/procureai-growth-setup-eokr5w
claude
```
Dentro de Claude:
1. `/mcp` → selecciona **ZoomInfo** → **Authenticate / Login** → autoriza en el navegador → debe decir **connected**.
2. La primera vez que use ZoomInfo saldrá un cuadro de permiso: dale **"Yes, and don't ask again for this tool"**.

## Prompt (pégalo tal cual)
```
Enriquece con ZoomInfo los contactos del archivo
GrowProkure/04-GoToMarket/ZoomInfo_Upload_Verticales.csv
(112 contactos de compras, ya filtrados por vertical: electronica + plasticos-empaque; todos traen email).

Reglas:
- Haz el match por EMAIL (columna Email). Si un contacto no hiciera match por email, intenta por
  Full Name + Company, pero marca ese match como confianza=media y NO lo uses si hay ambiguedad.
- Para cada contacto trae: telefono directo (direct_phone), celular (mobile_phone) y LinkedIn (linkedin_url).
- NO inventes datos (REGLAS R3): si ZoomInfo no devuelve un dato, deja el campo vacio.
- Uso acotado a ESTA lista de 112, sin extraccion masiva (REGLAS R10). Respeta terminos de ZoomInfo.
- Muestrame el COSTO en creditos ANTES de gastar (estimado para 112 matches por email) y el consumo real al terminar.
  Si el estimado supera lo esperado, PARA y preguntame antes de gastar.

Salida:
- Guarda GrowProkure/04-GoToMarket/ZoomInfo_RESULTADO_Verticales.csv con TODAS las columnas originales
  (First Name, Last Name, Full Name, Email, Company, Title, City, State, Country) MAS estas nuevas:
  telefono_zoominfo, celular_zoominfo, linkedin_zoominfo, match_status, confianza.
  - match_status: matched / not_found.
  - confianza: alta (match por email) / media (match por nombre+empresa) / vacio si not_found.
- NO modifiques la Base Maestra (Base_Maestra_GrowProkure.xlsx). Carlos la fusiona despues por email, sin duplicar.
- Al terminar: git add del RESULTADO, commit "Enriquecimiento ZoomInfo: compras verticales (electronica+plasticos)"
  y git push a la rama claude/procureai-growth-setup-eokr5w.
```

## Qué contiene la lista filtrada
- **112 contactos** = 17 electrónica (cliente Astute) + 95 plásticos/empaque (cliente TID).
- Salieron de 1,995 contactos de compras; se descartaron **1,883 "otro"** (hoteles, bancos, alimentos,
  acero/forja, autopartes mecánicas, servicios, etc.) para no quemar créditos en lo irrelevante.
- Todos con email válido; 20 son genéricos (compras@/info@) — aún así útiles para el match por dominio.

## Cuando termine
Súbelo (git push) y avísame: yo **fusiono** teléfono/celular/LinkedIn de vuelta a la Base Maestra
(match por email, sin duplicar, respetando el esquema R1 y conservando `Fuente`/`Origen` R5).

> Nota: en la sesión remota (la de Prokure) ZoomInfo NO se puede autenticar; por eso este paso va en terminal.
> Wiza NO sirve aquí (por nombre trae persona equivocada; por email no encuentra varios dominios).
> Si quisieras enriquecer la lista COMPLETA de todos modos, cambia el archivo del prompt por
> `GrowProkure/04-GoToMarket/ZoomInfo_Upload_IndEmp.csv` (1,995; más caro en créditos).
