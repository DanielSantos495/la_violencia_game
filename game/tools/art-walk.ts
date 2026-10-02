// Hoja de revisión del ciclo de caminata: N fases de un personaje cut-out, con la misma pose
// que usa el juego (src/core/animacion/caminata.ts) y la jerarquía data-padre del SVG.
//   node tools/art-walk.ts art/src/personajes/rosalba.svg [fases=8]
// Salida: art/build/revision/<nombre>-caminata.png (línea punteada = suelo).
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import { optimize } from 'svgo';
import {
  type PoseCaminata,
  poseCaminata,
} from '../src/core/animacion/caminata.ts';
import { configSvgo, framesDeSvg } from './art-build.ts';

const FONDO = '#ece4d0';

/** Cadena de transformaciones de una pieza: las de sus ancestros y luego la suya. */
function transformDe(
  id: string,
  pose: PoseCaminata,
  meta: Map<string, { pivote: { x: number; y: number }; padre: string | null }>,
): string {
  const cadena: string[] = [];
  for (
    let actual: string | null = id;
    actual;
    actual = meta.get(actual)?.padre ?? null
  ) {
    cadena.unshift(actual);
  }
  return cadena
    .flatMap((pieza) => {
      const m = meta.get(pieza);
      if (!m) return [];
      const t: string[] = [];
      const levante = pose.levante[pieza];
      if (levante) t.push(`translate(0 ${(-levante).toFixed(2)})`);
      t.push(
        `rotate(${(pose.angulos[pieza] ?? 0).toFixed(2)} ${m.pivote.x} ${m.pivote.y})`,
      );
      return t;
    })
    .join(' ');
}

export function hojaCaminata(
  fuente: string,
  nombre: string,
  fases = 8,
): string {
  const frames = framesDeSvg(fuente, nombre);
  const meta = new Map(
    frames
      .filter((f) => f.pivote)
      .map((f) => [
        f.nombre.slice(nombre.length + 1),
        { pivote: f.pivote as { x: number; y: number }, padre: f.padre },
      ]),
  );
  if (meta.size === 0)
    throw new Error(`${nombre}: no tiene piezas con data-pivote`);
  const primero = frames[0];
  if (!primero) throw new Error(`${nombre}: sin frames`);
  const { w, h } = primero.origen;
  const base = optimize(fuente, configSvgo).data;
  const suelo = (() => {
    const bbox = new Resvg(base).getBBox();
    return bbox ? bbox.y + bbox.height : h;
  })();

  const celdas: string[] = [];
  for (let i = 0; i < fases; i++) {
    const pose = poseCaminata((i / fases) * Math.PI * 2);
    const conPose = optimize(base, {
      plugins: [
        {
          name: 'aplicarPose',
          fn: () => ({
            element: {
              enter: (n) => {
                const id = n.attributes.id;
                if (
                  n.name === 'g' &&
                  'data-pieza' in n.attributes &&
                  id &&
                  meta.has(id)
                ) {
                  n.attributes.transform = transformDe(id, pose, meta);
                }
              },
            },
          }),
        },
      ],
    }).data;
    const interior = conPose
      .replace(/^[\s\S]*?<svg[^>]*>/, '')
      .replace(/<\/svg>\s*$/, '');
    celdas.push(
      `<g transform="translate(${i * w} ${(-pose.rebote).toFixed(2)})">${interior}</g>` +
        `<line x1="${i * w}" y1="${suelo}" x2="${(i + 1) * w}" y2="${suelo}" stroke="#000" stroke-width="0.6" stroke-dasharray="3 3"/>`,
    );
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${fases * w}" height="${h}" viewBox="0 0 ${fases * w} ${h}"><rect width="100%" height="100%" fill="${FONDO}"/>${celdas.join('')}</svg>`;
}

if (import.meta.main) {
  const ruta = process.argv[2];
  if (!ruta) {
    console.error('Uso: node tools/art-walk.ts <personaje.svg> [fases]');
    process.exit(1);
  }
  const fases = Number(process.argv[3] ?? 8);
  const nombre = basename(ruta, '.svg');
  const svg = hojaCaminata(readFileSync(resolve(ruta), 'utf8'), nombre, fases);
  const salida = join(
    resolve(import.meta.dirname, '..'),
    'art/build/revision',
    `${nombre}-caminata.png`,
  );
  mkdirSync(dirname(salida), { recursive: true });
  writeFileSync(
    salida,
    new Resvg(svg, { font: { loadSystemFonts: false } }).render().asPng(),
  );
  console.log(`✓ ${salida}`);
}
