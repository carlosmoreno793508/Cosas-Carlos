# Sesión 2 sep 2026 — La búsqueda gratis sí devuelve el dominio

**Gasto: 0 créditos de ZoomInfo, 0 de Wiza. Ningún correo enviado.**
Todo salió de `search_companies`, que es gratis.

## Lo que corrige esta sesión

La bitácora del 31 de agosto afirma que la búsqueda gratis devuelve
"nombre, país, estado, ciudad, empleados, ingresos y `companyId`. Nada más".

**Es incorrecto: también devuelve `website`.** Verificado contra el API en 30
búsquedas de esta sesión.

Eso mueve el bloqueo principal del proyecto. La decisión #4 —re-exportar el CRM
sin truncar— dejó de ser la única salida para las URLs cortadas: el dominio se
puede recuperar por nombre, gratis, empresa por empresa.

Lo que **sigue sin venir gratis es la industria**, y es justo lo que hace falta
para decidir OEM vs EMS vs Broker. Eso no cambió.

## 1. Los 14 del hueco mexicano — de 3 a 6 dominios usables

| Empresa | Dominio | Entidad ZoomInfo |
|---|---|---|
| CircuiTec | `circuitec.mx` | Cuernavaca, Morelos · 79 empl · id 458051197 |
| TKR de México | `tkrdemexico.com` | La Concordia, Tamaulipas · **430 empl** · id 557473450 |
| Bunker Electronics | `bunkeraudio.com` | Tlajomulco, Jalisco · 12 empl · id 356604023 |

Se suman a Gollet, Mextronics y Construlita. **6 de 14 con dominio mexicano
verificado.** Ningún correo inventado: la columna `email` sigue vacía en las 14
(R3).

TKR es la más grande del grupo con diferencia y la única de escala industrial.

Tres advertencias que salieron en el camino:

- **Bunker no usa su propio nombre**: el dominio es `bunkeraudio.com`. Y existe
  una homónima en Nueva York con `bunkerelectronics.com` que **no** es esta.
- **Fagor Electrónica: riesgo de trampa.** El único registro es la entidad de
  Andover, Massachusetts (819 empl). No hay entidad mexicana. Usar
  `fagorelectronica.com` para la planta de Querétaro repetiría el caso SIIX.
- **vielectronics e International Assembly: no asignados.** El match de
  vielectronics es una empresa de 2 empleados en San Antonio, Texas. El de
  International Assembly son dos homónimas en dos ciudades llamadas Guadalupe
  —Nuevo León y Estado de México— y el dominio pertenece a la que *no* coincide
  con el CRM.
- **Firstronic: confirmado ausente.** 0 resultados por nombre y 0 por dominio.

## 2. Fase 2, tanda 2 — `Tsunami_Fase2_Tanda2_VERIFICADA.csv`

Se verificaron gratis 18 de las 114 cuentas sin dominio: las 19 EMS/CM —el
encaje real de Astute— más Preh, que el CRM marca con planta en Nuevo León.

**9 dominios recuperados, 8 con riesgo de trampa marcado.**

Lo que más rinde:

- **Cal-Comp tiene dominio mexicano propio: `cal-comp.com.mx`.** La matriz es
  `calcomp.co.th` (Tailandia, 34,035 empl). Para la planta de Tamaulipas, el
  `.com.mx`. Es el mismo error que costó el rebote de SIIX, evitado antes de
  gastar.
- **CCM Assembly repite el patrón SEACOMP**: el CRM la pone en Baja California
  y ZoomInfo en San Marcos, California. Oficina de un lado de la frontera,
  planta del otro.
- **International Control Services**: el CRM dice Nuevo León, ZoomInfo sólo
  tiene Decatur, Illinois.
- **Zollner confirma que el sitio web no es el dominio de correo.** ZoomInfo
  publica `zollner.de`; el correo verificado que ya compramos es
  `@zollner-electronics.com`.

Y cuatro que **no** se asignaron por falta de match creíble: Flex, DREAMTECH,
Digitronic GmbH y API Technologies. En los cuatro casos hay homónimas que
habrían pasado por buenas: buscar "Flex" con `country=Mexico` devuelve Pk-Flex,
Flex-Coah y Fuel Flex, ninguna relacionada. **La búsqueda por nombre es difusa;
tomar el primer resultado es una fuente de falsos positivos.**

Quedan 96 cuentas de la tanda 2 sin verificar (casi todas OEM grandes) y las
tandas 3 y 4 completas (271).

## 3. Los 3,262 sin clasificar — sigue sin poderse en bloque

El hallazgo del `website` ayuda pero no resuelve esto:

- El dominio se recupera **de a una búsqueda por empresa**. Son 3,262 llamadas
  al API, una por una, desde la conversación. No hay forma de hacerlo por lote:
  `companyIdList` acepta 50 ids, pero para eso ya habría que tener los ids.
- Y aun con el dominio, **la industria no viene gratis**. Sin industria no se
  decide OEM vs EMS vs Broker, que es exactamente lo que falta.

Existe un rodeo: `industryList` sí funciona como **filtro**. Buscar el nombre
con un filtro de industria y ver si la empresa aparece permite inferir su
industria sin gastar créditos —pero son 2 llamadas por empresa en vez de 1, así
que el problema de escala empeora.

**El re-export del CRM sin truncar sigue siendo la acción de mayor retorno**, no
porque no haya alternativa, sino porque resuelve 1,074 registros de un golpe en
vez de uno a uno.

## 4. Archivos de Instantly — reconstruidos y re-verificados

El script se volvió a correr de cero y reproduce el resultado sin desviaciones.

| Archivo | Filas |
|---|---|
| `Instantly_FILTRADO_COMPLETO.csv` | 3,631 |
| `Instantly_TANDA1_LIMPIA.csv` | 1,102 |
| `_Instantly_EXCLUIDOS_auditoria.csv` | 524 |

Los cuatro filtros obligatorios se auditaron **contra el archivo de salida**, no
sólo contra el log del script:

| Filtro | Sobrevivientes |
|---|---|
| `no_contactar = SI` | **0** |
| `tipo_final = DUP/Inactivo` | **0** (116 removidos) |
| Correos de severidad ALTA | **0** (17 removidos) |
| Rebotes confirmados del repo Astute | **0** (63 removidos) |
| Duplicados de correo (R2) | **0** |
| Correos malformados o vacíos (R3) | **0** |

Reparto por idioma: 2,916 ES · 516 EN · 36 PT · **163 sin idioma**. Esos 163 van
en `tandas-envio/Astute_SIN_IDIOMA_S1.csv` y necesitan que alguien decida el
idioma antes de subirlos.

El filtro R11 —dominio secundario de envío— es configuración de Instantly, no
del archivo. Sigue pendiente del lado de Carlos.

## Lo que sigue esperando decisión

1. **Re-exportar el CRM sin truncar.** Gratis, desbloquea 1,074 pendientes y
   271 cuentas de las tandas 3 y 4.
2. **Presupuesto de compra de la Fase 2.** Sin aprobación no se gastó un crédito
   esta sesión ni la anterior.
3. **Datos de rebote de la campaña de julio** (63 contactos). Sin eso no se debe
   subir volumen: es lo que dice la regla de >5% de la bitácora.
4. **Los 163 sin idioma** del archivo de envío.
5. **TID lleva 34 días de infraestructura pagada sin usar.** No depende de nada.
