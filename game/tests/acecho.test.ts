import { describe, expect, it } from 'vitest';
import { poseAcecho } from '../src/core/animacion/acecho.ts';

describe('poseAcecho', () => {
  const muestras = Array.from({ length: 200 }, (_, i) => i * 0.05);

  it('mantiene la mano apoyada: el antebrazo compensa al brazo', () => {
    for (const t of muestras) {
      const { angulos } = poseAcecho(t);
      expect(
        (angulos['brazo-der'] ?? 0) + (angulos['antebrazo-der'] ?? 0),
      ).toBeCloseTo(0);
    }
  });

  it('mueve la cabeza en un rango contenido (mirada, no sacudida)', () => {
    const cabeza = muestras.map((t) => poseAcecho(t).angulos.cabeza ?? 0);
    expect(Math.max(...cabeza)).toBeLessThanOrEqual(7.5);
    expect(Math.min(...cabeza)).toBeGreaterThanOrEqual(-7.5);
    expect(Math.max(...cabeza) - Math.min(...cabeza)).toBeGreaterThan(5);
  });
});
