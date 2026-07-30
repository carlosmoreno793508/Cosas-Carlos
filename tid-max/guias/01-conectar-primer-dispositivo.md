# Guía para novatos — Conectar tu primer dispositivo

**Objetivo:** ver los primeros datos reales de tu WHOOP y tu Galaxy Watch entrando al sistema,
usando **Vital** y **Terra** (para comparar). Completa los ítems **0.1 → 0.2** del tracker.

## Nota sobre el Galaxy Watch (SM-R860 = Galaxy Watch 4)
- ✅ **Sirve** como fuente: HR, HRV (diaria), sueño, pasos, entrenamientos, SpO2, estrés — vía
  Samsung Health → Health Connect → agregador.
- ⚠️ **No** entrega PPG/IBI crudo por la nube (límite de Samsung). El dato crudo para DFA-α1 vendrá
  del **EVK (H1)** o de una correa BLE (Polar H10).
- 📱 Requiere **teléfono Android** con Samsung Health + Health Connect (Galaxy Watch 4 no funciona con iPhone).

## Antes de empezar — checklist
- [ ] WHOOP con membresía activa (usuario y contraseña).
- [ ] Galaxy Watch 4 emparejado a un teléfono Android con Samsung Health + Health Connect sincronizando.
- [ ] Una computadora y un correo.
- [ ] Un desarrollador para 2–3 pasos técnicos (unas horas). El registro lo puede hacer el fundador.
- [ ] ~medio día.

## Parte 1 — Regístrate (sin código)
1. Entra a **tryvital.com** → *Sign up* → crea tu organización → obtén tus **API keys** (modo sandbox, gratis).
2. Haz lo mismo en **tryterra.co** → *Sign up* → dashboard → **API keys**.
3. Guarda las llaves en un lugar seguro y **no las compartas** (son como la llave de tu casa).

> Los nombres de botones pueden variar; busca "Sign up / Dashboard / API Keys / Developers".

## Parte 2 — Conecta tu WHOOP (lo más fácil)
4. En el dashboard, abre el **widget de conexión** ("Connect / Link"). Tu dev lo abre en minutos.
5. Elige **WHOOP**, mete usuario/contraseña de WHOOP y **Autoriza**.
6. En pocos minutos llegan los datos de tu WHOOP. **Primer dato real. 🎉**

## Parte 3 — Conecta tu Galaxy Watch (necesita el Android)
7. En el Android, confirma que Samsung Health sincroniza con Health Connect (Samsung Health → Ajustes → Health Connect).
8. El agregador se conecta vía Health Connect (el dev instala su SDK/app móvil y da permisos).
9. Los datos del Galaxy Watch (HR, sueño, HRV diaria, pasos…) empiezan a fluir.

## Parte 4 — Mira y compara (decides Terra vs. Vital)
10. El dev saca el **JSON crudo** (por API o dashboard).
11. Comparen campo por campo Vital vs. Terra: HRV, muestras intra-día, sueño, entrenamientos.
12. Decide con dato real. Expectativa: Vital gana por costo; y confirmas que el PPG/IBI crudo no sale de aquí.

## Quién hace qué
| Tú (fundador) | El desarrollador |
|---|---|
| Registro en Vital y Terra | Abrir el widget de conexión |
| Conectar WHOOP y Galaxy Watch (autorizar) | Sacar y comparar el JSON |
| Decidir cuál gana | Dejar la ingesta corriendo (ítem 0.5) |

**Al terminar:** avisa "conecté WHOOP y Samsung en ambos" para marcar 0.1 → 0.2 como ✅.
