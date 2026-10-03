import { Resvg } from '@resvg/resvg-js';
import { optimize } from 'svgo';
import { describe, expect, it } from 'vitest';
import {
  type Atlas,
  configSvgo,
  empaquetar,
  framesDeSvg,
  rasterizar,
} from '../tools/art-build.ts';

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <defs><pattern id="trama" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 0v4" stroke="#000"/></pattern></defs>
  <g id="cuerpo" data-pieza="" data-pivote="50 80"><g id="interno"><rect x="10" y="40" width="80" height="50" fill="url(#trama)"/></g></g>
  <g id="cabeza" data-pieza=""><circle cx="50" cy="20" r="15" fill="#000"/></g>
</svg>`;

describe('SVGO para piezas de recorte', () => {
  it('preserva ids, grupos anidados y data-*', () => {
    const out = optimize(svg, configSvgo).data;
    for (const fragmento of [
      'id="cuerpo"',
      'id="interno"',
      'id="cabeza"',
      'id="trama"',
      'data-pieza',
      'data-pivote="50 80"',
    ]) {
      expect(out).toContain(fragmento);
    }
  });
});

describe('framesDeSvg', () => {
  it('separa una pieza por frame con su pivote', () => {
    const frames = framesDeSvg(svg, 'p/fig');
    expect(frames.map((f) => f.nombre)).toEqual([
      'p/fig/cuerpo',
      'p/fig/cabeza',
    ]);
    expect(frames[0]?.pivote).toEqual({ x: 50, y: 80 });
    expect(frames[1]?.pivote).toBeNull();
    expect(frames[1]?.svg).not.toContain('id="cuerpo"');
  });

  it('sin piezas, el archivo es un frame', () => {
    const frames = framesDeSvg(
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>',
      'fondo',
    );
    expect(frames.map((f) => f.nombre)).toEqual(['fondo']);
  });

  it('exige viewBox y ids únicos', () => {
    expect(() =>
      framesDeSvg(
        '<svg xmlns="http://www.w3.org/2000/svg"><rect width="1" height="1"/></svg>',
        'x',
      ),
    ).toThrow('viewBox');
    const dup = svg.replace('id="cabeza"', 'id="cuerpo"');
    expect(() => framesDeSvg(dup, 'x')).toThrow('duplicado');
  });
});

const definido = <T>(v: T | undefined): T => {
  if (v === undefined) throw new Error('valor indefinido en el test');
  return v;
};

/** Busca un frame en cualquier página del multiatlas; devuelve también el índice de página. */
const buscar = (atlas: Atlas, nombre: string) => {
  for (const [pagina, t] of atlas.json.textures.entries()) {
    const frame = t.frames.find((f) => f.filename === nombre);
    if (frame) return { frame, pagina };
  }
  throw new Error(`frame ${nombre} no está en el atlas`);
};

describe('rasterizar y empaquetar', () => {
  const frames = framesDeSvg(svg, 'p/fig');

  it('recorta a la caja visible y escala @2x', () => {
    const r1 = rasterizar(definido(frames[1]), 1);
    const r2 = rasterizar(definido(frames[1]), 2);
    expect(r1.recorte).toEqual({ x: 35, y: 5, w: 30, h: 30 });
    expect([r2.ancho, r2.alto]).toEqual([60, 60]);
  });

  it('el recorte no pasa de los bordes del viewBox (lo de fuera no se ve)', () => {
    const [fondo] = framesDeSvg(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><clipPath id="c"><rect width="100" height="50"/></clipPath><g clip-path="url(#c)"><rect x="-40" y="10" width="200" height="80"/></g></svg>`,
      'fondo',
    );
    const r = rasterizar(definido(fondo), 2);
    expect(r.recorte).toEqual({ x: 0, y: 10, w: 100, h: 40 });
    expect([r.ancho, r.alto]).toEqual([200, 80]);
  });

  it('genera un multiatlas de Phaser con trim, tamaño de origen y pivote normalizado', () => {
    const rasters = frames.map((f) => rasterizar(f, 2));
    const atlas = empaquetar(frames, rasters, 2, 'p@2x');
    expect(atlas.json.textures.map((t) => t.image)).toEqual(['p@2x-0.png']);
    const { frame: cuerpo } = buscar(atlas, 'p/fig/cuerpo');
    expect(cuerpo.trimmed).toBe(true);
    expect(cuerpo.sourceSize).toEqual({ w: 200, h: 200 });
    expect(cuerpo.spriteSourceSize).toMatchObject({ x: 20, y: 80 });
    expect(cuerpo.pivot).toEqual({ x: 0.5, y: 0.8 });
    expect(buscar(atlas, 'p/fig/cabeza').frame.pivot).toBeUndefined();
  });

  // Renderiza varias imágenes con resvg: bajo carga puede pasar de los 5 s por defecto.
  it('el atlas copia los píxeles de cada frame sin remuestrear', {
    timeout: 20_000,
  }, () => {
    const rasters = frames.map((f) => rasterizar(f, 1));
    const atlas = empaquetar(frames, rasters, 1, 'p@1x');
    const paginas = atlas.json.textures.map((t, i) =>
      new Resvg(
        `<svg xmlns="http://www.w3.org/2000/svg" width="${t.size.w}" height="${t.size.h}"><image href="data:image/png;base64,${definido(atlas.pngs[i]).toString('base64')}" width="100%" height="100%"/></svg>`,
      ).render(),
    );
    for (const r of rasters) {
      const { frame, pagina } = buscar(atlas, r.nombre);
      const pixAtlas = definido(paginas[pagina]);
      const pixFrame = new Resvg(
        `<svg xmlns="http://www.w3.org/2000/svg" width="${r.ancho}" height="${r.alto}"><image href="data:image/png;base64,${r.png.toString('base64')}" width="${r.ancho}" height="${r.alto}"/></svg>`,
      ).render().pixels;
      const f = frame.frame;
      let filasDistintas = 0;
      for (let y = 0; y < f.h; y++) {
        const filaAtlas = pixAtlas.pixels.subarray(
          ((f.y + y) * pixAtlas.width + f.x) * 4,
          ((f.y + y) * pixAtlas.width + f.x + f.w) * 4,
        );
        const filaFrame = pixFrame.subarray(y * f.w * 4, (y + 1) * f.w * 4);
        if (Buffer.compare(filaAtlas, filaFrame) !== 0) filasDistintas++;
      }
      expect(filasDistintas, r.nombre).toBe(0);
    }
  });

  it('reparte en varias páginas cuando no cabe en una', () => {
    const tres = framesDeSvg(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50">
        <g id="a" data-pieza=""><rect x="0" y="0" width="40" height="40"/></g>
        <g id="b" data-pieza=""><rect x="50" y="0" width="40" height="40"/></g>
        <g id="c" data-pieza=""><rect x="100" y="0" width="40" height="40"/></g>
      </svg>`,
      't',
    );
    // Páginas de 64 px (60 útiles): dos cuadrados de 40 no caben juntos.
    const atlas = empaquetar(
      tres,
      tres.map((f) => rasterizar(f, 1)),
      1,
      't@1x',
      { lado: 64 },
    );
    expect(atlas.json.textures.length).toBe(3);
    expect(atlas.pngs.length).toBe(3);
    expect(atlas.json.textures.map((t) => t.image)).toEqual([
      't@1x-0.png',
      't@1x-1.png',
      't@1x-2.png',
    ]);
    for (const t of atlas.json.textures) {
      for (const f of t.frames) {
        expect(f.frame.x + f.frame.w).toBeLessThanOrEqual(t.size.w);
        expect(f.frame.y + f.frame.h).toBeLessThanOrEqual(t.size.h);
      }
    }
  });

  it('exige un lado de página potencia de dos', () => {
    const rasters = frames.map((f) => rasterizar(f, 1));
    expect(() => empaquetar(frames, rasters, 1, 'p@1x', { lado: 100 })).toThrow(
      'potencia de dos',
    );
  });

  it('rechaza un frame más grande que una página, con un mensaje accionable', () => {
    const rasters = frames.map((f) => rasterizar(f, 1));
    expect(() => empaquetar(frames, rasters, 1, 'p@1x', { lado: 64 })).toThrow(
      'no cabe en una página de 64 px',
    );
  });
});

describe('jerarquía de piezas (data-padre)', () => {
  const conPadre = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <g id="brazo" data-pieza="" data-pivote="50 10"><rect x="45" y="10" width="10" height="40"/></g>
    <g id="antebrazo" data-pieza="" data-pivote="50 50" data-padre="brazo"><rect x="45" y="50" width="10" height="40"/></g>
  </svg>`;

  it('pasa el padre al frame fuente y al JSON del atlas', () => {
    const frames = framesDeSvg(conPadre, 'p');
    expect(frames.map((f) => f.padre)).toEqual([null, 'brazo']);
    const atlas = empaquetar(
      frames,
      frames.map((f) => rasterizar(f, 1)),
      1,
      'p@1x',
    );
    expect(buscar(atlas, 'p/antebrazo').frame.padre).toBe('brazo');
    expect(buscar(atlas, 'p/brazo').frame.padre).toBeUndefined();
  });

  it('exige que el padre exista y se declare antes', () => {
    const invertido = conPadre.replace(
      'data-padre="brazo"',
      'data-padre="mano"',
    );
    expect(() => framesDeSvg(invertido, 'p')).toThrow(
      'no es una pieza declarada antes',
    );
  });
});
