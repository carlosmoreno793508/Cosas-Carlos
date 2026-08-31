# Sesión 31 ago 2026 — Instantly listo, Fase 2 preparada, 3 premisas corregidas

Gasto de esta sesión: **13 créditos de ZoomInfo, 0 de Wiza.** Todo lo demás salió
de `search_companies` y `search_contacts`, que son gratis. **No se envió ningún correo.**

## 1. Archivos de Instantly — LISTOS

| Archivo | Filas | Qué es |
|---|---|---|
| `Instantly_TANDA1_LIMPIA.csv` | **625** | Prioridad 1 y 2, sin riesgo. Es el que se sube primero. |
| `Instantly_FILTRADO_COMPLETO.csv` | **1,858** | Todo lo enviable, ordenado por prioridad. |
| `_Instantly_EXCLUIDOS_auditoria.csv` | 301 | Cada exclusión con su motivo, para poder auditarla. |

Fuentes fusionadas: Astute (1,588) + Top100 Tsunami (78) + hueco MX (17) + contactos gratis del CRM (164) + **Fase 2 tanda 1 (11)**.

**Los 4 filtros obligatorios quedaron aplicados y verificados uno por uno:**

- `no_contactar = SI` → 0 sobrevivientes (las 8 cuentas con DO NOT CALL / quiebra).
- `tipo_final = DUP/Inactivo` → 61 removidos, 0 sobrevivientes.
- Los 25 correos de severidad ALTA → 0 sobrevivientes.
- Dominio secundario: es config de Instantly, no del archivo. Sigue en la guía (R11).

Además, por R2/R3/R9: 158 duplicados por correo, 36 sin correo, 12 buzones
genéricos, 9 dominios personales y 7 correos "(inferido)" que nunca se
verificaron. Esos 7 eran correos construidos, no reales.

## 2. Los 14 del hueco mexicano — `Tsunami_MX_Hueco_14_RECUPERACION.csv`

**La causa no era el patrón de dominio.** Los 14 (10 EMS + 4 OEM) fallaron
porque ZoomInfo no tiene correo para ellos, no porque el dominio estuviera mal.
Recuperarlos "por patrón" habría significado inventar el correo, que es
justo lo que prohíbe R3 y lo que ya nos costó el rebote de SIIX.

Lo que sí se recuperó, gratis:

- **Dominio mexicano verificado** para 3: `gollet.com.mx`, `mextronics.com`, `construlita.com`. El CRM los traía truncados.
- **Trampa de dominio detectada** en 3 más: `falco.com` es Miami (la planta está en Mérida), `seacomp.com` es Carlsbad (la planta está en Tijuana), `kscable.co.kr` es Corea (la planta está en Gómez Palacio). **Estos tres sí son el patrón SIIX** — usar ese dominio habría repetido el rebote.
- Los 8 restantes siguen sin dominio verificable: teléfono o LinkedIn.

La columna `email` va vacía en las 14. Ninguno inventado.

## 3. Patrón de dominio de verdad — `Correos_Patron_Dominio_RECUPERACION.csv`

Ese es otro conjunto: los 16 correos ALTA con dominio de matriz extranjera.

- **Jatco recuperado: `jatco.com.mx`** (Jatco México, Peñuelas, Aguascalientes, 50 empl). Afecta a 3 contactos. Falta confirmar el local-part — el patrón japonés `miguel_najeralopez@` casi seguro no aplica al `.com.mx`.
- Hyundai Mobis: entidad mexicana localizada (Pesquera, NL) pero ZoomInfo no le tiene sitio.
- Marquardt y Astemo: ZoomInfo no tiene entidad mexicana. No recuperados.

## 4. Los 3,262 sin clasificar — no se puede como se pidió

**La búsqueda gratis de ZoomInfo no devuelve industria.** Devuelve nombre,
país, estado, ciudad, empleados, ingresos y `companyId`. Nada más. Verificado
contra el API en esta sesión.

Sin industria ni descripción no se puede decidir OEM vs EMS vs Broker, que es
exactamente lo que falta. Eso sólo viene de `enrich_companies`, que **sí cuesta
créditos** — serían 3,262.

Segunda pasada gratis sobre las notas del propio archivo: **6 reclasificados**
y 20 mandados a revisión humana. La señal gratis ya estaba agotada.

**El bloqueo real sigue siendo la decisión #4:** re-exportar el CRM sin truncar.
33% de los pendientes traen la URL cortada (`www.c...`). Es gratis y es lo que
más rinde.

## 5. Fase 2 de Tsunami — tandas armadas, sin gastar todavía

571 objetivos (371 OEM + 200 EMS), en 4 tandas de 150.

| Tanda | Cuentas | Con dominio verificable |
|---|---|---|
| 1 | 150 | **150** |
| 2 | 150 | 36 |
| 3 | 150 | 0 |
| 4 | 121 | 0 |

**385 de 571 (67%) no tienen dominio.** Se ordenaron a propósito para que la
tanda 1 sean puros verificables.

La tanda 1 ya está verificada gratis (`Tsunami_Fase2_Tanda1_VERIFICADA.csv`),
133 de 150 encontradas. Lo que salió:

- **Sólo 49 de 133 son de EEUU (37%).** Hay 23 de Alemania, 9 de India, 8 de Italia, 7 de Francia, y 21 países más. Segmentar por TLD habría mandado copy en español a media Europa.
- **15 entidades no coinciden con el nombre del CRM (11%).** La peor: `Continental Aerospace Technologies GmbH` cae en `Continental Diesel`, Bronx NY, **1 empleado**. Comprar ahí es crédito tirado. También `CIRCUIT SYSTEMS (INDIA)` → PCB Power Market (California) y `Micro Systems Engineering` (Oregon) → Micro Systems Technologies (Berlín) — la matriz, no la planta.
- **2 plantas mexicanas que nadie había marcado:** APC Manufacturing (Guanajuato, 302 empl) y Brambilight (Jalisco, 14 empl).

Esa verificación gratis evitó ~15 créditos malgastados en la tanda 1 sola.

## Lo que falta que decidas

1. **¿Arranco la compra de la tanda 1?** Son ~150 créditos. Recomiendo comprar sólo las 118 con entidad verificada (`match_entidad = OK`) y dejar las 15 en revisión: eso baja el gasto y sube la tasa de acierto. El presupuesto de arranque (decisión #2) sigue sin aprobarse, por eso no gasté nada todavía.
2. **Re-exportar el CRM sin truncar.** Desbloquea 385 cuentas de Fase 2 y 1,074 pendientes. Gratis.
3. **Jatco:** confirmar el local-part de `@jatco.com.mx` antes de reactivar esos 3 contactos.


---

# Adenda — Compra de la Fase 2, tanda 1

**Gastado: 13 créditos. 13 enriquecimientos, 13 éxitos, 0 errores.**

## Por qué 13 y no 118

El embudo se cerró solo, y cada corte tiene su razón:

| Paso | Quedan | Por qué |
|---|---|---|
| Tanda 1 | 150 | Todas con dominio verificable |
| Entidad verificada (`match_entidad = OK`) | 118 | 15 caían en la empresa equivocada, 17 no aparecen en ZoomInfo |
| Dentro del ICP (EMS/CM o OEM mediano) | 83 | Los gigantes tipo GM, Lockheed o ZF necesitan targeting por planta, no por matriz |
| EMS/CM, el encaje real de Astute | 24 | Es a quien le vendes componentes y segundas fuentes |
| **Con comprador que tenga correo** | **13** | **Los otros 11 no tienen ningún rol de compras en ZoomInfo** |

Los 11 sin comprador tienen contactos — CEO, CFO, CTO, COO, RH — pero **ninguno
de compras**. Es el mismo patrón que ya vimos en los EMS mexicanos: ZoomInfo
cubre bien la dirección de las empresas chicas y mal el área de compras.
No se gastó un crédito en ellos, siguiendo la regla de la corrida anterior.

## Lo comprado

7 de confianza Alta, 4 Media, 2 Baja. **Los 2 de confianza Baja no entraron al
archivo de envío**: IMM electronics (valid_date de enero de **2015**) y CBE
(agosto 2024). Quedan en `Tsunami_Fase2_Tanda1_ENRIQUECIDO.csv` para verificar
por LinkedIn antes de usarlos.

Reparto: Alemania 3, Tailandia 2, y uno de Japón, Francia, España, Rumania,
Italia, India y Eslovenia. **Ninguno es de México ni de EEUU** — el copy de
estos 11 va en inglés, no en español.

## Tercera trampa de dominio

**El correo real de Zollner es `@zollner-electronics.com`, no `@zollner.de`**,
que es lo que traía el CRM. Van tres en la sesión (Falco, SEACOMP, Kyungshin, y
ahora Zollner). Confirma que comprar el correo verificado le gana a construirlo
a partir del dominio del sitio web.

## Nota técnica de ZoomInfo

`jobTitleList` con más de un puesto devuelve **0 resultados** — hace AND en vez
de OR. Hay que usar el campo `jobTitle` con sintaxis `"Buyer OR Purchasing OR
Procurement"`. Me costó varias búsquedas en falso; queda anotado para no
repetirlo. Los scripts y las búsquedas de esta sesión ya usan la forma correcta.

## Lo que queda de la Fase 2

- **94 OEM verificados sin comprar.** Casi todos son multinacionales grandes. Comprarlos requiere decidir primero *qué planta* es el objetivo, si no se repite el caso Continental. Dime si quieres que los compre igual.
- **32 de la tanda 1 descartados**: 15 por entidad equivocada, 17 sin resultado.
- **Tandas 2, 3 y 4 (421 cuentas):** 385 siguen sin dominio. Siguen bloqueadas por el re-export del CRM.
