import { describe, expect, it } from 'vitest';
import {
  poseCaminata,
  velocidadCaminata,
} from '../src/core/animacion/caminata.ts';

const fases = Array.from({ length: 64 }, (_, i) => (i / 64) * Math.PI * 2);

describe('poseCaminata', () => {
  it('mueve las piernas en contrafase y los brazos opuestos a la pierna del mismo lado', () => {
    for (const f of fases) {
      const { angulos } = poseCaminata(f);
      expect(angulos['pierna-der']).toBeCloseTo(-(angulos['pierna-izq'] ?? 0));
      expect(Math.sign(angulos['brazo-der'] ?? 0)).toBe(
        -Math.sign(angulos['pierna-der'] ?? 0),
      );
    }
  });

  it('nunca levanta los dos pies a la vez', () => {
    for (const f of fases) {
      const { levante } = poseCaminata(f);
      expect((levante['pierna-der'] ?? 0) * (levante['pierna-izq'] ?? 0)).toBe(
        0,
      );
    }
  });

  it('respeta la zancada, el rebote y que el codo solo se dobla hacia adelante', () => {
    for (const f of fases) {
      const p = poseCaminata(f, { zancada: 10, rebote: 4 });
      expect(Math.abs(p.angulos['pierna-der'] ?? 0)).toBeLessThanOrEqual(10);
      expect(p.rebote).toBeGreaterThanOrEqual(0);
      expect(p.rebote).toBeLessThanOrEqual(4);
      expect(p.angulos['antebrazo-der']).toBeLessThan(0);
    }
  });

  it('es periódica: la fase 0 y 2π dan la misma pose', () => {
    expect(poseCaminata(Math.PI * 2).angulos).toEqual(
      Object.fromEntries(
        Object.entries(poseCaminata(0).angulos).map(([k, v]) => [
          k,
          expect.closeTo(v, 9),
        ]),
      ),
    );
  });
});

describe('velocidadCaminata', () => {
  it('avanza dos cuerdas de pierna por ciclo', () => {
    const v = velocidadCaminata(200, 1000, 30);
    expect(v).toBeCloseTo(2 * 2 * 200 * 0.5);
  });
});
