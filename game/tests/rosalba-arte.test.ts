import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CAMINATA_ROSALBA } from '../src/game/personajes/rosalba.ts';
import { revisarPiernasBajoFalda } from '../tools/art-walk.ts';

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
