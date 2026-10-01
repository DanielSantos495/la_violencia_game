# La Violencia — Videojuego documental del conflicto armado colombiano

Narrativa jugable en 8 tomos cronológicos sobre el conflicto armado en Colombia, con fin documental y educativo. Este repo contiene la documentación de diseño y el código del juego.

## Estructura

Dos partes:

| Carpeta | Contenido |
|---|---|
| `planeacion/historia/` | Esquema general de los 8 tomos, guion base, biblia de nomenclatura y guion por tomo |
| `planeacion/produccion/` | Plan de implementación, backlog y prompts de configuración |
| `planeacion/arte/` | Dirección de arte, referencias de época y audio |
| `planeacion/tecnico/` | Plataforma, stack, arquitectura y esquema del Archivo |
| `game/` | Desarrollo: proyecto del juego (Phaser 4 + TypeScript + Ink). Se configura con `planeacion/produccion/tomo1/05_prompt_setup_desde_cero.md`; requisitos y scripts en `game/README.md` |

Cada carpeta de planeación se organiza por tomo (`tomo1/`, `tomo2/`, …).

## Fuente única

La fuente principal es la carpeta local `la_violencia_game` en el computador de Daniel, versionada en git y conectada a GitHub (`DanielSantos495/la_violencia_game`). Los documentos se editan aquí; GitHub es la copia remota y el Proyecto de claude.ai la tiene enlazada como contexto. No mantener copias editables en otro lugar.

## Reglas no negociables

- Personajes jugables ficticios o compuestos. Figuras históricas reales: solo hechos documentados, sin diálogos inventados (aunque estén renombradas).
- 2–3 perspectivas jugables por tomo (civil, insurgente, estatal/paramilitar), sin tomar partido.
- La violencia se representa por su peso narrativo, no como espectáculo. Nunca se premia matar; las atrocidades no son jugables.
- Modo Archivo con datos verificables (CNMH, Comisión de la Verdad). Lo no verificado se marca **[P]** y no entra a un build público.
