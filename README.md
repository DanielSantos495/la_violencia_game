# La Violencia — Videojuego documental del conflicto armado colombiano

Narrativa jugable en 8 tomos cronológicos sobre el conflicto armado en Colombia, con fin documental y educativo. Este repo contiene la documentación de diseño y el código del juego.

## Estructura

| Carpeta | Contenido |
|---|---|
| `historia/` | Esquema general de los 8 tomos, guion base, biblia de nomenclatura y guion por tomo |
| `planeacion/` | Plan de implementación, backlog y prompts de configuración |
| `arte/` | Dirección de arte, referencias de época y audio |
| `tecnico/` | Plataforma, stack, arquitectura y esquema del Archivo |
| `game/` | Proyecto del juego (Phaser 4 + TypeScript + Ink). Se configura con `planeacion/tomo1/05_prompt_setup_desde_cero.md` |

Cada carpeta de documentación se organiza por tomo (`tomo1/`, `tomo2/`, …).

## Fuente única

Los documentos de este repo son la versión oficial. Se editan aquí (o desde Claude con acceso al repo) y se sincronizan al Proyecto de claude.ai con la integración de GitHub. No mantener copias editables en otro lugar.

## Reglas no negociables

- Personajes jugables ficticios o compuestos. Figuras históricas reales: solo hechos documentados, sin diálogos inventados (aunque estén renombradas).
- 2–3 perspectivas jugables por tomo (civil, insurgente, estatal/paramilitar), sin tomar partido.
- La violencia se representa por su peso narrativo, no como espectáculo. Nunca se premia matar; las atrocidades no son jugables.
- Modo Archivo con datos verificables (CNMH, Comisión de la Verdad). Lo no verificado se marca **[P]** y no entra a un build público.
