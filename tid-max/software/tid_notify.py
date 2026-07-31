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
    L.append("")
    L.append("— TID-MAX (orientación de bienestar, no médica)")
    return "\n".join(L)


def enviar_telegram(texto):
    token = os.environ.get("TID_TELEGRAM_TOKEN")
    chat = os.environ.get("TID_TELEGRAM_CHAT")
    if not (token and chat):
        return False, "Telegram no configurado"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat, "text": texto}).encode()
    try:
        with urllib.request.urlopen(url, data=data, timeout=20) as r:
            ok = r.status == 200
        return ok, "Telegram enviado" if ok else "Telegram falló"
    except Exception as e:
        return False, f"Telegram error: {e}"


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

    canales = [enviar_telegram, enviar_whatsapp, enviar_email]
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
# Reporte automático cada mañana (macOS/Linux) con cron. Ejemplo a las 7:00 am:
#   crontab -e   y agrega (ajusta la ruta):
#   0 7 * * *  cd ~/Cosas-Carlos/tid-max/software && /usr/bin/python3 whoop_sync.py && \
#              python3 tid_data.py && python3 tid_agent.py && python3 tid_notify.py
# (En macOS puede requerir dar permiso de "Acceso total al disco" a cron/Terminal.)
# ---------------------------------------------------------------------------
