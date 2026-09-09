# Guía terminal — bajar/enriquecer más información (Apollo · Wiza · ZoomInfo)

> Para hacerlo en la **terminal (Claude Code interactivo)**, donde SÍ funcionan el login de conectores y el botón de permiso (a diferencia de la sesión remota). Objetivo: enriquecer el Top 25 (comprador real + email verificado) y bajar más contactos.

## Paso 0 — Requisitos
- Una **Mac o Windows** con terminal.
- Tu cuenta de Claude (la misma que usas aquí).
- Node.js instalado (si no, se instala en el paso 1).

## Paso 1 — Instalar Claude Code
En la terminal:
```
npm install -g @anthropic-ai/claude-code
```
(Si no tienes Node: instálalo desde nodejs.org, opción LTS, y repite.)

Luego inicia sesión:
```
claude
```
La primera vez te pide loguearte con tu cuenta de Claude (se abre el navegador). Acepta.

## Paso 2 — Bajar el proyecto
Clona tu repo (una sola vez):
```
git clone https://github.com/carlosmoreno793508/Cosas-Carlos.git
cd Cosas-Carlos
git checkout claude/procureai-growth-setup-eokr5w
```
Ahí está todo: `GrowProkure/` con la Base Maestra, los Intelligence Engine y los CSV del Top 25.

## Paso 3 — Abrir Claude en el proyecto
Dentro de la carpeta:
```
claude
```

## Paso 4 — Conectar Apollo / Wiza / ZoomInfo
Dentro de Claude, escribe:
```
/mcp
```
Ahí ves los conectores. Para cada uno (Apollo, Wiza, ZoomInfo):
- Selecciónalo → **Authenticate / Login** → se abre el navegador → autoriza.
- Cuando vuelvas, debe decir **connected**.

> Alternativa: en **claude.ai → Settings → Connectors**, conecta Apollo/Wiza/ZoomInfo una vez; la terminal los toma.

## Paso 5 — Aprobar la herramienta (aquí SÍ funciona el botón)
La primera vez que Claude use Apollo, sale un cuadro de permiso con botones:
- Dale **"Yes, and don't ask again for this tool"** (equivale a "Allow always").
- Repite para Wiza/ZoomInfo la primera vez.

## Paso 6 — Pegar el prompt de enriquecimiento
Copia y pega esto en Claude (terminal):
```
Enriquece las 25 cuentas de GrowProkure/04-GoToMarket/Astute_Top25_Instantly.csv.
Para cada empresa, usando Apollo (y Wiza/ZoomInfo si ayuda):
1. Encuentra el comprador REAL de componentes electrónicos (purchasing / procurement /
   commodity manager / sourcing / materials), no cualquier puesto.
2. Verifica su email.
3. Agrega columnas: comprador_real, puesto_real, email_verificado, fuente, confianza.
Respeta REGLAS.md (sin extracción masiva, uso acotado por ICP). Muéstrame el costo en
créditos antes de gastar y al terminar. Guarda el resultado como
Astute_Top25_ENRIQUECIDO.csv y haz commit.
```
Claude te dirá el costo estimado, te pedirá permiso, y correrá el enriquecimiento.

## Paso 7 — Bajar MÁS contactos (opcional)
Para ampliar la base (no solo enriquecer), pega:
```
Con Apollo, busca compradores de componentes electrónicos (purchasing/commodity/sourcing)
en fabricantes electrónicos de México que NO estén ya en
GrowProkure/05-Recursos/Base_Maestra_GrowProkure.xlsx. Trae máximo 200, verifica emails,
deduplica contra la Base Maestra e intégralos como nuevos (vertical Electronica, lado Demanda).
Muéstrame costo antes y después. Sin extracción masiva.
```

## Reglas de oro (no romper)
- **Costo:** Apollo/ZoomInfo/Wiza gastan créditos. Siempre pide ver el costo antes. (Tenías ~58k créditos de lead en Apollo — suficiente.)
- **Sin extracción masiva** ni reventa (términos de las herramientas + REGLAS R10).
- **Nunca** cold-email desde el corporativo ni growprokure.com.
- Al terminar, **git push** para que los datos enriquecidos suban al repo.

## Si algo falla
- Conector no conecta → reconéctalo en claude.ai → Settings → Connectors.
- "requires approval" que no avanza → asegúrate de darle al **botón** (no escribirlo).
- Sin créditos → avísame y ajustamos el alcance.

> Estado: guía lista (2026-08-29). En terminal se destraba el permiso que bloqueaba el enriquecimiento en la sesión remota.
