// Renderiza un PNG de revisión para inspeccionar arte (Daniel y Claude).
//   node tools/art-review.ts art/src/prueba/figura.svg   → piezas con su caja y pivote, a @2x
//   node tools/art-review.ts art/build/atlas@1x.json     → atlas con el contorno de cada frame
// Salida: art/build/revision/<nombre>.png. El fondo y los colores de marca son solo de revisión.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import { type Atlas, framesDeSvg, rasterizar } from './art-build.ts';

const FONDO = '#ece4d0';
const MARCA = '#d0006f';

function revisarSvg(ruta: string): Buffer {
  const escala = 2;
  const frames = framesDeSvg(
    readFileSync(ruta, 'utf8'),
    basename(ruta, '.svg'),
  );
  const primero = frames[0];
  if (!primero) throw new Error('SVG sin frames');
  const w = primero.origen.w * escala;
  const h = primero.origen.h * escala;
  const capas = frames.map((f) => {
    const r = rasterizar(f, escala);
    const x = r.recorte.x * escala;
    const y = r.recorte.y * escala;
    const caja = `<rect x="${x}" y="${y}" width="${r.ancho}" height="${r.alto}" fill="none" stroke="${MARCA}" stroke-dasharray="6 4"/>`;
    const pivote = f.pivote
      ? `<g stroke="${MARCA}" stroke-width="2"><line x1="${f.pivote.x * escala - 8}" y1="${f.pivote.y * escala}" x2="${f.pivote.x * escala + 8}" y2="${f.pivote.y * escala}"/><line x1="${f.pivote.x * escala}" y1="${f.pivote.y * escala - 8}" x2="${f.pivote.x * escala}" y2="${f.pivote.y * escala + 8}"/></g>`
      : '';
    return `<image x="${x}" y="${y}" width="${r.ancho}" height="${r.alto}" href="data:image/png;base64,${r.png.toString('base64')}"/>${caja}${pivote}`;
  });
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="100%" height="100%" fill="${FONDO}"/>${capas.join('')}</svg>`;
  return new Resvg(svg, { font: { loadSystemFonts: false } }).render().asPng();
}

function revisarAtlas(ruta: string): Buffer {
  const json = JSON.parse(readFileSync(ruta, 'utf8')) as Atlas['json'];
  const imagen = readFileSync(join(dirname(ruta), String(json.meta.image)));
  const { w, h } = json.meta.size as { w: number; h: number };
  const cajas = Object.values(json.frames)
    .map(
      (f) =>
        `<rect x="${f.frame.x}" y="${f.frame.y}" width="${f.frame.w}" height="${f.frame.h}" fill="none" stroke="${MARCA}"/>`,
    )
    .join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="100%" height="100%" fill="${FONDO}"/><image width="${w}" height="${h}" href="data:image/png;base64,${imagen.toString('base64')}"/>${cajas}</svg>`;
  return new Resvg(svg, { font: { loadSystemFonts: false } }).render().asPng();
}

const ruta = process.argv[2];
if (!ruta) {
  console.error('Uso: node tools/art-review.ts <archivo.svg | atlas.json>');
  process.exit(1);
}
const absoluta = resolve(ruta);
const png = absoluta.endsWith('.json')
  ? revisarAtlas(absoluta)
  : revisarSvg(absoluta);
const salida = join(
  resolve(import.meta.dirname, '..'),
  'art/build/revision',
  `${basename(absoluta).replace(/\.(svg|json)$/, '')}.png`,
);
mkdirSync(dirname(salida), { recursive: true });
writeFileSync(salida, png);
console.log(`✓ ${salida}`);
