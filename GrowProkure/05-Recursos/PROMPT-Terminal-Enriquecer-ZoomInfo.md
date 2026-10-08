# Prompt terminal — Enriquecer contactos nuevos con ZoomInfo

> Copiar/pegar en la **terminal Claude** (interactiva), donde sí funciona el login de ZoomInfo y el botón de permiso. Objetivo: jalar **teléfono + LinkedIn** de los contactos nuevos del CRM Tsunami, con match por **email** (confiable).

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
GrowProkure/04-GoToMarket/Enriquecer_Nuevos_CRM_Tsunami.csv (111 contactos, la mayoria con email).

Reglas:
- Haz el match por EMAIL (columna Email). Si un contacto no trae email, intenta por nombre + empresa,
  pero marca ese match como confianza=media y NO lo uses si hay ambiguedad.
- Para cada contacto trae: telefono directo (direct_phone), celular (mobile_phone) y LinkedIn (linkedin_url).
- NO inventes datos (REGLAS R3): si ZoomInfo no devuelve un dato, deja el campo vacio.
- Uso acotado a ESTA lista, sin extraccion masiva (REGLAS R10).
- Muestrame el COSTO en creditos ANTES de gastar (estimado) y el consumo real al terminar.

Salida:
- Guarda GrowProkure/04-GoToMarket/Enriquecer_Nuevos_RESULTADO.csv con TODAS las columnas originales
  MAS estas nuevas: telefono_zoominfo, celular_zoominfo, linkedin_zoominfo, match_status, confianza.
- No modifiques la Base Maestra todavia (yo la fusiono despues por email, sin duplicar).
- Al terminar: git add del RESULTADO, commit "Enriquecimiento ZoomInfo: contactos nuevos CRM Tsunami"
  y git push a la rama claude/procureai-growth-setup-eokr5w.
```

## Si quieres tambien la lista de Prioridad Alta (ambas verticales)
Cambia en el prompt el archivo por:
`GrowProkure/04-GoToMarket/Enriquecer_PrioridadAlta.csv` (109 contactos Alta).

## Cuando termine
Súbelo (git push) y avísame: yo **fusiono** telefono/LinkedIn de vuelta a la Base Maestra
(match por email, sin duplicar, respetando el esquema).

> Nota: en la sesion remota (esta) ZoomInfo no se puede autenticar; por eso va en terminal.
> Wiza NO sirve aqui (por nombre trae persona equivocada; por email no encuentra los @sanmina).
