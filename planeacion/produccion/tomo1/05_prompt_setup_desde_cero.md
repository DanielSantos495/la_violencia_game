# Prompt — Configuración desde cero: Tomo I "La Violencia"

> Pegar todo lo que sigue en un chat nuevo de **Claude Code abierto en la raíz de `la_violencia_game`** (carpeta local en el Mac de Daniel, conectada a `DanielSantos495/la_violencia_game`).
> El repo tiene dos partes: `planeacion/` (documentación) y `game/` (desarrollo). El juego se construye **solo dentro de `game/`**.

---

## Contexto

Juego narrativo-documental **2D lateral estilo novela gráfica** sobre La Violencia en Colombia (1946–1958). Es el Tomo I de una serie de 8.

- **Equipo:** Daniel es el único desarrollador (perfil JS/frontend, Shopify). Claude produce el arte SVG, la música y los efectos.
- **Plataforma:** web primero; escritorio después (Tauri 2, fuera de alcance aquí).
- **Lanzamiento:** por episodios.
- **Sin voces:** solo texto en globos.
- **Resolución:** base 1920×1080 con escalado; 60 fps en equipos modestos.

**Documentos de diseño (en el repo):**
- `planeacion/produccion/tomo1/00_plan_implementacion.md`: fases y backlog del Sprint 0.
- `planeacion/historia/tomo1/01_biblia_nomenclatura.md`: nombres ficticios y reales.
- `planeacion/historia/tomo1/02_guion_narrativa.md`: guion.
- `planeacion/arte/tomo1/03_direccion_arte.md`: estilo y referencias de época.
- `planeacion/tecnico/tomo1/04_documento_tecnico.md`: stack, arquitectura y esquema del Archivo.
- Contexto general: `planeacion/historia/esquema_tomos_conflicto_armado.md` y `planeacion/historia/tomo1/tomo1_la_violencia.md` (guion base, corregido por el doc 02).

Son la fuente de verdad. Si falta alguno, **detente y pídemelo**. **No edites** estos documentos durante el setup; si encuentras una contradicción, repórtala.

El código anterior se borró a propósito para reconstruir desde cero. **No intentes recuperarlo.** Las tareas técnicas marcadas `[x]` en el doc 00 corresponden a ese código borrado: trátalas como pendientes.

---

## Reglas de trabajo (obligatorias)

1. **Contexto antes de código.** Lee los 5 documentos (al menos el 04 completo y las secciones de Sprint 0 del 00) antes de crear cualquier archivo.
2. **No adivines.**
   - Versiones, comandos, flags, nombres de paquetes, plantillas, tags y SHAs se verifican en la documentación o el registro oficial (npm, GitHub, sitio del proyecto) en el momento de usarlos.
   - Lo que no puedas verificar va marcado **[P]**, y me preguntas.
   - Los números de versión que aparecen en los docs (p. ej. Phaser 4.2.1, Vite 8, TypeScript 7, inkjs 2.4.0) son **referencia, no instrucción**: confirma cuál es la versión estable vigente.
3. **Versiones exactas.** Sin `^` ni `~` en `package.json`. Commitea el lockfile. Fija la versión de Node (`.nvmrc` y `engines`).
4. **Nivel proyecto.** Skills en `.claude/skills/` versionadas en git. Nada en `~/.claude` sin mi aprobación.
5. **Licencias.** El juego se venderá (Steam/itch). Descarta toda dependencia o skill con licencia no comercial y reporta la licencia de cada una.
6. **Seguridad de skills de terceros.** Antes de activarlas, lee cada `SKILL.md` y cada script incluido. Reporta comandos de red, escritura fuera del repo, credenciales o ejecución remota.
7. **Mínimo necesario.** No agregues librerías "por si acaso". Cada dependencia debe justificarse en el doc 04 o en este prompt.
8. **Validar antes de declarar hecho.** Al cerrar cada bloque deben pasar `build`, `lint`, `typecheck` y `test`. No digas "listo" sin evidencia.
9. **Commits por bloque**, con mensajes claros. **No hagas push** sin mi aprobación.
10. **Comunicación.** En español, conciso, sin halagos. Separa lo confirmado de lo no verificado.

---

## Bloque 0 — Reconocimiento y decisiones (esperar aprobación)

1. Inspecciona el repo: contenido, `git log`, la versión de Node/npm disponible y que existan los documentos listados arriba.
2. Lee los documentos.
3. Pregúntame en **una sola tanda** lo que sea mi decisión:
   - **Estructura de `src/`:** el doc 04 §4 usa `scenes/ narrative/ mechanics/ archivo/ ui/`, mientras que el doc 00 menciona capas `src/core`, `src/game`, `src/ui`. Propón una estructura que reconcilie ambas (lógica pura sin Phaser vs. escenas/render vs. DOM) y espera mi elección.
   - **Gestor de paquetes:** npm, pnpm u otro. Recomienda uno.
   - **Ramas:** ¿se trabaja directo en `main` o en una rama de setup con PR?
4. Presenta un **plan corto** por bloques con las versiones verificadas de cada dependencia y su fuente. **Espera mi aprobación.**

## Bloque 1 — Proyecto base (todo dentro de `game/`)

1. El repo ya existe; no lo reinicialices. Todo el proyecto del juego (`package.json`, lockfile, config, código) vive en `game/`. La raíz queda solo para `planeacion/`, `CLAUDE.md`, `README.md`, `.claude/` y `.github/`.
2. Verifica si hay una plantilla oficial de Phaser 4 + Vite + TypeScript vigente.
   - Si existe y es limpia, úsala.
   - Si no, crea el proyecto Vite + TS a mano y añade Phaser.
   - Elimina cualquier demo de la plantilla.
3. Configura TypeScript en modo `strict`, con alias de rutas solo si hacen falta.
4. Crea dentro de `game/` la estructura completa de carpetas acordada, más:
   - `content/ink/`
   - `content/archivo/`
   - `art/src/`
   - `art/build/` (generado)
   - `audio/src/`
   - `tools/`
   - `tests/`
5. Configura `game/.gitignore` con `node_modules`, `dist`, `art/build`, salidas de audio y artefactos de Ink compilados (si se generan en build).
6. Arranque mínimo: `main.ts` con la configuración de juego (1920×1080 con escalado, WebGL con respaldo) y escenas vacías `Boot` y `Menu`.
7. **Validación:** `dev` y `build` funcionan; el canvas carga sin errores de consola.

## Bloque 2 — Calidad

1. Linter y formateador, en versiones verificadas y con configuración mínima.
2. Tests con un runner compatible con Vite (verifica cuál es el recomendado vigente).
3. Scripts en `package.json`: `dev`, `build`, `preview`, `lint`, `typecheck`, `test`, `validate:archivo`, `art:build`, `ink:build`.
4. **Validación:** todos los scripts corren en verde (los que aún no tienen contenido terminan sin error).

## Bloque 3 — Narrativa (Ink)

1. Instala `inkjs`. Verifica cómo compilar `.ink` → JSON en build: compilador incluido en inkjs u otra vía oficial de inkle. Elige la que no dependa de binarios de pago.
2. Crea `InkRunner` y `NarrativeState` según el doc 04 §4.
3. Crea un `.ink` de prueba con **una decisión** y globos renderizados en DOM sobre el canvas.
   - Texto neutro de prueba.
   - **No** escribas diálogos de figuras reales ni contenido del guion definitivo.
4. Los tests de `InkRunner` cubren carga, avance y decisión.

## Bloque 4 — Archivo (fuente única)

1. Define el esquema de entrada según el doc 04 §7 como tipo TS + validación en runtime (elige una librería verificada o validación propia; justifica).
2. Crea `tools/validate-archivo` con dos modos:
   - Modo normal: valida estructura.
   - Modo release: **excluye** entradas con `estado_verificacion: "pendiente"` o con licencia distinta de `concedida`/`no_aplica`.
3. Crea `ArchivoStore` leyendo entradas validadas.
4. Agrega 3 entradas de prueba **marcadas como de prueba** (no datos históricos reales sin fuente).
5. Tests: entrada válida, entrada inválida y exclusión en release.

## Bloque 5 — Pipeline de arte

1. **Rasterizado:** script SVG → PNG @1x y @2x en `tools/`.
   - Referencia previa: `@resvg/resvg-js`. Verifica que esté vigente y compárala con 1 alternativa.
2. **Optimización SVG:** SVGO (verificar versión) antes de rasterizar. La configuración **preserva IDs y grupos** de las piezas de recorte (cut-out).
3. **Atlas:** compara 2–3 empaquetadores compatibles con el formato de atlas JSON de Phaser 4 (mantenimiento, licencia, Node). **Recomiéndame uno y espera mi aprobación** antes de instalarlo.
4. Encadena todo en `art:build`: `art/src` → SVGO → PNG → atlas en `art/build`. Los PNG nunca se editan a mano.
5. **Verificación visual:** script que renderice un SVG o un atlas a PNG de revisión, para que yo y Claude podamos inspeccionarlo.
6. Usa un SVG de prueba simple (una figura articulada en 3 piezas con IDs estables) y cárgala en una escena de prueba con un tween.
7. **Audio:** **solo investigación**. Herramientas para MIDI → render con bancos libres y para efectos por síntesis, con licencias de los bancos. No instales nada.

## Bloque 6 — CI

GitHub Actions (workflow en `.github/` de la raíz, con `working-directory: game`) con estos pasos: instalar con lockfile → `lint` → `typecheck` → `test` → `validate:archivo` (modo release) → `ink:build` → `art:build` → `build`.

Las versiones de las actions se verifican en sus repos oficiales.

## Bloque 7 — Skills de terceros (nivel proyecto)

Fija cada skill a un tag o SHA. Audítala (regla 6) y verifica su licencia antes de copiarla.

1. **Skills oficiales de Phaser 4** (`phaserjs/phaser`, carpeta `skills/`).
   - Usa el tag igual a la versión de Phaser instalada; si no existe, el más cercano, y avísame.
   - Excluye `v3-to-v4-migration`.
   - **No** instales `phaserjs/phaser-game-agent` (MCP con login).
2. **`gamedev-skills/awesome-gamedev-agent-skills`** (Apache-2.0). Verifica en su `docs/INSTALLATION.md` cómo instalar un subconjunto **sin `-g`**.
   - Instala **solo:** `router`, `phaser-core`, `phaser-arcade-physics`, `create-game-assets`, `game-feel`, `audio-design`, `dialogue-systems`, `save-systems`, `camera-systems`, `game-ui-ux`, `input-systems`, `performance-optimization`, `prototype-fast`.
   - Comprueba que el router detecte Phaser en este repo.
   - Si el router entra en conflicto con las skills oficiales de Phaser, prevalecen las oficiales para la API del motor.
3. **`anthropics/skills`:** copia **solo** `algorithmic-art` y `canvas-design`.
   - **No** uses los plugins `document-skills` ni `example-skills`: según issues reportados, instalan las 17 skills duplicadas.
4. **Condicionales (pregúntame antes):**
   - `greensock/gsap-skills`: solo si adoptamos GSAP en la capa DOM; antes, verifica la licencia vigente de GSAP. Dentro del canvas se usan siempre los tweens de Phaser.
   - `iart-ai/web-animation-skills` (solo `svg-animation`).
   - `steam-publish` e `itch-publish`.
5. **Descartadas, no instalar:**
   - Spine Animation AI: licencia no comercial.
   - Wiggle/Lottie: fuera del pipeline.
   - three.js game skills: el juego es 2D.
   - anime.js skills: redundante.
   - `svg-animation-studio`: solo como referencia de patrón.

## Bloque 8 — Skills propias

Créalas con `skill-creator` (si no está disponible, usa el formato estándar de `SKILL.md`).

**`la-violencia-art`** (desde el doc 03):
- **Estilo:** tinta negra sobre papel hueso; grises por trama, sin degradados; rojo liberal y azul conservador como únicos acentos; plano lateral con 2–3 capas de paralaje.
- **Personajes por piezas:** cabeza, torso, brazos, piernas, ruana, sombrero. Convención de IDs y grupos estable para el cut-out. Rostros simplificados.
- **Violencia:** silueta y mancha negra; sin sangre roja, sin gore, sin rostros de víctimas identificables; atrocidades solo en viñetas fijas.
- **Época:** tabla [V]/[P] del doc 03. **Un elemento [P] no se dibuja en versión final.** Silueta de arma correcta para el año (cerrojo ≠ automático).
- **Pipeline** del Bloque 5 y **checklist** de revisión por asset.
- **Paleta y grosores:** si la hoja de estilo no existe aún, deja la sección como `[P]` con TODO. **No inventes valores hex definitivos.**

**`la-violencia-historia`** (desde los docs 01, 02 y 04 §5 y §7):
- **Nombres:** alterados en la ficción y reales en el Archivo, según la tabla de la biblia.
- **Diálogos:** prohibido inventar diálogos a figuras reales, aunque estén renombradas. Las víctimas reales no se ficcionalizan.
- **Marcas [V]/[P]:** nada [P] entra a un build público.
- **Esquema del Archivo:** fuente, licencia y `estado_verificacion`.
- **Diseño:** nunca premiar matar; sin contador de bajas; atrocidades no jugables; combate solo contra armados, máximo 1 por misión.
- **Fuentes de referencia:** CNMH, Comisión de la Verdad, informe ¡Basta Ya!

## Bloque 9 — Documentación del repo

1. **`CLAUDE.md` en la raíz** (corto):
   - Propósito del proyecto y reglas no negociables (resumen de las skills propias).
   - Mapa del repo: `planeacion/` (documentación: `historia/`, `produccion/`, `arte/`, `tecnico/`) y `game/` (desarrollo).
   - Comandos (se ejecutan en `game/`).
   - Cuándo usar cada skill (las propias tienen prioridad en arte e historia).
2. **`.claude/SKILLS.md`:** tabla por skill con nombre, fuente, tag/SHA, licencia, fecha, motivo y resultado de la auditoría.
3. **`game/README.md`:** requisitos, instalación y scripts. Actualiza el `README.md` de la raíz solo con Edit, si hace falta.

## Bloque 10 — Validación final

1. Clon limpio (o, en `game/`, `rm -rf node_modules dist art/build` + instalación con lockfile) → todos los scripts en verde.
2. La escena de prueba muestra la figura SVG animada con tween, el diálogo Ink con decisión y el visor con 1 entrada del Archivo.
3. Las skills aparecen como disponibles. Prompts de prueba:
   - "crea un tween de caminata para Rosalba" → Phaser + `la-violencia-art`.
   - "añade una entrada al Archivo" → `la-violencia-historia`.
4. Commit final. Sin push.

## Reporte final (breve)

- Versiones instaladas, con su fuente de verificación.
- Skills instaladas, con tag/SHA y licencia.
- Lo descartado y por qué.
- Decisiones que quedaron pendientes de mi parte.
- Lista de [P].
- Riesgos de la auditoría.
- Próximo paso sugerido según el Sprint 0/1 del doc 00.
