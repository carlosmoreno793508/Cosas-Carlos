# Guía terminal — Enriquecer contactos Prioridad ALTA (tel + LinkedIn)

> Decisión (2026-09-25): enriquecer **solo Prioridad Alta**, en la **terminal Claude** (ahí sí funcionan el login de conectores y el botón de permiso). Acotado = respeta REGLAS **R10** (nada de extracción masiva).

## Por qué en terminal y no aquí
- **ZoomInfo**: en la sesión remota está **sin autenticar** (no se puede hacer el login OAuth aquí). En terminal reconectas con `/mcp`.
- **Wiza**: conectada, pero con **0 créditos de teléfono** (1,063 API / 500 email). Para teléfonos hay que **recargar phone credits** o usar ZoomInfo.
- El **botón de permiso** de las herramientas solo funciona en la terminal interactiva.

## Objetivo
Completar **teléfono** y **LinkedIn** de los contactos marcados `Prioridad = Alta` que les falta.

- Lista objetivo: **`04-GoToMarket/Enriquecer_PrioridadAlta.csv`** (109 contactos; ~78 sin teléfono, ~70 sin LinkedIn).
- Columna `Necesita` dice qué le falta a cada uno (`tel`, `+ LinkedIn`, o `completo`).

## Paso a paso
1. Abrir terminal en el repo:
   ```
   cd Cosas-Carlos
   git pull origin claude/procureai-growth-setup-eokr5w
   claude
   ```
2. Conectar herramientas (dentro de Claude): `/mcp` → autenticar **ZoomInfo** (y **Wiza** si vas a usar email). Si vas a sacar teléfonos con Wiza, primero **recarga phone credits** en tu cuenta Wiza.
3. Aprobar la herramienta la primera vez con **"Yes, and don't ask again for this tool"**.
4. Pegar este prompt:
   ```
   Enriquece SOLO los contactos de GrowProkure/04-GoToMarket/Enriquecer_PrioridadAlta.csv.
   Para cada uno, con ZoomInfo (y Wiza si ayuda), completa: telefono directo/celular y LinkedIn.
   Usa el email y la empresa como llave de match. NO inventes datos: si no hay match, deja
   el campo vacio y marca confianza=baja. Respeta REGLAS.md (R3 no inventar, R10 sin extraccion
   masiva: solo esta lista acotada). Muestrame el costo en creditos ANTES de gastar y al terminar.
   Guarda el resultado como GrowProkure/04-GoToMarket/Enriquecer_PrioridadAlta_RESULTADO.csv
   con columnas extra: telefono_enriquecido, linkedin_enriquecido, fuente, confianza. Haz commit y push.
   ```
5. Cuando termine, avísame y yo **fusiono** los teléfonos/LinkedIn enriquecidos de vuelta a la Base Maestra (sin duplicar, match por email).

## Reglas de oro
- **Costo primero:** siempre pide ver créditos antes de gastar.
- **Sin extracción masiva** — solo los 109 de la lista Alta.
- **Nunca** cold-email desde el corporativo ni growprokure.com.
- Al terminar, **git push** para que suba el resultado.

> Estado: guía lista (2026-09-25). El CSV objetivo se regenera desde la Base Maestra filtrando Prioridad=Alta.
