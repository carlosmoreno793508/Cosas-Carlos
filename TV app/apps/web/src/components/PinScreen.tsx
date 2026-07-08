import { useState } from "react";

/**
 * Pantalla de PIN (control parental). Teclado numérico grande navegable con el
 * control remoto. Verifica contra el PIN del perfil; tras varios fallos avisa.
 */
export function PinScreen({
  expected,
  title = "Introduce el PIN",
  onOk,
  onCancel,
}: {
  expected: string;
  title?: string;
  onOk: () => void;
  onCancel: () => void;
}) {
  const [pin, setPin] = useState("");
  const [error, setError] = useState(false);

  function push(d: string) {
    setError(false);
    const next = (pin + d).slice(0, 4);
    setPin(next);
    if (next.length === 4) {
      if (next === expected) onOk();
      else {
        setError(true);
        setTimeout(() => setPin(""), 400);
      }
    }
  }

  return (
    <div className="pin">
      <h2 className="pin__title">{title}</h2>
      <div className={`pin__dots ${error ? "pin__dots--err" : ""}`}>
        {[0, 1, 2, 3].map((i) => (
          <span key={i} className={`pin__dot ${i < pin.length ? "is-on" : ""}`} />
        ))}
      </div>
      {error && <p className="error">PIN incorrecto</p>}
      <div className="pin__pad">
        {["1", "2", "3", "4", "5", "6", "7", "8", "9"].map((d) => (
          <button key={d} data-focusable className="pin__key" onClick={() => push(d)}>
            {d}
          </button>
        ))}
        <button data-focusable className="pin__key pin__key--wide" onClick={onCancel}>
          Cancelar
        </button>
        <button data-focusable className="pin__key" onClick={() => push("0")}>
          0
        </button>
        <button data-focusable className="pin__key" onClick={() => setPin((p) => p.slice(0, -1))}>
          ⌫
        </button>
      </div>
    </div>
  );
}
