# Plan de envío — septiembre 2026

Tandas listas en `04-GoToMarket/tandas-envio/`. **Nada se ha enviado.**
La configuración de Instantly la tienes que aplicar tú: no tengo acceso a la
cuenta, sólo dejo los archivos y los parámetros.

## Antes de subir nada: dos cosas que revisar

### 1. La campaña de Astute lleva 34 días con 63 leads

Se lanzó el 28 de julio con `Astute_Tier1_Clave_Instantly.csv` (63 contactos) y
una secuencia de 4 correos que termina en el día 12. **Esa campaña acabó hace
tres semanas.** Los buzones llevan desde entonces sin mandar nada en frío.

**Necesito el dato de rebote de esos 63 antes de subir volumen.** Está en el
Unibox / la pestaña Analytics de la campaña. La regla que tú mismo pusiste en la
bitácora es >5% = limpiar lista. Si esos 63 rebotaron feo, subir 500 la primera
semana empeora el problema en vez de arreglarlo. Si vienen limpios, la rampa de
abajo es segura.

### 2. TID lleva 33 días de infraestructura pagada sin usar

El warm-up de TID terminó el 29 de julio y la campaña **nunca se lanzó**. Son 5
buzones y ~$29/mes de Workspace corriendo en vacío desde entonces. Los contactos
ya existen (`02-Investigacion/plasticos/`, estudio Foil: 120 contactos / 63
correos). Esto no depende de nada más — se puede lanzar cuando quieras.

Ojo: TID es **plásticos/foil**, campaña aparte de Astute. Las tandas de este
documento son todas de electrónica (Astute).

## Los 60 que NO se vuelven a contactar

De los 63 de la tanda 1, **60 siguen apareciendo en el archivo nuevo**. Ya
quedan excluidos de todas las tandas. Repetirles un ciclo de 4 correos es la
forma más rápida de que marquen spam.

## Tandas

3,619 contactos disponibles, partidos por idioma porque **cada idioma es una
campaña distinta en Instantly** (el copy cambia).

| Archivo | Filas | Qué trae |
|---|---|---|
| `Astute_ES_S1.csv` | 500 | 15 clave electrónicos + 485 decisores de compras |
| `Astute_ES_S2.csv` | 500 | 325 decisores + 175 compradores |
| `Astute_ES_S3.csv` | 500 | 334 compradores + 166 directorio |
| `Astute_ES_S4..S6.csv` | 1,403 | directorio ampliado |
| `Astute_EN_S1.csv` | 500 | mezcla completa, mercado US/Europa/Asia |
| `Astute_EN_S2.csv` | 16 | cola del anterior, súbelo junto con S1 |
| `Astute_PT_S1.csv` | 37 | Brasil — **necesita copy en portugués, no existe todavía** |
| `Astute_SIN_IDIOMA_S1.csv` | 163 | **no enviar**: sin país, no se sabe qué copy va |

## Configuración de Instantly (la misma que ya funcionó, con la rampa ajustada)

| Parámetro | Valor |
|---|---|
| Secuencia | 4 correos, día 0 / 3 / 7 / 12 |
| Buzones | los 7 de Astute, en rotación |
| Stop on reply | **ON** |
| Open / Link tracking | **OFF** |
| Delivery | Text-only, sin HTML |
| Horario | L–V, 9:00–17:00, America/Mexico_City |
| Semana 1 | **100/día** (≈14 por buzón) |
| Semana 2 | 140/día, sólo si el rebote de la semana 1 < 3% |
| Semana 3+ | 175/día (25 por buzón), techo recomendado |

Mapeo al subir el CSV: `email`→Email · `first_name`→First Name ·
`last_name`→Last Name · `company_name`→Company Name.

## Orden sugerido

1. Sacar el rebote de la tanda de julio. **Gate de todo lo demás.**
2. Lanzar TID con el estudio Foil — lleva un mes parado y no depende de nada.
3. `Astute_ES_S1` a 100/día.
4. Revisar rebote a los 5 días. Si < 3%, subir a 140/día y cargar S2.
5. `Astute_EN_S1` como campaña separada, en inglés.
6. El PT y el SIN_IDIOMA quedan pendientes: uno necesita copy, el otro país.

## Lo que sigue sin resolverse

**El re-export del CRM sin truncar.** 385 cuentas de Fase 2 y 1,074 pendientes
de clasificar siguen bloqueadas ahí. Es gratis y es lo que más rinde.
