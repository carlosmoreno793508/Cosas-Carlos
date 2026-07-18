# Bitácora de auditoría — Ámbito Proyecto

> El agente `adm-tid` registra aquí cada auditoría de información del proyecto nuevo (sistema de ventas).
> No se borran entradas: solo se agregan. Orden cronológico (más reciente arriba).

---

### [2026-07-18] Registro de decisiones raíz D1–D3
- **Veredicto**: ✅ Aprobado
- **Revisado**: decisiones de Carlos sobre el modelo del proyecto.
- **Hallazgos**:
  - D1 = Híbrido (software + servicio). D2 = Híbrido (plataforma + capa propia). D3 = Opción A (fabricantes/maquilas).
  - Piloto candidato: TID o Astute → se abre **D4** (elegir empresa piloto). Falta confirmar el giro exacto de TID y de Astute para poder redactar propuesta de valor y VSL con datos reales.
  - Decisiones consistentes entre sí y con la tesis vertical del proyecto (no violan reglas).
- **Acciones generadas**: D4 (elegir piloto). Habilita P3 (propuesta de valor) y P10 (formulario de calificación).

### [2026-07-18] Auditoría de transcripción del VSL de Zolutium
- **Veredicto**: ✅ Aprobado
- **Revisado**: IMG_0100–0104 (transcripción del video de Zolutium, 3:17 min). Integrada a `docs/expediente-competitivo.md` (sección 6d).
- **Hallazgos**:
  - Guion reconstruido: fórmula VSL "gancho de miedo (97% pierde clientes) → demo con marca famosa → pruébalo gratis".
  - **El video usa marcas de terceros (Chevrolet, Maserati, McDonald's, Fridays, PraxMED) como "ejemplos"** — muy probablemente demos genéricas, no clientes reales. Posible uso no autorizado de marcas + prueba social de baja fiabilidad. Se marca como no verificado.
  - La estadística "97%" es claim de marketing sin fuente (R2).
  - Nota de contexto: las capturas incluyen notificaciones personales de otra app (MeetMobile, resultados de natación) ajenas al análisis; se ignoran, no son dato del proyecto.
- **Acciones generadas**: Ninguna nueva.

### [2026-07-18] Auditoría de demo/reel de Zolutium (vertical salud)
- **Veredicto**: ⚠️ Aprobado con observaciones
- **Revisado**: IMG_0095 (captura de video/reel de Zolutium, demo para "PraxMED Centros Médicos", asistente IA "Tatiana"). Integrada a `docs/expediente-competitivo.md` (sección 6c).
- **Hallazgos**:
  - Zolutium hace **demos verticalizadas** (aquí, salud/médico) igual que LeadSales — pero ninguno cubre el vertical industrial/manufactura.
  - **Inconsistencia de cifras confirmada**: este material dice "+11.000 negocios", el sitio decía "+30.000 negocios" y "103,021 usuarios", y el anuncio de FB decía "+11,000". Tres cifras distintas → claim de marketing no confiable. Refuerza P9.
- **Acciones generadas**: Ninguna nueva (refuerza P9, ya abierto).

### [2026-07-18] Auditoría de 3 capturas de casos de éxito de LeadSales (YouTube)
- **Veredicto**: ✅ Aprobado
- **Revisado**: IMG_0092–0094 (capturas de videos del canal oficial "Leadsales - CRM para WhatsApp", 29 jul 2025). Integradas a `docs/expediente-competitivo.md` (sección 6b). Además, Carlos aportó un 4º enlace de YouTube (`youtu.be/7UJyJ4SEGks`) que no pudo abrirse (red restringida).
- **Hallazgos**:
  - Los videos son **testimonios/casos de éxito por vertical**: salón de belleza, inmobiliaria, educación. Ninguno industrial → refuerza el vacío de manufactura también en marketing de contenidos.
  - Cifras de los casos ("300%", "10x", "+60%") son claims de marketing del competidor, registradas como tales (R2).
  - LeadSales usa dominio de tracking propio `leadsal.es` para YouTube.
  - Esto **resuelve P7** (contenido de videos aportado por Carlos vía capturas). El 4º video queda documentado pero sin analizar por falta de acceso.
- **Acciones generadas**: P7 marcado como Hecho. Sin pendientes nuevos.

### [2026-07-18] Auditoría de 40 capturas de competencia (LeadSales en vivo + Zolutium en vivo)
- **Veredicto**: ⚠️ Aprobado con observaciones
- **Revisado**: 40 imágenes (IMG_0047 a IMG_0088, con salto en 0076 y 0080) aportadas por Carlos, correspondientes a navegación real en vivo de `lp.leadsales.io`, `es.typeform.com` (formulario de calificación de LeadSales) y `zolutium.com`. Todo consolidado en `docs/expediente-competitivo.md`.
- **Hallazgos**:
  - **32 imágenes de LeadSales** y **8 imágenes de Zolutium**, todas con fuente verificable (navegación en vivo por Carlos), a diferencia del perfil preliminar anterior de LeadSales que se basaba en conocimiento general del modelo. Esto **resuelve P6**.
  - Precios exactos de LeadSales confirmados con fuente: Plan Básico $2,362.92 MXN/mes (sin IA), Plan Profesional desde $3,239.88 MXN/mes (4 usuarios, 20,000 conversaciones), Plan Avanzado desde $6,016.92 MXN/mes (5 usuarios, 50,000 conversaciones). Ambos planes superiores incluyen "Lead Agent" (IA).
  - LeadSales confirma explícitamente que su Lead Agent **no lee imágenes, audio ni documentos** del prospecto (solo texto) — dato funcional relevante para diferenciación.
  - El formulario de calificación de leads de LeadSales trata "Manufactura" como una sola categoría junto con "Moda y Textil", sin distinguir comprador industrial (OEM/EMS/Tier 1) — confirma con evidencia directa el vacío vertical ya sospechado.
  - Zolutium (sitio `zolutium.com`, distinto del dominio `zolutium-es.com` visto en el anuncio auditado antes) **no muestra precios ni planes** en ninguna de las 8 capturas; solo CTAs de demo y countdowns de urgencia.
  - **Hallazgo de integridad relevante en Zolutium**: el mismo testimonio, palabra por palabra, aparece atribuido a dos personas y países distintos (Hermes C. de Panamá y Fernando P. de Ecuador), con titulares que citan cifras distintas (85% vs. "duplicamos" ventas). Se marca explícitamente como prueba social de baja fiabilidad, no usable como benchmark.
  - Cifras de Zolutium ("Total 103,021 usuarios" vs. "+30,000 negocios nos eligen", "-85% curiosos", "+50% ventas", "edificio propio... única compañía global de IA") son **claims de marketing no verificados de forma independiente**, registrados como tales (cumple R2).
  - **Dato sensible detectado**: las capturas IMG_0066 e IMG_0067 (formulario de LeadSales) contienen el correo y el número de WhatsApp personal de Carlos, introducidos al probar el flujo del competidor. Es dato propio (no de terceros) de sensibilidad baja; no se reprodujo en el expediente, solo se señala su presencia en las capturas fuente (cumple R3).
  - LeadSales compra la keyword "zolutium" en Google Ads — se posiciona activamente en SEM contra su competidor directo.
- **Acciones generadas**: P6 marcado como Hecho (verificación completada). Se agregan P8, P9, P10, P11, P12 (ver pendientes.md).

### [2026-07-18] Auditoría de perfil competitivo LeadSales
- **Veredicto**: ⚠️ Aprobado con observaciones
- **Revisado**: `docs/competidor-leadsales.md` (competidor Lead Agent v3) y los 3 enlaces de YouTube aportados.
- **Hallazgos**:
  - **Los 4 enlaces (landing LeadSales + 3 videos) NO pudieron abrirse** desde este entorno (red restringida, 403/000). No hay captura en vivo.
  - El perfil de LeadSales se basa en **conocimiento general del modelo**, no en la fuente aportada → NO cumple plenamente R2 (fuente verificable). Registrado explícitamente como preliminar/sin verificar.
  - Los 3 videos de YouTube quedan **sin analizar** por falta de acceso; se requiere que Carlos aporte título/contenido.
- **Acciones generadas**: P6 (verificar landing LeadSales), P7 (aportar contenido de los 3 videos).

### [2026-07-18] Auditoría de anuncio Zolutium (inteligencia competitiva)
- **Veredicto**: ✅ Aprobado
- **Revisado**: captura de anuncio de Facebook de Zolutium.es aportada por Carlos → `docs/assets/anuncio-zolutium-fb.png` y `docs/analisis-anuncio-zolutium.md`.
- **Hallazgos**:
  - Fuente verificable (anuncio público de perfil verificado). Cumple R2 (fuente indicada).
  - La imagen es un anuncio público; contiene rostro de modelo y nombres de comentaristas → dato personal de terceros, sin sensibilidad crítica pero se conserva solo como evidencia de análisis (R3 respetada, no hay credenciales).
  - Cifras del anuncio ("+10.000 citas", "1,287 reacciones") son **claims de marketing del competidor**, no verificadas de forma independiente. Registradas como tales, no como hechos.
- **Acciones generadas**: P3, P4, P5 (ver pendientes).

### [2026-07-18] Inicialización del proyecto
- **Veredicto**: ✅ Aprobado
- **Revisado**: estructura base del proyecto (`README.md`, `reglas.md`, `pendientes.md`, `auditoria.md`, carpetas `docs/` y `src/`).
- **Hallazgos**: Sin hallazgos. Estructura de administración y auditoría lista para operar.
- **Acciones generadas**: P1 (definir alcance), P2 (cargar primer set de información).
