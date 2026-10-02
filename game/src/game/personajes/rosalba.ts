import type { OpcionesCaminar } from '../Caminata.ts';
import type { DefinicionPose } from '../Personaje.ts';

/**
 * Poses dibujadas de Rosalba (game/art/src/personajes/). Las piezas van en orden de
 * dibujo; la jerarquía (data-padre) llega desde el atlas. Hoja de personaje:
 * planeacion/arte/tomo1/personajes/rosalba.md.
 */

/**
 * Cómo camina Rosalba: con falda casi al tobillo las piernas no giran desde la cadera; los
 * pies se deslizan bajo el ruedo (pivote en el tobillo) con pasos cortos y rápidos.
 * La guarda tests/rosalba-arte.test.ts comprueba que ninguna pierna salga de la falda.
 */
export const CAMINATA_ROSALBA: OpcionesCaminar = {
  faldaLarga: true,
  ciclo: 800,
};

/** Punto de apoyo entre los pies, común a todas las poses (coordenadas del SVG). */
export const APOYO_ROSALBA = { x: 150, y: 474 };

export const ROSALBA_MERCADO: Record<string, DefinicionPose> = {
  'de-pie': {
    base: 'personajes/rosalba',
    piezas: [
      'brazo-izq',
      'antebrazo-izq',
      'pierna-izq',
      'pierna-der',
      'enagua',
      'falda',
      'torso',
      'cabeza',
      'zarcillo',
      'sombrero',
      'brazo-der',
      'antebrazo-der',
      'panolon',
      'trenza',
    ],
  },
};

export const ROSALBA_MONTE: Record<string, DefinicionPose> = {
  'de-pie': {
    base: 'personajes/rosalba-monte',
    piezas: [
      'brazo-izq',
      'antebrazo-izq',
      'pierna-izq',
      'pierna-der',
      'enagua',
      'falda',
      'torso',
      'cabeza',
      'zarcillo',
      'ruana',
      'trenza',
      'brazo-der',
      'antebrazo-der',
      'ruana-doblez',
    ],
  },
  agachada: {
    base: 'personajes/rosalba-agachada',
    piezas: [
      'cuerpo',
      'cabeza',
      'zarcillo',
      'ruana',
      'trenza',
      'brazo-der',
      'antebrazo-der',
      'ruana-doblez',
    ],
  },
};
