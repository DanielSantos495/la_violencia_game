# Skills del proyecto

Instaladas en `.claude/skills/` (nivel proyecto, versionadas). Fecha de instalación y
auditoría: **2026-10-01**. Licencias de redistribución en `.claude/licencias/`.

## Propias

| Skill | Fuente | Licencia | Motivo |
|---|---|---|---|
| `la-violencia-art` | Este repo (resume doc 03) | Del proyecto | Estilo, violencia, época [V]/[P], piezas cut-out, pipeline de arte |
| `la-violencia-historia` | Este repo (resume docs 01, 02, 04 §5 y §7) | Del proyecto | Nombres, diálogos, [V]/[P], Archivo, reglas de diseño |
| `paleta-tematica` | Este repo (2026-10-02) | Del proyecto | Método para crear o revisar paletas con contexto (significados reservados, fuentes, registros con techo de croma, OKLCH, guion de color) y scripts Python sin dependencias: `validar_paleta.py` (gamut, zonas reservadas, contraste WCAG, daltonismo Machado 2009, grises) y `muestrario.py` (hoja SVG). Datos del juego en `game/art/paleta.json`; reglas en `planeacion/arte/tomo1/paleta.md`. Subordinada a `la-violencia-art` |
| `la-violencia-narrativa` | Este repo (doc 06, Bloque 2; cita docs 00–04) | Del proyecto | Oficio narrativo con filtro de rigor: 3 alternativas, pruebas de decisión, voz por personaje, formato de propuesta. Subordinada a `la-violencia-historia` en rigor. También en la cuenta de claude.ai |

## De terceros

| Skill(s) | Fuente | Tag / SHA | Licencia | Motivo | Auditoría |
|---|---|---|---|---|---|
| 27 skills oficiales: `actions-and-utilities`, `animations`, `audio-and-sound`, `cameras`, `curves-and-paths`, `data-manager`, `events-system`, `filters-and-postfx`, `game-object-components`, `game-setup-and-config`, `geometry-and-math`, `graphics-and-shapes`, `groups-and-containers`, `input-keyboard-mouse-touch`, `loading-assets`, `particles`, `physics-arcade`, `physics-matter`, `render-textures`, `scale-and-responsive`, `scenes`, `sprites-and-images`, `text-and-bitmaptext`, `tilemaps`, `time-and-timers`, `tweens`, `v4-new-features` | `phaserjs/phaser` `skills/` | `v4.2.1` = `41be1e462bc600064e498cba370bfa8c5c055a22` (igual a la versión instalada) | MIT | API de Phaser 4; prevalecen para la API del motor | Solo Markdown (35 archivos), sin scripts; URLs de ejemplo (`example.com`); sin red, credenciales ni escritura. Excluida `v3-to-v4-migration` |
| `router` | `gamedev-skills/awesome-gamedev-agent-skills` | `d4b0e35550c55ae70bdfcab4ef5a0e94610438a9` (main, 2026-09-27) | Apache-2.0 | Elegir la skill de gamedev adecuada | Markdown + `agents/openai.yaml` (metadatos). Detecta Phaser por `game/package.json`. Sus rutas `skills/<categoría>/<nombre>` no existen aquí (instalación plana): se resuelven por nombre. Menciona skills no instaladas |
| `phaser-core`, `phaser-arcade-physics`, `game-feel`, `audio-design`, `dialogue-systems`, `save-systems`, `camera-systems`, `game-ui-ux`, `input-systems`, `performance-optimization`, `prototype-fast` | ídem | ídem | Apache-2.0 | Prácticas de gamedev (diálogo/Ink, guardado, cámara, UI, etc.) | Solo Markdown; sin red ni credenciales. Ejemplos en GDScript/C# que no aplican directo |
| `create-game-assets` | ídem | ídem | Apache-2.0 | Flujo de producción/QA de assets | 2 scripts Python locales (`asset_report.py`, `build_preview_sheet.py`): leen imágenes y escriben en `--out`; sin red. **Riesgo:** el SKILL.md sugiere `python -m pip install` (Pillow) — no ejecutar sin aprobación. Subordinada a `la-violencia-art` |
| `algorithmic-art` | `anthropics/skills` | `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4` | Apache-2.0 (LICENSE.txt de la skill) | Arte generativo de apoyo | La plantilla `viewer.html` carga p5.js de cdnjs y Google Fonts en el navegador (red al abrir el HTML) |
| `canvas-design` | ídem | ídem | Apache-2.0; fuentes OFL-1.1 | Piezas gráficas de apoyo | 81 archivos de fuentes (5,5 MB). IBM Plex Serif e Instrument Serif venían sin licencia: se añadieron sus OFL desde `IBM/plex` e `Instrument/instrument-serif` |
| 12 skills de narrativa: `story-sense`, `character-arc`, `dialogue`, `interactive-fiction`, `perspectival-constellation`, `moral-parallax`, `key-moments`, `scene-sequencing`, `endings`, `cliche-transcendence`, `sensitivity-check`, `oblique-worldbuilding` | `jwynia/agent-skills` `skills/creative/fiction/` | `e02ec7e226a6e4f8419fd3b88a1d8e472d421b32` (2026-02-24; sin tags) | MIT **declarada solo en el frontmatter**, sin archivo LICENSE (ver `.claude/licencias/jwynia-agent-skills-MIT-declarada.md`) | Diagnóstico y pulido narrativo del guion (doc 06). Subordinadas a `la-violencia-historia` y `la-violencia-narrativa` | Markdown + scripts Deno de solo lectura local (`Deno.readTextFile`); sin red, escritura ni credenciales. Deno no está instalado: los scripts quedan inactivos. **Adaptación:** `description` acortada a ≤200 caracteres (límite de claude.ai) en 11 de 12; original y procedencia en el `ADAPTACION.md` de cada una. También subidas a la cuenta de claude.ai |
| `ink-syntax`, `ink-style`, `ink-testing` | `spaceninja/narrative-ink-skills` `plugins/narrative-ink/skills/` | `v1.0.0` = `afe2a0926e90bdeaa231d329f2459a373ec6bd6d` | MIT (LICENSE copiado en cada skill y en `.claude/licencias/narrative-ink-skills-MIT.txt`) | Escribir, formatear y probar `.ink` (inkjs + vitest) | `ink-style/format-ink.py` (Python 3, sin dependencias): reescribe el `.ink` indicado; con `--verify-blocks` ejecuta `inkjs-compiler` (variable `INKJS_COMPILER`; está en `game/node_modules/.bin`). Sin red ni credenciales. Fixture de prueba tomado del tutorial MIT de inkle |
| `color-expert` | `meodai/skill.color-expert` (601 ★; autor de Poline, RampenSau y color-names) | `f74624ceadcde459b4fe07fb8a0ea1c1e97967a0` (main, 2026-09-23; sin tags) | CC BY 4.0, solo el material original (`LICENSE`, `THIRD_PARTY_NOTICES.md`) | Ciencia del color: espacios (OKLCH), gamut, contraste WCAG/APCA, daltonismo, mezcla, nombres, color en la narración. Subordinada a `paleta-tematica` y `la-violencia-art` | Solo `SKILL.md`, sin scripts, red ni credenciales. **Adaptación:** `references/` no se instaló (unos 4 MB con transcripciones y copias íntegras de sitios de terceros, sin relicenciar) y se añadió una nota al inicio de `SKILL.md`; detalles en su `ADAPTACION.md` |
| `critique-color` | `Owl-Listener/designer-skills` `visual-critique/skills/critique-color/` (2,8 K ★) | `9a6930cf84a822eb458624bd11c61aac5bbdf224` | MIT (`LICENSE` copiado) | Revisar el color de una pantalla renderizada: contraste, coherencia con la paleta, color nunca como único indicador | Un Markdown, sin cambios, sin scripts ni red |

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
| `jakubkrehel/oklch-skill` | Descartada | Sin licencia (todos los derechos reservados). Lo que aporta (OKLCH, gamut, contraste) lo cubren `color-expert` y `paleta-tematica` |
| `Atmosaero/art-director-loop` | Solo referencia | Sin licencia y 2 ★. Su idea de convertir la dirección de arte en reglas que se prueban inspira el validador de `paleta-tematica`; no se copió texto |
| `nhatmobile1/color-palette-skill` (MIT) | Descartada | 3 ★. Paletas de UI web por industria; no aplica a una paleta histórica |
| `yanliudesign/mono-color-skill` (MIT) | Solo referencia | Genera imágenes con modelos (impresión a una tinta) e incluye unos 45 MB de ejemplos; el juego dibuja en SVG por código |
| `jezweb` `color-palette` | Descartada | Escalas para Tailwind v4 |
| jwynia `character-naming` | Descartada | Su script importa código remoto (`deno.land/std@0.208.0`) al ejecutarse; los nombres ya están aprobados en el doc 01 |
| jwynia `story-analysis`, `revision` | No instaladas | Solapan con `story-sense`; `revision` se reevalúa tras el diagnóstico |
| `howells/fiction` | Descartada | Sistema completo de novela (portadas, publicación, críticos-persona); MIT solo en el README, sin LICENSE |
| `danjdewhurst/story-skills` (MIT) | Descartada por ahora | Su motor de continuidad exige una story bible propia que duplicaría `planeacion/`; se reevalúa si el diagnóstico pide control de continuidad |
| `v3-to-v4-migration` | Excluida | El proyecto nace en Phaser 4 |
| Plugins `document-skills` / `example-skills` | Descartados | Instalan las 17 skills duplicadas |
| Spine Animation AI | Descartada | Licencia no comercial |
| Wiggle / Lottie, three.js, anime.js | Descartadas | Fuera del pipeline / 2D / redundante |
| `svg-animation-studio` | Solo referencia | Patrón, no se instala |
| `greensock/gsap-skills` (MIT), `iart-ai/web-animation-skills` (`svg-animation`), `steam-publish`, `itch-publish` | Pendientes de decisión de Daniel | Condicionales del doc 05 §B7.4 |
