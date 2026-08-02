# 03 · Envío automático del reporte (mañana, tarde y 10 pm)

Que tu Mac corra el pipeline y mande el mensaje **con el link** solo, a las horas
que quieras. Usamos **launchd** (el agendador de macOS) porque, a diferencia de
cron, sí puede usar la app **Mensajes** para el iMessage.

Son **3 piezas**:

1. `tid_diario.sh` — corre la corrida completa (WHOOP → coach → tarjeta → envío).
2. `com.tidmax.diario.plist` — la dispara a las 7:00, 15:00 y 22:00 (editable).
3. `com.tidmax.tunel.plist` — mantiene vivo el link de Cloudflare.

---

## Paso 1 — Variables

```bash
cd ~/Cosas-Carlos/tid-max/software
cp .tid_env.example ~/.tid_env
# edita ~/.tid_env: pon TID_IMESSAGE_TO y lo que uses
```

## Paso 2 — Instala los dos agentes de launchd

```bash
cd ~/Cosas-Carlos/tid-max/software
chmod +x tid_diario.sh tid_publicar.sh
mkdir -p ~/Library/LaunchAgents
cp launchd/com.tidmax.diario.plist ~/Library/LaunchAgents/
cp launchd/com.tidmax.tunel.plist  ~/Library/LaunchAgents/

launchctl load ~/Library/LaunchAgents/com.tidmax.tunel.plist
launchctl load ~/Library/LaunchAgents/com.tidmax.diario.plist
```

> Si tu usuario NO es `carlosmorenoaguilar`, edita las rutas dentro de los dos
> `.plist` antes de copiarlos.

## Paso 3 — Permisos (una vez)

macOS pedirá permiso la primera vez. En **Ajustes → Privacidad y seguridad**:
- **Automatización** → permite que el script controle **Mensajes** y **Contactos**.
- **Acceso total al disco** → agrega **Mensajes** (para el envío) y, si usas cron algún día, la Terminal.

## Probar sin esperar

```bash
# corre la corrida ya mismo (como lo hará launchd):
./tid_diario.sh && tail -n 30 publico/tid_diario.log

# forzar un disparo del agente:
launchctl start com.tidmax.diario
```

## Cambiar las horas

Edita `~/Library/LaunchAgents/com.tidmax.diario.plist` (bloques `Hour`/`Minute`,
hora local), y recarga:

```bash
launchctl unload ~/Library/LaunchAgents/com.tidmax.diario.plist
launchctl load   ~/Library/LaunchAgents/com.tidmax.diario.plist
```

## Para apagarlo

```bash
launchctl unload ~/Library/LaunchAgents/com.tidmax.diario.plist
launchctl unload ~/Library/LaunchAgents/com.tidmax.tunel.plist
```

---

## Notas importantes

- **La Mac debe estar encendida y con sesión iniciada** a la hora del envío. Si
  está dormida, launchd corre el trabajo **al despertar**. Para el envío de las
  10 pm, deja la Mac despierta o en **Ajustes → Batería → Opciones → "Evitar que
  se duerma"** (o usa `caffeinate`).
- El **link es del túnel** (`trycloudflare`): vive mientras el agente del túnel
  corra. Si se reinicia, la URL cambia, pero `tid_notify.py` la vuelve a leer
  sola de `publico/url.txt`, así que el mensaje siempre lleva la vigente.
- Todo queda logueado en `publico/tid_diario.log`, `publico/launchd.err.log` y
  `publico/tunel.err.log` por si algo falla.
