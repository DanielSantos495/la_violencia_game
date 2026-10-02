import { describe, expect, it } from 'vitest';
import { LADO_MAXIMO_ATLAS } from '../src/core/arte/atlas.ts';
import {
  ALTURA_VISIBLE_M,
  anchoCapa,
  escalaPersonaje,
  LADO_MAXIMO_MODULO,
  ORDEN_CAPAS,
  PARALAJE,
  PX_POR_METRO,
  pxPorMetroCapa,
  VIEWPORT,
  Y_HORIZONTE,
  Y_SUELO,
  ySueloCapa,
} from '../src/core/escena/escala.ts';

describe('contrato de escala', () => {
  it('deja 4,5 m de mundo visible sobre el suelo', () => {
    expect(ALTURA_VISIBLE_M).toBe(4.5);
  });

  it('pone el horizonte a la altura de los ojos de alguien de pie', () => {
    expect(Y_HORIZONTE).toBe(580);
    expect(Y_SUELO - Y_HORIZONTE).toBe(1.6 * PX_POR_METRO);
  });

  it('el plano de juego conserva escala y suelo; el cielo apoya en el horizonte', () => {
    expect(pxPorMetroCapa(PARALAJE.juego)).toBe(PX_POR_METRO);
    expect(ySueloCapa(PARALAJE.juego)).toBe(Y_SUELO);
    expect(ySueloCapa(PARALAJE.cielo)).toBe(Y_HORIZONTE);
  });

  it('las capas van del fondo al frente con paralaje, escala y suelo crecientes', () => {
    const factores = ORDEN_CAPAS.map((c) => PARALAJE[c]);
    for (let i = 1; i < factores.length; i++) {
      const anterior = factores[i - 1] ?? 0;
      const actual = factores[i] ?? 0;
      expect(actual).toBeGreaterThan(anterior);
      expect(pxPorMetroCapa(actual)).toBeGreaterThan(pxPorMetroCapa(anterior));
      expect(ySueloCapa(actual)).toBeGreaterThan(ySueloCapa(anterior));
    }
  });

  it('una capa cubre la pantalla más lo que recorre la cámara por su factor', () => {
    expect(anchoCapa(5760, 0)).toBe(VIEWPORT.ancho);
    expect(anchoCapa(5760, 1)).toBe(5760);
    expect(anchoCapa(5760, 0.5)).toBe(1920 + 3840 * 0.5);
  });

  it('escala un personaje a su estatura de diseño', () => {
    // Rosalba: 1,55 m, 431 px de la coronilla a la suela → ~310 px en pantalla.
    const escala = escalaPersonaje(1.55, 431);
    expect(escala * 431).toBeCloseTo(310);
    expect(() => escalaPersonaje(0, 431)).toThrow('positivas');
  });

  it('un módulo a @2x cabe en una página de atlas', () => {
    expect(LADO_MAXIMO_MODULO * 2).toBe(LADO_MAXIMO_ATLAS);
  });
});
