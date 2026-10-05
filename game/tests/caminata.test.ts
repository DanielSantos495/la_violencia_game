import { describe, expect, it } from 'vitest';
import {
  CANILLA_POR_DEFECTO,
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

describe('poseCaminata con canillas bajo falda a media pierna', () => {
  const { largo, apoyo, angulo, rodilla } = CANILLA_POR_DEFECTO;
  const RAD = Math.PI / 180;
  const TAU = Math.PI * 2;
  /** Fase de la pierna derecha (0 = apoya el talón adelante) → fase de la caminata. */
  const fase = (u: number) => (u + 0.75) * TAU;
  /** Altura del pie sobre el suelo y posición respecto al cuerpo. */
  function pie(u: number, id: 'pierna-der' | 'pierna-izq') {
    const p = poseCaminata(fase(u), { canilla: true });
    const a = -(p.angulos[id] ?? 0) * RAD; // positivo = adelante
    return {
      alto: p.rebote + (p.levante[id] ?? 0) + largo * (1 - Math.cos(a)),
      x: (p.avance[id] ?? 0) + largo * Math.sin(a),
    };
  }

  it('el pie de apoyo no patina ni se despega, y hay doble apoyo (nunca vuela)', () => {
    for (const [id, inicio] of [
      ['pierna-der', 0],
      ['pierna-izq', 0.5],
    ] as const) {
      const xs: number[] = [];
      for (let i = 0; i <= 10; i++) {
        const p = pie(inicio + (i / 10) * apoyo * 0.999, id);
        expect(p.alto).toBeCloseTo(0, 6);
        xs.push(p.x);
      }
      const pasos = xs.slice(1).map((x, i) => x - (xs[i] ?? 0));
      for (const d of pasos) expect(d).toBeCloseTo(pasos[0] ?? 0, 6);
      expect(pasos[0]).toBeLessThan(0);
    }
    for (let i = 0; i < 200; i++) {
      const der = pie(i / 200, 'pierna-der');
      const izq = pie(i / 200, 'pierna-izq');
      expect(der.alto).toBeGreaterThan(-1e-6);
      expect(izq.alto).toBeGreaterThan(-1e-6);
      expect(Math.min(der.alto, izq.alto)).toBeCloseTo(0, 6);
    }
  });

  it('el talón apoya adelante cuando el brazo derecho va más atrás', () => {
    const p = poseCaminata(fase(0), { canilla: true });
    expect(pie(0, 'pierna-der').x).toBeCloseTo(
      rodilla + largo * Math.sin(angulo * RAD),
    );
    expect(p.angulos['brazo-der']).toBeGreaterThan(0);
  });

  it('es periódica y la velocidad iguala lo que retrocede el pie de apoyo', () => {
    const a = poseCaminata(0, { canilla: true });
    const b = poseCaminata(TAU, { canilla: true });
    for (const id of Object.keys(a.angulos)) {
      expect(b.angulos[id]).toBeCloseTo(a.angulos[id] ?? 0, 6);
    }
    const ciclo = 820;
    const recorrido =
      pie(0, 'pierna-der').x - pie(apoyo * 0.999999, 'pierna-der').x;
    expect(velocidadCaminata(ciclo, { canilla: true })).toBeCloseTo(
      recorrido / ((apoyo * ciclo) / 1000),
      0,
    );
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
