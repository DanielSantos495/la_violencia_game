/**
 * Pose de caminata procedural para personajes cut-out (función pura, sin Phaser).
 *
 * Una sola fase (0..2π = un ciclo de dos pasos) produce todos los ángulos con senos
 * desfasados, así el movimiento es continuo y nunca se descuadra:
 * - Piernas en contrafase; el pie que avanza se levanta (fase de vuelo).
 * - Brazos opuestos a la pierna del mismo lado; el codo se dobla con retraso.
 * - El cuerpo sube cuando las piernas pasan por la vertical (dos veces por ciclo).
 * - Prendas y pelo siguen con retraso, como tela (inercia secundaria).
 * Convención de Phaser: ángulo positivo = sentido horario; con el personaje mirando a la
 * derecha, un ángulo positivo lleva la pierna o el brazo hacia atrás.
 */
export interface OpcionesCaminata {
  /** Amplitud de la cadera en grados. */
  zancada?: number;
  /** Altura máxima que se despega el pie que avanza, en px del SVG. */
  levantePie?: number;
  /** Rebote vertical del cuerpo, en px del SVG. */
  rebote?: number;
}

export interface PoseCaminata {
  /** Ángulo en grados por id de pieza (las ausentes del personaje se ignoran). */
  angulos: Record<string, number>;
  /** Desplazamiento hacia arriba, en px, de las piernas que se despegan. */
  levante: Record<string, number>;
  /** Cuánto sube el cuerpo entero, en px. */
  rebote: number;
}

export const ZANCADA_POR_DEFECTO = 8;

export function poseCaminata(
  fase: number,
  {
    zancada = ZANCADA_POR_DEFECTO,
    levantePie = 7,
    rebote = 3.5,
  }: OpcionesCaminata = {},
): PoseCaminata {
  const s = Math.sin(fase);
  const c = Math.cos(fase);
  return {
    angulos: {
      'pierna-der': zancada * s,
      'pierna-izq': -zancada * s,
      'brazo-der': -zancada * 1.3 * s,
      'brazo-izq': zancada * 1.3 * s,
      'antebrazo-der': -6 - 7 * (0.5 - 0.5 * Math.sin(fase - 0.7)),
      'antebrazo-izq': -6 - 7 * (0.5 + 0.5 * Math.sin(fase - 0.7)),
      cabeza: 0.8 * Math.sin(2 * fase + 0.5),
      falda: 1.6 * Math.sin(fase - 0.9),
      enagua: 2.2 * Math.sin(fase - 1.3),
      panolon: 0.9 * Math.sin(2 * fase - 1.1) + 0.6 * Math.sin(fase - 1),
      ruana: 0.9 * Math.sin(2 * fase - 1.1),
      trenza: 3.5 * Math.sin(fase - 1.7) + 1.5 * Math.sin(2 * fase - 1.2),
      zarcillo: 9 * Math.sin(2 * fase - 1.5),
    },
    levante: {
      // El pie que avanza (ángulo decreciendo) está en el aire.
      'pierna-der': levantePie * Math.max(0, -c) ** 1.5,
      'pierna-izq': levantePie * Math.max(0, c) ** 1.5,
    },
    rebote: rebote * (0.5 + 0.5 * Math.cos(2 * fase)),
  };
}

/**
 * Velocidad de avance (px/s a escala 1) para que los pies no patinen: cada paso recorre la
 * cuerda del arco de la pierna, 2·L·sen(zancada), y hay dos pasos por ciclo.
 */
export function velocidadCaminata(
  largoPierna: number,
  cicloMs: number,
  zancada = ZANCADA_POR_DEFECTO,
): number {
  const paso = 2 * largoPierna * Math.sin((zancada * Math.PI) / 180);
  return (2 * paso) / (cicloMs / 1000);
}
