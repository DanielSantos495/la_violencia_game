// Ciclo de caminata de un personaje cut-out con la misma pose que usa el juego
// (src/core/animacion/caminata.ts) y la jerarquía data-padre del SVG.
//   node tools/art-walk.ts art/src/personajes/rosalba.svg [fases=8] [--falda-larga]
//   node tools/art-walk.ts art/src/personajes/acto1/rosalba-corriendo.svg [fases=8] --carrera
//   node tools/art-walk.ts art/src/personajes/acto2/rosalba-llano.svg [fases=8] --canilla
//   node tools/art-walk.ts art/src/personajes/acto2/rosalba-llano-corriendo.svg --carrera --bracea-ambos
// - Hoja de revisión: art/build/revision/<nombre>-caminata.png o -carrera.png (línea
//   punteada = suelo).
// - Con --falda-larga además verifica, fase a fase, que ninguna pierna salga de la falda
//   (canilla cortada a la vista o pie por detrás del ruedo); termina con error si sale.
// - Con --carrera (src/core/animacion/carrera.ts) verifica que la rodilla, donde se corta la
//   canilla, nunca asome bajo la falda o la enagua. --bracea-ambos: los dos brazos bracean.
// - Con --canilla (caminata con falda a media pierna, pivote en la rodilla) verifica lo mismo
//   al caminar.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import { optimize } from 'svgo';
import {
  type OpcionesCaminata,
  type PoseCaminata,
  poseCaminata,
} from '../src/core/animacion/caminata.ts';
import {
  type OpcionesCarrera,
  poseCarrera,
} from '../src/core/animacion/carrera.ts';
import { configSvgo, framesDeSvg } from './art-build.ts';

const FONDO = '#ece4d0';

type Meta = Map<
  string,
  { pivote: { x: number; y: number }; padre: string | null }
>;

interface Personaje {
  meta: Meta;
  base: string;
  w: number;
  h: number;
  suelo: number;
}

function prepararPersonaje(fuente: string, nombre: string): Personaje {
  const frames = framesDeSvg(fuente, nombre);
  const meta: Meta = new Map(
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
  const base = optimize(fuente, configSvgo).data;
  const bbox = new Resvg(base).getBBox();
  return {
    meta,
    base,
    w: primero.origen.w,
    h: primero.origen.h,
    suelo: bbox ? bbox.y + bbox.height : primero.origen.h,
  };
}

/** Cadena de transformaciones de una pieza: las de sus ancestros y luego la suya. */
function transformDe(id: string, pose: PoseCaminata, meta: Meta): string {
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
      const dx = pose.avance[pieza] ?? 0;
      const dy = -(pose.levante[pieza] ?? 0);
      if (dx || dy) t.push(`translate(${dx.toFixed(2)} ${dy.toFixed(2)})`);
      t.push(
        `rotate(${(pose.angulos[pieza] ?? 0).toFixed(2)} ${m.pivote.x} ${m.pivote.y})`,
      );
      return t;
    })
    .join(' ');
}

/** El SVG del personaje en una pose; con `incluir`, solo esas piezas (para medir). */
function svgEnPose(
  p: Personaje,
  pose: PoseCaminata,
  incluir: (id: string) => boolean = () => true,
): string {
  return optimize(p.base, {
    plugins: [
      {
        name: 'aplicarPose',
        fn: () => ({
          element: {
            enter: (n, padre) => {
              const id = n.attributes.id;
              if (n.name !== 'g' || !('data-pieza' in n.attributes) || !id)
                return;
              if (!incluir(id)) {
                padre.children = padre.children.filter((c) => c !== n);
                return;
              }
              if (p.meta.has(id))
                n.attributes.transform = transformDe(id, pose, p.meta);
            },
          },
        }),
      },
    ],
  }).data;
}

export function hojaCaminata(
  fuente: string,
  nombre: string,
  fases = 8,
  opciones: OpcionesCaminata = {},
): string {
  return hojaCiclo(fuente, nombre, fases, (fase) =>
    poseCaminata(fase, opciones),
  );
}

/** Hoja de fases de la carrera (pose de correr, canillas con pivote en la rodilla). */
export function hojaCarrera(
  fuente: string,
  nombre: string,
  fases = 8,
  opciones: OpcionesCarrera = {},
): string {
  return hojaCiclo(fuente, nombre, fases, (fase) =>
    poseCarrera(fase, opciones),
  );
}

function hojaCiclo(
  fuente: string,
  nombre: string,
  fases: number,
  poseEn: (fase: number) => PoseCaminata,
): string {
  const p = prepararPersonaje(fuente, nombre);
  const celdas: string[] = [];
  for (let i = 0; i < fases; i++) {
    const pose = poseEn((i / fases) * Math.PI * 2);
    const interior = svgEnPose(p, pose)
      .replace(/^[\s\S]*?<svg[^>]*>/, '')
      .replace(/<\/svg>\s*$/, '');
    celdas.push(
      `<g transform="translate(${i * p.w} ${(-pose.rebote).toFixed(2)})">${interior}</g>` +
        `<line x1="${i * p.w}" y1="${p.suelo}" x2="${(i + 1) * p.w}" y2="${p.suelo}" stroke="#000" stroke-width="0.6" stroke-dasharray="3 3"/>`,
    );
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${fases * p.w}" height="${p.h}" viewBox="0 0 ${fases * p.w} ${p.h}"><rect width="100%" height="100%" fill="${FONDO}"/>${celdas.join('')}</svg>`;
}

export interface FugaPierna {
  fase: number;
  /** Píxeles de pierna visibles por encima del borde inferior de la enagua (canilla cortada). */
  cortada: number;
  /** Píxeles de pierna más atrás que el borde trasero de falda y enagua. */
  detras: number;
}

const OPACO = 64;

/**
 * Mide, fase a fase, cuánto de las piernas queda fuera de la falda. Bajo una falda larga
 * solo deben verse los pies bajo el ruedo: nada de canilla por los lados ni pies por detrás.
 */
export function revisarPiernasBajoFalda(
  fuente: string,
  nombre: string,
  opciones: OpcionesCaminata,
  fases = 32,
): FugaPierna[] {
  const p = prepararPersonaje(fuente, nombre);
  const pixeles = (svg: string) =>
    new Resvg(svg, { font: { loadSystemFonts: false } }).render();
  const resultado: FugaPierna[] = [];
  for (let i = 0; i < fases; i++) {
    const pose = poseCaminata((i / fases) * Math.PI * 2, opciones);
    const imgPiernas = pixeles(
      svgEnPose(p, pose, (id) => id.startsWith('pierna-')),
    );
    const imgCubre = pixeles(
      svgEnPose(p, pose, (id) => id === 'falda' || id === 'enagua'),
    );
    const { width: w, height: h } = imgPiernas;
    // El getter .pixels copia el búfer en cada acceso: se lee una sola vez.
    const piernas = imgPiernas.pixels;
    const cubre = imgCubre.pixels;
    const a = (img: Buffer, x: number, y: number) =>
      img[(y * w + x) * 4 + 3] ?? 0;

    // Borde trasero de la tela y altura del ruedo más alto (por columnas).
    let minX = w;
    let bordeInferior = h;
    for (let x = 0; x < w; x++) {
      let ultimo = -1;
      for (let y = 0; y < h; y++) if (a(cubre, x, y) > OPACO) ultimo = y;
      if (ultimo >= 0) {
        minX = Math.min(minX, x);
        bordeInferior = Math.min(bordeInferior, ultimo);
      }
    }

    let cortada = 0;
    let detras = 0;
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        if (a(piernas, x, y) <= OPACO) continue;
        if (x < minX) detras++;
        if (y < bordeInferior - 1 && a(cubre, x, y) <= OPACO) cortada++;
      }
    }
    resultado.push({ fase: i / fases, cortada, detras });
  }
  return resultado;
}

export interface FugaRodilla {
  fase: number;
  /** Píxeles de pierna a la vista cerca de la rodilla (el corte de la canilla). */
  rodilla: number;
}

/**
 * Cuenta, fase a fase, los píxeles de canilla que quedan a la vista a menos de `radio` px de
 * la rodilla (pivote de la pierna, movido con la pose): ahí la canilla está cortada y debe
 * quedar siempre bajo la falda o la enagua. `opciones` son las de la carrera o, para otra pose
 * cíclica con canillas (caminata en modo canilla), la función que da la pose en cada fase.
 */
export function revisarRodillas(
  fuente: string,
  nombre: string,
  opciones: OpcionesCarrera | ((fase: number) => PoseCaminata) = {},
  fases = 32,
  radio = 16,
): FugaRodilla[] {
  const poseEn =
    typeof opciones === 'function'
      ? opciones
      : (fase: number) => poseCarrera(fase, opciones);
  const p = prepararPersonaje(fuente, nombre);
  const pixeles = (svg: string) =>
    new Resvg(svg, { font: { loadSystemFonts: false } }).render();
  const resultado: FugaRodilla[] = [];
  for (let i = 0; i < fases; i++) {
    const pose = poseEn((i / fases) * Math.PI * 2);
    const imgPiernas = pixeles(
      svgEnPose(p, pose, (id) => id.startsWith('pierna-')),
    );
    const imgCubre = pixeles(
      svgEnPose(p, pose, (id) => id === 'falda' || id === 'enagua'),
    );
    const { width: w, height: h } = imgPiernas;
    const piernas = imgPiernas.pixels;
    const cubre = imgCubre.pixels;
    const a = (img: Buffer, x: number, y: number) =>
      img[(y * w + x) * 4 + 3] ?? 0;
    const rodillas = ['pierna-der', 'pierna-izq'].flatMap((id) => {
      const m = p.meta.get(id);
      if (!m) return [];
      return [
        {
          x: m.pivote.x + (pose.avance[id] ?? 0),
          y: m.pivote.y - (pose.levante[id] ?? 0),
        },
      ];
    });
    let rodilla = 0;
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        if (a(piernas, x, y) <= OPACO || a(cubre, x, y) > OPACO) continue;
        if (rodillas.some((k) => Math.hypot(x - k.x, y - k.y) < radio))
          rodilla++;
      }
    }
    resultado.push({ fase: i / fases, rodilla });
  }
  return resultado;
}

if (import.meta.main) {
  const args = process.argv.slice(2);
  const ruta = args.find((a) => !a.startsWith('--') && !/^\d+$/.test(a));
  if (!ruta) {
    console.error(
      'Uso: node tools/art-walk.ts <personaje.svg> [fases] [--falda-larga | --canilla | --carrera [--bracea-ambos]]',
    );
    process.exit(1);
  }
  const fases = Number(args.find((a) => /^\d+$/.test(a)) ?? 8);
  const opciones: OpcionesCaminata = args.includes('--falda-larga')
    ? { faldaLarga: true }
    : args.includes('--canilla')
      ? { canilla: true }
      : {};
  const opcionesCarrera: OpcionesCarrera = args.includes('--bracea-ambos')
    ? { bracea: 'ambos' }
    : {};
  const nombre = basename(ruta, '.svg');
  const fuente = readFileSync(resolve(ruta), 'utf8');

  const carrera = args.includes('--carrera');
  const salida = join(
    resolve(import.meta.dirname, '..'),
    'art/build/revision',
    `${nombre}-${carrera ? 'carrera' : 'caminata'}.png`,
  );
  mkdirSync(dirname(salida), { recursive: true });
  const svg = carrera
    ? hojaCarrera(fuente, nombre, fases, opcionesCarrera)
    : hojaCaminata(fuente, nombre, fases, opciones);
  writeFileSync(
    salida,
    new Resvg(svg, { font: { loadSystemFonts: false } }).render().asPng(),
  );
  console.log(`✓ ${salida}`);

  if (opciones.faldaLarga) {
    const fugas = revisarPiernasBajoFalda(fuente, nombre, opciones).filter(
      (f) => f.cortada > 0 || f.detras > 0,
    );
    if (fugas.length > 0) {
      for (const f of fugas) {
        console.error(
          `✗ fase ${f.fase.toFixed(3)}: canilla visible ${f.cortada} px, pie detrás ${f.detras} px`,
        );
      }
      process.exit(1);
    }
    console.log('✓ piernas siempre bajo la falda (32 fases)');
  }

  if (carrera || opciones.canilla) {
    const fugas = revisarRodillas(
      fuente,
      nombre,
      carrera ? opcionesCarrera : (fase) => poseCaminata(fase, opciones),
    ).filter((f) => f.rodilla > 0);
    if (fugas.length > 0) {
      for (const f of fugas) {
        console.error(
          `✗ fase ${f.fase.toFixed(3)}: rodilla a la vista ${f.rodilla} px`,
        );
      }
      process.exit(1);
    }
    console.log('✓ rodillas siempre bajo la falda o la enagua (32 fases)');
  }
}
