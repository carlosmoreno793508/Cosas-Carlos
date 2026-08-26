import { useState } from "react";
import { DEFAULT_PROXY, getProxy, setProxy } from "../settings.js";

/**
 * Ajustes del reproductor. Por ahora: el "proxy" que permite reproducir listas
 * IPTV de terceros en el navegador (salta la restricción CORS de Chrome). En el
 * TV nativo no hace falta.
 */
export function SettingsScreen({ onBack }: { onBack: () => void }) {
  const [proxy, setProxyValue] = useState(getProxy());
  const [saved, setSaved] = useState(false);

  function save(value: string) {
    setProxyValue(value);
    setProxy(value);
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  }

  return (
    <div className="sheet settings">
      <h2 className="sheet__title">Ajustes</h2>

      <label className="field">
        <span>Proxy de reproducción (para ver listas IPTV en el navegador)</span>
        <input
          data-focusable
          value={proxy}
          onChange={(e) => setProxyValue(e.target.value)}
          placeholder="http://localhost:8080/proxy"
        />
      </label>

      <div className="settings__actions">
        <button data-focusable className="btn btn--primary" onClick={() => save(DEFAULT_PROXY)}>
          Usar proxy local
        </button>
        <button data-focusable className="btn btn--ghost" onClick={() => save("")}>
          Sin proxy
        </button>
        <button data-focusable className="btn btn--ghost" onClick={() => save(proxy)}>
          Guardar
        </button>
      </div>

      {saved && <p className="settings__ok">✓ Guardado</p>}

      <p className="legal-note">
        El proxy usa el servidor incluido para reenviar tu lista y evitar el bloqueo
        de Chrome. Actívalo si tu M3U/Xtream no reproduce en el navegador. En Fire TV,
        Android TV o Samsung no se necesita.
      </p>

      <div className="sheet__actions">
        <button data-focusable className="btn btn--ghost" autoFocus onClick={onBack}>
          ‹ Volver
        </button>
      </div>
    </div>
  );
}
