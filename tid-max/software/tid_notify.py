#!/usr/bin/env python3
"""
tid_notify.py — Notificaciones de TID-MAX al teléfono (Capa 3, entrega).

Toma el reporte del coach (datos/procesado/coach-hoy.json) y arma un mensaje CORTO,
apto para celular, con: semáforo del día, veredicto, sueño, hidratación, nado de hoy y
cuenta regresiva al evento. Lo envía por:
  • Telegram  (gratis, push instantáneo)  -> TID_TELEGRAM_TOKEN + TID_TELEGRAM_CHAT
  • Email     (SMTP)                       -> TID_MAIL_* (abajo)
Sin configuración, hace un ENSAYO (imprime el mensaje sin enviarlo) para que veas cómo queda.

Ideal correrlo cada mañana justo después del pipeline (ver bloque 'cron' al final del archivo).

Uso:
    python tid_agent.py            # genera coach-hoy.json
    python tid_notify.py           # envía por los canales configurados
    python tid_notify.py --dry     # solo imprime el mensaje (no envía)

Variables de entorno (pon las que uses):
    # Telegram (lo más fácil, gratis):
    export TID_TELEGRAM_TOKEN=123456:ABC...      # token del bot (de @BotFather)
    export TID_TELEGRAM_CHAT=987654321           # chat_id de Gael (o del grupo)
    # iMessage (macOS, gratis, sin API): manda el reporte de texto desde la app Mensajes.
    export TID_IMESSAGE_TO="+525512345678"       # número(s), Apple ID o NOMBRE de contacto, con coma
    # Link del tablero (se agrega al final del mensaje de texto en todos los canales):
    export TID_DASHBOARD_URL="https://claude.ai/code/artifact/XXXX"
    # WhatsApp (API oficial de Meta - lo que más usan):
    export TID_WA_TOKEN=EAAG...                  # access token de la app de WhatsApp
    export TID_WA_PHONE_ID=1234567890            # Phone Number ID del número de negocio
    export TID_WA_TO=5215512345678               # celular destino (código país, sin +)
    export TID_WA_TEMPLATE=reporte_diario        # plantilla aprobada (para envío proactivo)
    export TID_WA_LANG=es_MX
    # Email (opcional):
    export TID_MAIL_TO=gael@ejemplo.com
    export TID_MAIL_FROM=coach@ejemplo.com
    export TID_SMTP_HOST=smtp.gmail.com
    export TID_SMTP_PORT=465
    export TID_SMTP_USER=coach@ejemplo.com
    export TID_SMTP_PASS=xxxxxxxxxxxx            # contraseña de app (no la normal)
"""
import os
import sys
import json
import ssl
import smtplib
import urllib.request
import urllib.parse
from email.message import EmailMessage

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COACH_JSON = os.path.join(SCRIPT_DIR, "datos", "procesado", "coach-hoy.json")
SEM_EMOJI = {"verde": "🟢", "amarillo": "🟡", "rojo": "🔴"}


def cargar():
    if not os.path.exists(COACH_JSON):
        sys.exit("No encuentro coach-hoy.json. Corre primero:  python tid_agent.py")
    with open(COACH_JSON, encoding="utf-8") as f:
        return json.load(f)


def fmt_nado(d):
    if not d:
        return None
    ses = " + ".join(
        f"{s.get('hora') or '—'} {s.get('km')}km" for s in d.get("sesiones", []))
    return f"{d.get('tipo')} · {d.get('km_dia')} km" + (f" ({ses})" if ses else "")


def _url_tunel():
    """Lee la URL pública del túnel de Cloudflare (publico/url.txt), que deja escrita
    tid_publicar.sh. Así el mensaje diario lleva el link sin configurar nada a mano."""
    f = os.path.join(SCRIPT_DIR, "publico", "url.txt")
    try:
        if os.path.exists(f):
            return open(f, encoding="utf-8").read().strip()
    except Exception:
        pass
    return ""


def construir_mensaje(p):
    f = p.get("hechos", {})
    pil = p.get("pilares", {})
    sem = p.get("semaforo", "amarillo")
    emoji = SEM_EMOJI.get(sem, "🟡")
    fecha = (p.get("generado_utc") or "")[:10]

    L = [f"🏊 TID-MAX · {p.get('atleta', 'Gael')} — {fecha}",
         f"{emoji} {sem.upper()}  ·  Recovery {f.get('recovery_pct', '—')}%"]
    if f.get("dias_al_evento") is not None:
        L.append(f"⏳ {f['dias_al_evento']} días al evento ({f.get('evento', '')})")
    L.append("")
    if p.get("veredicto"):
        L.append(p["veredicto"])
    L.append("")
    if pil.get("Sueño"):
        L.append(f"😴 Sueño ({f.get('sueno_pct', '—')}%): {pil['Sueño']}")
    if pil.get("Hidratación"):
        L.append(f"💧 Hidratación: {pil['Hidratación']}")
    if pil.get("Nutrición"):
        L.append(f"🍽️ Nutrición: {pil['Nutrición']}")
    nado = fmt_nado(f.get("plan_nado_hoy"))
    if nado:
        L.append(f"🏊 Nado hoy: {nado}")
    alertas = p.get("alertas") or []
    for a in alertas[:2]:
        L.append(f"⚠️ {a}")
    # El túnel vivo (publico/url.txt) manda; TID_DASHBOARD_URL solo si no hay túnel.
    url = _url_tunel() or os.environ.get("TID_DASHBOARD_URL")
    if url:
        L.append("")
        L.append(f"📊 Tablero del día: {url}")
    L.append("")
    L.append("— TID-MAX (orientación de bienestar, no médica)")
    return "\n".join(L)


def _telegram_chats():
    # TID_TELEGRAM_CHAT admite varios destinatarios separados por coma (mamá, Gael, o un grupo)
    return [c.strip() for c in (os.environ.get("TID_TELEGRAM_CHAT") or "").split(",") if c.strip()]


def enviar_telegram(texto):
    token = os.environ.get("TID_TELEGRAM_TOKEN")
    chats = _telegram_chats()
    if not (token and chats):
        return False, "Telegram no configurado"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    oks = 0
    for chat in chats:
        data = urllib.parse.urlencode({"chat_id": chat, "text": texto}).encode()
        try:
            with urllib.request.urlopen(url, data=data, timeout=20) as r:
                oks += 1 if r.status == 200 else 0
        except Exception as e:
            return False, f"Telegram error: {e}"
    return oks == len(chats), f"Telegram enviado a {oks}/{len(chats)}"


def enviar_foto_telegram(png_path, caption=""):
    """Envía una IMAGEN (sendPhoto) a cada chat configurado."""
    token = os.environ.get("TID_TELEGRAM_TOKEN")
    chats = _telegram_chats()
    if not (token and chats):
        return False, "Telegram no configurado"
    if not os.path.exists(png_path):
        return False, f"No existe la imagen: {png_path}"
    with open(png_path, "rb") as fh:
        img = fh.read()
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    boundary = "----tidmaxboundary7d3f"
    oks = 0
    for chat in chats:
        parts = []
        for k, v in (("chat_id", chat), ("caption", caption[:1000])):
            parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"tidmax.png\"\r\n"
            f"Content-Type: image/png\r\n\r\n".encode() + img + b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        body = b"".join(parts)
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                oks += 1 if r.status == 200 else 0
        except Exception as e:
            return False, f"Telegram foto error: {e}"
    return oks == len(chats), f"Foto enviada a {oks}/{len(chats)} por Telegram"


def _es_handle(d):
    import re
    return bool(re.match(r'^[+\d][\d\s\-()]{6,}$', d)) or "@" in d


def _resolver_contacto(nombre):
    """Busca un contacto por nombre en Contactos de macOS y devuelve su teléfono/Apple ID."""
    if sys.platform != "darwin":
        return ""
    import subprocess
    n = nombre.replace('"', "'")
    script = (
        'tell application "Contacts"\n'
        f'  set matches to (people whose name contains "{n}")\n'
        '  if (count of matches) is 0 then return ""\n'
        '  set p to item 1 of matches\n'
        '  try\n    return value of item 1 of (phones of p)\n  end try\n'
        '  try\n    return value of item 1 of (emails of p)\n  end try\n'
        '  return ""\n'
        'end tell'
    )
    try:
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=20)
        return r.stdout.strip()
    except Exception:
        return ""


def _imessage_dests():
    """Resuelve TID_IMESSAGE_TO a una lista de handles (número/Apple ID), traduciendo
    nombres de contacto vía Contactos de macOS. Devuelve (lista, 'ok') o (None, motivo)."""
    entradas = [d.strip() for d in (os.environ.get("TID_IMESSAGE_TO") or "").split(",") if d.strip()]
    if not entradas:
        return None, "iMessage no configurado"
    if sys.platform != "darwin":
        return None, "iMessage solo corre en macOS (tu Mac)"
    dests = []
    for e in entradas:
        if _es_handle(e):
            dests.append(e)
        else:
            h = _resolver_contacto(e)
            if not h:
                return None, f"No encontré el contacto '{e}' en Contactos"
            print(f"(Contacto '{e}' → {h})")
            dests.append(h)
    return dests, "ok"


def enviar_imessage_texto(texto):
    """Envía el reporte como TEXTO por iMessage (SIN adjunto). El texto siempre entrega
    —a diferencia del adjunto, que la caja de arena de Mensajes suele marcar 'No entregado'—
    así que este es el canal recomendado para el envío diario con el link del tablero."""
    import subprocess
    dests, motivo = _imessage_dests()
    if dests is None:
        return False, motivo
    # AppleScript: cada línea como literal unido con `linefeed` para conservar el formato.
    lineas = [ln.replace("\\", " ").replace('"', "'") for ln in (texto or "").split("\n")]
    msg_expr = " & linefeed & ".join(f'"{ln}"' for ln in lineas) or '""'
    oks = 0
    for to in dests:
        script = (
            'tell application "Messages"\n'
            '  set svc to 1st service whose service type = iMessage\n'
            f'  set toBuddy to buddy "{to}" of svc\n'
            f'  send {msg_expr} to toBuddy\n'
            'end tell'
        )
        try:
            r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)
            if r.returncode == 0:
                oks += 1
            else:
                return False, f"iMessage texto falló para {to}: {r.stderr.strip()[:120]}"
        except Exception as e:
            return False, f"iMessage texto error: {e}"
    return oks == len(dests), f"iMessage (texto) enviado a {oks}/{len(dests)}"


def enviar_imessage(png_path, caption=""):
    """iMessage vía la app Mensajes de macOS (AppleScript). GRATIS. SOLO corre EN TU MAC,
    con Mensajes con sesión de iMessage. TID_IMESSAGE_TO admite números/Apple ID O nombres
    de contacto (los resuelve de tus Contactos de Apple), separados por coma."""
    import subprocess
    if not os.path.exists(png_path):
        return False, f"No existe la imagen: {png_path}"
    dests, motivo = _imessage_dests()
    if dests is None:
        return False, motivo
    cap = (caption or "").replace("\\", " ").replace('"', "'").replace("\n", " · ")
    png_abs = os.path.abspath(png_path)
    # Mensajes.app corre en sandbox: si no puede LEER el archivo de origen, el
    # adjunto se manda vacio y llega como "No entregado" (el texto si entra
    # porque no lee ningun archivo). Copiamos la imagen a una ruta limpia
    # (/tmp, legible) para bajar la probabilidad de ese fallo. El fix definitivo
    # es dar "Acceso total al disco" a Mensajes en Ajustes del Sistema.
    try:
        import shutil
        safe_png = "/tmp/tid-status.png"
        shutil.copy(png_abs, safe_png)
        png_abs = safe_png
    except Exception:
        pass
    oks = 0
    for to in dests:
        # Mandamos la IMAGEN primero y le damos tiempo a subir ANTES del texto.
        # Si se manda el adjunto pegado al texto, iMessage a veces lo marca
        # "No entregado" porque el script suelta el mensaje antes de que el
        # archivo termine de subir. Con la imagen sola + delay entrega parejo.
        script = (
            'tell application "Messages"\n'
            '  set svc to 1st service whose service type = iMessage\n'
            f'  set toBuddy to buddy "{to}" of svc\n'
            f'  send (POSIX file "{png_abs}") to toBuddy\n'
            '  delay 4\n'
            f'  send "{cap}" to toBuddy\n'
            '  delay 1\n'
            'end tell'
        )
        try:
            r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=45)
            if r.returncode == 0:
                oks += 1
            else:
                return False, f"iMessage falló para {to}: {r.stderr.strip()[:120]}"
        except Exception as e:
            return False, f"iMessage error: {e}"
    return oks == len(dests), f"iMessage enviado a {oks}/{len(dests)}"


def enviar_whatsapp(texto):
    """WhatsApp vía la API oficial de Meta (WhatsApp Cloud API).
    Mensaje libre solo funciona dentro de la ventana de 24 h tras un mensaje del usuario;
    para el reporte diario proactivo se usa una PLANTILLA aprobada (TID_WA_TEMPLATE) con un
    parámetro de cuerpo que recibe el texto."""
    token = os.environ.get("TID_WA_TOKEN")
    phone_id = os.environ.get("TID_WA_PHONE_ID")
    to = os.environ.get("TID_WA_TO")
    if not (token and phone_id and to):
        return False, "WhatsApp no configurado"
    template = os.environ.get("TID_WA_TEMPLATE")
    lang = os.environ.get("TID_WA_LANG", "es_MX")
    url = f"https://graph.facebook.com/v21.0/{phone_id}/messages"
    if template:
        payload = {"messaging_product": "whatsapp", "to": to, "type": "template",
                   "template": {"name": template, "language": {"code": lang},
                                "components": [{"type": "body",
                                                "parameters": [{"type": "text", "text": texto}]}]}}
    else:
        payload = {"messaging_product": "whatsapp", "to": to, "type": "text",
                   "text": {"body": texto}}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {token}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            ok = r.status in (200, 201)
        return ok, "WhatsApp enviado" if ok else "WhatsApp falló"
    except Exception as e:
        return False, f"WhatsApp error: {e}"


def enviar_email(texto):
    to = os.environ.get("TID_MAIL_TO")
    frm = os.environ.get("TID_MAIL_FROM")
    host = os.environ.get("TID_SMTP_HOST")
    user = os.environ.get("TID_SMTP_USER")
    pw = os.environ.get("TID_SMTP_PASS")
    port = int(os.environ.get("TID_SMTP_PORT", "465"))
    if not (to and frm and host and user and pw):
        return False, "Email no configurado"
    msg = EmailMessage()
    msg["Subject"] = "🏊 TID-MAX · Reporte del día"
    msg["From"] = frm
    msg["To"] = to
    msg.set_content(texto)
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=ctx, timeout=25) as s:
            s.login(user, pw)
            s.send_message(msg)
        return True, f"Email enviado a {to}"
    except Exception as e:
        return False, f"Email error: {e}"


def main():
    p = cargar()
    texto = construir_mensaje(p)
    print("\n----- MENSAJE -----\n" + texto + "\n-------------------")

    if "--dry" in sys.argv:
        print("\n(--dry: no se envió nada.)")
        return

    # --foto: manda la IMAGEN del día (cliente.png) por Telegram, con el texto como pie
    if "--foto" in sys.argv:
        i = sys.argv.index("--foto")
        png = sys.argv[i + 1] if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("-") \
            else os.path.join(SCRIPT_DIR, "cliente.png")
        cap = f"🏊 TID-MAX · {p.get('atleta', 'Gael')} — {(p.get('generado_utc') or '')[:10]}\n" \
              f"{SEM_EMOJI.get(p.get('semaforo'), '🟡')} {p.get('veredicto', '')}"
        algun = False
        for fn in (enviar_foto_telegram, enviar_imessage):
            ok, detalle = fn(png, cap)
            if "no configurado" in detalle:
                continue
            algun = True
            print(("✅ " if ok else "❌ ") + detalle)
        if not algun:
            print("Ningún canal de imagen configurado. Opciones:\n"
                  "  • Telegram: TID_TELEGRAM_TOKEN + TID_TELEGRAM_CHAT (varios chats con coma)\n"
                  "  • iMessage (macOS, gratis): TID_IMESSAGE_TO=\"+52155...,mamá@icloud.com\"")
        return

    canales = [enviar_telegram, enviar_imessage_texto, enviar_whatsapp, enviar_email]
    algun_intento = False
    for fn in canales:
        ok, detalle = fn(texto)
        if "no configurado" in detalle:
            continue
        algun_intento = True
        print(("✅ " if ok else "❌ ") + detalle)
    if not algun_intento:
        print("\nNingún canal configurado todavía — fue un ensayo. Configura Telegram o Email "
              "(ver variables arriba) y vuelve a correr.")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Reporte diario a la mamá de Gael y a Gael (imagen por Telegram) — cron 7:00 am.
# 1) Crea un bot con @BotFather -> TID_TELEGRAM_TOKEN.
# 2) Crea un grupo de Telegram con la mamá + Gael (+ el bot), o usa sus chat_id
#    separados por coma en TID_TELEGRAM_CHAT.
# 3) crontab -e  y agrega (ajusta la ruta y exporta las variables en el script/env):
#   0 7 * * *  cd ~/Cosas-Carlos/tid-max/software && python3 whoop_sync.py && \
#              python3 tid_data.py && python3 tid_agent.py && \
#              python3 tid_cliente.py && python3 tid_notify.py
# RECOMENDADO: envío de TEXTO + LINK del tablero (TID_DASHBOARD_URL). El texto siempre
# entrega por iMessage; el link abre la tarjeta completa. Es el canal más confiable.
# Sin flags manda texto por los canales configurados (Telegram, iMessage, WhatsApp, correo).
# Con --foto intenta la IMAGEN cliente.png (adjunto: frágil en iMessage; ok en Telegram).
# (macOS: da permiso de "Acceso total al disco" a cron/Terminal.)
# ---------------------------------------------------------------------------
