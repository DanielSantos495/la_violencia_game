# game/

Proyecto del juego (Tomo I "La Violencia"): Phaser 4 + TypeScript 7 + Vite + Ink (inkjs).
El diseño vive en `../planeacion/`; aquí solo hay código, contenido y herramientas.
Configurado con `../planeacion/produccion/tomo1/05_prompt_setup_desde_cero.md`.

## Requisitos

- Node **24.21.0** (`.nvmrc`; con nvm: `nvm use`).
- pnpm **11.2.2** (`packageManager`; con Corepack: `corepack enable pnpm`).

## Instalación

```bash
pnpm install --frozen-lockfile
```

## Scripts

| Script | Qué hace |
|---|---|
| `pnpm dev` | Compila Ink, valida el Archivo (modo normal) y abre Vite |
| `pnpm build` | Ink + Archivo `--release` + arte + typecheck + `vite build` → `dist/` |
| `pnpm preview` | Sirve `dist/` |
| `pnpm lint` / `pnpm format` | Biome (lint + formato) / aplica correcciones |
| `pnpm typecheck` | `tsc --noEmit` (TS 7) |
| `pnpm test` | Vitest |
| `pnpm validate:archivo [--release]` | Valida `content/archivo/*.json`; `--release` excluye pendientes, licencias no concedidas y `arch-prueba-*` |
| `pnpm ink:build` | `content/ink/*.ink` → `public/generated/ink/*.json` |
| `pnpm art:build` | `art/src/**/*.svg` → SVGO → PNG @1x/@2x → atlas (`art/build/`, `public/generated/art/`) |
| `pnpm art:review <svg\|atlas.json>` | PNG de revisión en `art/build/revision/` |
| `pnpm art:walk <personaje.svg> [fases]` | Hoja del ciclo de caminata en `art/build/revision/` |

Los scripts de `tools/` son TypeScript ejecutado por Node 24 sin transpilar (solo sintaxis
borrable: `erasableSyntaxOnly`).

## Estructura

```
src/
  main.ts       arranque (1920×1080, Scale.FIT, WebGL con respaldo Canvas)
  core/         lógica pura sin Phaser ni DOM: narrative/, archivo/, mechanics/
  game/         Phaser: scenes/, mechanics/, Recorte.ts (personajes por piezas)
  ui/           DOM sobre el canvas: globos, visor del Archivo
content/ink/    guion (.ink)            content/archivo/  entradas del Archivo (.json)
art/src/        SVG fuente              art/build/        generado, no se edita
art/gen/        generadores de SVG por personaje (python3 sin dependencias)
audio/src/      fuentes de audio        tools/            scripts de build
tests/          Vitest
```

`public/generated/`, `art/build/` y `dist/` se generan y no se versionan.
