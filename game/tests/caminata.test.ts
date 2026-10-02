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

describe('poseCaminata con pies bajo falda larga', () => {
  const opciones = { faldaLarga: { adelante: 30, atras: 20, inclinacion: 8 } };

  it('desliza los pies dentro del rango, sin girar desde la cadera', () => {
    for (const f of fases) {
      const p = poseCaminata(f, opciones);
      for (const id of ['pierna-der', 'pierna-izq']) {
        expect(p.avance[id]).toBeGreaterThanOrEqual(-20 - 1e-9);
        expect(p.avance[id]).toBeLessThanOrEqual(30 + 1e-9);
        expect(Math.abs(p.angulos[id] ?? 0)).toBeLessThanOrEqual(8);
      }
    }
  });

  it('apoya el talón adelante (punta arriba) y despega la punta atrás (talón arriba)', () => {
    const adelante = poseCaminata((3 * Math.PI) / 2, opciones); // pie derecho al frente
    expect(adelante.avance['pierna-der']).toBeCloseTo(30);
    expect(adelante.angulos['pierna-der']).toBeLessThan(0);
    const atras = poseCaminata(Math.PI / 2, opciones); // pie derecho atrás
    expect(atras.avance['pierna-der']).toBeCloseTo(-20);
    expect(atras.angulos['pierna-der']).toBeGreaterThan(0);
  });

  it('en modo cadera no desliza los pies', () => {
    expect(poseCaminata(1).avance).toEqual({});
  });
});

describe('velocidadCaminata', () => {
  it('modo cadera: avanza dos cuerdas de pierna por ciclo', () => {
    const v = velocidadCaminata(1000, { zancada: 30 }, 200);
    expect(v).toBeCloseTo(2 * 2 * 200 * 0.5);
  });

  it('falda larga: avanza dos recorridos de pie (adelante + atrás) por ciclo', () => {
    const v = velocidadCaminata(800, {
      faldaLarga: { adelante: 30, atras: 20 },
    });
    expect(v).toBeCloseTo((2 * 50) / 0.8);
  });
});
