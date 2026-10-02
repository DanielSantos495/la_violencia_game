import { describe, expect, it } from 'vitest';
import {
  DATOS_EXPRESION,
  EXPRESIONES,
  esExpresion,
  intervaloParpadeo,
} from '../src/core/animacion/expresiones.ts';

describe('expresiones', () => {
  it('cada expresión tiene postura contenida y un parpadeo coherente', () => {
    for (const e of EXPRESIONES) {
      const { postura, parpadeo } = DATOS_EXPRESION[e];
      for (const angulo of Object.values(postura))
        expect(Math.abs(angulo)).toBeLessThanOrEqual(12);
      expect(parpadeo.cada[0]).toBeLessThan(parpadeo.cada[1]);
      expect(parpadeo.dura).toBeGreaterThan(0);
      expect(parpadeo.dura).toBeLessThan(parpadeo.cada[0]);
      expect(parpadeo.doble).toBeGreaterThanOrEqual(0);
      expect(parpadeo.doble).toBeLessThanOrEqual(1);
    }
  });

  it('la postura cuenta la emoción: el miedo echa la cabeza atrás, el duelo la deja caer', () => {
    expect(DATOS_EXPRESION.miedo.postura.cabeza).toBeLessThan(0);
    expect(DATOS_EXPRESION.duelo.postura.cabeza).toBeGreaterThan(
      DATOS_EXPRESION.rabia.postura.cabeza ?? 0,
    );
    expect(DATOS_EXPRESION.neutral.postura).toEqual({});
  });

  it('el intervalo de parpadeo queda dentro del rango de la expresión', () => {
    for (const e of EXPRESIONES) {
      const [min, max] = DATOS_EXPRESION[e].parpadeo.cada;
      expect(intervaloParpadeo(e, () => 0)).toBe(min);
      expect(intervaloParpadeo(e, () => 0.999)).toBeLessThan(max);
    }
  });

  it('reconoce nombres válidos', () => {
    expect(esExpresion('duelo')).toBe(true);
    expect(esExpresion('alegria')).toBe(false);
  });
});
