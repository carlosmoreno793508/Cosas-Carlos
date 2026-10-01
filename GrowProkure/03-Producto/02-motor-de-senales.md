# Capa 2 — Motor de señales (inteligencia)

> El diferenciador: no mandamos frío ciego, detectamos *momentos de compra*. Cada señal = una razón real para contactar = mayor conversión. Arranca manual/semi-automático; se automatiza con las APIs conectadas.

## Catálogo de señales por vertical

### Electrónica
| Señal | Qué indica | Dónde detectarla |
|---|---|---|
| **EOL (End-of-Life)** | Un componente se descontinúa → necesitan segunda fuente/last-time-buy | PCN de fabricantes, avisos EOL, estudio Astute |
| **Allocation / escasez** | Falta de suministro → buscan fuentes alternas | Reportes de mercado, noticias, foros de la industria |
| **Expansión / nueva planta** | Más volumen de compra → nuevo proveedor | Noticias, ZoomInfo scoops, comunicados |
| **Nearshoring a México** | Rebalanceo de base de proveedores | Anuncios de inversión, notas sectoriales |
| **RFQ activo** | Compra inminente | LinkedIn, contactos, señales de intención |
| **Nuevas vacantes de compras** | Crece el equipo → nuevos decisores | Job postings (Apollo/ZoomInfo) |
| **Vacantes SMT** (purchasing/production/técnico/sourcing/operadores) | Línea SMT activa o creciendo → comprador de componentes | SMTA Career Center, IPC, LinkedIn, ATS (Ashby/Greenhouse/Lever) |
| ⭐ **Importación de consumibles SMT** (HS 3810/3506, pasta/flux) | **Línea SMT ACTIVA** — produce AHORA = comprador vivo | Trade-data (ImportYeti gratis, Panjiva, ImportGenius) |
| **Importación de equipo SMT** (HS 8486, 8479.89) | Nueva capacidad instalándose | Trade-data por HS code |
| **Arancel / cambio comercial** | Presión de costo → re-sourcing | Noticias de política comercial |

> ⭐ **Señal estrella (del estudio USA-SMT):** buscar por HS code en aduana (bill-of-lading público) da la lista de importadores US = employers/compradores reales. Los **consumibles (3810/3506)** son el mejor indicador de "línea activa comprando ahora". Ver `02-Investigacion/electronica/estudio-usa-smt.md`.

### Plásticos (foil / tintas) — proceso secundario
| Señal | Qué indica | Dónde detectarla |
|---|---|---|
| **Nuevo lanzamiento de producto** | Nueva pieza decorada → necesitan foil/tinta | Noticias de producto, empaque |
| **Cambio de proveedor de decoración** | Ventana para entrar | Contactos, RFQ |
| **Expansión de planta de inyección** | Más volumen de decoración | Anuncios de inversión |
| **Requisitos de marca/estética** | Hot stamping / tampografía premium | Tendencias de empaque/cosmética/automotriz |

## Cómo se opera (flujo)

```
1. Detectar señal (manual o API)
2. Registrar en tabla `senales` (empresa, tipo, prioridad)
3. Priorizar cuenta+contacto asociados
4. Disparar secuencia de copy con el ángulo de esa señal
5. Medir conversión por tipo de señal → doblar en lo que funciona
```

## Automatización con herramientas conectadas

- **ZoomInfo scoops / intent / news:** expansiones, movimientos, intención de compra.
- **Apollo job postings:** vacantes de compras = crecimiento de equipo.
- **Wiza:** enriquecer los contactos de las cuentas con señal.

> MVP: empezar registrando señales a mano desde el estudio Astute + noticias, y usar las APIs para las de mayor volumen. La señal cambia el ángulo del correo (ver `04-copy-cold-email-electronica.md`).

## Por qué esto es el foso

Un competidor de cold email manda lo mismo a todos. Nosotros contactamos **cuando hay una razón real** (un EOL, una expansión). Eso sube conversión y construye la reputación de "estos sí saben del sector" — que es lo que retiene clientes y atrae al lado comprador.
