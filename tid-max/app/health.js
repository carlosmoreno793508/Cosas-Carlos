/* ============================================================================
   TID-MAX · Puente de Salud  (window.TIDHealth)
   ----------------------------------------------------------------------------
   Una sola interfaz para leer el "tanque de salud" del telefono:
     - iPhone  -> Apple Salud (HealthKit)
     - Android -> Health Connect (donde Samsung Health, Fitbit, Garmin, etc. escriben)
     - Navegador/PWA -> no hay acceso (HealthKit/Health Connect NO existen en web):
       se expone estado "solo-app" para que la UI lo muestre con gracia.

   Diseño: todo lo especifico del plugin nativo vive en el bloque ADAPTER de
   abajo. Si cambias de plugin, ajustas SOLO ese bloque y el resto de la app
   no se entera.
   ========================================================================== */
(function (global) {
  "use strict";

  // --- Datos que pedimos, por prioridad (P1 primero) ------------------------
  const READ_TYPES = [
    "heart-rate",          // FC   · P1
    "workouts",            // entrenos/sesiones · P1
    "hrv",                 // variabilidad · P1
    "resting-heart-rate",  // FC reposo · P2
    "sleep",               // sueno · P2
    "vo2max",              // VO2max · P2
  ];

  const WINDOW_DAYS = 14;               // ventana reciente (como Polar Flow)
  const STATE_KEY = "tidmax_health";    // { enabled, lastSync, counts }

  // ==========================================================================
  //  ADAPTER  ·  <<< AJUSTA AQUI SEGUN EL PLUGIN ELEGIDO >>>
  //  Aisla las llamadas al plugin nativo. Recomendado: `capacitor-health`
  //  (cubre HealthKit + Health Connect). Alternativa: `cordova-plugin-health`.
  // ==========================================================================
  const ADAPTER = {
    // Nombre con el que el plugin se registra en window.Capacitor.Plugins
    pluginName: "Health",

    plugin() {
      return (global.Capacitor && global.Capacitor.Plugins &&
              global.Capacitor.Plugins[this.pluginName]) || null;
    },

    // ¿El telefono soporta el tanque de salud? (HealthKit / Health Connect)
    async isAvailable() {
      const p = this.plugin();
      if (!p) return false;
      try {
        // capacitor-health: isHealthAvailable() -> { available: bool }
        const r = await p.isHealthAvailable();
        return !!(r && (r.available ?? r.value ?? r));
      } catch (_) { return false; }
    },

    // Pide permisos de lectura por tipo. Devuelve true si el usuario concede.
    async requestAuth(types) {
      const p = this.plugin();
      if (!p) throw new Error("plugin-no-disponible");
      // capacitor-health: requestHealthPermissions({ permissions: [...] })
      await p.requestHealthPermissions({ permissions: types });
      return true;
    },

    // Lee la ventana reciente y devuelve muestras crudas del plugin.
    // NOTA: el formato exacto depende del plugin -> se normaliza en normalize().
    async readWindow(days, types) {
      const p = this.plugin();
      if (!p) throw new Error("plugin-no-disponible");
      const end = new Date();
      const start = new Date(end.getTime() - days * 86400000);
      const out = {};
      for (const t of types) {
        try {
          // Firma generica: query({ dataType, startDate, endDate })
          const r = await p.query({
            dataType: t,
            startDate: start.toISOString(),
            endDate: end.toISOString(),
          });
          out[t] = (r && (r.samples || r.data || r.result)) || [];
        } catch (_) {
          out[t] = []; // tipo no soportado por esta plataforma/plugin: se ignora
        }
      }
      return out;
    },
  };
  // ==========================================================================
  //  fin ADAPTER
  // ==========================================================================

  // --- Normaliza lo que devuelve el plugin a un shape estable de TID-MAX ----
  function normalize(raw) {
    const counts = {};
    let total = 0;
    for (const t of READ_TYPES) {
      const n = Array.isArray(raw[t]) ? raw[t].length : 0;
      counts[t] = n; total += n;
    }
    return { counts, total, raw };
  }

  // --- Estado persistente (localStorage) ------------------------------------
  function getState() {
    try { return JSON.parse(global.localStorage.getItem(STATE_KEY)) || {}; }
    catch (_) { return {}; }
  }
  function setState(patch) {
    const s = Object.assign(getState(), patch);
    global.localStorage.setItem(STATE_KEY, JSON.stringify(s));
    return s;
  }

  // --- Plataforma / entorno --------------------------------------------------
  function isNative() {
    return !!(global.Capacitor && typeof global.Capacitor.isNativePlatform === "function" &&
              global.Capacitor.isNativePlatform());
  }
  function platform() {
    if (global.Capacitor && typeof global.Capacitor.getPlatform === "function") {
      return global.Capacitor.getPlatform(); // 'ios' | 'android' | 'web'
    }
    return "web";
  }
  function hubName() {
    const p = platform();
    if (p === "ios") return "Apple Salud";
    if (p === "android") return "Health Connect";
    return null; // web
  }

  // fmt dd/mm/aa como en la pantalla de Polar
  function fmtDate(iso) {
    if (!iso) return null;
    const d = new Date(iso);
    const p = (n) => String(n).padStart(2, "0");
    return `${p(d.getDate())}/${p(d.getMonth() + 1)}/${p(d.getFullYear() % 100)}`;
  }

  // ==========================================================================
  //  API PUBLICA  ·  window.TIDHealth
  // ==========================================================================
  const TIDHealth = {
    READ_TYPES,
    WINDOW_DAYS,

    platform,
    hubName,
    isNative,

    // ¿Se puede usar salud del telefono en este entorno? (solo app nativa)
    supported() { return isNative() && platform() !== "web"; },

    // Estado para pintar la UI (sincrono, desde localStorage)
    state() {
      const s = getState();
      return {
        supported: this.supported(),
        hub: hubName(),
        enabled: !!s.enabled,
        lastSync: s.lastSync || null,
        lastSyncText: fmtDate(s.lastSync),
        counts: s.counts || null,
      };
    },

    // Conectar: comprueba disponibilidad, pide permisos y hace la 1a lectura.
    async connect() {
      if (!this.supported()) {
        return { ok: false, reason: "solo-app",
                 msg: "Salud del telefono solo funciona en la app instalada (iPhone/Android), no en el navegador." };
      }
      const available = await ADAPTER.isAvailable();
      if (!available) {
        return { ok: false, reason: "no-disponible",
                 msg: `${hubName()} no esta disponible en este telefono.` };
      }
      try {
        await ADAPTER.requestAuth(READ_TYPES);
      } catch (e) {
        return { ok: false, reason: "permiso", msg: "No se concedieron los permisos de salud." };
      }
      setState({ enabled: true });
      return await this.sync();
    },

    // Sincronizar ahora: lee la ventana reciente y guarda la marca de tiempo.
    async sync(days = WINDOW_DAYS) {
      if (!this.supported()) {
        return { ok: false, reason: "solo-app", msg: "Disponible en la app instalada." };
      }
      if (!getState().enabled) {
        return { ok: false, reason: "sin-conectar", msg: "Primero conecta la salud del telefono." };
      }
      const raw = await ADAPTER.readWindow(days, READ_TYPES);
      const norm = normalize(raw);
      const now = new Date().toISOString();
      setState({ lastSync: now, counts: norm.counts });
      // Aqui, mas adelante, se puede empujar `norm` al motor TID-MAX
      // (mismo patron de "clave de sincronizacion" que los eventos).
      return { ok: true, lastSync: now, total: norm.total, counts: norm.counts, data: norm };
    },

    // Desconectar (solo apaga el toggle local; los permisos se quitan en Ajustes del SO).
    async disconnect() {
      setState({ enabled: false });
      return { ok: true };
    },
  };

  global.TIDHealth = TIDHealth;
})(window);
