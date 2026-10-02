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
- **Violencia jugable, nunca objetivo:** nunca se premia matar, sin contador de bajas; combate
  libre solo contra armados y máximo 1 por misión; violencia contra civiles solo en momentos
  guionizados, con control directo y coste narrativo; nunca contra víctimas reales
  (doc 02 §1 regla 1, doc 04 §5).
- **Arte:** tinta y trama sobre papel hueso; rojo liberal y azul conservador como únicos
  acentos; la sangre es roja solo un instante (orgánica, con textura) y se oxida a tinta
  negra; lo [P] de época no se dibuja como final (doc 03).

## Comandos (en `game/`, Node 24.21.0 + pnpm 11)

```
pnpm install --frozen-lockfile
pnpm dev | build | preview | lint | format | typecheck | test
pnpm validate:archivo [--release] | ink:build | art:build | art:review <svg|atlas.json>
```

Antes de dar algo por hecho: `lint`, `typecheck`, `test` y `build` en verde.

## Trabajo en paralelo (varios chats)

Daniel trabaja con varios chats a la vez. Cada área tiene su **worktree** (carpeta hermana) y
su **rama**; la carpeta principal queda para la integración y los chats sin área propia.

| Área | Carpeta | Rama | Territorio |
|---|---|---|---|
| Integración y otros chats | `la_violencia_game` | `setup/tomo1-base` | Lo que no sea de un área |
| Rosalba | `la_violencia_game--rosalba` | `arte/rosalba` | `game/art/src/personajes/`, `game/art/gen/rosalba.py`, `game/src/game/personajes/`, `Personaje.ts`, `Caminata.ts`, `game/src/core/animacion/`, `game/src/game/scenes/Prueba.ts` (escena de prueba de Rosalba), `planeacion/arte/tomo1/personajes/` |
| Fondos y escenarios | `la_violencia_game--fondos` | `arte/fondos` | Fondos y escenarios, `game/tools/art-build.ts` (un atlas por carpeta), escala del personaje en escena y su propia escena de prueba |

- **Integración:** `setup/tomo1-base` es la rama de integración. Cuando un bloque de un área
  está en verde, se fusiona ahí desde la carpeta principal
  (`git merge --no-ff arte/<área>`); luego cada área trae lo integrado a su rama
  (`git merge setup/tomo1-base`) para que los conflictos sean pequeños. Al cerrar el Sprint,
  PR de `setup/tomo1-base` a `main`. Push solo con aprobación de Daniel.
- **Archivos compartidos** (`main.ts`, `package.json`, `pnpm-lock.yaml`, skill
  `la-violencia-art`, READMEs, `CLAUDE.md`, docs 00/03): cambios mínimos, en commits aparte,
  y avisa a Daniel. No toques el territorio de otra área.
- **Contexto:** la memoria de Claude se guarda por carpeta y **no se comparte entre
  worktrees**. Lo que deba durar va en git: este archivo, `planeacion/` y las hojas de personaje.
- **Worktree nuevo:** `pnpm install --frozen-lockfile` y `pnpm ink:build`,
  `pnpm validate:archivo`, `pnpm art:build` en `game/` (lo generado no se versiona y cada
  worktree tiene el suyo).
- **Servidor de desarrollo:** `preview_start` con la configuración `game-dev`
  (`.claude/launch.json`). Tiene `autoPort`: si el 5173 está ocupado por otro chat, se asigna
  otro puerto libre; usa la URL que devuelve la herramienta. No detengas ni reinicies el
  servidor de otro chat. Desde una terminal: `pnpm dev --port <puerto libre>`.
  **Ojo en un worktree:** `game-dev` se ejecuta desde la carpeta principal (sirve
  `la_violencia_game`, no el worktree). En un worktree arranca el servidor en `game/` con
  `pnpm exec vite --port <libre> --strictPort` (en segundo plano) y abre la URL con
  `preview_start` + `url`. Comprueba qué carpeta sirve antes de verificar nada.
- **Commits:** `git add <rutas>` de tu territorio, nunca `git add .` ni carpetas enteras;
  revisa `git status`, otro chat puede tener cambios sin commitear en la misma carpeta.
- **Stash:** la pila de `git stash` es común a todos los worktrees; no uses `git stash` sin
  más (podrías sacar el de otro chat). Prefiere un commit temporal.

## Skills

| Cuándo | Skill |
|---|---|
| Arte, personajes, fondos, tweens de piezas, atlas | `la-violencia-art` (prioridad en arte) |
| Archivo, Ink/diálogos, nombres, fechas, diseño de misiones/combate | `la-violencia-historia` (prioridad en historia) |
| API de Phaser 4 | skills oficiales de Phaser (`scenes`, `tweens`, `loading-assets`, …); prevalecen sobre `phaser-core`/`phaser-arcade-physics` |
| Elegir qué skill de gamedev aplica | `router`, luego `dialogue-systems`, `save-systems`, `game-feel`, `camera-systems`, `game-ui-ux`, `input-systems`, `audio-design`, `performance-optimization`, `prototype-fast` |
| Arte generativo o piezas gráficas fuera del juego | `algorithmic-art`, `canvas-design` (subordinadas a `la-violencia-art`) |

Las skills propias mandan sobre las genéricas en arte e historia.
