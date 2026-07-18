# Adm TID

Proyecto de administración TID.

## Agente administrador

El proyecto cuenta con un agente de Claude Code, **`adm-tid`** (definido en `.claude/agents/adm-tid.md`), con dos funciones:

1. **Administración** — mantiene las reglas (`reglas.md`) y las acciones pendientes (`pendientes.md`).
2. **Auditoría** — revisa toda la información que se sube y registra el resultado en `auditoria.md`.

El mismo agente **divide sus labores en dos ámbitos independientes** (no mezcla información entre ellos):

- **TID** (`Adm-TID/tid/`) — la unidad de negocio existente.
- **Proyecto** (`Adm-TID/proyecto/`) — el proyecto/producto nuevo (sistema de ventas).

### Cómo usarlo

Indícale siempre el ámbito. Por ejemplo:
- *"adm-tid: audita en el ámbito **proyecto** los archivos que subí."*
- *"adm-tid: en **TID**, agrega la regla de que todo dato lleve fuente."*
- *"adm-tid: dame el estado de pendientes de **TID**."*

Si no indicas ámbito, el agente te preguntará a cuál corresponde.

## Estructura

```
Adm-TID/
├── README.md
├── tid/               # Ámbito TID (unidad de negocio existente)
│   ├── reglas.md
│   ├── pendientes.md
│   └── auditoria.md
├── proyecto/          # Ámbito Proyecto (sistema de ventas nuevo)
│   ├── reglas.md
│   ├── pendientes.md
│   └── auditoria.md
├── docs/              # Documentación
└── src/               # Código fuente
```

## Estado

🚧 En desarrollo inicial.
