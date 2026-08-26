import type { FetchLike } from "@tvapp/core";

/**
 * Ajustes del reproductor. El principal es el "proxy": una URL del servidor que
 * reenvía las peticiones de tu lista IPTV para saltar la restricción CORS del
 * navegador. Si usas el servidor incluido, es http://localhost:8080/proxy.
 * Vacío = sin proxy (para el TV nativo o fuentes que ya permiten CORS).
 */
const PROXY_KEY = "tvapp.proxy.v1";

/** Valor por defecto sugerido cuando el usuario corre el servidor incluido. */
export const DEFAULT_PROXY = "http://localhost:8080/proxy";

export function getProxy(): string {
  try {
    return localStorage.getItem(PROXY_KEY) ?? "";
  } catch {
    return "";
  }
}

export function setProxy(value: string): void {
  localStorage.setItem(PROXY_KEY, value.trim());
}

/** Envuelve una URL para que pase por el proxy (si está configurado). */
export function proxied(url: string): string {
  const p = getProxy();
  if (!p || !url) return url;
  // No re-proxear una URL que ya apunta al proxy.
  if (url.startsWith(p)) return url;
  return `${p}?url=${encodeURIComponent(url)}`;
}

/**
 * fetch que enruta por el proxy. Se pasa a XtreamClient para que TODAS sus
 * llamadas (API, EPG) funcionen en el navegador. Devuelve undefined si no hay
 * proxy, para que el cliente use el fetch normal.
 */
export function proxiedFetch(): FetchLike | undefined {
  if (!getProxy()) return undefined;
  return ((url: string, init?: { signal?: AbortSignal }) =>
    fetch(proxied(url), init)) as unknown as FetchLike;
}
