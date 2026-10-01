---
name: la-violencia-art
description: >
  Dirección de arte y pipeline de assets del juego "La Violencia" (Tomo I): estilo novela
  gráfica de tinta, personajes SVG por piezas (cut-out), exactitud de época 1946–1958 y
  representación de la violencia sin espectáculo. Úsala SIEMPRE que se cree, edite, revise o
  anime cualquier asset visual del juego — SVG, personajes, fondos, paralaje, objetos, armas,
  uniformes, UI dibujada, viñetas de cómic, tweens de piezas o el atlas — aunque la petición
  no diga "arte" (p. ej. "crea un tween de caminata para Rosalba", "dibuja la plaza de Puente
  Alto", "añade el fusil de Aurelio"). Tiene prioridad sobre skills genéricas de arte o
  assets (create-game-assets, canvas-design, algorithmic-art) en este repo.
---

# La Violencia — arte

El juego es un documental jugable: el arte puede ser simple, pero no puede mentir sobre la
época ni convertir la violencia en espectáculo. Esta skill resume las reglas; **la fuente es
`planeacion/arte/tomo1/03_direccion_arte.md` (doc 03)**. Léelo antes de actuar: aquí no se
copian sus tablas para que no queden desactualizadas. `planeacion/` es solo lectura salvo
que Daniel pida editarla.

## Antes de dibujar

1. Lee el doc 03 §1 (lenguaje visual y violencia) y la sección de §3 que corresponda al
   lugar o actor (Boyacá rural, Bogotá 9-abr-1948, Llanos, fuerzas armadas y policía).
2. Busca cada elemento que vas a dibujar en la tabla [V]/[P] del doc 03 §3. Si está **[P]**
   o no aparece, no lo dibujes como versión final: haz un placeholder marcado
   (`data-p="motivo"` en el grupo y "[P]" en el nombre del archivo o en un comentario) y
   avísalo. Un [P] dibujado con aplomo se lee como hecho histórico.
3. Si el asset es de un personaje, revisa su nombre y rol en
   `planeacion/historia/tomo1/01_biblia_nomenclatura.md` (doc 01): las figuras reales
   aparecen con nombre alterado y nunca se retratan con rasgos inventados como si fueran
   documentales.

## Estilo (resumen del doc 03 §1)

- Tinta negra de grosor variable (gruesa en siluetas y primer plano, fina en fondo) sobre
  papel hueso con textura leve.
- Grises solo por **trama** (rayado o semitono, con `<pattern>`), sin degradados complejos.
- Únicos acentos de color: **rojo liberal** y **azul conservador**, y solo en lo que cuenta
  la división (pañuelos, banderas, afiches, fachadas). Ningún otro color de acento.
- Plano lateral con 2–3 capas de paralaje por escena.
- Rostros simplificados: expresión por ojos, cejas y postura; nada de retrato realista.

## Violencia (doc 03 §1 "Violencia")

- Silueta y mancha negra. **Sin sangre roja** (el rojo es del partido liberal), sin gore,
  sin mutilaciones detalladas.
- Rostros de víctimas nunca identificables; muertos en silueta o cubiertos.
- Las atrocidades solo existen como viñetas fijas (antes/después, humo, objetos
  abandonados). Ningún asset debe permitir que el jugador la ejecute o la anime.
- Armas: silueta correcta para el año. Un fusil de cerrojo no se dibuja como uno automático;
  los modelos por año están [P] en el doc 03 §3.4 hasta que se resuelvan.

## Paleta y grosores — [P]

La hoja de estilo con hex, grosores y tramas es un entregable pendiente (doc 03 §6.1;
doc 00 Sprint 0 "Arte"). **TODO [P]:** hasta que exista, no inventes valores hex
definitivos. Usa `#000` y `#fff` (o `currentColor`) como placeholders y deja el color de
acento como referencia a "rojo liberal" / "azul conservador" en un comentario. Cuando la
hoja exista en `planeacion/arte/`, esta sección debe apuntar a ella, no copiarla.

## Personajes por piezas (cut-out)

Piezas mínimas (doc 03 §2): cabeza, torso, brazos, piernas, ruana, sombrero.

Convención del pipeline (`game/tools/art-build.ts`):

- Un archivo por personaje: `game/art/src/personajes/<personaje>.svg`, con
  `viewBox="0 0 W H"` (1 unidad = 1 px a @1x).
- Cada pieza es un `<g id="…" data-pieza data-pivote="x y">` directo bajo la raíz.
  El pivote está en la articulación (hombro, cadera, cuello) en coordenadas del viewBox.
- IDs estables en kebab-case, con lado del **propio personaje**:
  `cabeza`, `torso`, `brazo-izq`, `brazo-der`, `antebrazo-izq`, `antebrazo-der`,
  `pierna-izq`, `pierna-der`, `ruana`, `sombrero`. Detalles internos pueden llevar ids
  propios dentro de la pieza (`ojo-izq`, `ceja-der`), pero no cambies un id publicado:
  el código y los tweens los referencian como frame `personajes/<personaje>/<id>`.
- El orden en el documento es el orden de dibujo (lo primero queda detrás).
- `<defs>` compartidas (tramas) arriba; SVGO conserva ids, grupos y `data-*`.

En Phaser se arma con `armarRecorte()` (`game/src/game/Recorte.ts`): todas las piezas en el
mismo punto, cada una con su pivote como origen. Las animaciones son **tweens de Phaser**
sobre esas piezas (ángulo en articulaciones, leve vaivén del contenedor), no cuadro a
cuadro. Para la API de tweens consulta la skill oficial `tweens`.

## Pipeline (no edites PNG a mano)

```
art/src/**/*.svg → SVGO → PNG @1x/@2x → atlas JSON Hash (art/build, public/generated/art)
```

- `pnpm run art:build` (en `game/`) genera todo; los PNG jamás se editan a mano.
- `pnpm run art:review <ruta.svg | art/build/atlas@1x.json>` crea un PNG de revisión en
  `art/build/revision/` con cajas y pivotes. Ábrelo (Read) para inspeccionarlo antes de
  dar un asset por bueno.
- Las referencias de época se usan solo para dibujar; las fotos reales con licencia viven
  en el Archivo, no en el arte del juego (doc 03 §4).

## Checklist por asset

1. ¿Cada elemento de época está [V] en el doc 03 §3? Lo [P] queda como placeholder marcado.
2. ¿Solo tinta, trama y los dos acentos partidistas? ¿Sin degradados ni colores extra?
3. ¿Violencia en silueta/mancha, sin sangre roja ni rostros de víctimas identificables?
4. ¿Silueta de arma/uniforme/vehículo correcta para el año?
5. Personajes: ¿piezas con ids de la convención, pivotes en articulaciones, orden de capas?
6. `pnpm run art:build` sin errores y PNG de revisión inspeccionado.
7. ¿Se ve bien a escala de juego (1920×1080) sobre su fondo y con el paralaje?
8. Si es la figura de una persona real: ¿sin rasgos inventados presentados como documentales?
