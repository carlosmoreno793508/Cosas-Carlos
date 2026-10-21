# Capa 1 — Esquema de la base de datos (activo defensible)

> Modelo de datos de DOS lados. Arranca como Google Sheets / CSV; migra a base real (Postgres/Airtable) cuando escale. Lo importante es empezar a capturar YA, con cada campaña y respuesta.

## Entidades

### 1. `empresas` (accounts)
| Campo | Tipo | Ejemplo |
|---|---|---|
| id | uuid | — |
| nombre | text | Mabe |
| tipo | enum | OEM / EMS / Distribuidor |
| lado | enum | comprador / proveedor |
| vertical | enum | electronica / plasticos |
| industria | text | Línea blanca |
| pais | text | México |
| ciudad_planta | text | Querétaro |
| tamano | text | 1000+ |
| dominio_web | text | mabe.com.mx |
| fuente | text | estudio Astute / ZoomInfo |
| created_at | date | — |

### 2. `contactos` (people)
| Campo | Tipo | Ejemplo |
|---|---|---|
| id | uuid | — |
| empresa_id | fk | — |
| nombre | text | Juan Pérez |
| titulo | text | Commodity Manager |
| rol | enum | buyer / procurement / supply_chain / plant_mgr |
| email | text | (verificado) |
| linkedin | url | — |
| commodity | text | pasivos / semiconductores |
| estatus | enum | frío / contactado / respondió / reunión / cliente |
| fuente | text | Apollo / Wiza |
| consentimiento/base_legal | text | interés legítimo B2B |

### 3. `senales` (signals / oportunidades)
| Campo | Tipo | Ejemplo |
|---|---|---|
| id | uuid | — |
| empresa_id | fk | — |
| tipo | enum | expansión / nueva_planta / RFQ / EOL / fusión / arancel / escasez |
| descripcion | text | "Nueva planta en Saltillo 2026" |
| fecha_detectada | date | — |
| fuente | text | noticia / ZoomInfo scoops / job posting |
| prioridad | enum | alta / media / baja |

### 4. `campanas` y `reuniones`
- `campanas`: id, dominio, buzones, copy_version, fecha_inicio, enviados, opens, replies.
- `reuniones`: id, contacto_id, cliente (Astute), fecha, resultado, notas.

## Relaciones

```
empresas 1──* contactos
empresas 1──* senales
contactos 1──* reuniones
campanas *──* contactos
```

## Regla del activo

- Los datos (empresas, contactos, señales) son **de GrowProkure**, no del cliente.
- Cada campaña, respuesta y reunión **alimenta** la base → mientras más operamos, más valioso el activo (el foso).
- Higiene legal: registrar `fuente` y `base_legal` de cada contacto (interés legítimo B2B, cumplimiento CAN-SPAM / privacidad).

## MVP inmediato

1. Crear el Sheet con estas 4 pestañas (empresas / contactos / señales / campañas).
2. Sembrar `empresas` con la lista de `06-icp-y-cuentas-objetivo.md`.
3. Enriquecer `contactos` con ZoomInfo/Apollo/Wiza.
4. Registrar `señales` desde el estudio Astute.
