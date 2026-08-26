import { useEffect } from "react";

/**
 * Mapeo de teclas del control remoto. Los TV envían códigos distintos según la
 * plataforma; aquí unificamos los más comunes de navegador, Samsung/Tizen y
 * LG/webOS.
 */
export type RemoteKey = "up" | "down" | "left" | "right" | "enter" | "back";

const KEY_MAP: Record<number, RemoteKey> = {
  37: "left",
  38: "up",
  39: "right",
  40: "down",
  13: "enter",
  // Tecla "Atrás": 8 (Backspace/navegador), 461 (Tizen), 10009 (Tizen legacy), 427 (webOS).
  8: "back",
  461: "back",
  10009: "back",
  427: "back",
};

/**
 * Navegación espacial simple para control remoto (D-pad). En lugar de calcular
 * geometría, se apoya en el orden del DOM y en `tabindex`, moviendo el foco al
 * elemento con `[data-focusable]` más cercano en la dirección pulsada.
 */
export function useRemote(handler: (key: RemoteKey) => void): void {
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      const key = KEY_MAP[e.keyCode];
      if (!key) return;
      e.preventDefault();
      handler(key);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [handler]);
}

/** Devuelve todos los elementos enfocables actualmente visibles, en orden DOM. */
export function focusables(root: ParentNode = document): HTMLElement[] {
  return Array.from(root.querySelectorAll<HTMLElement>("[data-focusable]")).filter(
    (el) => el.offsetParent !== null,
  );
}

/**
 * Mueve el foco desde el elemento activo hacia la dirección pedida usando la
 * posición en pantalla (getBoundingClientRect), que es robusto para rejillas.
 */
export function moveFocus(direction: RemoteKey): void {
  const current = document.activeElement as HTMLElement | null;
  const candidates = focusables();
  if (candidates.length === 0) return;
  if (!current || !current.hasAttribute("data-focusable")) {
    candidates[0].focus();
    return;
  }

  const origin = current.getBoundingClientRect();
  let best: HTMLElement | null = null;
  let bestScore = Infinity;

  for (const el of candidates) {
    if (el === current) continue;
    const r = el.getBoundingClientRect();
    const dx = r.left + r.width / 2 - (origin.left + origin.width / 2);
    const dy = r.top + r.height / 2 - (origin.top + origin.height / 2);

    const aligned =
      (direction === "left" && dx < -1) ||
      (direction === "right" && dx > 1) ||
      (direction === "up" && dy < -1) ||
      (direction === "down" && dy > 1);
    if (!aligned) continue;

    // Penaliza la distancia en el eje perpendicular para preferir el vecino recto.
    const primary = direction === "left" || direction === "right" ? Math.abs(dx) : Math.abs(dy);
    const secondary = direction === "left" || direction === "right" ? Math.abs(dy) : Math.abs(dx);
    const score = primary + secondary * 3;
    if (score < bestScore) {
      bestScore = score;
      best = el;
    }
  }

  best?.focus();
}
