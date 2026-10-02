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
      for (const [id, angulo] of Object.entries(postura)) {
        // La cabeza se inclina poco; el antebrazo puede cerrarse sobre el pecho (miedo).
        expect(Math.abs(angulo)).toBeLessThanOrEqual(
          id === 'cabeza' ? 12 : 160,
        );
      }
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

  it('el miedo lleva la mano al pecho; el duelo deja caer los brazos', () => {
    // Codo atrás y antebrazo cerrado hacia arriba y adelante: la mano queda sobre el pecho.
    expect(DATOS_EXPRESION.miedo.postura['brazo-der']).toBeGreaterThan(0);
    expect(DATOS_EXPRESION.miedo.postura['antebrazo-der']).toBeLessThan(-120);
    expect(DATOS_EXPRESION.duelo.postura['brazo-der']).toBeGreaterThan(0);
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
