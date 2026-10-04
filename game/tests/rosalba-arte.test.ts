import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { EXPRESIONES } from '../src/core/animacion/expresiones.ts';
import { color } from '../src/core/arte/paleta.ts';
import {
  type ActoRosalba,
  ALTURA_DIBUJO_ROSALBA_PX,
  atlasRosalba,
  CAMINATA_ROSALBA,
  retratoRosalba,
  rosalbaMercado,
  rosalbaMonte,
} from '../src/game/personajes/rosalba.ts';
import { framesDeSvg, rasterizar } from '../tools/art-build.ts';
import { revisarPiernasBajoFalda, revisarRodillas } from '../tools/art-walk.ts';

const leer = (nombre: string) =>
  readFileSync(
    new URL(`../art/src/personajes/${nombre}.svg`, import.meta.url),
    'utf8',
  );

// Guarda sobre el arte real: al caminar, ninguna pierna de Rosalba sale de la falda
// (ni canilla cortada a la vista ni pie por detrás del ruedo).
describe('Rosalba camina con las piernas bajo la falda', () => {
  for (const nombre of ['rosalba', 'acto1/rosalba-monte']) {
    it(`${nombre}: sin fugas en ninguna fase`, () => {
      const fuente = readFileSync(
        new URL(`../art/src/personajes/${nombre}.svg`, import.meta.url),
        'utf8',
      );
      const fugas = revisarPiernasBajoFalda(
        fuente,
        nombre,
        CAMINATA_ROSALBA,
        16,
      ).filter((f) => f.cortada > 0 || f.detras > 0);
      expect(fugas).toEqual([]);
    }, 60_000);
  }
});

// Guarda: cada expresión tiene su cabeza y su capa de parpadeo, de pie y agachada, con
// pivote (el juego cambia el frame de la cabeza conservando el pivote del cuello).
describe('Rosalba tiene todas sus expresiones dibujadas', () => {
  for (const nombre of ['rosalba-cabezas', 'acto1/rosalba-agachada-cabezas']) {
    it(`${nombre}: cabeza y parpadeo por expresión`, () => {
      const frames = framesDeSvg(leer(nombre), nombre);
      const piezas = frames.map((f) => f.nombre.slice(nombre.length + 1));
      for (const e of EXPRESIONES) {
        expect(piezas).toContain(e);
        expect(piezas).toContain(`parpado-${e}`);
      }
      expect(frames.every((f) => f.pivote !== null)).toBe(true);
    });
  }
});

// Guarda del contrato de escala: la altura declarada coincide con el dibujo (coronilla→suela).
describe('Rosalba mide en el SVG lo que declara', () => {
  for (const nombre of ['rosalba', 'acto1/rosalba-monte']) {
    it(`${nombre}: ${ALTURA_DIBUJO_ROSALBA_PX} px de la coronilla a la suela`, () => {
      const frames = framesDeSvg(leer(nombre), nombre);
      const recorte = (id: string) => {
        const frame = frames.find((f) => f.nombre === `${nombre}/${id}`);
        if (!frame) throw new Error(`Falta la pieza ${id}`);
        return rasterizar(frame, 1).recorte;
      };
      const coronilla = recorte('cabeza').y;
      const suela = Math.max(
        ...['pierna-der', 'pierna-izq'].map(
          (id) => recorte(id).y + recorte(id).h,
        ),
      );
      expect(suela - coronilla).toBe(ALTURA_DIBUJO_ROSALBA_PX);
    });
  }
});

// Guarda del retrato en tres cuartos: base por variante y rasgos/parpadeo por expresión.
describe('el retrato de Rosalba tiene todas sus capas', () => {
  it('rosalba-retrato: bases mercado y monte, rasgos y parpadeo por expresión', () => {
    const nombre = 'rosalba-retrato';
    const piezas = framesDeSvg(leer(nombre), nombre).map((f) =>
      f.nombre.slice(nombre.length + 1),
    );
    expect(piezas).toEqual(
      expect.arrayContaining([
        'base-mercado',
        'base-monte',
        ...EXPRESIONES.flatMap((e) => [`rasgos-${e}`, `parpado-${e}`]),
      ]),
    );
  });
});

// Guarda de la cinta roja (doc 10 P31–P32): es una pieza propia, hija de la trenza, en todas las
// poses y en el retrato, y existe suelta como objeto para el Prólogo b2.
describe('la cinta roja de Rosalba se quita y se pone', () => {
  for (const nombre of [
    'rosalba',
    'acto1/rosalba-monte',
    'acto1/rosalba-agachada',
  ]) {
    it(`${nombre}: cinta hija de la trenza`, () => {
      const frames = framesDeSvg(leer(nombre), nombre);
      const cinta = frames.find((f) => f.nombre === `${nombre}/cinta`);
      expect(cinta?.padre).toBe('trenza');
    });
  }
  it('rosalba-retrato: capa de la cinta', () => {
    const nombres = framesDeSvg(leer('rosalba-retrato'), 'rosalba-retrato').map(
      (f) => f.nombre,
    );
    expect(nombres).toContain('rosalba-retrato/cinta');
  });
  it('cinta-roja: suelta a escala de personaje y de viñeta', () => {
    const nombres = framesDeSvg(leer('cinta-roja'), 'cinta-roja').map(
      (f) => f.nombre,
    );
    expect(nombres).toEqual(
      expect.arrayContaining([
        'cinta-roja/cinta-suelta',
        'cinta-roja/cinta-suelta-vineta',
      ]),
    );
  });
});

// Guarda de la huida (M2): en la pose de correr la canilla está cortada en la rodilla, que
// nunca debe asomar bajo la falda recogida ni bajo la enagua.
describe('Rosalba corre con las rodillas bajo la falda', () => {
  it('rosalba-corriendo: sin rodilla a la vista en ninguna fase', () => {
    const fugas = revisarRodillas(
      leer('acto1/rosalba-corriendo'),
      'acto1/rosalba-corriendo',
      {},
      16,
    ).filter((f) => f.rodilla > 0);
    expect(fugas).toEqual([]);
  }, 60_000);
});

// Guarda de las variantes por acto (paleta.md §5): cada acto tiene los dibujos que piden sus
// poses y su retrato, y la cinta roja (partido) no cambia de color en ningún acto.
describe('Rosalba tiene sus variantes por acto', () => {
  const actos: ActoRosalba[] = [
    'prologo',
    'acto1',
    'acto2',
    'acto3',
    'epilogo',
  ];
  const existe = (frame: string) =>
    existsSync(new URL(`../art/src/${frame}.svg`, import.meta.url));
  for (const acto of actos) {
    it(`${acto}: poses, cabezas y retrato`, () => {
      const poses = [
        ...(acto === 'prologo' || acto === 'acto1'
          ? Object.values(rosalbaMercado(acto))
          : []),
        ...(acto === 'prologo' ? [] : Object.values(rosalbaMonte(acto))),
      ];
      expect(poses.length).toBeGreaterThan(0);
      for (const pose of poses) {
        expect(existe(pose.base), pose.base).toBe(true);
        if (pose.cabezas) expect(existe(pose.cabezas), pose.cabezas).toBe(true);
        expect(pose.base.startsWith(`${atlasRosalba(acto)}/`)).toBe(true);
      }
      expect(existe(retratoRosalba(acto))).toBe(true);
    });
  }
  it('la cinta es del mismo rojo en el Prólogo y en el Epílogo', () => {
    const rojo = (svg: string) =>
      /<g id="cinta"[\s\S]*?fill="(#[0-9a-f]{6})"/.exec(svg)?.[1];
    expect(rojo(leer('epilogo/rosalba-monte'))).toBe(rojo(leer('rosalba')));
  });
  it('cada acto apaga sus lavados y deja igual la tinta, el papel y el rojo', () => {
    const colores = (svg: string) => new Set(svg.match(/#[0-9a-f]{6}/g));
    const fijos = [color('tinta'), color('papel'), color('rojo-liberal')];
    const acto1 = colores(leer('acto1/rosalba-monte'));
    const epilogo = colores(leer('epilogo/rosalba-monte'));
    for (const c of fijos) {
      expect(acto1.has(c)).toBe(true);
      expect(epilogo.has(c)).toBe(true);
    }
    const lavados = [...acto1].filter((c) => !fijos.includes(c));
    expect(lavados.length).toBeGreaterThan(5);
    expect(lavados.filter((c) => epilogo.has(c))).toEqual([]);
  });
});
