// Pipeline de arte (doc 03 §2): art/src/**/*.svg → SVGO → PNG @1x/@2x → un multiatlas de Phaser
// por carpeta (convención en src/core/arte/atlas.ts).
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
  rmSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { type BBox, Resvg } from '@resvg/resvg-js';
import { MaxRectsPacker } from 'maxrects-packer';
import { type Config, optimize, type XastElement } from 'svgo';
import {
  archivoDeGrupo,
  grupoDe,
  LADO_MAXIMO_ATLAS,
} from '../src/core/arte/atlas.ts';

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
  // Alinear el recorte a la rejilla de píxeles de la escala para que no haya medio píxel, sin
  // salir del viewBox: lo de fuera no se ve (getBBox no descuenta los clipPath).
  const x = Math.max(0, Math.floor(bbox.x * escala) / escala);
  const y = Math.max(0, Math.floor(bbox.y * escala) / escala);
  const w =
    Math.min(
      frame.origen.w,
      Math.ceil((bbox.x + bbox.width) * escala) / escala,
    ) - x;
  const h =
    Math.min(
      frame.origen.h,
      Math.ceil((bbox.y + bbox.height) * escala) / escala,
    ) - y;
  if (w <= 0 || h <= 0)
    throw new Error(`${frame.nombre}: sin contenido dentro del viewBox`);
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
  filename: string;
  frame: { x: number; y: number; w: number; h: number };
  rotated: false;
  trimmed: true;
  spriteSourceSize: { x: number; y: number; w: number; h: number };
  sourceSize: { w: number; h: number };
  pivot?: { x: number; y: number };
  /** Pieza padre (data-padre); Phaser la expone en frame.customData.padre. */
  padre?: string;
}

/** Una página (textura) de un multiatlas de Phaser. */
export interface PaginaAtlas {
  image: string;
  format: 'RGBA8888';
  size: { w: number; h: number };
  scale: number;
  frames: FrameAtlas[];
}

/** Multiatlas de Phaser (`load.multiatlas`): una o más páginas bajo una misma clave. */
export interface Atlas {
  pngs: Buffer[];
  json: { textures: PaginaAtlas[]; meta: { app: string; escala: number } };
}

const RELLENO = 2;

/**
 * Empaqueta los frames de una escala en un multiatlas (maxrects-packer) y compone cada
 * página con resvg. Si no caben en una página de `lado` px se reparten en varias.
 */
export function empaquetar(
  frames: FrameFuente[],
  rasters: FrameRaster[],
  escala: number,
  nombreBase: string,
  { lado = LADO_MAXIMO_ATLAS }: { lado?: number } = {},
): Atlas {
  // maxrects-packer con pot:true redondea la página a potencia de dos hacia abajo: con otro
  // lado los frames se saldrían de la página y se solaparían.
  if (!Number.isInteger(Math.log2(lado))) {
    throw new Error(
      `El lado del atlas debe ser potencia de dos (recibido ${lado})`,
    );
  }
  const util = lado - 2 * RELLENO;
  for (const r of rasters) {
    if (r.ancho > util || r.alto > util) {
      throw new Error(
        `${r.nombre}: ${r.ancho}×${r.alto} px a @${escala}x no cabe en una página de ${lado} px; ` +
          'divídelo en módulos o tramos (p. ej. capas de paralaje en segmentos)',
      );
    }
  }
  const packer = new MaxRectsPacker(lado, lado, RELLENO, {
    smart: true,
    pot: true,
    border: RELLENO,
  });
  // Orden estable (más altos primero, luego por nombre) para que el atlas sea reproducible.
  const ordenados = [...rasters].sort(
    (a, b) =>
      b.alto - a.alto || b.ancho - a.ancho || a.nombre.localeCompare(b.nombre),
  );
  for (const r of ordenados) packer.add(r.ancho, r.alto, r);
  if (packer.bins.length === 0) throw new Error('Atlas vacío');

  const fuentes = new Map(frames.map((f) => [f.nombre, f]));
  const pngs: Buffer[] = [];
  const textures = packer.bins.map((bin, i): PaginaAtlas => {
    const paginaFrames: FrameAtlas[] = [];
    const imagenes: string[] = [];
    for (const rect of bin.rects) {
      const r = rect.data as FrameRaster;
      if (rect.x + r.ancho > bin.width || rect.y + r.alto > bin.height) {
        throw new Error(`${r.nombre}: quedó fuera de la página ${i} del atlas`);
      }
      const f = fuentes.get(r.nombre);
      if (!f) throw new Error(`Frame sin fuente: ${r.nombre}`);
      const entrada: FrameAtlas = {
        filename: r.nombre,
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
      paginaFrames.push(entrada);
      imagenes.push(
        `<image x="${rect.x}" y="${rect.y}" width="${r.ancho}" height="${r.alto}" href="data:image/png;base64,${r.png.toString('base64')}"/>`,
      );
    }
    // Composición a escala 1:1 en posiciones enteras: resvg copia los píxeles sin remuestrear.
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${bin.width}" height="${bin.height}" viewBox="0 0 ${bin.width} ${bin.height}">${imagenes.join('')}</svg>`;
    pngs.push(
      new Resvg(svg, { font: { loadSystemFonts: false } }).render().asPng(),
    );
    return {
      image: `${nombreBase}-${i}.png`,
      format: 'RGBA8888',
      size: { w: bin.width, h: bin.height },
      scale: escala,
      frames: paginaFrames.sort((a, b) => a.filename.localeCompare(b.filename)),
    };
  });
  return {
    pngs,
    json: { textures, meta: { app: 'tools/art-build.ts', escala } },
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
  const salidaAtlas = join(salida, 'atlas');
  const publico = join(raiz, 'public/generated/art');

  const archivos = listarSvg(origen);
  // Las salidas de atlas se regeneran completas: sin restos de grupos que ya no existen.
  rmSync(salidaAtlas, { recursive: true, force: true });
  rmSync(publico, { recursive: true, force: true });
  if (archivos.length === 0) {
    console.log('art:build: no hay SVG en art/src');
    process.exit(0);
  }

  const porGrupo = new Map<string, FrameFuente[]>();
  for (const archivo of archivos) {
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
    const grupo = grupoDe(nombre);
    porGrupo.set(grupo, [
      ...(porGrupo.get(grupo) ?? []),
      ...framesDeSvg(optimizado, nombre),
    ]);
  }

  mkdirSync(salidaAtlas, { recursive: true });
  mkdirSync(publico, { recursive: true });
  for (const [grupo, frames] of porGrupo) {
    for (const escala of ESCALAS) {
      const rasters = frames.map((f) => rasterizar(f, escala));
      for (const r of rasters) {
        const destino = join(salida, 'png', `${r.nombre}@${escala}x.png`);
        mkdirSync(dirname(destino), { recursive: true });
        writeFileSync(destino, r.png);
      }
      const base = `${archivoDeGrupo(grupo)}@${escala}x`;
      const atlas = empaquetar(frames, rasters, escala, base);
      const salidas = [
        ...atlas.json.textures.map((t, i) => {
          writeFileSync(join(salidaAtlas, t.image), atlas.pngs[i] as Buffer);
          return t.image;
        }),
        `${base}.json`,
      ];
      writeFileSync(
        join(salidaAtlas, `${base}.json`),
        JSON.stringify(atlas.json, null, 2),
      );
      for (const archivo of salidas)
        copyFileSync(join(salidaAtlas, archivo), join(publico, archivo));
      const tamanos = atlas.json.textures
        .map((t) => `${t.size.w}×${t.size.h}`)
        .join(', ');
      console.log(
        `✓ ${grupo} @${escala}x: ${rasters.length} frames en ${atlas.json.textures.length} página(s) [${tamanos}]`,
      );
    }
  }
}
