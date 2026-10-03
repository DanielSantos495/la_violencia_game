// Compone un escenario como lo verá la cámara, sin navegador (Daniel y Claude).
//   node tools/art-escena.ts [escenario] [scrollX…]
//   p. ej. node tools/art-escena.ts puente-alto 0 1460 2900
// Usa los PNG recortados de art/build/png y sus recortes del atlas: corre antes `pnpm art:build`.
// Salida en art/build/revision/: escena-<escenario>-<scrollX>.png (1920×1080, una por posición)
// y escena-<escenario>.png (todas apiladas a 1/2). Las nubes salen en su x inicial.
// La marca vertical en x=640 de pantalla mide 1,55 m (Rosalba) y es solo de revisión.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import { archivoDeGrupo } from '../src/core/arte/atlas.ts';
import {
  anchoCapa,
  ORDEN_CAPAS,
  PARALAJE,
  PX_POR_METRO,
  VIEWPORT,
  Y_SUELO,
} from '../src/core/escena/escala.ts';
import {
  copiasMosaico,
  type DefinicionEscenario,
  frameDe,
  xEnPantalla,
  yArriba,
} from '../src/core/escenarios/escenario.ts';
import { PUENTE_ALTO } from '../src/core/escenarios/puente-alto.ts';
import type { Atlas, FrameAtlas } from './art-build.ts';

const ESCENARIOS: Record<string, DefinicionEscenario> = {
  'puente-alto': PUENTE_ALTO,
};

/** Papel de la paleta (game/art/paleta.json): el fondo de cámara de las escenas. */
const FONDO = (
  JSON.parse(
    readFileSync(resolve(import.meta.dirname, '../art/paleta.json'), 'utf8'),
  ) as { colores: { id: string; hex: string }[] }
).colores.find((c) => c.id === 'papel')?.hex;
if (!FONDO) throw new Error('paleta.json sin el color papel');
const MARCA = '#d0006f';

interface Pieza {
  id: string;
  datos: FrameAtlas;
}

/** Imágenes de los frames (una vez cada una) y su recorte dentro del módulo. */
function cargarFrames(
  raiz: string,
  def: DefinicionEscenario,
): { piezas: Map<string, Pieza>; defs: string } {
  const json = JSON.parse(
    readFileSync(
      join(raiz, 'art/build/atlas', `${archivoDeGrupo(def.atlas)}@1x.json`),
      'utf8',
    ),
  ) as Atlas['json'];
  const piezas = new Map<string, Pieza>();
  const defs: string[] = [];
  for (const pagina of json.textures) {
    for (const datos of pagina.frames) {
      const id = `f${piezas.size}`;
      const png = readFileSync(
        join(raiz, 'art/build/png', `${datos.filename}@1x.png`),
      );
      const { x, y, w, h } = datos.spriteSourceSize;
      defs.push(
        `<image id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" href="data:image/png;base64,${png.toString('base64')}"/>`,
      );
      piezas.set(datos.filename, { id, datos });
    }
  }
  return { piezas, defs: `<defs>${defs.join('')}</defs>` };
}

/** Una vista de 1920×1080 con la cámara en `scrollX` (sin las <defs>). */
function vista(
  def: DefinicionEscenario,
  piezas: Map<string, Pieza>,
  scrollX: number,
): string {
  const usos: string[] = [];
  const poner = (
    modulo: string,
    x: number,
    arriba: number,
    espejo: boolean,
  ) => {
    const pieza = piezas.get(frameDe(def, modulo));
    if (!pieza) throw new Error(`${modulo}: no está en el atlas (¿art:build?)`);
    const { w } = pieza.datos.sourceSize;
    if (x + w < 0 || x > VIEWPORT.ancho) return;
    // Volteo en el sitio, como Phaser: el módulo ocupa el mismo rectángulo.
    usos.push(
      espejo
        ? `<use href="#${pieza.id}" transform="translate(${x + w} ${arriba}) scale(-1 1)"/>`
        : `<use href="#${pieza.id}" transform="translate(${x} ${arriba})"/>`,
    );
  };
  for (const id of ORDEN_CAPAS) {
    const datos = def.capas[id];
    if (!datos) continue;
    const ancho = anchoCapa(def.anchoNivel, PARALAJE[id]);
    for (const mosaico of datos.mosaicos ?? []) {
      const pieza = piezas.get(frameDe(def, mosaico.modulo));
      if (!pieza) throw new Error(`${mosaico.modulo}: no está en el atlas`);
      for (const x of copiasMosaico(pieza.datos.sourceSize.w, ancho))
        poner(mosaico.modulo, xEnPantalla(x, id, scrollX), mosaico.y, false);
    }
    for (const col of datos.colocaciones) {
      const pieza = piezas.get(frameDe(def, col.modulo));
      if (!pieza) throw new Error(`${col.modulo}: no está en el atlas`);
      poner(
        col.modulo,
        xEnPantalla(col.x, id, scrollX),
        yArriba(col, id, pieza.datos.sourceSize.h),
        col.espejo ?? false,
      );
    }
  }
  const alto = 1.55 * PX_POR_METRO;
  usos.push(
    `<rect x="632" y="${Y_SUELO - alto}" width="16" height="${alto}" fill="none" stroke="${MARCA}" stroke-width="2" stroke-dasharray="8 5"/>`,
  );
  return `<rect width="${VIEWPORT.ancho}" height="${VIEWPORT.alto}" fill="${FONDO}"/>${usos.join('')}`;
}

if (import.meta.main) {
  const raiz = resolve(import.meta.dirname, '..');
  const [nombre = 'puente-alto', ...posiciones] = process.argv.slice(2);
  const def = ESCENARIOS[nombre];
  if (!def) {
    console.error(
      `Escenario desconocido: ${nombre}. Hay: ${Object.keys(ESCENARIOS).join(', ')}`,
    );
    process.exit(1);
  }
  const maximo = def.anchoNivel - VIEWPORT.ancho;
  const scrolls = (
    posiciones.length > 0
      ? posiciones.map(Number)
      : [0, 0.25, 0.5, 0.75, 1].map((t) => Math.round(t * maximo))
  ).map((s) => Math.min(maximo, Math.max(0, s)));
  const { piezas, defs } = cargarFrames(raiz, def);
  const salida = join(raiz, 'art/build/revision');
  mkdirSync(salida, { recursive: true });
  const { ancho: w, alto: h } = VIEWPORT;
  const tiras: string[] = [];
  scrolls.forEach((s, i) => {
    const cuerpo = vista(def, piezas, s);
    const png = new Resvg(
      `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${defs}${cuerpo}</svg>`,
      { font: { loadSystemFonts: false } },
    )
      .render()
      .asPng();
    writeFileSync(join(salida, `escena-${nombre}-${s}.png`), png);
    tiras.push(
      `<g transform="translate(0 ${i * (h / 2 + 12)}) scale(0.5)"><svg width="${w}" height="${h}">${cuerpo}</svg></g>`,
    );
  });
  const altoHoja = scrolls.length * (h / 2 + 12) - 12;
  const hoja = new Resvg(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w / 2}" height="${altoHoja}">${defs}${tiras.join('')}</svg>`,
    { font: { loadSystemFonts: false } },
  )
    .render()
    .asPng();
  writeFileSync(join(salida, `escena-${nombre}.png`), hoja);
  console.log(
    `✓ ${nombre}: cámara en ${scrolls.join(', ')} → art/build/revision/escena-${nombre}[-<scrollX>].png`,
  );
}
