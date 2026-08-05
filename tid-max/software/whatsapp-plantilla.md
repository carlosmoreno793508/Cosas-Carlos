# Plantilla de WhatsApp para el reporte diario (TID-MAX)

Para mandar el reporte **proactivo cada mañana** (sin que Gael escriba primero), WhatsApp
exige una **plantilla aprobada** por Meta. Aquí está lista para registrar.

> ⚠️ Truco de aprobación: una plantilla cuyo cuerpo es **solo** una variable (`{{1}}`) suele
> rechazarse por "genérica". Por eso lleva **encabezado y pie fijos** + una sola variable en el
> cuerpo. Así se aprueba fácil y funciona tal cual con `tid_notify.py` (que manda 1 parámetro).

## Datos de la plantilla

| Campo | Valor |
|---|---|
| **Nombre** | `reporte_diario` |
| **Categoría** | `UTILITY` (Utilidad) — NO marketing |
| **Idioma** | Español (México) — `es_MX` |

**Encabezado** (tipo *Texto*, fijo):
```
🏊 TID-MAX · Reporte del día
```

**Cuerpo** (con 1 variable):
```
{{1}}
```

**Pie de página** (fijo):
```
Orientación de bienestar, no médica.
```

**Ejemplo para el campo de muestra de `{{1}}`** (Meta lo pide para revisar):
```
Gael — 2026-07-30
🟡 AMARILLO · Recovery 54%
Precaución: modera hoy, entrena con cabeza.
Sueño 81%: apunta a 8-9 h. Hidrátate con electrolitos. Nado hoy: sencilla 4.5 km (15:30).
```

## Pasos para registrarla
1. Entra a **business.facebook.com** → **WhatsApp Manager** → **Plantillas de mensajes** → **Crear plantilla**.
2. Categoría **Utilidad**, idioma **Español (MX)**, nombre **reporte_diario**.
3. Pega el **encabezado**, el **cuerpo** (`{{1}}`) y el **pie** de arriba.
4. En "contenido de muestra" pega el ejemplo de `{{1}}`.
5. **Enviar a revisión** (aprobación: de minutos a ~1 día).

## Cuando esté aprobada — variables en tu Mac
```bash
export TID_WA_TOKEN=EAAG...           # token de la app de WhatsApp
export TID_WA_PHONE_ID=1234567890     # Phone Number ID del número de negocio
export TID_WA_TO=5215512345678        # celular destino (código país 52, sin +)
export TID_WA_TEMPLATE=reporte_diario # el nombre de la plantilla
export TID_WA_LANG=es_MX
python tid_notify.py                  # ¡manda el reporte por WhatsApp!
```

> Nota: sin `TID_WA_TEMPLATE`, el envío solo funciona dentro de la **ventana de 24 h** después
> de que el usuario te escribe (mensaje libre). Con la plantilla, puedes mandarlo **proactivo**
> cualquier mañana.
