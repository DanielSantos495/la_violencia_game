// Pipeline de arte (doc 03 §2): art/src/**/*.svg → SVGO → PNG @1x/@2x → atlas JSON Hash de Phaser.
// Los PNG se generan siempre; nunca se editan a mano.
//
// Convención de los SVG fuente:
// - Raíz con viewBox; 1 unidad = 1 px a @1x.
// - Personajes por piezas (cut-out): cada pieza es un <g id="…" data-pieza> y opcionalmente
//   data-pivote="x y" (en coordenadas del viewBox) para rotar en tweens, y data-padre="id"
//   si cuelga de otra pieza (antebrazo → brazo); el padre se declara antes que el hijo.
//   Frame: "<archivo>/<id>". Sin piezas, el archivo entero es un frame: "<archivo>".
// - Las piezas se exportan recortadas (trimmed) conservando su posición en el personaje,
//   así que todas se colocan en el mismo x,y y la figura se arma sola.
import {
  copyFileSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { type BBox, Resvg } from '@resvg/resvg-js';
import { MaxRectsPacker } from 'maxrects-packer';
import { type Config, optimize, type XastElement } from 'svgo';

export const ESCALAS = [1, 2] as const;

/** Preserva IDs, grupos y atributos data-* de las piezas de recorte. */
export const configSvgo: Config = {
  multipass: true,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          cleanupIds: false,
          collapseGroups: false,
          moveElemsAttrsToGroup: false,
          moveGroupAttrsToElems: false,
          mergePaths: false,
          removeEmptyContainers: false,
          removeEmptyAttrs: false,
        },
      },
    },
  ],
};

export interface Pieza {
  id: string;
  pivote: { x: number; y: number } | null;
  padre: string | null;
}

export interface FrameFuente {
  nombre: string;
  /** SVG con solo esta pieza (y las defs compartidas). */
  svg: string;
  pivote: { x: number; y: number } | null;
  /** Id de la pieza de la que cuelga (data-padre), o null. */
  padre: string | null;
  /** Tamaño del viewBox del archivo (tamaño de origen del frame a @1x). */
  origen: { w: number; h: number };
}

const esPieza = (n: XastElement): boolean =>
  n.name === 'g' && 'data-pieza' in n.attributes;

function leerViewBox(svg: string, archivo: string): { w: number; h: number } {
  const m =
    /<svg\b[^>]*\bviewBox="\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([-\d.]+)[\s,]+([-\d.]+)\s*"/.exec(
      svg,
    );
  if (!m) throw new Error(`${archivo}: falta viewBox en la raíz`);
  if (Number(m[1]) !== 0 || Number(m[2]) !== 0)
    throw new Error(`${archivo}: el viewBox debe empezar en 0 0`);
  return { w: Number(m[3]), h: Number(m[4]) };
}

function listarPiezas(svg: string, archivo: string): Pieza[] {
  const piezas: Pieza[] = [];
  optimize(svg, {
    plugins: [
      {
        name: 'listarPiezas',
        fn: () => ({
          element: {
            enter: (n) => {
              if (!esPieza(n)) return;
              const id = n.attributes.id;
              if (!id)
                throw new Error(
                  `${archivo}: una pieza (data-pieza) no tiene id`,
                );
              if (piezas.some((p) => p.id === id))
                throw new Error(`${archivo}: id de pieza duplicado "${id}"`);
              const pv = n.attributes['data-pivote']
                ?.trim()
                .split(/[\s,]+/)
                .map(Number);
              const pivote =
                pv && pv.length === 2 && pv.every(Number.isFinite)
                  ? { x: pv[0] as number, y: pv[1] as number }
                  : null;
              if (n.attributes['data-pivote'] !== undefined && !pivote) {
                throw new Error(
                  `${archivo}: data-pivote inválido en "${id}" (formato "x y")`,
                );
              }
              const padre = n.attributes['data-padre'] ?? null;
              if (padre !== null && !piezas.some((p) => p.id === padre)) {
                throw new Error(
                  `${archivo}: data-padre "${padre}" de "${id}" no es una pieza declarada antes`,
                );
              }
              if (padre !== null && !pivote) {
                throw new Error(
                  `${archivo}: "${id}" tiene data-padre pero no data-pivote`,
                );
              }
              piezas.push({ id, pivote, padre });
            },
          },
        }),
      },
    ],
  });
  return piezas;
}

function aislarPieza(svg: string, id: string): string {
  return optimize(svg, {
    plugins: [
      {
        name: 'aislarPieza',
        fn: () => ({
          element: {
            enter: (n, padre) => {
              if (esPieza(n) && n.attributes.id !== id)
                padre.children = padre.children.filter((c) => c !== n);
            },
          },
        }),
      },
    ],
  }).data;
}

/** Optimiza un SVG fuente y lo separa en frames (uno por pieza, o uno si no hay piezas). */
export function framesDeSvg(fuente: string, nombreBase: string): FrameFuente[] {
  const svg = optimize(fuente, configSvgo).data;
  const origen = leerViewBox(svg, nombreBase);
  const piezas = listarPiezas(svg, nombreBase);
  if (piezas.length === 0)
    return [{ nombre: nombreBase, svg, pivote: null, padre: null, origen }];
  return piezas.map((p) => ({
    nombre: `${nombreBase}/${p.id}`,
    svg: aislarPieza(svg, p.id),
    pivote: p.pivote,
    padre: p.padre,
    origen,
  }));
}

export interface FrameRaster {
  nombre: string;
  png: Buffer;
  /** Recorte en coordenadas del viewBox, alineado a píxel a esta escala. */
  recorte: { x: number; y: number; w: number; h: number };
  ancho: number;
  alto: number;
}

export function rasterizar(frame: FrameFuente, escala: number): FrameRaster {
  const resvg = new Resvg(frame.svg, {
    fitTo: { mode: 'zoom', value: escala },
    font: { loadSystemFonts: false },
  });
  const bbox = resvg.getBBox();
  if (!bbox) throw new Error(`${frame.nombre}: sin contenido visible`);
  // Alinear el recorte a la rejilla de píxeles de la escala para que no haya medio píxel.
  const x = Math.floor(bbox.x * escala) / escala;
  const y = Math.floor(bbox.y * escala) / escala;
  const w = Math.ceil((bbox.x + bbox.width) * escala) / escala - x;
  const h = Math.ceil((bbox.y + bbox.height) * escala) / escala - y;
  const recorte: BBox = Object.assign(bbox, { x, y, width: w, height: h });
  resvg.cropByBBox(recorte);
  const img = resvg.render();
  return {
    nombre: frame.nombre,
    png: img.asPng(),
    recorte: { x, y, w, h },
    ancho: img.width,
    alto: img.height,
  };
}

export interface FrameAtlas {
  frame: { x: number; y: number; w: number; h: number };
  rotated: false;
  trimmed: true;
  spriteSourceSize: { x: number; y: number; w: number; h: number };
  sourceSize: { w: number; h: number };
  pivot?: { x: number; y: number };
  /** Pieza padre (data-padre); Phaser la expone en frame.customData.padre. */
  padre?: string;
}

export interface Atlas {
  png: Buffer;
  json: { frames: Record<string, FrameAtlas>; meta: Record<string, unknown> };
}

const MAX_ATLAS = 4096;
const RELLENO = 2;

/** Empaqueta los frames de una escala en un atlas (maxrects-packer) y lo compone con resvg. */
export function empaquetar(
  frames: FrameFuente[],
  rasters: FrameRaster[],
  escala: number,
  imagen: string,
): Atlas {
  const packer = new MaxRectsPacker(MAX_ATLAS, MAX_ATLAS, RELLENO, {
    smart: true,
    pot: true,
    border: RELLENO,
  });
  for (const r of rasters) packer.add(r.ancho, r.alto, r);
  if (packer.bins.length !== 1)
    throw new Error(`Los frames no caben en un atlas de ${MAX_ATLAS}px`);
  const bin = packer.bins[0];
  if (!bin) throw new Error('Atlas vacío');

  const jsonFrames: Record<string, FrameAtlas> = {};
  const imagenes: string[] = [];
  for (const rect of bin.rects) {
    const r = rect.data as FrameRaster;
    const f = frames.find((x) => x.nombre === r.nombre);
    if (!f) throw new Error(`Frame sin fuente: ${r.nombre}`);
    const entrada: FrameAtlas = {
      frame: { x: rect.x, y: rect.y, w: r.ancho, h: r.alto },
      rotated: false,
      trimmed: true,
      spriteSourceSize: {
        x: Math.round(r.recorte.x * escala),
        y: Math.round(r.recorte.y * escala),
        w: r.ancho,
        h: r.alto,
      },
      sourceSize: {
        w: Math.round(f.origen.w * escala),
        h: Math.round(f.origen.h * escala),
      },
    };
    if (f.pivote)
      entrada.pivot = {
        x: f.pivote.x / f.origen.w,
        y: f.pivote.y / f.origen.h,
      };
    if (f.padre) entrada.padre = f.padre;
    jsonFrames[r.nombre] = entrada;
    imagenes.push(
      `<image x="${rect.x}" y="${rect.y}" width="${r.ancho}" height="${r.alto}" href="data:image/png;base64,${r.png.toString('base64')}"/>`,
    );
  }
  // Composición a escala 1:1 en posiciones enteras: resvg copia los píxeles sin remuestrear.
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${bin.width}" height="${bin.height}" viewBox="0 0 ${bin.width} ${bin.height}">${imagenes.join('')}</svg>`;
  const png = new Resvg(svg, { font: { loadSystemFonts: false } })
    .render()
    .asPng();
  return {
    png,
    json: {
      frames: jsonFrames,
      meta: {
        app: 'tools/art-build.ts',
        image: imagen,
        format: 'RGBA8888',
        size: { w: bin.width, h: bin.height },
        scale: String(escala),
      },
    },
  };
}

function listarSvg(dir: string): string[] {
  return readdirSync(dir, { recursive: true, encoding: 'utf8' })
    .filter((f) => f.endsWith('.svg'))
    .sort();
}

if (import.meta.main) {
  const raiz = resolve(import.meta.dirname, '..');
  const origen = join(raiz, 'art/src');
  const salida = join(raiz, 'art/build');
  const publico = join(raiz, 'public/generated/art');

  const archivos = listarSvg(origen);
  if (archivos.length === 0) {
    console.log('art:build: no hay SVG en art/src');
    process.exit(0);
  }

  const frames = archivos.flatMap((archivo) => {
    const nombre = relative(origen, join(origen, archivo))
      .replace(/\.svg$/, '')
      .split(sep)
      .join('/');
    const optimizado = optimize(
      readFileSync(join(origen, archivo), 'utf8'),
      configSvgo,
    ).data;
    const destinoSvg = join(salida, 'svg', `${nombre}.svg`);
    mkdirSync(dirname(destinoSvg), { recursive: true });
    writeFileSync(destinoSvg, optimizado);
    return framesDeSvg(optimizado, nombre);
  });

  mkdirSync(publico, { recursive: true });
  for (const escala of ESCALAS) {
    const rasters = frames.map((f) => rasterizar(f, escala));
    for (const r of rasters) {
      const destino = join(salida, 'png', `${r.nombre}@${escala}x.png`);
      mkdirSync(dirname(destino), { recursive: true });
      writeFileSync(destino, r.png);
    }
    const imagen = `atlas@${escala}x.png`;
    const atlas = empaquetar(frames, rasters, escala, imagen);
    writeFileSync(join(salida, imagen), atlas.png);
    writeFileSync(
      join(salida, `atlas@${escala}x.json`),
      JSON.stringify(atlas.json, null, 2),
    );
    copyFileSync(join(salida, imagen), join(publico, imagen));
    copyFileSync(
      join(salida, `atlas@${escala}x.json`),
      join(publico, `atlas@${escala}x.json`),
    );
    console.log(
      `✓ atlas@${escala}x: ${rasters.length} frames, ${atlas.json.meta.size ? JSON.stringify(atlas.json.meta.size) : ''}`,
    );
  }
}
