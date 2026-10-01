import { readFileSync } from 'node:fs';
import { Compiler } from 'inkjs/full';
import { describe, expect, it } from 'vitest';
import { InkRunner } from '../src/core/narrative/InkRunner.ts';

const fuente = readFileSync(
  new URL('../content/ink/prueba.ink', import.meta.url),
  'utf8',
);
const compilar = (): string => {
  const json = new Compiler(fuente).Compile().ToJson();
  if (typeof json !== 'string') throw new Error('Compilación sin JSON');
  return json;
};

describe('InkRunner', () => {
  it('carga el JSON compilado (string u objeto)', () => {
    const json = compilar();
    expect(new InkRunner(json).puedeContinuar).toBe(true);
    expect(new InkRunner(JSON.parse(json)).puedeContinuar).toBe(true);
  });

  it('avanza línea a línea y lee el hablante del tag', () => {
    const r = new InkRunner(compilar());
    expect(r.continuar()).toEqual({
      texto: 'Este es un texto de prueba del sistema de globos.',
      hablante: 'Narrador',
      tags: ['hablante: Narrador'],
    });
    expect(r.continuar()?.hablante).toBe('Personaje A');
    r.continuar();
    expect(r.continuar()).toBeNull();
    expect(r.opciones().map((o) => o.texto)).toEqual([
      'Opción uno',
      'Opción dos',
    ]);
  });

  it('aplica la decisión, actualiza la variable y termina', () => {
    const r = new InkRunner(compilar());
    while (r.continuar()) {}
    r.elegir(1);
    expect(r.continuar()?.texto).toBe('Elegiste la opción dos.');
    expect(r.variable('decision_prueba')).toBe(2);
    expect(r.continuar()?.texto).toBe('Fin de la prueba.');
    expect(r.terminado).toBe(true);
  });

  it('rechaza una opción inexistente', () => {
    const r = new InkRunner(compilar());
    while (r.continuar()) {}
    expect(() => r.elegir(5)).toThrow('Opción inexistente');
  });
});
