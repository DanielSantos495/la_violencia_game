# La Violencia — Tomo I

Juego narrativo-documental 2D lateral (novela gráfica) sobre La Violencia en Colombia
(1946–1958), Tomo I de 8. Web primero (Phaser 4 + TypeScript + Ink); escritorio después.
Daniel es el único desarrollador; Claude produce arte SVG, música y efectos. Sin voces.

## Mapa del repo

- `planeacion/` — **fuente única de diseño**: `historia/`, `produccion/`, `arte/`, `tecnico/`
  (por tomo). Solo lectura desde Claude Code salvo que Daniel pida editarla.
- `game/` — desarrollo: código, contenido (`content/`), arte fuente (`art/src`), `tools/`,
  `tests/`. Ver `game/README.md`. Nada de documentación de diseño aquí.
- `.claude/skills/` — skills del proyecto (inventario y auditoría en `.claude/SKILLS.md`).

## Regla de trabajo

Ante cualquier duda de diseño, historia o arte, lee el doc correspondiente en `planeacion/`
**antes** de escribir código. El código y las skills citan los docs por ruta y sección
(p. ej. "doc 04 §7"); no copian su contenido.

## Reglas no negociables

- **Hechos fieles, ficción solo en los personajes.** Lo no verificado se marca **[P]** y no
  entra a un build público (Archivo `pendiente` → excluido en release).
- **Figuras reales:** nombre alterado en la ficción (doc 01) y sin diálogos inventados.
  Las víctimas reales no se ficcionalizan; solo aparecen en el Archivo con su nombre real.
- **Violencia sin espectáculo:** nunca se premia matar, sin contador de bajas, atrocidades no
  jugables (solo viñetas), combate solo contra armados y máximo 1 por misión (doc 04 §5).
- **Arte:** tinta y trama sobre papel hueso; rojo liberal y azul conservador como únicos
  acentos; sin sangre roja; lo [P] de época no se dibuja como final (doc 03).

## Comandos (en `game/`, Node 24.21.0 + pnpm 11)

```
pnpm install --frozen-lockfile
pnpm dev | build | preview | lint | format | typecheck | test
pnpm validate:archivo [--release] | ink:build | art:build | art:review <svg|atlas.json>
```

Antes de dar algo por hecho: `lint`, `typecheck`, `test` y `build` en verde.

## Trabajo en paralelo (varios chats)

Daniel trabaja con varios chats a la vez sobre este mismo repo y la misma rama.

- **Servidor de desarrollo:** levántalo con `preview_start` y la configuración `game-dev`
  (`.claude/launch.json`). Tiene `autoPort`: si el 5173 está ocupado por otro chat, se asigna
  otro puerto libre. Usa la URL que devuelve la herramienta; no asumas el 5173.
- No detengas ni reinicies el servidor de otro chat. Cada chat usa el suyo; todos sirven los
  mismos archivos, así que Vite recarga con los cambios de cualquier chat.
- Desde una terminal: `pnpm dev --port <puerto libre>`.
- **Commits:** añade solo tus archivos (`git add <rutas>`, nunca `git add .` ni carpetas
  enteras de otros); revisa `git status` porque otro chat puede tener cambios sin commitear.
- `art:build` regenera `public/generated/` para todos los servidores: si otro chat está
  editando arte, coordina antes de regenerar.

## Skills

| Cuándo | Skill |
|---|---|
| Arte, personajes, fondos, tweens de piezas, atlas | `la-violencia-art` (prioridad en arte) |
| Archivo, Ink/diálogos, nombres, fechas, diseño de misiones/combate | `la-violencia-historia` (prioridad en historia) |
| API de Phaser 4 | skills oficiales de Phaser (`scenes`, `tweens`, `loading-assets`, …); prevalecen sobre `phaser-core`/`phaser-arcade-physics` |
| Elegir qué skill de gamedev aplica | `router`, luego `dialogue-systems`, `save-systems`, `game-feel`, `camera-systems`, `game-ui-ux`, `input-systems`, `audio-design`, `performance-optimization`, `prototype-fast` |
| Arte generativo o piezas gráficas fuera del juego | `algorithmic-art`, `canvas-design` (subordinadas a `la-violencia-art`) |

Las skills propias mandan sobre las genéricas en arte e historia.
