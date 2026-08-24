# Eventos objetivo por atleta

Cada atleta captura su **evento objetivo** (próxima competencia) desde la app:

`app → Evento objetivo → Nuevo evento` → `POST /api/evento` con su **token de sesión**.

El endpoint guarda aquí un archivo por persona:

```
eventos/<slug>.json
```

El driver del pipeline (`tid_multi.py`) copia ese archivo a la carpeta aislada del atleta
como `evento.json`, que es lo que `build_evento` (en `tid_data.py`) lee para calcular los
**días al evento** y la **fase** (carga / taper / pico).

- Es **por-atleta**: el evento de uno nunca pisa el de otro (a diferencia del `evento.json`
  global de `software/`, que quedó como respaldo legacy).
- **Quitar el evento**: cuando ya no queda ninguna competencia futura, la app manda `evento: null`
  y el archivo se marca `"_vaciado": true` → el atleta queda **sin evento** (no se muestra).

Formato de un evento activo:

```json
{
  "slug": "gael-moreno",
  "nombre": "Nacional de Natación 2027",
  "tipo_deporte": "natacion",
  "prioridad": "A",
  "sede": "Ciudad de México, MX",
  "fecha_inicio": "2027-03-15",
  "fecha_fin": "2027-03-19",
  "fecha_viaje": "2027-03-12",
  "meta": "Llegar afinado al pico",
  "actualizado": "2026-08-24T03:40:00.000Z"
}
```
