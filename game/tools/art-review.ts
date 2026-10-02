// Renderiza un PNG de revisión para inspeccionar arte (Daniel y Claude).
//   node tools/art-review.ts art/src/prueba/figura.svg   → piezas con su caja y pivote, a @2x
//   node tools/art-review.ts art/build/atlas/personajes@1x.json → páginas del atlas con el contorno de cada frame
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
  // Páginas apiladas en vertical, cada una con el contorno de sus frames.
  let y = 0;
  const capas = json.textures.map((t) => {
    const imagen = readFileSync(join(dirname(ruta), t.image));
    const cajas = t.frames
      .map(
        (f) =>
          `<rect x="${f.frame.x}" y="${y + f.frame.y}" width="${f.frame.w}" height="${f.frame.h}" fill="none" stroke="${MARCA}"/>`,
      )
      .join('');
    const capa = `<image y="${y}" width="${t.size.w}" height="${t.size.h}" href="data:image/png;base64,${imagen.toString('base64')}"/>${cajas}<line x1="0" y1="${y + t.size.h + 4}" x2="${t.size.w}" y2="${y + t.size.h + 4}" stroke="${MARCA}" stroke-dasharray="6 4"/>`;
    y += t.size.h + 8;
    return capa;
  });
  const w = Math.max(...json.textures.map((t) => t.size.w));
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${y}"><rect width="100%" height="100%" fill="${FONDO}"/>${capas.join('')}</svg>`;
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
