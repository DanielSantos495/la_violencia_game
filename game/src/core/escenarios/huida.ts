/**
 * Huida de la Misión 2 (doc 02 §5, M2 b4–b5), Acto I: los cultivos de noche con la casa ardiendo a
 * lo lejos, la quebrada y el monte al amanecer. Composición y fuentes:
 * planeacion/arte/tomo1/escenarios/huida-m2.md.
 * Módulos: game/art/gen/huida.py → art/src/fondos/huida/<tramo>/*.svg.
 */
import type { DefinicionEscenario } from './escenario.ts';

const arriba = (modulo: string, x: number, y = 0) =>
  ({ modulo, x, y, ancla: 'arriba' }) as const;

/**
 * Los cultivos, de noche: de la cerca del solar (izquierda) al borde del barranco (derecha), con
 * el maizal donde esconderse en medio y la casa ardiendo a lo lejos.
 */
export const HUIDA_CULTIVOS: DefinicionEscenario = {
  atlas: 'fondos/huida/cultivos',
  anchoNivel: 5760,
  acto: 'acto1',
  fondo: 'sepia-oscuro',
  capas: {
    cielo: { colocaciones: [arriba('cielo-noche', 0)] },
    lejos: {
      colocaciones: [
        arriba('lomas-1', 0, 380),
        arriba('lomas-2', 860, 380),
        arriba('lomas-3', 1720, 380),
        // se ve al empezar y se va quedando atrás, despacio (lx 290–710)
        arriba('casa-ardiendo', 150),
      ],
    },
    medio: {
      colocaciones: [
        arriba('campos-1', 0, 120),
        arriba('campos-2', 900, 120),
        arriba('campos-3', 1800, 120),
        arriba('campos-4', 2700, 120),
      ],
    },
    juego: {
      colocaciones: [
        arriba('salida', 0),
        arriba('maizal-1', 960),
        arriba('maizal-2', 1920),
        arriba('trigal', 2880),
        arriba('papal', 3840),
        arriba('barranco', 4800),
      ],
    },
    frente: {
      colocaciones: [
        { modulo: 'maguey', x: 900, y: 1240 },
        { modulo: 'maguey', x: 3300, y: 1250, espejo: true },
        { modulo: 'maguey', x: 6200, y: 1240 },
      ],
    },
  },
};

/**
 * La quebrada, de noche: la bajada entre helechos, el agua con las piedras para pasar, el tronco
 * caído y la subida al monte. Las paredes de la quebrada encierran la vista; por encima solo se
 * ven el humo y el resplandor de la casa.
 */
export const HUIDA_QUEBRADA: DefinicionEscenario = {
  atlas: 'fondos/huida/quebrada',
  anchoNivel: 3840,
  acto: 'acto1',
  fondo: 'sepia-oscuro',
  capas: {
    cielo: { colocaciones: [arriba('cielo-noche', 0)] },
    lejos: { colocaciones: [arriba('resplandor', 0)] },
    medio: {
      colocaciones: [
        arriba('barranca-1', 0, 60),
        arriba('barranca-2', 940, 60),
        arriba('barranca-3', 1880, 60),
      ],
    },
    juego: {
      colocaciones: [
        arriba('bajada', 0),
        arriba('cauce-1', 960),
        arriba('cauce-2', 1920),
        arriba('subida', 2880),
      ],
    },
    frente: {
      colocaciones: [
        { modulo: 'maguey', x: 600, y: 1240 },
        { modulo: 'maguey', x: 3800, y: 1250, espejo: true },
      ],
    },
  },
};

/**
 * El monte al amanecer (M2 b5): el sendero en la bruma hasta el claro donde esperan otros
 * desplazados alrededor de una fogata; abajo, el valle con un hilo de humo.
 */
export const HUIDA_MONTE: DefinicionEscenario = {
  atlas: 'fondos/huida/monte',
  anchoNivel: 3840,
  acto: 'acto1',
  fondo: 'niebla',
  capas: {
    cielo: { colocaciones: [arriba('cielo-alba', 0)] },
    lejos: {
      colocaciones: [arriba('valle-1', 0, 380), arriba('valle-2', 1100, 380)],
    },
    medio: {
      colocaciones: [
        arriba('monte-1', 0),
        arriba('monte-2', 940),
        arriba('monte-3', 1880),
      ],
    },
    juego: {
      colocaciones: [
        arriba('sendero-1', 0),
        arriba('sendero-2', 960),
        arriba('claro', 1920),
        arriba('salida-monte', 2880),
      ],
    },
    frente: {
      colocaciones: [
        { modulo: 'maguey', x: 1400, y: 1250 },
        { modulo: 'maguey', x: 3600, y: 1240, espejo: true },
      ],
    },
  },
};
