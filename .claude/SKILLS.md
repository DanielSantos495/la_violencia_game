# Skills del proyecto

Instaladas en `.claude/skills/` (nivel proyecto, versionadas). Fecha de instalación y
auditoría: **2026-10-01**. Licencias de redistribución en `.claude/licencias/`.

## Propias

| Skill | Fuente | Licencia | Motivo |
|---|---|---|---|
| `la-violencia-art` | Este repo (resume doc 03) | Del proyecto | Estilo, violencia, época [V]/[P], piezas cut-out, pipeline de arte |
| `la-violencia-historia` | Este repo (resume docs 01, 02, 04 §5 y §7) | Del proyecto | Nombres, diálogos, [V]/[P], Archivo, reglas de diseño |

## De terceros

| Skill(s) | Fuente | Tag / SHA | Licencia | Motivo | Auditoría |
|---|---|---|---|---|---|
| 27 skills oficiales: `actions-and-utilities`, `animations`, `audio-and-sound`, `cameras`, `curves-and-paths`, `data-manager`, `events-system`, `filters-and-postfx`, `game-object-components`, `game-setup-and-config`, `geometry-and-math`, `graphics-and-shapes`, `groups-and-containers`, `input-keyboard-mouse-touch`, `loading-assets`, `particles`, `physics-arcade`, `physics-matter`, `render-textures`, `scale-and-responsive`, `scenes`, `sprites-and-images`, `text-and-bitmaptext`, `tilemaps`, `time-and-timers`, `tweens`, `v4-new-features` | `phaserjs/phaser` `skills/` | `v4.2.1` = `41be1e462bc600064e498cba370bfa8c5c055a22` (igual a la versión instalada) | MIT | API de Phaser 4; prevalecen para la API del motor | Solo Markdown (35 archivos), sin scripts; URLs de ejemplo (`example.com`); sin red, credenciales ni escritura. Excluida `v3-to-v4-migration` |
| `router` | `gamedev-skills/awesome-gamedev-agent-skills` | `d4b0e35550c55ae70bdfcab4ef5a0e94610438a9` (main, 2026-09-27) | Apache-2.0 | Elegir la skill de gamedev adecuada | Markdown + `agents/openai.yaml` (metadatos). Detecta Phaser por `game/package.json`. Sus rutas `skills/<categoría>/<nombre>` no existen aquí (instalación plana): se resuelven por nombre. Menciona skills no instaladas |
| `phaser-core`, `phaser-arcade-physics`, `game-feel`, `audio-design`, `dialogue-systems`, `save-systems`, `camera-systems`, `game-ui-ux`, `input-systems`, `performance-optimization`, `prototype-fast` | ídem | ídem | Apache-2.0 | Prácticas de gamedev (diálogo/Ink, guardado, cámara, UI, etc.) | Solo Markdown; sin red ni credenciales. Ejemplos en GDScript/C# que no aplican directo |
| `create-game-assets` | ídem | ídem | Apache-2.0 | Flujo de producción/QA de assets | 2 scripts Python locales (`asset_report.py`, `build_preview_sheet.py`): leen imágenes y escriben en `--out`; sin red. **Riesgo:** el SKILL.md sugiere `python -m pip install` (Pillow) — no ejecutar sin aprobación. Subordinada a `la-violencia-art` |
| `algorithmic-art` | `anthropics/skills` | `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4` | Apache-2.0 (LICENSE.txt de la skill) | Arte generativo de apoyo | La plantilla `viewer.html` carga p5.js de cdnjs y Google Fonts en el navegador (red al abrir el HTML) |
| `canvas-design` | ídem | ídem | Apache-2.0; fuentes OFL-1.1 | Piezas gráficas de apoyo | 81 archivos de fuentes (5,5 MB). IBM Plex Serif e Instrument Serif venían sin licencia: se añadieron sus OFL desde `IBM/plex` e `Instrument/instrument-serif` |

Notas:
- `create-game-assets` no existe en el tag `v1.1.0` de gamedev-skills; por eso todo ese
  repo va fijado al SHA de `main`.
- `AbhishekBarali/awesome-gamedev-agent-skills` (citado en su `INSTALLATION.md`) redirige a
  `gamedev-skills/…`: es una transferencia del repo, no un fork.
- Instalación manual (copia de carpetas), sin `npx skills`, sin `-g` y sin plugins.

## Descartadas o condicionales

| Skill | Estado | Motivo |
|---|---|---|
| `phaserjs/phaser-game-agent` | Descartada | MCP con login |
| `v3-to-v4-migration` | Excluida | El proyecto nace en Phaser 4 |
| Plugins `document-skills` / `example-skills` | Descartados | Instalan las 17 skills duplicadas |
| Spine Animation AI | Descartada | Licencia no comercial |
| Wiggle / Lottie, three.js, anime.js | Descartadas | Fuera del pipeline / 2D / redundante |
| `svg-animation-studio` | Solo referencia | Patrón, no se instala |
| `greensock/gsap-skills` (MIT), `iart-ai/web-animation-skills` (`svg-animation`), `steam-publish`, `itch-publish` | Pendientes de decisión de Daniel | Condicionales del doc 05 §B7.4 |
