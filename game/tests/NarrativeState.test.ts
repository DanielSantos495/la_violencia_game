import { Compiler } from 'inkjs/full';
import { describe, expect, it } from 'vitest';
import { InkRunner } from '../src/core/narrative/InkRunner.ts';
import {
  type AlmacenGuardado,
  NarrativeState,
} from '../src/core/narrative/NarrativeState.ts';

const json = new Compiler('VAR x = 0\nHola.\n* [A]\n~ x = 1\nA.\n-> END\n')
  .Compile()
  .ToJson() as string;

const almacenEnMemoria = (): AlmacenGuardado => {
  const datos = new Map<string, string>();
  return {
    leer: (k) => datos.get(k) ?? null,
    escribir: (k, v) => void datos.set(k, v),
  };
};

describe('NarrativeState', () => {
  it('guarda y restaura el estado de Ink con sus variables', () => {
    const almacen = almacenEnMemoria();
    const estado = new NarrativeState(
      almacen,
      () => new Date('2026-01-01T00:00:00Z'),
    );
    const a = new InkRunner(json);
    while (a.continuar()) {}
    a.elegir(0);
    a.continuar();
    expect(estado.guardar(a, 1).actualizado).toBe('2026-01-01T00:00:00.000Z');

    const b = new InkRunner(json);
    expect(estado.cargar(b)).toBe(true);
    expect(b.variable('x')).toBe(1);
  });

  it('sin guardado devuelve false', () => {
    expect(
      new NarrativeState(almacenEnMemoria()).cargar(new InkRunner(json)),
    ).toBe(false);
  });

  it('rechaza un guardado inválido', () => {
    expect(() => NarrativeState.parsear('{"version":99}')).toThrow(
      'Guardado inválido',
    );
  });
});
