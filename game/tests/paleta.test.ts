import { describe, expect, it } from 'vitest';
import { color, colorNumero } from '../src/core/arte/paleta.ts';

describe('paleta', () => {
  it('da los tokens de los que dependen escenas y fondos', () => {
    for (const id of ['papel', 'tinta', 'rojo-liberal', 'azul-conservador']) {
      expect(color(id)).toMatch(/^#[0-9a-f]{6}$/);
    }
  });

  it('convierte a número para Phaser sin cambiar el color', () => {
    expect(colorNumero('papel').toString(16).padStart(6, '0')).toBe(
      color('papel').slice(1),
    );
  });

  it('falla con un token que no existe', () => {
    expect(() => color('verde-chillon')).toThrow(/verde-chillon/);
  });
});
