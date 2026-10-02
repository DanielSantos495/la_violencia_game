import { describe, expect, it } from 'vitest';
import {
  archivoDeGrupo,
  GRUPO_RAIZ,
  grupoDe,
  rutaAtlas,
} from '../src/core/arte/atlas.ts';

describe('convención de atlas por carpeta', () => {
  it('agrupa por la carpeta que contiene el SVG', () => {
    expect(grupoDe('personajes/rosalba')).toBe('personajes');
    expect(grupoDe('fondos/puente-alto/plaza-lejos')).toBe(
      'fondos/puente-alto',
    );
    expect(grupoDe('suelto')).toBe(GRUPO_RAIZ);
  });

  it('nombra los archivos y la ruta pública del atlas', () => {
    expect(archivoDeGrupo('fondos/puente-alto')).toBe('fondos-puente-alto');
    expect(rutaAtlas('fondos/puente-alto', 2)).toEqual({
      json: 'generated/art/fondos-puente-alto@2x.json',
      carpeta: 'generated/art/',
    });
  });
});
