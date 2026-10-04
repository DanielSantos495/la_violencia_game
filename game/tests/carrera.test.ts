import { describe, expect, it } from 'vitest';
import {
  CARRERA_POR_DEFECTO,
  poseCarrera,
  velocidadCarrera,
} from '../src/core/animacion/carrera.ts';

const { largo, apoyo } = CARRERA_POR_DEFECTO;
const TAU = Math.PI * 2;
const RAD = Math.PI / 180;

/** Altura del pie sobre su reposo (px, arriba positivo) y posición respecto al cuerpo. */
function pie(u: number, id: 'pierna-der' | 'pierna-izq') {
  const pose = poseCarrera(u * TAU);
  const a = -(pose.angulos[id] ?? 0) * RAD; // positivo = adelante
  return {
    // Sube el cuerpo, sube la rodilla y la canilla inclinada acorta lo que baja el pie.
    alto: pose.rebote + (pose.levante[id] ?? 0) + largo * (1 - Math.cos(a)),
    x: (pose.avance[id] ?? 0) + largo * Math.sin(a),
  };
}

describe('poseCarrera', () => {
  it('es periódica y continua (sin saltos entre cuadros)', () => {
    const a = poseCarrera(0);
    const b = poseCarrera(TAU);
    for (const id of Object.keys(a.angulos)) {
      expect(b.angulos[id]).toBeCloseTo(a.angulos[id] ?? 0, 6);
    }
    let previa = poseCarrera(0);
    for (let i = 1; i <= 400; i++) {
      const p = poseCarrera((i / 400) * TAU);
      for (const id of ['pierna-der', 'pierna-izq']) {
        expect(
          Math.abs((p.angulos[id] ?? 0) - (previa.angulos[id] ?? 0)),
        ).toBeLessThan(4);
        expect(
          Math.abs((p.levante[id] ?? 0) - (previa.levante[id] ?? 0)),
        ).toBeLessThan(1.5);
      }
      expect(Math.abs(p.rebote - previa.rebote)).toBeLessThan(1);
      previa = p;
    }
  });

  it('el pie de apoyo no se despega del suelo y retrocede a velocidad constante', () => {
    for (const [id, inicio] of [
      ['pierna-der', 0],
      ['pierna-izq', 0.5],
    ] as const) {
      const xs: number[] = [];
      for (let i = 0; i <= 10; i++) {
        const u = inicio + (i / 10) * apoyo * 0.999;
        const p = pie(u, id);
        expect(p.alto).toBeCloseTo(0, 6);
        xs.push(p.x);
      }
      const pasos = xs.slice(1).map((x, i) => x - (xs[i] ?? 0));
      for (const d of pasos) expect(d).toBeCloseTo(pasos[0] ?? 0, 6);
      expect(pasos[0]).toBeLessThan(0);
    }
  });

  it('en el aire ningún pie baja del suelo y hay dos fases de vuelo', () => {
    let vuelos = 0;
    let enElAire = false;
    for (let i = 0; i < 400; i++) {
      const u = i / 400;
      const der = pie(u, 'pierna-der');
      const izq = pie(u, 'pierna-izq');
      expect(der.alto).toBeGreaterThan(-1e-6);
      expect(izq.alto).toBeGreaterThan(-1e-6);
      const ambos = der.alto > 0.5 && izq.alto > 0.5;
      if (ambos && !enElAire) vuelos++;
      enElAire = ambos;
    }
    expect(vuelos).toBe(2);
  });

  it('la velocidad iguala lo que retrocede el pie de apoyo', () => {
    const ciclo = 620;
    const a = pie(0, 'pierna-der').x;
    const b = pie(apoyo * 0.999999, 'pierna-der').x;
    const v = velocidadCarrera(ciclo);
    expect(v).toBeCloseTo((a - b) / ((apoyo * ciclo) / 1000), 0);
    expect(v).toBeGreaterThan(400);
  });
});
