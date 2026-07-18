# Reglas — Ámbito TID (unidad de negocio)

> Reglas y acuerdos de la unidad de negocio TID. El agente `adm-tid` las mantiene y verifica.
> No se elimina una regla: se marca como derogada con fecha.

| # | Regla | Fecha alta | Estado |
|---|-------|-----------|--------|
| T1 | Toda información de TID que se suba debe pasar por auditoría del agente `adm-tid` antes de darse por válida. | 2026-07-18 | Vigente |
| T2 | Ninguna cifra o dato clave se registra sin indicar su fuente. | 2026-07-18 | Vigente |
| T3 | No se suben credenciales, tokens ni datos personales sensibles al repositorio. | 2026-07-18 | Vigente |
| T4 | Los datos de contactos/empresas se usan solo para fines B2B legítimos y conforme a las políticas de las fuentes (Apollo, ZoomInfo, etc.). | 2026-07-18 | Vigente |

## Cómo agregar una regla

Nueva fila con prefijo `T` y número consecutivo, la regla, fecha de alta (`date +%F`) y estado `Vigente`.
