# 🗺️ TID-MAX — Mapa del proyecto

Guía rápida de dónde está todo y cómo usarlo.

## Repositorio
| | |
|---|---|
| **Repo** | `carlosmoreno793508/Cosas-Carlos` (GitHub) |
| **Rama de trabajo** | `claude/smartwatch-analysis-9eua05` |
| **Carpeta del código** | `tid-max/software/` |
| **Datos reales (local, NO se sube)** | `tid-max/software/datos/` |

### Actualizar en tu Mac
```bash
cd ~/Cosas-Carlos/tid-max/software
git pull origin claude/smartwatch-analysis-9eua05
```

## Flujo diario (el pipeline completo)
```bash
python whoop_sync.py      # 1. baja datos de WHOOP
python tid_data.py        # 2. normaliza todo (dataset.json)
python tid_agent.py       # 3. coach del día (opus-5) -> coach-hoy.json
python tid_cliente.py     # 4. arma la tarjeta cliente (cliente.png)
python tid_notify.py --foto   # 5. la manda por Telegram (mamá + Gael)
```

## Los scripts (Capa por capa)
| Archivo | Qué hace |
|---|---|
| `whoop_auth.py` / `whoop_sync.py` | Conexión y descarga de WHOOP |
| `polar_capture.py` | Captura del Polar Verity Sense por Bluetooth (HR latido a latido) |
| **`tid_data.py`** | **Motor de datos**: normaliza WHOOP+Polar+plan al esquema canónico; calcula recovery/HRV/FC/sueño, ACWR, plan del día, zonas FC, nutrición y detección de esfuerzo |
| **`tid_agent.py`** | **Agentes de Claude**: coach del día, preventivo y Q&A (`--pregunta "..."`) |
| **`tid_nutricion.py`** | **Nutriólogo AI**: foto de comida -> macros; `--plan` arma el menú del día |
| **`tid_cliente.py`** | **Tarjeta cliente**: genera la imagen (PNG) para la familia |
| **`tid_notify.py`** | **Notificador**: manda texto/imagen por Telegram, WhatsApp o email |
| `tid_dashboard.py` | Dashboard técnico (HTML) |
| `tid_coach.py` / `tid_plan.py` | Versiones previas (parqueadas) |

## Config (lo que puedes editar)
| Archivo | Contiene |
|---|---|
| `evento.json` | Evento objetivo (Pan Pacific, fechas, sede) |
| `plan-macro.json` | Km por semana de toda la temporada (columna K de Gael, con el taper) |
| `plan-semana.json` | Patrón semanal + horarios (dobles L/M/V, sencillas Mar/Jue/Sab) |
| `nutricion-gael.json` | Perfil de Gael (18 años, 81 kg, 1.86 m, VO₂máx, zonas FC), alimentos y suplementos |
| `.env` (creas tú, no se sube) | Llaves: `ANTHROPIC_API_KEY`, WHOOP, Telegram/WhatsApp |

## Documentación
| Archivo | Contiene |
|---|---|
| `tid-max/perfil-gael.md` | Análisis de sus estudios (VO₂máx, umbrales, labs, antropometría) |
| `tid-max/analisis/esquema-canonico.md` | Esquema de datos que leen los agentes |
| `tid-max/software/whatsapp-plantilla.md` | Plantilla para el envío diario por WhatsApp |
| `tid-max/software/README.md` | Guía de instalación y uso |
| `tid-max/guias/` | Guías de dispositivos (WHOOP, Polar) |

## Comandos útiles sueltos
```bash
python tid_agent.py --pregunta "¿cómo va el descanso de Gael?"   # Q&A libre
python tid_nutricion.py foto.jpg --tipo doble                    # analiza una comida
python tid_nutricion.py --plan                                   # menú del día
python polar_capture.py --scan                                   # busca el Polar
```
