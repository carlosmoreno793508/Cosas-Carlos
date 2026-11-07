# MPSL — Modelo de negocio (v2, revisado)

**Liga Profesional de Natación de México · 2027–2031**
Acompaña al archivo `MPSL-modelo-financiero.xlsx` (7 hojas, todas con fórmulas; las celdas azules de *Supuestos* se pueden editar y el escenario se cambia en `Supuestos!C4`).

---

## 1. Veredicto en 30 segundos

Los dos documentos tienen buena tesis: crear una propiedad deportiva, no un torneo con premios, y no depender de un multimillonario. **Pero tal como están escritos, los números no se sostienen**, por cuatro razones:

1. **El equilibrio de $55 M es contable, no real.** El documento 2 cuenta los $6 M de cuotas de franquicia como ingreso *y* también suma el costo de esas franquicias. Al eliminar ese doble conteo, el ecosistema cubre unos $49 M y le faltan ~$6 M. Además, la nómina no incluye la carga social (IMSS, INFONAVIT, ISN, aguinaldo), que agrega ~32%.
2. **Con ese diseño nadie compraría una franquicia.** Un dueño paga $1.5 M de entrada y $1 M de cuota, gasta ~$5.5 M y solo vende ~$1.25 M de patrocinio local: pierde unos $4 M al año. En la primera versión del modelo eso dio −$4 M/año por dueño, todos los años.
3. **No hay 108 nadadores de nivel profesional disponibles en 2028.** Según la base de RankingsMX, desde 2025 solo **50 mujeres** y 82 hombres mexicanos (17+) pasan de 700 puntos WA (detalle en la sección 7).
4. **Se paga sueldo fijo 8 meses para competir 8 días**, desde el primer día y antes de probar que hay ingresos. Es justo el error de la ISL.

**La versión corregida funciona como negocio por etapas:**

| Escenario base (MXN) | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| Ingreso del ecosistema | 5.0 M | 41.4 M | 67.8 M | 103.2 M | 135.2 M |
| Resultado del ecosistema | −8.9 M | −6.8 M | **+2.3 M** | −2.7 M (expansión) | **+12.5 M** |
| Resultado de cada operador de franquicia | — | −0.15 M | +0.9 M | +1.3 M | +2.7 M |
| Nadadores con contrato | 48 | 72 | 72 | 112 | 112 |

**Capital a levantar para la liga, escenario base: ~$46 M** ($38 M de pérdidas acumuladas + $8 M de fondo de garantía de nómina). En el pesimista sube a ~$105 M y en el optimista baja a ~$20 M. Esa diferencia es la razón de ser de las compuertas de la sección 5.

---

## 2. Qué corregí de los documentos originales

| # | En los documentos | Problema | Corrección en el modelo |
|---|---|---|---|
| 1 | $6 M de cuotas de franquicia como ingreso del total de $55 M | Doble conteo: es dinero que se mueve de un bolsillo a otro del mismo ecosistema | Hojas *Liga*, *Franquicia* y *Consolidado* separadas; el consolidado elimina cuotas y repartos (tiene una fila de control) |
| 2 | Nómina sin carga social | IMSS + INFONAVIT + ISN + prestaciones ≈ 30–35% | 32% sobre retainer y staff |
| 3 | Contratos de "prestación de servicios" con exclusividad, horario y cesión de imagen | Hay subordinación, así que es relación laboral (la LFT tiene un capítulo de deportistas profesionales). Riesgo de demanda e IMSS | Retainer = nómina con carga social; el pago por etapa queda como honorario. **Validar con abogado laboral** |
| 4 | Desarrollo con sueldo de $8–12 k/mes | Prácticamente es el salario mínimo 2026: mal titular para una "liga profesional" | Desarrollo = pago por etapa + beca de academia, sin sueldo fijo hasta que el modelo lo aguante |
| 5 | Escenario conservador: los costos bajan de $55 M a $45 M | Contradice la regla "contratos garantizados": la nómina comprometida no se recorta | En el modelo los costos no se flexionan; el control está **antes** de firmar (compuertas) |
| 6 | Patrocinador titular de $12–15 M en el año 1 | Precio de una propiedad con audiencia probada; en 2028 todavía no hay datos de audiencia | $8 M en 2028, subiendo a $13 M en 2031 (en pesos de 2027) |
| 7 | Derechos de medios desde el año 1 | El propio documento dice "no presupuestar sin firma" | $0 en 2027–28; $1 M en 2029 solo si hay contrato |
| 8 | 18 nadadores × 6 equipos | No hay profundidad de talento (sección 7) | 12 por equipo (6/6) y 2 plazas de importación |
| 9 | El patrocinio es 60–72% del ingreso y casi todo lo demás también depende de terceros | Repite la fragilidad de la ISL | Se agregan fuentes recurrentes propias: Festival, academias, VIP y expo (sección 4). Aun así el patrocinio queda en ~60%: sigue siendo el riesgo n.º 1 |
| 10 | Sedes con nombre específico (p. ej. "Complejo Kukulcán" en Mérida, "CARE Niños Héroes" en Monterrey) | No pude confirmar que esas instalaciones tengan alberca de 50 m con gradas; algunas pueden ser otro tipo de recinto | Etiquetadas como "candidatas, por verificar" en una auditoría de sedes |
| 11 | Afirmaciones como "gasto descontrolado" de la ISL | Es una interpretación, no un dato publicado | En un memo para inversionistas, citar cifras con fuente y dejar el juicio aparte |

---

## 3. El modelo: entidad única + operadores locales

En lugar de 6 empresas que contratan cada una a sus nadadores, propongo un esquema **tipo MLS (entidad única)**:

- **MPSL (la liga)** contrata y paga a **todos** los atletas, sus viajes y la bolsa de premios. Así hay un solo fondo de garantía de nómina, equilibrio competitivo (draft y tope salarial) y ningún nadador queda sin cobrar porque un dueño quebró. Esta es la lección de la ISL y de PRO 16.
- **El operador de cada ciudad** (empresario, club, universidad) compra el derecho de entrada ($1.5 M), paga una cuota escalonada ($0.3 M en 2028 → $0.8 M en 2031) y cubre staff técnico y administración local. A cambio se queda con el **patrocinio local**, el **margen de las academias** con la marca del equipo y un **reparto** del patrocinio y medios centrales (10% → 20%).
- Resultado para el operador: casi en equilibrio en 2028, positivo desde 2029, y **recupera su entrada en 2030**. Eso sí se puede vender.

La cuota y el % de reparto deciden **quién se queda el margen** (liga vs. operadores). En la calibración actual la liga absorbe el riesgo de la nómina y los operadores ganan pronto, para que las franquicias se vendan. Con más tracción se puede subir la cuota.

### Fuentes de ingreso (2029, escenario base, ecosistema)

| Fuente | MXN | Tipo |
|---|---|---|
| Patrocinio central (titular, socios, proveedores, presentadores) | 26.9 M | Contrato anual |
| Patrocinio local de franquicias | 15.7 M | Contrato anual |
| **Festival: inscripciones + expo + merch** | 7.8 M | **Recurrente, no depende de marcas** |
| Boletaje + VIP | 8.0 M | Por evento |
| Ciudades sede (efectivo, además de la alberca en especie) | 4.4 M | Convenio de 3 años |
| Academias (margen operador) | 2.6 M | **Recurrente mensual** |
| Medios + digital | 2.4 M | Crece con audiencia |

---

## 4. Pensando como organizador de eventos masivos: el "MPSL Fest"

Una noche de natación profesional con 2,500 asientos nunca va a pagar la producción. **Un maratón tampoco se paga con los 30 corredores de élite: lo pagan los 30,000 amateurs.** La natación en México tiene esa masa: RankingsMX registra **~17,700 nadadores mexicanos activos en 2025** y ~100 competencias en el país. La mayoría paga inscripción varias veces al año y viaja con su familia.

**Cada etapa se convierte en un festival de fin de semana:**

| Bloque | Qué es | Para qué sirve |
|---|---|---|
| Viernes–domingo mañana | **Competencia abierta de categorías + másters** (1,200 nadadores en 2028 → 2,000 en 2031) en la misma sede | Inscripciones ($650 promedio), familias que llenan gradas y hoteles |
| Sábado | Aguas abiertas o "milla urbana" si la ciudad tiene cuerpo de agua | Foto icónica para la ciudad y el gobierno |
| Todo el fin | **Expo** de marcas (25–40 stands), clínicas con los profesionales y firma de autógrafos | Ingreso por stand y activación para patrocinadores |
| Viernes y sábado noche | **La noche MPSL**: 2 horas para TV, finales por equipos, skins, relevos mixtos, luces y DJ | El producto televisivo y de patrocinio |

Por qué funciona:
- Los niños de categorías **son el público** de la noche profesional: compiten en la mañana y en la noche ven a sus ídolos. Es el embudo de fans y de alumnos para las academias.
- El gobierno estatal recibe lo que quiere comprar: **ocupación hotelera, miles de visitantes y niños en la alberca**, no solo un evento de élite.
- En la hoja *Sensibilidad*, cada 1,000 nadadores extra por etapa valen ~$1.7 M al año de margen y amortigua una caída de patrocinios.

**Detalles de operación que no estaban:** cronometraje electrónico y placas para dos programas el mismo fin de semana; jueces certificados por la FMN; gradas temporales (el aforo real de cada sede define el boletaje: hay que verificarlo); protocolo de protección civil y plan de flujo de personas para ~5,000 asistentes por día; voluntariado con universidades locales; ventana de montaje y desmontaje negociada en el convenio con la sede.

---

## 5. Pensando como creador: la liga es un medio, la natación es el contenido

La ISL gastó en producción para TV y tuvo poca audiencia recurrente. El orden correcto es **audiencia primero, derechos después**:

1. **Atletas creadores.** Cada contrato incluye obligaciones de contenido (p. ej. 2 piezas al mes) y la liga les da un equipo de edición compartido. 72 nadadores × 2 piezas = ~1,700 piezas al año sin pagar agencia. Los atletas conservan sus derechos de imagen individuales (el documento 1 lo señala bien) y la liga licencia el uso colectivo.
2. **Serie documental de temporada** ("la pretemporada de Tijuana Pacific", "el draft") en YouTube. Es el producto que después se le vende a Claro Sports o ESPN, junto con la final.
3. **Formato vertical primero:** cada carrera estelar dura <60 s, que es la medida natural de un clip. Gráficos de Swimmx en pantalla (parcial vs. récord, línea virtual, posición en vivo).
4. **Swimmx como hub del fan:** perfil de cada profesional con su historial real (la base ya tiene sus marcas desde categorías infantiles), resultados en vivo y **fantasy gratuito** patrocinado. Sin apuestas: un fantasy con premio en dinero requiere permiso de SEGOB bajo la Ley Federal de Juegos y Sorteos.
5. **Rivalidades diseñadas** (la lección de Duel in the Pool): Norte vs. Centro, un clásico CDMX–Guadalajara, y en 2029 una noche **México vs. Brasil** (Pinheiros / Minas).
6. **El draft como evento**, transmitido y con los clubes formadores presentes. Es contenido gratis y da orgullo local.

---

## 6. Fases y compuertas (no avanzar sin cumplir la anterior)

| Fase | Qué pasa | Compuerta para pasar a la siguiente |
|---|---|---|
| **2027 · Piloto** | 1 Festival + noche MPSL, 4 equipos por draft operados por la liga, 48 atletas pagados **por etapa** | ≥1,500 asistentes, ≥800 inscritos al Festival, ≥$8 M en cartas de intención de patrocinio, aval técnico de la FMN |
| **2028 · Temporada 1 (modo circuito)** | 6 franquicias vendidas, 4 etapas, 72 atletas **pagados por etapa** (sin sueldo fijo) | ≥$20 M de patrocinio **firmado** para 2029; ecosistema con pérdida ≤ $8 M |
| **2029 · Contratos** | Retainer de 4 meses para estrellas y titulares, academias en las 6 ciudades | Ecosistema ≥ $0; escrow de 3 meses de nómina depositado |
| **2030 · Latam** | +2 franquicias internacionales (entrada $3 M), 5 etapas | Solo si 2029 cerró en positivo |
| **2031 · Consolidación** | Derechos de medios regionales, retainer de 6 meses | Valuación y entrada de capital privado |

**Regla de oro (del documento original y correcta): nadie firma un contrato cuyo pago no esté depositado en escrow.**

---

## 7. ¿Hay nadadores? (datos propios de RankingsMX)

Nadadores mexicanos de 17+ años, mejor marca desde 2025, CL/CC, sin marcas en revisión:

| Puntos WA | ≥600 | ≥650 | ≥700 | ≥750 | ≥800 |
|---|---|---|---|---|---|
| Hombres | 359 | 196 | 82 | 38 | 13 |
| Mujeres | 185 | 89 | **50** | 15 | 7 |

- Con 54 plazas por sexo (original), la última mujer está en ~690 pts. Con 36 (este modelo), en ~715, y el último hombre en ~755: nivel nacional sólido en todo el roster.
- **Calendario:** muchos de los mejores nadan en la NCAA (oct–mar). Propongo etapas en **mayo, junio, septiembre y diciembre** (diciembre = receso NCAA), a validar con el calendario de la FMN y con el área de cumplimiento de la NCAA (elegibilidad, premios en efectivo).
- RankingsMX no tiene todas las competencias del país, así que estos conteos son un piso.

Esto es una ventaja que ninguna otra liga tuvo: **la liga sabe, con datos, a quién draftear y a quién contratar.** Swimmx es la herramienta de scouting del draft.

---

## 8. Riesgos que agregué

| Riesgo | Mitigación |
|---|---|
| Relación laboral encubierta (contratos de servicios) | Asesoría laboral; retainer en nómina; pago por etapa documentado |
| Elegibilidad NCAA de los mejores mexicanos | Calendario fuera de temporada NCAA y revisión con compliance |
| Marcas: "MPSL", "Monterrey Sharks", "Tijuana Pacific", etc. pueden estar registradas | Búsqueda en el IMPI (clases 41, 25, 9) **antes** de imprimir nada |
| "Swimmx" escrito de varias formas (Swimmx / SwimMx) | Unificar la marca antes del dossier |
| Patrocinio en el pesimista (−40%) | Compuertas; el Festival amortigua; no subir a retainer sin firmas |
| Sedes no aptas (50 m, gradas, iluminación de TV) | Auditoría técnica de sedes en 2027 (está en el CAPEX) |

---

## 9. Próximos pasos sugeridos

1. **Validar 5 supuestos que mueven todo el modelo:** precio real de un patrocinador titular (2–3 conversaciones con marcas), aforo real de las 4 sedes, costo de producción (cotizar 2 casas productoras), inscritos posibles al Festival (preguntar a asociaciones estatales) y criterio laboral.
2. **Conversación técnica con la FMN** antes de cualquier anuncio público: aval, jueces, homologación de tiempos y fechas.
3. **Piloto 2027** en una sede con el formato Festival completo: es la prueba de mercado más barata (~$13 M netos: ~$18 M de costo e inversión menos ~$5 M de ingresos).
4. Después: el deck para gobiernos (con el Festival como argumento de turismo) y el deck para marcas.

> Todas las cifras son supuestos de planeación en MXN de 2027, ajustados por inflación de 4.5%, **no cotizaciones**. El modelo existe para cambiarlos y ver el efecto, no para darlos por hechos.
