import { Resvg } from '@resvg/resvg-js';
import { optimize } from 'svgo';
import { describe, expect, it } from 'vitest';
import {
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

describe('rasterizar y empaquetar', () => {
  const frames = framesDeSvg(svg, 'p/fig');

  it('recorta a la caja visible y escala @2x', () => {
    const r1 = rasterizar(definido(frames[1]), 1);
    const r2 = rasterizar(definido(frames[1]), 2);
    expect(r1.recorte).toEqual({ x: 35, y: 5, w: 30, h: 30 });
    expect([r2.ancho, r2.alto]).toEqual([60, 60]);
  });

  it('genera JSON Hash de Phaser con trim, tamaño de origen y pivote normalizado', () => {
    const rasters = frames.map((f) => rasterizar(f, 2));
    const atlas = empaquetar(frames, rasters, 2, 'atlas@2x.png');
    const cuerpo = atlas.json.frames['p/fig/cuerpo'];
    expect(cuerpo?.trimmed).toBe(true);
    expect(cuerpo?.sourceSize).toEqual({ w: 200, h: 200 });
    expect(cuerpo?.spriteSourceSize).toMatchObject({ x: 20, y: 80 });
    expect(cuerpo?.pivot).toEqual({ x: 0.5, y: 0.8 });
    expect(atlas.json.frames['p/fig/cabeza']?.pivot).toBeUndefined();
  });

  it('el atlas copia los píxeles de cada frame sin remuestrear', () => {
    const rasters = frames.map((f) => rasterizar(f, 1));
    const atlas = empaquetar(frames, rasters, 1, 'atlas@1x.png');
    const pixAtlas = new Resvg(
      `<svg xmlns="http://www.w3.org/2000/svg" width="${(atlas.json.meta.size as { w: number }).w}" height="${(atlas.json.meta.size as { h: number }).h}"><image href="data:image/png;base64,${atlas.png.toString('base64')}" width="100%" height="100%"/></svg>`,
    ).render();
    const anchoAtlas = pixAtlas.width;
    for (const r of rasters) {
      const f = definido(atlas.json.frames[r.nombre]).frame;
      const pixFrame = new Resvg(
        `<svg xmlns="http://www.w3.org/2000/svg" width="${r.ancho}" height="${r.alto}"><image href="data:image/png;base64,${r.png.toString('base64')}" width="${r.ancho}" height="${r.alto}"/></svg>`,
      ).render().pixels;
      for (let y = 0; y < f.h; y++) {
        const filaAtlas = pixAtlas.pixels.subarray(
          ((f.y + y) * anchoAtlas + f.x) * 4,
          ((f.y + y) * anchoAtlas + f.x + f.w) * 4,
        );
        const filaFrame = pixFrame.subarray(y * f.w * 4, (y + 1) * f.w * 4);
        expect(Buffer.compare(filaAtlas, filaFrame)).toBe(0);
      }
    }
  });
});
