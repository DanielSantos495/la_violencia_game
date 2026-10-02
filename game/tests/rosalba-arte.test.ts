import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { EXPRESIONES } from '../src/core/animacion/expresiones.ts';
import {
  ALTURA_DIBUJO_ROSALBA_PX,
  CAMINATA_ROSALBA,
} from '../src/game/personajes/rosalba.ts';
import { framesDeSvg, rasterizar } from '../tools/art-build.ts';
import { revisarPiernasBajoFalda } from '../tools/art-walk.ts';

const leer = (nombre: string) =>
  readFileSync(
    new URL(`../art/src/personajes/${nombre}.svg`, import.meta.url),
    'utf8',
  );

// Guarda sobre el arte real: al caminar, ninguna pierna de Rosalba sale de la falda
// (ni canilla cortada a la vista ni pie por detrás del ruedo).
describe('Rosalba camina con las piernas bajo la falda', () => {
  for (const nombre of ['rosalba', 'rosalba-monte']) {
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
  for (const nombre of ['rosalba-cabezas', 'rosalba-agachada-cabezas']) {
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
  for (const nombre of ['rosalba', 'rosalba-monte']) {
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
