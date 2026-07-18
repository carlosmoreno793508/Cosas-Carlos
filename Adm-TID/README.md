# Adm TID

Proyecto de administración TID.

## Agente administrador

El proyecto cuenta con un agente de Claude Code, **`adm-tid`** (definido en `.claude/agents/adm-tid.md`), con dos funciones:

1. **Administración** — mantiene las reglas (`reglas.md`) y las acciones pendientes (`pendientes.md`).
2. **Auditoría** — revisa toda la información que se sube al proyecto y registra el resultado en `auditoria.md`.

### Cómo usarlo

Pídele a Claude, por ejemplo:
- *"Usa el agente adm-tid para auditar los archivos que acabo de subir a Adm-TID."*
- *"adm-tid: agrega la regla de que todo dato lleve fuente."*
- *"adm-tid: dame el estado de pendientes."*

## Estructura

```
Adm-TID/
├── README.md
├── reglas.md      # Reglas y acuerdos del proyecto
├── pendientes.md  # Acciones pendientes con estado
├── auditoria.md   # Bitácora de auditorías
├── docs/          # Documentación
└── src/           # Código fuente
```

## Estado

🚧 En desarrollo inicial.
