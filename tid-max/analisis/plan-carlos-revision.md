# Revisión del plan de carrera de Carlos (atleta #2)

**Fecha:** 5-ago-2026 · **Coach:** IA de TID-MAX · **Revisor:** Carlos (tú)
**Objetivos:** medio maratón 11-oct-2026 · maratón ~13-dic-2026
**Punto de partida:** nivel bajo, retomando tras tiempo sin correr · reloj **Polar**

---

## Qué generó el coach IA

- **Perfil:** `software/perfil-carlos.json` — atleta #2, separado de Gael. Datos de FC aún vacíos (ver abajo).
- **Plan periodizado (19 semanas):** `software/plan-macro-carlos.json` — de hoy al maratón, con el medio del 11-oct integrado como test de forma.

**Forma del plan:** reconstruir durabilidad → base aeróbica → construcción (medio) → bloque específico de maratón → taper. 80/20 (fácil/duro), subidas de ~10%/semana, **semanas de descarga** cada 3-4, y freno por **ACWR** para no lesionarte.

---

## Mi lectura honesta (lo que tú revisas)

### 🟢 Lo que está bien planteado
- **El medio del 11-oct es realista** como test: ~9-10 semanas dan para llegar a correr 21 km cómodo desde una base baja, si eres consistente. Lo tratamos como *terminar fuerte*, no PR.
- **Empezar con run-walk** (semanas 1-2) es lo correcto para no romperte tendones/tibias al arrancar. El limitante de un corredor que retoma **no es el pulmón, son las articulaciones y tejidos** — por eso subimos volumen despacio.
- **Los largos crecen escalonado** (5→32 km) con descargas intercaladas, que es como se construye un maratón sin lesión.

### 🟡 Mi bandera principal — el maratón de diciembre
Un **maratón a ~19 semanas partiendo de base baja es agresivo.** Se puede terminar, pero con dos condiciones:
1. **Consistencia real** — si faltan semanas por trabajo/viajes/molestias, el bloque de maratón (oct-nov) es el que sufre y el riesgo de lesión sube.
2. **Correrlo para TERMINAR**, no para un tiempo. Ritmo conservador desde el km 1, comer/beber temprano. La meta es cruzar con energía.

**Regla de seguridad que propongo:** si para finales de septiembre (rumbo al medio) **no estás corriendo 16 km cómodo**, el maratón de diciembre pasa a "correr/caminar para terminar" o lo recorremos a ene/feb. **La salud manda sobre el calendario.** Eso ya quedó anotado como `_flag` en tu perfil.

### 🔴 Lo que necesito para afinar (no frena el plan, sí la precisión)
El plan de **volumen/semanas ya está** y no depende de tu FC. Pero para prescribir **intensidad por zonas** (y no "a ojo") necesito, del Polar o de ti:
1. **Edad**
2. **Peso**
3. **FC en reposo** (el Polar la da al despertar)
4. Idealmente, **FC máxima real** de una salida dura (o un test de campo de 20 min)

Mientras tanto, la intensidad va por **sensación** (poder-conversar = fácil; frases cortas = tempo) y por las **zonas automáticas del Polar**. Cuando lleguen esos datos, recalibro las zonas medidas (VT1/VT2), igual que hicimos con Gael.

**Fecha del maratón:** la asumí **13-dic**. Si es otra, ajusto el taper en 2 minutos (mueve las últimas 2-3 semanas).

---

## Cómo se conecta al ecosistema
- Tu Polar es la fuente de datos (no WHOOP — ese es solo de Gael, y su token de sincronización no se toca).
- Tu comida (como el desayuno de hoy) se trackea a **tu** perfil de corredor, aparte del `data.json` de Gael, cuando montemos tu tablero.
- El coach IA usa `deportes/running.json` como "lente": te habla como corredor, prioriza ACWR y zonas de FC, y en taper prioriza **llegar fresco**.

---

## Siguiente paso (cuando quieras)
1. Me pasas **edad, peso, FC reposo** (y el **modelo del Polar** — no me llegó la foto en este chat) → cierro tus zonas de FC.
2. Confirmas la **fecha exacta del maratón** → ajusto el taper.
3. Montamos tu **tablero de corredor** (igual que el de Gael pero con tus datos del Polar).
