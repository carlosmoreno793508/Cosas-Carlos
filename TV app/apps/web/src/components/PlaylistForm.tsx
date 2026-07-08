import { useState } from "react";
import type { Playlist, PlaylistKind } from "@tvapp/core";
import { newId } from "../storage.js";

/**
 * Formulario "Nueva lista de reproducción" (equivalente a la pantalla de la
 * captura): permite M3U o Xtream con nombre opcional, URL y credenciales.
 */
export function PlaylistForm({
  onCreate,
  onCancel,
}: {
  onCreate: (p: Playlist) => void;
  onCancel: () => void;
}) {
  const [kind, setKind] = useState<PlaylistKind>("xtream");
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  function submit() {
    if (!url.trim()) {
      setError("La URL es obligatoria");
      return;
    }
    if (kind === "xtream" && (!username.trim() || !password.trim())) {
      setError("Xtream requiere usuario y contraseña");
      return;
    }
    onCreate({
      id: newId(),
      kind,
      name: name.trim() || undefined,
      url: url.trim(),
      username: kind === "xtream" ? username.trim() : undefined,
      password: kind === "xtream" ? password.trim() : undefined,
      createdAt: Date.now(),
    });
  }

  return (
    <div className="sheet">
      <h2 className="sheet__title">Nueva lista de reproducción</h2>

      <div className="segmented">
        <button
          data-focusable
          className={`segmented__btn ${kind === "m3u" ? "is-active" : ""}`}
          onClick={() => setKind("m3u")}
        >
          M3U
        </button>
        <button
          data-focusable
          className={`segmented__btn ${kind === "xtream" ? "is-active" : ""}`}
          onClick={() => setKind("xtream")}
        >
          Xtream
        </button>
      </div>

      <label className="field">
        <span>Nombre (opcional)</span>
        <input data-focusable value={name} onChange={(e) => setName(e.target.value)} />
      </label>

      <label className="field">
        <span>{kind === "m3u" ? "URL del archivo M3U" : "URL"}</span>
        <input
          data-focusable
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder={kind === "m3u" ? "https://.../lista.m3u" : "https://portal.com:8080"}
        />
      </label>

      {kind === "xtream" && (
        <>
          <label className="field">
            <span>Nombre de usuario</span>
            <input data-focusable value={username} onChange={(e) => setUsername(e.target.value)} />
          </label>
          <label className="field">
            <span>Contraseña</span>
            <input
              data-focusable
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
        </>
      )}

      {error && <p className="error">{error}</p>}

      <p className="legal-note">
        Solo se guardan estos datos en este dispositivo. Usa fuentes de contenido
        para las que tengas derechos.
      </p>

      <div className="sheet__actions">
        <button data-focusable className="btn btn--ghost" onClick={onCancel}>
          Cancelar
        </button>
        <button data-focusable className="btn btn--primary" onClick={submit}>
          Crear lista de reproducción
        </button>
      </div>
    </div>
  );
}
