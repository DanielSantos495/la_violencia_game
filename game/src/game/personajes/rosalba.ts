import { escalaPersonaje } from '../../core/escena/escala.ts';
import type { OpcionesCaminar } from '../Caminata.ts';
import type { DefinicionPose } from '../Personaje.ts';

/**
 * Poses dibujadas de Rosalba (game/art/src/personajes/). Las piezas van en orden de
 * dibujo; la jerarquía (data-padre) llega desde el atlas. Hoja de personaje:
 * planeacion/arte/tomo1/personajes/rosalba.md.
 */

/**
 * Estatura de diseño (hoja de personaje §1): campesina boyacense nacida hacia 1927. Ver la
 * fuente y el cálculo en planeacion/arte/tomo1/personajes/rosalba.md.
 */
export const ESTATURA_ROSALBA_M = 1.52;

/**
 * Altura dibujada de pie, de la coronilla a la suela (px del SVG, con trazo). La guarda
 * tests/rosalba-arte.test.ts la vuelve a medir en el SVG.
 */
export const ALTURA_DIBUJO_ROSALBA_PX = 433;

/** Escala en el plano de juego según el contrato de escala (core/escena/escala.ts). */
export const ESCALA_ROSALBA = escalaPersonaje(
  ESTATURA_ROSALBA_M,
  ALTURA_DIBUJO_ROSALBA_PX,
);

/**
 * Cómo camina Rosalba: con falda casi al tobillo las piernas no giran desde la cadera; los
 * pies se deslizan bajo el ruedo (pivote en el tobillo) con pasos cortos y rápidos.
 * La guarda tests/rosalba-arte.test.ts comprueba que ninguna pierna salga de la falda.
 */
export const CAMINATA_ROSALBA: OpcionesCaminar = {
  faldaLarga: true,
  ciclo: 740,
};

/**
 * Cabezas por expresión (neutral, alerta, miedo, rabia, duelo) y su capa de parpadeo:
 * de pie y agachada (inclinada). Ver core/animacion/expresiones.ts.
 */
const CABEZAS_DE_PIE = 'personajes/rosalba-cabezas';
const CABEZAS_AGACHADA = 'personajes/rosalba-agachada-cabezas';

/** Punto de apoyo entre los pies, común a todas las poses (coordenadas del SVG). */
export const APOYO_ROSALBA = { x: 150, y: 474 };

/**
 * La cinta roja de la trenza es una pieza propia (hija de `trenza`): en la historia se la quitan
 * (Prólogo b4) y va sin ella desde la M2 hasta que vuelve a atársela en el Acto II
 * (planeacion/historia/tomo1/10_registro_propuestas.md P31–P32). Sin cinta, la trenza termina
 * en un amarre oscuro: `new Personaje(..., { ocultas: [PIEZA_CINTA] })` o `mostrarPieza`.
 */
export const PIEZA_CINTA = 'cinta';

export const ROSALBA_MERCADO: Record<string, DefinicionPose> = {
  'de-pie': {
    base: 'personajes/rosalba',
    cabezas: CABEZAS_DE_PIE,
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
      'cinta',
    ],
  },
};

export const ROSALBA_MONTE: Record<string, DefinicionPose> = {
  'de-pie': {
    base: 'personajes/rosalba-monte',
    cabezas: CABEZAS_DE_PIE,
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
      'mechones',
      'ruana',
      'trenza',
      'cinta',
      'brazo-der',
      'antebrazo-der',
      'ruana-doblez',
    ],
  },
  agachada: {
    base: 'personajes/rosalba-agachada',
    cabezas: CABEZAS_AGACHADA,
    // La mano de apoyo sigue en el suelo: la expresión solo mueve la cabeza.
    postura: 'cabeza',
    piezas: [
      'cuerpo',
      'cabeza',
      'zarcillo',
      'mechones',
      'ruana',
      'trenza',
      'cinta',
      'brazo-der',
      'antebrazo-der',
      'ruana-doblez',
    ],
  },
};
