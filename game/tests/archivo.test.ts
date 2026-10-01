import { readdirSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { ArchivoStore } from '../src/core/archivo/ArchivoStore.ts';
import { validarEntrada } from '../src/core/archivo/esquema.ts';
import { procesar } from '../tools/validate-archivo.ts';

const dir = new URL('../content/archivo/', import.meta.url);
const archivos = readdirSync(dir)
  .filter((f) => f.endsWith('.json'))
  .sort()
  .map((nombre) => ({
    nombre,
    contenido: readFileSync(new URL(nombre, dir), 'utf8'),
  }));
const valida = JSON.parse(archivos[0]?.contenido ?? '{}') as Record<
  string,
  unknown
>;

describe('esquema del Archivo', () => {
  it('acepta una entrada válida', () => {
    expect(validarEntrada(valida).ok).toBe(true);
  });

  it('rechaza una entrada inválida con errores legibles', () => {
    const r = validarEntrada({
      ...valida,
      id: 'sin-prefijo',
      fecha: '9 de abril',
      licencia: { estado: 'quizas' },
    });
    expect(r.ok).toBe(false);
    if (!r.ok) {
      expect(r.errores.some((e) => e.startsWith('id'))).toBe(true);
      expect(r.errores.some((e) => e.startsWith('fecha'))).toBe(true);
      expect(r.errores.some((e) => e.startsWith('licencia'))).toBe(true);
    }
  });

  it('exige fuente en entradas verificadas', () => {
    const r = validarEntrada({ ...valida, fuentes: [] });
    expect(r.ok).toBe(false);
  });
});

describe('validate-archivo', () => {
  it('modo normal: incluye todas las entradas válidas', () => {
    const inf = procesar(archivos, false);
    expect(inf.errores).toEqual([]);
    expect(inf.incluidas).toHaveLength(3);
  });

  it('modo release: excluye pendientes, licencias no concedidas y pruebas', () => {
    const real = { ...valida, id: 'arch-real-01' };
    const pendiente = {
      ...real,
      id: 'arch-real-02',
      estado_verificacion: 'pendiente',
    };
    const solicitada = {
      ...real,
      id: 'arch-real-03',
      licencia: { titular: 'X', estado: 'solicitada' },
    };
    const inf = procesar(
      [
        ...archivos,
        ...[real, pendiente, solicitada].map((e) => ({
          nombre: `${e.id}.json`,
          contenido: JSON.stringify(e),
        })),
      ],
      true,
    );
    expect(inf.incluidas.map((e) => e.id)).toEqual(['arch-real-01']);
    expect(inf.excluidas.map((e) => e.motivo)).toEqual([
      'entrada de prueba',
      'entrada de prueba',
      'entrada de prueba',
      'verificación pendiente',
      'licencia solicitada',
    ]);
  });

  it('reporta JSON inválido e ids duplicados como errores', () => {
    const inf = procesar(
      [
        { nombre: 'roto.json', contenido: '{' },
        { nombre: 'a.json', contenido: JSON.stringify(valida) },
        { nombre: 'b.json', contenido: JSON.stringify(valida) },
      ],
      false,
    );
    expect(inf.errores.map((e) => e.archivo)).toEqual(['roto.json', 'b.json']);
  });
});

describe('ArchivoStore', () => {
  it('carga entradas válidas y descarta las inválidas', () => {
    const store = new ArchivoStore([valida, { id: 'mal' }, valida]);
    expect(store.todas()).toHaveLength(1);
    expect(store.porId('arch-prueba-01')?.titulo).toContain('[PRUEBA]');
    expect(store.porEpisodio(1)).toHaveLength(1);
    expect(store.descartadas).toHaveLength(2);
  });
});
