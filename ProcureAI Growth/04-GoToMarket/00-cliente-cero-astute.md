# Cliente Cero — Astute Electronics (piloto experimental)

> Decisión de Carlos (2026-07-12): el cliente cero experimental es **Astute Electronics**, distribuidor de componentes electrónicos. Carlos trabaja actualmente ahí, lo que da acceso directo para correr el experimento.

---

## Por qué Astute es el cliente cero ideal

- **Acceso interno:** Carlos está dentro → puede correr el piloto sin fricción de ventas, con datos reales y feedback inmediato.
- **Encaja el ICP:** distribuidor de componentes electrónicos con necesidad real de abrir cuentas nuevas (justo el dolor del concepto original).
- **Vertical con estudio hecho:** ya existe el estudio "Astute / Electronic Market Study USA" (repo `Astute`) → inteligencia de arranque.
- **Prueba de valor barata:** validamos el motor operativo con costo mínimo antes de venderlo a terceros.

## Cómo lo estructuramos (reglas del piloto)

Alineado con el enfoque de Gemini (proteger reputación) y con buena higiene de conflicto de interés:

1. **Dominios secundarios, nunca el principal.** No tocamos el dominio corporativo de Astute. Usamos dominios de prospección aparte (p.ej. `try-astute…`, `astute-supply…` — a confirmar con ellos).
2. **Autorización clara.** Aunque Carlos trabaja ahí, el piloto debe correrse con visto bueno de quien corresponda en Astute (evita problemas y permite usar la marca en el outreach).
3. **Separación de activos.** La base de datos, el motor de señales y los aprendizajes (SOPs) son **de ProcureAI Growth (el proyecto)**, no de Astute. Astute es el caso de uso; el activo defensible se queda en el proyecto.
4. **Métrica de éxito del piloto:** nº de reuniones calificadas agendadas con compradores reales (buyers / commodity managers) en 6–8 semanas.

## Qué probamos con Astute (hipótesis)

- ¿El motor de cold email + inteligencia genera **reuniones reales** con compradores de línea blanca / automotriz / electrónica?
- ¿El copy basado en dolores del sector (EOL, escasez, segunda fuente, aranceles/nearshoring) convierte mejor que un pitch genérico?
- ¿Cuántos dominios/cuentas y qué volumen se necesitan para sostener N reuniones/mes?

## Objetivo del piloto

- **Semanas 1–3:** montar infraestructura (dominios + warm-up) y listas segmentadas desde el estudio Astute + Apollo.
- **Semanas 4–8:** operar campañas, agendar las primeras reuniones, documentar todo en SOPs (Loom).
- **Entregable:** un caso de éxito propio con números reales → base para vender a los otros distribuidores (TTI, Arrow, Avnet, Future, Mouser, DigiKey) y, después, al lado comprador.

## Fase 2 (mes 3): lado comprador

Una vez validado el lado proveedor con Astute, metemos el lado comprador (buyers / procurement de los OEMs objetivo) con inteligencia gratuita + comunidad, cerrando el efecto de red.
