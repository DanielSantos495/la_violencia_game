# Tomo I — Documento técnico (plataforma y stack)

**Contexto que define el stack:** juego 2D lateral estilo novela gráfica · desarrollador único con perfil JavaScript/frontend · web como plataforma principal y escritorio como segunda · lanzamiento por episodios · assets SVG, música y efectos producidos por Claude · sin voces (solo texto).
Versiones verificadas al 1 de octubre de 2026; lo no verificado va marcado **[P]**.

---

## 1. Decisión de plataforma
- **Web (principal):** se juega en el navegador desde un enlace. Renderizado 2D con WebGL (y Canvas como respaldo), que funciona en prácticamente cualquier navegador actual; no depende de WebGPU.
- **Escritorio (segunda):** el mismo código empaquetado como app para Steam/itch.io.
- **Portal del Archivo:** sección del mismo sitio (no un proyecto aparte), para que un solo desarrollador mantenga una sola base de código.

## 2. Motor

| Opción | Estado verificado | Ajuste |
|---|---|---|
| **Phaser 4 + TypeScript** | Phaser 4 lanzado; vigente 4.2.1 (verificado en npm, 1-oct-2026) | **Recomendado.** JavaScript/TypeScript nativo, pensado para web 2D, el mismo ecosistema que ya dominas (npm, Vite) |
| Godot 4.6 | Estable (ene-2026), exporta a web | Buena alternativa, pero implica aprender GDScript y su editor; la exportación web es más pesada |
| Unreal / Unity | — | Descartados: sobredimensionados para 2D cómic |

**Política de versión:** fijar la versión de Phaser 4.x vigente al iniciar (verificar número exacto en phaser.io/npm antes de instalar con `pnpm`) y no actualizar de versión menor en mitad de un episodio.

## 3. Stack

| Área | Tecnología | Nota |
|---|---|---|
| Lenguaje | TypeScript 7 (compilador nativo) | Tipado de estados narrativos y del Archivo |
| Entorno | Node 24 LTS + **pnpm** | Versiones fijadas (`.nvmrc`, `engines`, `packageManager`); pnpm por sus protecciones de supply chain |
| Build | Vite | Proyecto creado a mano (sin la plantilla oficial: desactualizada y con telemetría) |
| Calidad | Biome (lint + formato) · Vitest (tests) | `typescript-eslint` no soporta TS 7 |
| Motor 2D | Phaser 4 | Escenas, cámara con paralaje, físicas arcade simples, tweens |
| Narrativa | **Ink** (lenguaje de inkle) + **inkjs** (runtime oficial en JavaScript) | Guion en texto plano (`.ink`), compilado a JSON; variables del guion viven en Ink |
| Arte | SVG fuente → PNG + atlas en build | Script Node (librería de rasterizado SVG **[P: elegir y verificar]**) + empaquetador de atlas **[P]** |
| Animación | Recortes por piezas con tweens de Phaser | Sin software de animación de pago |
| UI (menús, Archivo, libreta) | DOM/HTML+CSS sobre el canvas | Aprovecha tu perfil frontend; accesible y fácil de maquetar |
| Audio (reproducción) | Web Audio vía Phaser | Música en bucle y efectos; sin voces |
| Audio (producción) | Scripts de generación: música en MIDI + render con bancos de sonido libres; efectos por síntesis | Fuentes en `audio/src`, salida OGG/M4A en build **[P: herramientas y licencias de bancos]** |
| Guardado | localStorage con respaldo exportable (archivo JSON descargable) | En escritorio, archivo local |
| Escritorio | **Tauri 2** (app liviana con webview del sistema) | **[P]** integración con Steam (overlay/logros) tiene problemas reportados; validar en spike. Alternativa: Electron |
| Hosting web | Estático en CDN | Costo bajo |
| Control de versiones | Git | SVG y fuentes de audio son texto/MIDI; los binarios se generan en build |
| CI | GitHub Actions: lint, tests, validación del Archivo, build web | |

## 4. Arquitectura del código
Todo el proyecto vive en `game/`. Tres capas (decidido el 1-oct-2026): `core/` es lógica pura sin Phaser ni DOM (se testea en Node); `game/` es todo lo que usa Phaser; `ui/` es DOM.
```
src/
  main.ts                 arranque de Phaser
  core/                   lógica pura (sin Phaser ni DOM)
    narrative/
      InkRunner.ts        carga el JSON de Ink, expone diálogos y decisiones
      NarrativeState.ts   puente entre variables de Ink y el guardado
    archivo/
      ArchivoStore.ts     carga entradas validadas (esquema §7)
    mechanics/            reglas puras: rollo de 12 exposiciones, conciencia, munición…
  game/                   Phaser
    scenes/               Boot, Menu, Episodio, Mision (base), PaginaComic, Archivo
    mechanics/
      Movimiento.ts       caminar, correr, agacharse, ocultarse (lateral)
      Sigilo.ts           conos de visión, ruido, escondites
      Camara.ts           encuadre y viñeta de foto (Custodia)
      Libreta.ts          notas y testimonios
      Combate.ts          enfrentamientos breves (ver §5)
      Ordenes.ts          órdenes y conciencia (Aurelio)
  ui/                     componentes DOM (globos, libreta, visor de Archivo)
content/
  ink/                    guion por episodio (.ink)
  archivo/                entradas JSON (fuente única)
art/
  src/                    SVG fuente por personaje/escenario
  build/                  PNG y atlas generados (no se editan a mano)
```

## 5. Combate (simple y raro)
- Solo contra combatientes armados; nunca contra civiles.
- Máximo 1 enfrentamiento por misión, y solo en misiones de Rosalba y Aurelio.
- Mecánica lateral: cubrirse tras obstáculos, asomarse, disparar con **munición muy limitada** y recarga lenta propia de armas de la época (cerrojo, escopeta de un tiro). Retirarse es siempre una opción válida.
- Sin contador de bajas en ningún sistema ni UI. La misión se evalúa por supervivencia, civiles protegidos e información registrada.
- Las atrocidades no son jugables: se narran en páginas de cómic.

## 6. Episodios
| Episodio | Contenido | Lanzamiento |
|---|---|---|
| **1 — "El 9 de abril"** | Prólogo + Acto I (M1–M3) | Primero |
| **2 — "El monte y la ley"** | Acto II (M4–M6) + 13 de junio | Segundo |
| **3 — "La amnistía rota"** | Acto III (M7–M9) + Epílogo | Tercero |

El guardado es compatible entre episodios: las decisiones del episodio 1 se arrastran.

## 7. Esquema de entrada del Archivo (fuente única)
```json
{
  "id": "arch-1948-04-09-tranvia",
  "titulo": "Tranvía incendiado en la Carrera Séptima",
  "fecha": "1948-04-09",
  "lugar": "Carrera 7 con Av. Jiménez, Bogotá",
  "nombre_en_juego": null,
  "nombre_real": null,
  "texto": "…",
  "estado_verificacion": "verificado | pendiente",
  "fuentes": [{ "titulo": "Fototeca Archivo de Bogotá, reg. 266", "url": "…", "tipo": "fotografia" }],
  "licencia": { "titular": "Banco de la República", "estado": "solicitada | concedida | no_aplica" },
  "desbloqueo": { "episodio": 1, "mision": "M1", "condicion": "fotografiar_tranvia" }
}
```
Regla de CI: entradas `pendiente` o sin licencia concedida no se incluyen en builds públicos.

## 8. Requisitos objetivo
- Navegadores de escritorio actuales; 60 fps en computadores escolares modestos.
- Resolución base 1920×1080 con escalado; soporte de teclado y control.
- Móvil: fuera de alcance del Tomo I.
- Tamaño de descarga inicial por episodio: objetivo < 100 MB **[P: validar con el slice]**.

## Fuentes técnicas
- [Phaser 4 — descargas](https://phaser.io/download/phaser4) · [Phaser v4.1.0](https://phaser.io/download/release/v4.1.0) · [Phaser 3 vs Phaser 4](https://phaser.io/news/2026/05/phaser-3-vs-phaser-4)
- [inkjs (inkle)](https://github.com/inkle/inkjs)
- [Portar un juego web a Steam con Tauri](https://pixelartcode.uk/posts/porting-pixel-game-to-steam-with-tauri) · [Issue de Steam Overlay en Tauri](https://github.com/tauri-apps/tauri/issues/6196)
- Godot 4.6: 80.lv, ene-2026.
