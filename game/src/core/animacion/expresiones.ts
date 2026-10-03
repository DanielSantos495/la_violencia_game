/**
 * Expresiones de los personajes cut-out (datos puros, sin Phaser).
 *
 * Rostro simplificado (doc 03 §2): la expresión vive en ojos, cejas, boca y **postura**.
 * El dibujo de cada expresión es una cabeza completa en el atlas
 * ("<base de cabezas>/<expresión>") con su capa de parpadeo ("…/parpado-<expresión>");
 * aquí se define lo que no es dibujo: cómo se inclina la cabeza y cómo parpadea.
 *
 * Convención de Phaser: ángulo positivo = horario; mirando a la derecha, positivo baja el
 * mentón (cabeza hacia adelante) y negativo lo sube (cabeza hacia atrás).
 */
export const EXPRESIONES = [
  'neutral',
  'alerta',
  'miedo',
  'rabia',
  'duelo',
] as const;
export type Expresion = (typeof EXPRESIONES)[number];

export interface DatosExpresion {
  /**
   * Ángulo que se suma a cada pieza (grados): la postura de la expresión. Las poses que
   * no pueden mover el cuerpo (p. ej. agachada con la mano en el suelo) aplican solo la
   * cabeza (ver PIEZAS_POSTURA_CABEZA).
   */
  postura: Readonly<Record<string, number>>;
  parpadeo: {
    /** Intervalo entre parpadeos, en ms (mínimo y máximo). */
    cada: readonly [number, number];
    /** Cuánto dura el ojo cerrado, en ms. */
    dura: number;
    /** Probabilidad de un parpadeo doble. */
    doble: number;
  };
}

export const DATOS_EXPRESION: Readonly<Record<Expresion, DatosExpresion>> = {
  // Tranquila.
  neutral: {
    postura: {},
    parpadeo: { cada: [2600, 5200], dura: 110, doble: 0.1 },
  },
  // Atenta: la cabeza se alza un poco y el brazo se adelanta, listo; parpadea más seguido.
  alerta: {
    postura: { cabeza: -2, 'brazo-der': -4, 'antebrazo-der': -8 },
    parpadeo: { cada: [1800, 3600], dura: 90, doble: 0.15 },
  },
  // Miedo: la cabeza se echa atrás, el codo se pega al cuerpo y la mano sube a aferrarse
  // al pañolón o a la ruana sobre el pecho; parpadeo rápido y nervioso.
  miedo: {
    postura: {
      cabeza: -5,
      'brazo-der': 28,
      'antebrazo-der': -148,
      'brazo-izq': 24,
      'antebrazo-izq': -140,
      trenza: -2,
    },
    parpadeo: { cada: [900, 2000], dura: 80, doble: 0.35 },
  },
  // Rabia: mentón abajo, brazos tensos hacia adelante, mirada fija; casi no parpadea.
  rabia: {
    postura: {
      cabeza: 4,
      'brazo-der': -5,
      'antebrazo-der': -14,
      'brazo-izq': -3,
      'antebrazo-izq': -10,
    },
    parpadeo: { cada: [4200, 7000], dura: 130, doble: 0 },
  },
  // Duelo: la cabeza cae, los brazos cuelgan sin fuerza; párpados lentos y pesados.
  duelo: {
    postura: {
      cabeza: 9,
      'brazo-der': 3,
      'antebrazo-der': 2,
      'brazo-izq': 3,
      'antebrazo-izq': 2,
      trenza: 2,
    },
    parpadeo: { cada: [2400, 4400], dura: 240, doble: 0 },
  },
};

/** Piezas que mueve la postura en poses que solo admiten la cabeza. */
export const PIEZAS_POSTURA_CABEZA: readonly string[] = ['cabeza'];

export function esExpresion(valor: string): valor is Expresion {
  return (EXPRESIONES as readonly string[]).includes(valor);
}

/** Espera hasta el próximo parpadeo (ms); `azar` devuelve un número en [0, 1). */
export function intervaloParpadeo(
  expresion: Expresion,
  azar: () => number,
): number {
  const [min, max] = DATOS_EXPRESION[expresion].parpadeo.cada;
  return min + (max - min) * azar();
}
