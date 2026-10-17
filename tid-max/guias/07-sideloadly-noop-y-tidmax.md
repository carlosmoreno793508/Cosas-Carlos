# Guía 07 — Sideloadly: instalar NOOP (analizar) + TID-MAX nativa (beta)

**Objetivo:** (1) meter **NOOP** al iPhone para estudiar sus gráficas/métricas/estructura y, de paso,
destrabar WHOOP gratis + R-R crudo para Gael; (2) meter **TID-MAX nativa** para el beta.

> **La diferencia clave entre las dos:**
> - **NOOP** ya publica un **`.ipa` compilado** → Sideloadly lo firma e instala. **No necesitas Mac.**
> - **TID-MAX** **no** tiene `.ipa`. Hay que **compilarlo primero en una Mac con Xcode** (un `.ipa` de iOS
>   no se puede generar en Windows ni en la nube). Sideloadly **instala** `.ipa`, no los crea.

---

## Parte 0 — Lo que necesitas (una vez)

- [ ] Una **computadora** (Mac **o** Windows) con **Sideloadly** instalado (https://sideloadly.io).
- [ ] Un **Apple ID** (gratis sirve; ver límites abajo).
- [ ] El **iPhone** + su **cable** (la primera vez es por cable; luego puede ser por Wi-Fi).
- [ ] (Solo TID-MAX) una **Mac con Xcode** para generar el `.ipa` **una vez**.

**Límites del Apple ID GRATIS (son de Apple, no de Sideloadly):**
- La app **caduca a los 7 días** (hay que re-firmar) · máximo **3 apps** sideloadeadas a la vez ·
  máximo **10 app-IDs por semana**.
- **Apple Developer ($99 USD/año):** la app dura **1 año** y permite más apps. Para beta vale la pena.

---

## Parte A — NOOP (para ANALIZAR + Gael) · **sin Mac**

1. En el iPhone o la compu, abre el **GitHub de NOOP → Releases**: https://github.com/ryanbr/noop/releases
2. Baja el **`.ipa` de iOS**. Si el release estable no lista `.ipa`, usa el de **"NOOP Staging"**:
   **`NOOP-ios-unsigned-v12.1.0.ipa`** (es *unsigned* a propósito; Sideloadly lo firma al instalar).
   - ⚠️ Es un build **de pruebas (pre-release)** y usa el **bundle ID oficial**: si ya tuvieras NOOP
     instalada, lo **reemplaza y comparte sus datos** → haz respaldo antes si aplica. (No es el caso de Gael si es primera vez.)
3. Abre **Sideloadly** → conecta el iPhone por cable → arrastra el **`.ipa`** a la ventana.
4. Escribe tu **Apple ID** (Sideloadly pide la contraseña para firmar; si tienes 2FA, usa una
   **contraseña específica de app** de appleid.apple.com). **No me pegues esa contraseña en el chat.**
5. Clic en **Start**. Al terminar, en el iPhone:
   **Ajustes → General → VPN y gestión de dispositivos** → **confía** en tu perfil de desarrollador.
6. Abre **NOOP**. Para ver **gráficas reales** (no solo pantallas vacías): conecta el **strap WHOOP por
   Bluetooth** o **importa CSVs de WHOOP** (NOOP lee `physiological_cycles.csv`, `sleeps.csv`,
   `workouts.csv`). Para solo estudiar la **estructura/estética**, con abrirla basta.

> Qué mirar para nuestro análisis: los **orbes de llenado líquido** (Charge/Effort/Rest), el **cielo
> vivo** de fondo, las **tarjetas customizables** de Hoy, y las **pantallas de tendencia por métrica**
> (selector W/M/3M + MIN/AVG/MAX). Eso es lo que evaluamos robar para nuestra Fase-1 visual.

---

## Parte B — TID-MAX nativa (BETA)

La concha nativa ya está en el repo (`tid-max/native/`, Capacitor) y apunta a la **app de producción**
(`server.url = https://tid-max-app.vercel.app`) → el beta carga la app en vivo, sin recompilar web.

### B.1 — Generar el `.ipa` (necesita **Mac con Xcode**, una vez)
```bash
git clone https://github.com/carlosmoreno793508/Cosas-Carlos.git
cd Cosas-Carlos/tid-max/native
npm install
npm run build            # copia la PWA a www/
npx cap add ios
npx cap sync
npx cap open ios         # abre Xcode
```
En Xcode: **Product → Archive** → **Distribute App → Custom → Ad Hoc / Development** → **Export** →
obtienes el **`TID-MAX.ipa`**.

### B.2 — Instalar en el iPhone — dos caminos
- **Tienes Mac:** lo más simple es **saltarte Sideloadly**: en Xcode, con el iPhone conectado, pon tu
  *Team* en **Signing & Capabilities** y dale **▶ Run** — Xcode lo instala directo (mismo límite de 7 días
  con Apple ID gratis). O exporta el `.ipa` y úsalo con Sideloadly si prefieres el auto-refresco.
- **Solo Windows:** no puedes compilar iOS ahí. Necesitas que **alguien con Mac genere el `.ipa` una vez**
  (pasos B.1) y te lo pase; luego en Windows **Sideloadly instala ese `.ipa`** igual que NOOP (Parte A, pasos 3–5).

> Nota: para que el beta tenga **FC en vivo del H10 + GPS en segundo plano** falta cerrar el método
> `RunHR._nativeConnect` y los *background modes* (guía 04). Sin eso, el beta igual **carga y funciona**
> como la app web dentro de la concha nativa — suficiente para probar en el teléfono.

---

## Parte C — El problema de los 7 días (auto-refresco)

Con Apple ID gratis la firma caduca cada 7 días. Sideloadly trae un **demonio de auto-refresco** que
**re-firma las apps cada pocos días** para que no mueran:
- En Sideloadly, activa el **auto-refresh** y elige qué apps refrescar.
- Requiere que la **computadora esté encendida** y **alcance el iPhone** (USB o Wi-Fi en la misma red).
- Alternativa definitiva: **Apple Developer $99/año** → 1 año sin re-firmar.

---

## Resumen

| | NOOP | TID-MAX beta |
|---|---|---|
| ¿Hay `.ipa` listo? | ✅ Sí (Releases, unsigned) | ❌ No — hay que compilarlo |
| ¿Necesita Mac? | **No** (Sideloadly firma) | **Sí**, para generar el `.ipa` una vez |
| ¿Windows sirve? | Sí (instala el `.ipa`) | Solo para **instalar** un `.ipa` que una Mac ya generó |
| Caducidad (Apple ID gratis) | 7 días (auto-refresco) | 7 días (auto-refresco) o $99/año |
| Para datos reales | strap WHOOP BLE o CSVs | carga la app de producción en vivo |

**Para clientes NO es esto:** sideload es para nosotros y el beta. Clientes reales → **TestFlight → App Store**.
